#!/usr/bin/env python3
"""LLMC — Lo-Fi Instrumental Batch Generator.

Generates a batch of NO-VOCAL Lo-Fi hip hop instrumental tracks via ACE-Step.
Uses lyrics="[Instrumental]" which triggers ACE-Step's instrumental mode.
"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

API = "http://127.0.0.1:8001/release_task"
CACHE = Path("/home/sovthpaw/Models/ace-step/.cache/acestep/tmp/api_audio")
OUT = Path.home() / "music" / "output" / "llmc-lofi-instrumentals"
OUT.mkdir(parents=True, exist_ok=True)

# 8 diverse Lo-Fi instrumental tracks — NO VOCALS, all different vibes
TRACKS = [
    {
        "name": "01_midnight_coffee",
        "bpm": 72,
        "key": "F minor",
        "caption": (
            "lo-fi hip hop instrumental, no vocals, dusty vinyl crackle, "
            "jazzy electric piano chords, warm sub-bass, "
            "soft boom bap drums with swing, "
            "rain ambience, late night study, "
            "mellow nostalgic, tape saturation, "
            "instrumental"
        ),
        "duration": 180,
    },
    {
        "name": "02_paper_cranes",
        "bpm": 68,
        "key": "C minor",
        "caption": (
            "lo-fi chillhop instrumental, no vocals, "
            "mellow Rhodes piano melody, "
            "brushed snare drums, gentle kick, "
            "warm analog bass, distant bird sounds, "
            "soft focus, dreamy afternoon, "
            "cassette tape warmth, instrumental"
        ),
        "duration": 180,
    },
    {
        "name": "03_empty_rooms",
        "bpm": 65,
        "key": "A minor",
        "caption": (
            "lo-fi ambient instrumental, no vocals, "
            "ethereal synth pads, minimal piano notes, "
            "no drums, soft reverb tail, "
            "distant city hum, late night introspection, "
            "vinyl crackle, ambient drift, "
            "instrumental"
        ),
        "duration": 180,
    },
    {
        "name": "04_brushed_silk",
        "bpm": 75,
        "key": "D minor",
        "caption": (
            "lo-fi jazz instrumental, no vocals, "
            "upright bass walking line, "
            "brushed jazz drums with rimshot, "
            "warm tenor saxophone phrases, "
            "dusty piano comping, "
            "smoky jazz bar atmosphere, "
            "tape hiss, instrumental"
        ),
        "duration": 180,
    },
    {
        "name": "05_velvet_static",
        "bpm": 70,
        "key": "G minor",
        "caption": (
            "lo-fi R&B instrumental, no vocals, "
            "smooth electric piano with tremolo, "
            "soft 808 sub-bass, "
            "lazy trap hi-hats, rimshot snare, "
            "warm vinyl crackle, "
            "dim red light mood, "
            "cassette saturation, instrumental"
        ),
        "duration": 180,
    },
    {
        "name": "06_focus_bloom",
        "bpm": 74,
        "key": "E minor",
        "caption": (
            "lo-fi study beat instrumental, no vocals, "
            "clean grand piano arpeggios, "
            "light percussion, soft kick drum, "
            "warm pad sustain, "
            "morning sunlight, fresh focus, "
            "minimal melody, gentle, instrumental"
        ),
        "duration": 180,
    },
    {
        "name": "07_cherry_blossom_drive",
        "bpm": 78,
        "key": "B minor",
        "caption": (
            "lo-fi anime style instrumental, no vocals, "
            "bright piano lead, nostalgic melody, "
            "soft strings swell, "
            "gentle boom bap drums, "
            "warm bass, cassette wow, "
            "spring afternoon, bittersweet, "
            "vinyl warmth, instrumental"
        ),
        "duration": 180,
    },
    {
        "name": "08_3am_ashes",
        "bpm": 60,
        "key": "D# minor",
        "caption": (
            "dark lo-fi instrumental, no vocals, "
            "mournful piano in minor key, "
            "dusty vinyl crackle heavy, "
            "sparse slow drums, deep sub-bass, "
            "distant thunder rumble, "
            "insomnia, melancholic, "
            "tape degradation, instrumental"
        ),
        "duration": 180,
    },
]


def post_task(caption, bpm, key, duration):
    payload = {
        "prompt": caption,
        "lyrics": "[Instrumental]",
        "thinking": True,
        "use_format": False,
        "bpm": bpm,
        "key_scale": key,
        "time_signature": "4",
        "vocal_language": "unknown",
        "inference_steps": 50,
        "guidance_scale": 7.0,
        "audio_duration": duration,
        "audio_format": "wav",
        "task_type": "text2music",
    }
    req = Request(
        API,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    resp = urlopen(req, timeout=60)
    return json.loads(resp.read())


def wait_for_wav(baseline, timeout=600):
    deadline = time.time() + timeout
    while time.time() < deadline:
        current = {p.name for p in CACHE.glob("*.wav")}
        new_files = current - baseline
        if new_files:
            new_wavs = [p for p in CACHE.glob("*.wav") if p.name in new_files]
            return max(new_wavs, key=lambda p: p.stat().st_mtime)
        time.sleep(2)
    return None


def convert_to_mp3(wav_path, mp3_path):
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", str(wav_path), "-codec:a", "libmp3lame", "-b:a", "192k", str(mp3_path)],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def main():
    print(f"=== LLMC Lo-Fi Instrumental Batch ===")
    print(f"Output: {OUT}")
    print(f"Tracks: {len(TRACKS)}")
    print(f"Mode: INSTRUMENTAL (no vocals)")
    print()

    # Verify cache dir exists
    if not CACHE.exists():
        print(f"ERROR: Cache dir not found: {CACHE}")
        sys.exit(1)

    results = []
    for i, track in enumerate(TRACKS):
        name = track["name"]
        print(f"[{i+1}/{len(TRACKS)}] Generating: {name}")
        print(f"  BPM: {track['bpm']} | Key: {track['key']} | Duration: {track['duration']}s")
        print(f"  Caption: {track['caption'][:80]}...")
        t0 = time.time()

        # Snapshot cache BEFORE
        baseline = {p.name for p in CACHE.glob("*.wav")}

        try:
            resp = post_task(track["caption"], track["bpm"], track["key"], track["duration"])
            task_id = resp.get("data", {}).get("task_id", "unknown")
            print(f"  Task posted: {task_id}")
        except Exception as e:
            print(f"  FAIL posting task: {e}")
            results.append({"name": name, "status": "failed", "error": str(e)})
            continue

        # Wait for WAV
        wav_file = wait_for_wav(baseline, timeout=600)
        if not wav_file:
            print(f"  TIMEOUT — no WAV after 600s")
            results.append({"name": name, "status": "timeout"})
            continue

        print(f"  WAV found: {wav_file.name} ({wav_file.stat().st_size:,} bytes)")

        # Copy WAV
        wav_out = OUT / f"{name}.wav"
        shutil.copy2(wav_file, wav_out)

        # Convert to MP3
        mp3_out = OUT / f"{name}.mp3"
        if convert_to_mp3(wav_out, mp3_out):
            mp3_size = mp3_out.stat().st_size / (1024 * 1024)
            elapsed = time.time() - t0
            print(f"  ✅ {mp3_out.name} ({mp3_size:.1f}MB) in {elapsed:.1f}s")
            results.append({
                "name": name,
                "status": "ok",
                "wav": str(wav_out),
                "mp3": str(mp3_out),
                "size_mb": round(mp3_size, 1),
                "elapsed_s": round(elapsed, 1),
            })
        else:
            print(f"  MP3 conversion failed, WAV saved")
            results.append({"name": name, "status": "wav_only", "wav": str(wav_out)})

        print()

    # Summary
    print("=" * 60)
    print("BATCH SUMMARY")
    print("=" * 60)
    ok = sum(1 for r in results if r["status"] == "ok")
    print(f"Success: {ok}/{len(TRACKS)}")
    for r in results:
        if r["status"] == "ok":
            print(f"  ✅ {r['name']} — {r['size_mb']}MB ({r['elapsed_s']}s)")
        else:
            print(f"  ❌ {r['name']} — {r['status']}")
    print()
    print(f"All outputs: {OUT}")
    return results


if __name__ == "__main__":
    main()
