---
name: song-forge
description: "End-to-end song creation pipeline: lyrics → ACE-Step generation → MP3 conversion → Discord push → playlist for Evolutionary Radio."
version: 1.0.0
tags: [music, generation, ace-step, discord, playlist, pipeline]
triggers:
  - generate song
  - create song
  - forge song
  - make music
  - push to discord
  - add to playlist
---

# Song Forge

The end-to-end pipeline that turns lyrics into a generated song, pushes it to Discord, and adds it to the playlist for Evolutionary Radio integration.

## Prerequisites

- **ACE-Step API** running at `http://127.0.0.1:8001` (local GPU required)
- **ffmpeg** for WAV → MP3 conversion
- **hermes send** CLI for Discord distribution
- **Discord channel ID** for the target server

## Pipeline Steps

### Step 1: Prepare Lyrics

Ensure lyrics have structural tags:
```
[Verse 1]
...
[Pre-Chorus]
...
[Chorus]
...
[Verse 2]
...
[Bridge]
...
[Outro]
...
```

### Step 2: Choose Style Prompt

Default (dark cinematic rap):
```
dark cinematic rap, deep 808s, haunting piano loop, atmospheric trap production, dark orchestral strings, 70 BPM, C minor, introspective aggressive delivery, cinematic crescendo, ethereal choir pads
```

Alternatives:
- **Spoken word ambient:** `dark ambient cinematic spoken word, deep calm narration, haunting drone, melancholic piano, VHS dreamcore, 60 BPM, D minor, no drums, pure atmospheric`
- **Dark trap:** `dark trap, menacing 808s, hi-hats, dark piano, ominous atmosphere, 140 BPM, F minor, aggressive`
- **Cinematic orchestral:** `epic cinematic orchestral, sweeping strings, french horns, building tension, 90 BPM, D minor, instrumental`

### Step 3: Generate via ACE-Step

Use the `/release_task` endpoint with `thinking: false` (skips LM planner, fastest path):

```python
import json, time, shutil, urllib.request
from pathlib import Path

CACHE = Path('/home/sovthpaw/Models/ace-step/.cache/acestep/tmp/api_audio')
baseline = set(p.name for p in CACHE.glob('*.wav'))

payload = {
    "prompt": style_prompt,
    "lyrics": lyrics,
    "thinking": False,
    "use_format": False,
    "bpm": 70,
    "key_scale": "C minor",
    "time_signature": "4",
    "vocal_language": "en",
    "inference_steps": 50,
    "guidance_scale": 7.0,
    "audio_duration": 95,
    "audio_format": "wav",
    "task_type": "text2music"
}

req = urllib.request.Request(
    "http://127.0.0.1:8001/release_task",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"},
    method="POST"
)
resp = urllib.request.urlopen(req, timeout=30)
result = json.loads(resp.read())

# Watch cache for new WAV (GPU: ~6s, CPU: 4-15min)
deadline = time.time() + 300
while time.time() < deadline:
    current = set(p.name for p in CACHE.glob('*.wav'))
    new_files = current - baseline
    if new_files:
        newest = sorted(CACHE.glob('*.wav'), key=lambda p: p.stat().st_mtime, reverse=True)[0]
        shutil.copy(newest, output_path)
        break
    time.sleep(1)
```

**CRITICAL:** Do NOT use turbo mode (`infer_step=8`). It produces near-silence. Always use `infer_step=50` for full quality.

**CRITICAL:** Do NOT poll `/query_result`. It's unreliable. Watch the cache directory for new WAV files instead.

### Step 4: Convert to MP3

```bash
ffmpeg -y -i output.wav -codec:a libmp3lame -b:a 192k output.mp3
```

### Step 5: Push to Discord

```bash
# Send lyrics
hermes send --to discord:<channel_id> --file /tmp/lyrics.txt

# Send MP3 as attachment
hermes send --to discord:<channel_id> "MEDIA:/path/to/song.mp3"
```

### Step 6: Add to Playlist

```bash
# Copy to playlist directory for Evolutionary Radio
cp output.mp3 ~/music/output/veiled-playlist/veiled_<theme>_<version>.mp3
```

The Evolutionary Radio can pull crafted tracks from `~/music/output/veiled-playlist/` and interject them between generated tracks.

## ACE-Step API Details

### Endpoints
- `POST /release_task` — Submit a generation task (async, returns task_id)
- `POST /query_result` — Poll task status (UNRELIABLE — use cache-watch instead)
- `POST /v1/init` — Force eager model load (optional, speeds up first request)
- `GET /v1/audio?path=<path>` — Serve a file from cache

### Field Names (Gotchas)
- The style prompt field is called `prompt` in `/release_task` (NOT `query`)
- `thinking: false` skips the 5Hz LM planner (60s+ on CPU) — always use this
- `inference_steps: 50` = full quality. `8` = turbo (near-silence). NEVER use 8.
- `audio_duration` is in seconds. 95 = full song, 30 = short clip.

### Cache Directory
```
/home/sovthpaw/Models/ace-step/.cache/acestep/tmp/api_audio/
```
Files are UUIDs (e.g. `6aeb54b9-9c80-b502-bf6d-68207655a365.wav`). Always snapshot before posting a task, then diff to find the new file.

### GPU vs CPU
- **GPU (RTX 3090):** ~6 seconds per 95s song
- **CPU offload:** 4-15 minutes per song
- GPU mode requires `CUDA_VISIBLE_DEVICES=0` and free VRAM (~9GB)
- If GPU is held by other services, ACE-Step falls back to CPU automatically

## Playlist Integration with Evolutionary Radio

The Evolutionary Radio (`~/projects/evolutionary-radio/`) uses an asyncio.Queue for its track pipeline. Crafted songs from Veiled can be interjected by:

1. Placing MP3s in `~/music/output/veiled-playlist/`
2. The radio's queue-fill loop can check this directory for crafted tracks
3. Mix crafted tracks with on-the-fly generated ones

The radio's `code/config.yaml` has a `crafted_tracks_dir` setting that points to the playlist directory. When set, the radio plays a crafted track every N generated tracks (configurable).

## Style Prompt Builder

When building a style prompt, combine:
```
[Genre] + [Mood] + [Instruments] + [BPM] + [Key] + [Vocal style] + [Production] + [Dynamics]
```

Example:
```
dark cinematic rap, introspective aggressive, deep 808s, haunting piano, atmospheric strings, 70 BPM, C minor, ethereal choir pads, cinematic crescendo, building from quiet to powerful
```

## Pitfalls

1. **Turbo mode = silence.** `infer_step=8` produces -27dB RMS noise. Always use 50.
2. **Don't poll /query_result.** It returns empty even after completion. Watch the cache.
3. **GPU contention.** If other services hold VRAM, generation drops to CPU (4-15 min). Check `nvidia-smi` first.
4. **Field name `prompt` not `query`.** `/release_task` uses `prompt`. `/v1/create_sample` uses `query`. Don't mix them up.
5. **Lyrics must have structural tags.** Without [Verse], [Chorus], etc., ACE-Step produces flat verse/chorus with no emotional arc.
6. **Audio duration cap.** ACE-Step v1.5 caps at ~100 seconds per generation. For longer songs, generate in sections and stitch.
