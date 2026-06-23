#!/usr/bin/env python3
"""LLMC Song Forge — batch rap generator. Edit the TRACKS list, run, get 3:33 MP3s."""
import json, time, shutil, subprocess
from pathlib import Path
from urllib.request import Request, urlopen

ACE = "http://127.0.0.1:8001/release_task"
CACHE = Path("/home/sovthpaw/Models/ace-step/.cache/acestep/tmp/api_audio")
OUT = Path("/tmp/llmc-wayne")
OUT.mkdir(parents=True, exist_ok=True)

# EDIT THIS LIST — one tuple per track: (name, bpm, key, time_sig, caption, lyrics)
# RULES: vary BPM, key, and genre EVERY track. NEVER copy influence lines.
# Use thinking=True for correct 3:33 duration.
TRACKS = [
    ("01_example", 79, "F# minor", "4",
     "southern rap, crisp snare, sub-bass 808s, tape saturation, confident delivery, 2008 Cash Money production",
     "[Intro - spoken]\\n(yeah)\\ntesting\\n\\n[Verse 1 - conversational]\\nthis is a test of the format\\n"),
    # Add more tracks...
]

def generate_one(name, bpm, key, ts, caption, lyrics):
    payload = {
        "prompt": caption, "lyrics": lyrics,
        "thinking": True,    # MANDATORY — LM handles duration
        "use_format": False,
        "bpm": bpm, "key_scale": key, "time_signature": ts,
        "vocal_language": "en",
        "inference_steps": 50, "guidance_scale": 7.0,
        "audio_duration": 213,
        "audio_format": "wav", "task_type": "text2music"
    }
    r = Request(ACE, data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"}, method="POST")
    return json.loads(urlopen(r, timeout=30).read())

def wait_for_wav(baseline):
    import time
    dl = time.time() + 600
    while time.time() < dl:
        ns = {p.name for p in CACHE.glob("*.wav")}
        nf = ns - baseline
        if nf:
            return sorted(CACHE.glob("*.wav"), key=lambda p: p.stat().st_mtime)[-1]
        time.sleep(2)
    return None

for name, bpm, key, ts, caption, lyrics in TRACKS:
    print(f"GEN: {name}...", end=" ", flush=True)
    t0 = time.time()
    try:
        generate_one(name, bpm, key, ts, caption, lyrics)
    except Exception as e:
        print(f"FAIL: {e}")
        continue
    
    baseline = {p.name for p in CACHE.glob("*.wav")}
    wav = wait_for_wav(baseline)
    if not wav:
        print("TIMEOUT")
        continue
    
    src = CACHE / wav
    # HARD VERIFY duration from raw bytes (48kHz stereo 16-bit)
    raw_bytes = src.stat().st_size - 44
    actual = raw_bytes / 192000
    
    tmp = OUT / f"{name}_raw.wav"
    shutil.copy2(src, tmp)
    final = OUT / f"{name}.mp3"
    subprocess.run(["ffmpeg", "-y", "-i", str(tmp), "-t", "213",
                    "-codec:a", "libmp3lame", "-b:a", "192k", str(final)],
                   capture_output=True)
    
    mb = final.stat().st_size / (1024*1024)
    elapsed = time.time() - t0
    ok = "OK" if abs(actual - 213) < 5 else f"SHORT({actual:.1f}s)"
    print(f"{ok} {mb:.1f}MB in {elapsed:.1f}s")

print("DONE")
