#!/usr/bin/env python3
"""
LLMC Batch Song Generator — Standardized pipeline.
Usage: python3 batch_generate.py --channel DISCORD_CHANNEL_ID

Reads song definitions from songs.json, generates each via ACE-Step,
converts to MP3, pushes to Discord (song + lyrics), copies to playlist.
"""
import json, time, shutil, subprocess, os, sys, argparse
from pathlib import Path
from urllib.request import Request, urlopen

ACE = "http://127.0.0.1:8001/release_task"
CACHE = Path("/home/sovthpaw/Models/ace-step/.cache/acestep/tmp/api_audio")
OUT = Path("/tmp/llmc-batch/output")
PLAYLIST = Path.home() / "music/output/llmc-playlist"

def post_task(style, lyrics, bpm, key, duration_cap=300):
    payload = json.dumps({
        "prompt": style, "lyrics": lyrics,
        "thinking": False, "use_format": False,
        "bpm": bpm, "key_scale": key,
        "time_signature": "4", "vocal_language": "en",
        "inference_steps": 50, "guidance_scale": 7.0,
        "audio_duration": duration_cap, "audio_format": "wav",
        "task_type": "text2music"
    }).encode()
    req = Request(ACE, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    return json.loads(urlopen(req, timeout=30).read())

def watch_cache(baseline, timeout=300):
    deadline = time.time() + timeout
    while time.time() < deadline:
        current = {p.name for p in CACHE.glob("*.wav")}
        new_files = current - baseline
        if new_files:
            new_wavs = [p for p in CACHE.glob("*.wav") if p.name in new_files]
            return max(new_wavs, key=lambda p: p.stat().st_mtime)
        time.sleep(1)
    return None

def to_mp3(wav_path, mp3_path):
    subprocess.run(["ffmpeg", "-y", "-i", str(wav_path),
                    "-codec:a", "libmp3lame", "-b:a", "192k", str(mp3_path)],
                   capture_output=True, timeout=60)

def send_discord(channel_id, message, media_path=None):
    cmd = ["hermes", "send", "-t", f"discord:{channel_id}"]
    if media_path:
        msg = f"{message}\nMEDIA:{media_path}" if message else f"MEDIA:{media_path}"
        cmd.append(msg)
    else:
        cmd.append(message)
    subprocess.run(cmd, capture_output=True, timeout=30)

def write_lyrics_file(path, title, theme, style, bpm, key, duration, lyrics):
    with open(path, "w") as f:
        f.write(f"LLMC — {title}\n")
        f.write(f"Theme: {theme}\n")
        f.write(f"Style: {style}\n")
        f.write(f"BPM: {bpm} | Key: {key} | Duration: ~{duration:.0f}s ({duration/60:.1f} min)\n")
        f.write("=" * 60 + "\n\n")
        f.write(lyrics)

def generate_song(song, channel_id, index, total):
    name = song["name"]
    title = name.replace("_", " ").title()
    lyrics = song["lyrics"]
    style = song["style"]
    bpm = song["bpm"]
    key = song["key"]
    theme = song["theme"]

    line_count = len(lyrics.strip().splitlines())
    print(f"\n[{index}/{total}] {title}")
    print(f"  Theme: {theme}")
    print(f"  {line_count} lines, {bpm} BPM, {key}")

    # Snapshot cache BEFORE posting
    baseline = {p.name for p in CACHE.glob("*.wav")}

    # Post task
    t0 = time.time()
    resp = post_task(style, lyrics, bpm, key)
    task_id = resp.get("data", {}).get("task_id", "?")
    print(f"  Task: {task_id}")

    # Watch for NEW file (filtered to baseline diff)
    wav_file = watch_cache(baseline, timeout=300)
    if not wav_file:
        print(f"  ❌ TIMEOUT")
        return None

    duration = (wav_file.stat().st_size - 44) / 192000
    elapsed = time.time() - t0
    meets = duration >= 213
    flag = "✅" if meets else "⚠️ SHORT"
    print(f"  {flag} {duration:.0f}s ({duration/60:.1f} min), {elapsed:.0f}s wall")

    # Copy WAV
    wav_out = OUT / f"{name}.wav"
    shutil.copy2(wav_file, wav_out)

    # Convert to MP3
    mp3_out = OUT / f"{name}.mp3"
    to_mp3(wav_out, mp3_out)

    # Write lyrics file
    lyrics_out = OUT / f"{name}_lyrics.txt"
    write_lyrics_file(lyrics_out, title, theme, style, bpm, key, duration, lyrics)

    # Copy to playlist
    playlist_mp3 = PLAYLIST / f"llmc_{name}.mp3"
    shutil.copy2(mp3_out, playlist_mp3)

    # Push to Discord
    msg = f"🎵 **LLMC — {title}**\n*Theme: {theme}*\n*{bpm} BPM, {key} | ~{duration:.0f}s ({duration/60:.1f} min) {'✅' if meets else '⚠️'}*"
    send_discord(channel_id, msg, str(mp3_out))
    time.sleep(2)
    send_discord(channel_id, f"📜 Lyrics: {title}", str(lyrics_out))
    time.sleep(1)

    print(f"  ✅ Done")
    return {"name": name, "duration": round(duration, 1), "meets_333": meets}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", required=True, help="Discord channel ID")
    parser.add_argument("--songs", default="songs.json", help="Path to songs JSON")
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    PLAYLIST.mkdir(parents=True, exist_ok=True)

    with open(args.songs) as f:
        songs = json.load(f)

    results = []
    for i, song in enumerate(songs, 1):
        r = generate_song(song, args.channel, i, len(songs))
        if r:
            results.append(r)
        time.sleep(3)

    # Summary
    summary = f"🎵 **LLMC Batch Complete — {len(results)}/{len(songs)} songs**\n\n"
    for r in results:
        flag = "✅" if r["meets_333"] else "⚠️"
        title = r["name"].replace("_", " ").title()
        summary += f"{flag} **{title}** — {r['duration']}s\n"
    send_discord(args.channel, summary)
    print(f"\n{'='*60}\nBatch complete: {len(results)}/{len(songs)}\n{'='*60}")

if __name__ == "__main__":
    main()
