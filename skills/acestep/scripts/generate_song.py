#!/usr/bin/env python3
"""
ACE-Step song generation script — the reliable cache-watch pattern.

Usage:
    python generate_song.py --lyrics-file lyrics.txt --style "dark cinematic rap, 70 BPM, C minor" --output song.wav
    python generate_song.py --lyrics "..." --style "..." --output song.wav --duration 95 --bpm 70 --key "C minor"
    python generate_song.py --lyrics-file lyrics.txt --style "..." --output song.wav --convert-mp3

Posts to /release_task with thinking:false (skips LM planner), then watches
the cache directory for the new WAV. Does NOT poll /query_result (unreliable).

Requires: ACE-Step API running at http://127.0.0.1:8001
"""

import argparse
import json
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

API_URL = "http://127.0.0.1:8001"
CACHE_DIR = Path("/home/sovthpaw/Models/ace-step/.cache/acestep/tmp/api_audio")


def generate_song(
    lyrics: str,
    style_prompt: str,
    output_path: str,
    duration: int = 95,
    bpm: int = 70,
    key_scale: str = "C minor",
    inference_steps: int = 50,
    guidance_scale: float = 7.0,
    timeout: int = 300,
) -> bool:
    """Generate a song via ACE-Step API. Returns True on success."""

    if not CACHE_DIR.exists():
        print(f"ERROR: Cache directory not found: {CACHE_DIR}")
        return False
    baseline = set(p.name for p in CACHE_DIR.glob("*.wav"))
    print(f"Cache baseline: {len(baseline)} existing files")

    payload = {
        "prompt": style_prompt,
        "lyrics": lyrics,
        "thinking": False,
        "use_format": False,
        "bpm": bpm,
        "key_scale": key_scale,
        "time_signature": "4",
        "vocal_language": "en",
        "inference_steps": inference_steps,
        "guidance_scale": guidance_scale,
        "audio_duration": duration,
        "audio_format": "wav",
        "task_type": "text2music",
    }

    req = urllib.request.Request(
        f"{API_URL}/release_task",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read())
        task_id = result.get("data", {}).get("task_id", "unknown")
        print(f"Task posted: {task_id}")
    except Exception as e:
        print(f"ERROR posting task: {e}")
        return False

    print(f"Watching cache for new WAV (timeout: {timeout}s)...")
    deadline = time.time() + timeout
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    while time.time() < deadline:
        current = set(p.name for p in CACHE_DIR.glob("*.wav"))
        new_files = current - baseline
        if new_files:
            for f in new_files:
                fp = CACHE_DIR / f
                print(f"  New file: {f} ({fp.stat().st_size:,} bytes)")
            newest = sorted(
                CACHE_DIR.glob("*.wav"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )[0]
            shutil.copy(newest, output)
            print(f"Saved: {output} ({output.stat().st_size:,} bytes)")
            return True
        time.sleep(1)

    print(f"TIMEOUT: no new WAV after {timeout}s")
    return False


def convert_to_mp3(wav_path: str, mp3_path: str = None) -> str:
    """Convert WAV to MP3 via ffmpeg. Returns MP3 path or None."""
    if mp3_path is None:
        mp3_path = wav_path.rsplit(".", 1)[0] + ".mp3"
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", wav_path, "-codec:a", "libmp3lame", "-b:a", "192k", mp3_path],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        print(f"Converted: {mp3_path}")
        return mp3_path
    else:
        print(f"ERROR converting: {result.stderr[:200]}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Generate a song via ACE-Step API")
    parser.add_argument("--lyrics", help="Lyrics text (inline)")
    parser.add_argument("--lyrics-file", help="Path to lyrics file")
    parser.add_argument("--style", required=True, help="Style/prompt string")
    parser.add_argument("--output", required=True, help="Output WAV path")
    parser.add_argument("--duration", type=int, default=95, help="Audio duration in seconds")
    parser.add_argument("--bpm", type=int, default=70, help="BPM")
    parser.add_argument("--key", default="C minor", help="Key scale")
    parser.add_argument("--steps", type=int, default=50, help="Inference steps (50=full, 8=turbo=DON'T)")
    parser.add_argument("--guidance", type=float, default=7.0, help="Guidance scale")
    parser.add_argument("--timeout", type=int, default=300, help="Cache watch timeout (s)")
    parser.add_argument("--convert-mp3", action="store_true", help="Also convert to MP3")
    args = parser.parse_args()

    if args.lyrics_file:
        with open(args.lyrics_file, "r") as f:
            lyrics = f.read()
    elif args.lyrics:
        lyrics = args.lyrics
    else:
        print("ERROR: provide --lyrics or --lyrics-file")
        sys.exit(1)

    success = generate_song(
        lyrics=lyrics, style_prompt=args.style, output_path=args.output,
        duration=args.duration, bpm=args.bpm, key_scale=args.key,
        inference_steps=args.steps, guidance_scale=args.guidance,
        timeout=args.timeout,
    )
    if not success:
        sys.exit(1)
    if args.convert_mp3:
        mp3 = convert_to_mp3(args.output)
        print(f"\nDone! WAV: {args.output} | MP3: {mp3 or 'failed'}")
    else:
        print(f"\nDone! WAV: {args.output}")


if __name__ == "__main__":
    main()
