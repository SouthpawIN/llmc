---
name: acestep
description: "ACE-Step 1.5 — local music generation (2B/4B DiT) with built-in LoRA fine-tuning. Generate songs from lyrics + tags, train style LoRAs from 8+ tracks."
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [music, audio, generation, ai, acestep, ace-step, lora, fine-tuning, rap, beats]
    related_skills: [heartmula, evolutionary-radio, songwriting-and-ai-music, comfyui]
---

# ACE-Step 1.5 — Local Music Generation & LoRA Training

## Overview
ACE-Step 1.5 is a hybrid-architecture music generation model (LM planner + DiT decoder) that runs locally and supports LoRA fine-tuning from just 8 songs. Co-developed by ACE Studio & StepFun. Quality between Suno v4.5 and Suno v5.

## When to Use
- Generate music/songs from lyrics + style tags locally
- Train a LoRA to capture a specific musical style (rap beats, jazz, metal, etc.)
- User mentions ACE-Step, acestep, or wants Suno-quality local generation
- Fine-tune a music model on a custom dataset
- User wants rap beats, trap beats, or genre-specific generation

## Model Zoo

### DiT Models (audio decoder)

| Model | Params | CFG Steps | Turbo Steps | Quality | HuggingFace |
|-------|--------|-----------|-------------|---------|-------------|
| `acestep-v15-base` | 2B | 50 | — | Medium | [Link](https://huggingface.co/ACE-Step/acestep-v15-base) |
| `acestep-v15-sft` | 2B | 50 | — | High | [Link](https://huggingface.co/ACE-Step/acestep-v15-sft) |
| `acestep-v15-turbo` | 2B | — | 8 | Very High | [Link](https://huggingface.co/ACE-Step/Ace-Step1.5) |
| `acestep-v15-xl-base` | 4B | 50 | — | High | [Link](https://huggingface.co/ACE-Step/acestep-v15-xl-base) |
| `acestep-v15-xl-sft` | 4B | 50 | — | Very High | [Link](https://huggingface.co/ACE-Step/acestep-v15-xl-sft) |
| `acestep-v15-xl-turbo` | 4B | — | 8 | Very High | [Link](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo) |

### LM Models (planner — transforms simple queries into song blueprints)

| Model | Base | CoT | Composition | Copy Melody |
|-------|------|-----|-------------|-------------|
| `acestep-5Hz-lm-0.6B` | Qwen3-0.6B | ✅ | Medium | Weak |
| `acestep-5Hz-lm-1.7B` | Qwen3-1.7B | ✅ | Medium | Medium |
| `acestep-5Hz-lm-4B` | Qwen3-4B | ✅ | Strong | Strong |

### GPU Selection Guide

| VRAM | DiT | LM | Backend |
|------|-----|----|---------|
| ≤6GB | 2B turbo | None (DiT only) | — |
| 6-8GB | 2B turbo | 0.6B | `pt` |
| 8-16GB | 2B turbo/sft | 0.6B/1.7B | `vllm` |
| 16-20GB | 2B sft or XL turbo | 1.7B | `vllm` |
| 20-24GB | XL turbo/sft | 1.7B | `vllm` |
| ≥24GB | XL sft | 4B | `vllm` |

## Installation

```bash
git clone https://github.com/ace-step/ACE-Step-1.5.git
cd ACE-Step-1.5
uv sync
```

Python 3.11-3.12 required. Models auto-download on first run.

## Usage

### Gradio UI (interactive)
```bash
uv run acestep                    # http://localhost:7860
```

### REST API
```bash
uv run acestep-api                # http://localhost:8001
```

### Programmatic (Python)
```python
from acestep.pipeline_acestep import ACEStepPipeline

pipeline = ACEStepPipeline(checkpoint_dir="...", dtype="bfloat16")
result = pipeline(
    audio_duration=60,
    prompt="hard-hitting trap beat, deep 808s, hi-hats, dark piano, 140 bpm",
    lyrics="[Instrumental]",
    infer_step=50,
    save_path="output.wav",
)
```

### Input Formatting

**Tags** (comma-separated): `trap,808,hi-hats,dark-piano,140bpm,instrumental`

**Lyrics** (bracketed structural tags):
```
[Intro]
[Verse 1]
Your lyrics here...
[Chorus]
Chorus lyrics...
[Outro]
```

## LoRA Training

ACE-Step 1.5 has **built-in LoRA training** via the Gradio UI. You can train from just 8 songs in ~1 hour on a 3090.

### Hardware Requirements

| VRAM | Notes |
|------|-------|
| 16 GB (minimum) | May OOM on longer songs |
| 20 GB+ (recommended) | Handles full-length songs (~17 GB during training) |

### Dataset Preparation

Per-song files needed:
1. **Audio file** — `.mp3`, `.wav`, `.flac`, `.ogg`, `.opus`
2. **Lyrics** — `{filename}.lyrics.txt`
3. **Annotations** (optional) — `{filename}.json` with `caption`, `bpm`, `keyscale`, `timesignature`, `language`

**Directory structure:**
```
dataset/
├── track_001.mp3
├── track_001.lyrics.txt
├── track_001.json          # {"caption": "...", "bpm": 140, "keyscale": "C minor"}
├── track_002.mp3
├── track_002.lyrics.txt
└── ...
```

**Minimum data:** 8 tracks for basic style capture. 20-50 for robust generalization.

### Training Parameters (Recommended)

| Parameter | Value | Range | Note |
|-----------|-------|-------|------|
| LoRA Rank | 16 | 4-64 | Higher = more capacity, slower |
| LoRA Alpha | 32 | 8-128 | Usually 2× rank |
| Learning Rate | 1e-4 | 5e-5 – 5e-4 | Lower for small datasets |
| Batch Size | 4 | 1-16 | Reduce if OOM |
| Epochs | 50-150 | 20-500 | Monitor for overfitting |
| Warmup Steps | 50 | 0-200 | Stabilizes early training |

### Gradio UI LoRA Training Workflow

1. **Disable service pre-init** — change `INIT_SERVICE=--init_service true` → `--init_service false` in startup script
2. **Load models** (optional — only if using auto-labeling)
3. **LoRA Training tab** → enter dataset path → **Scan** (auto-recognizes audio, lyrics, captions)
4. **Review & adjust** — duration auto-read; edit entries; uncheck "All Instrumental" if not; keep Genre Ratio at 0
5. **Auto Label** (optional) — skip if captions exist; get BPM/Key from external tool first (LM hallucinates BPM/Key)
6. **Review & edit** — click Save after each edit
7. **Save dataset** — export as JSON
8. **Preprocess tensors** — if VRAM tight after LM use, restart Gradio without LM, reload
9. **Start training** — monitor loss; should decrease steadily
10. **Test** — load LoRA checkpoint, generate with style prompts

### Audio Preprocessing for Training

```bash
# Normalize to -14 LUFS (expected input format)
ffmpeg -i input.wav -ar 44100 -ac 1 -af "loudnorm=I=-14:TP=-1.5:LRA=11" output.wav
```

### YouTube Playlist → Training Data

Use `yt-dlp` to download raw WAV + metadata:
```bash
yt-dlp -x --audio-format wav \
  -o "./dataset/raw/%(playlist_title)s/%(title)s.%(ext)s" \
  --write-info-json \
  --embed-metadata \
  "https://youtube.com/playlist?list=YOUR_PLAYLIST_ID"
```

Then process to 44.1kHz mono -14 LUFS:
```bash
find ./dataset/raw -name "*.wav" | while read -r file; do
  safe_name=$(basename "$file" .wav | tr ' ' '_' | tr -cd 'a-zA-Z0-9_.-')
  ffmpeg -y -i "$file" -ar 44100 -ac 1 -af "loudnorm=I=-14:TP=-1.5:LRA=11" \
    "./dataset/processed/${safe_name}.wav"
done
```

### Lyrics Transcription Tools

| Tool | Structural Tags | Ease | Cost |
|------|----------------|------|------|
| acestep-transcriber | No | Hard | Free (self-hosted) |
| Gemini | Yes | Easy | Paid API |
| Whisper | No | Moderate | Free (self-hosted) |
| ElevenLabs | No | Moderate | Paid (generous free tier) |

Scripts in `scripts/lora_data_prepare/`: `whisper_transcription.py`, `elevenlabs_transcription.py`.

### Testing the Trained LoRA

```python
pipeline = ACEStepPipeline(checkpoint_dir="...", dtype="bfloat16")
result = pipeline(
    audio_duration=60,
    prompt="aggressive rap beat, heavy 808, triplet flows, dark atmosphere",
    lyrics="[Instrumental]",
    infer_step=50,
    lora_path="./lora_output/checkpoint-100",
    lora_weight=0.8,
    save_path="rap_beat.wav",
)
```

## HTTP API Gotchas (uvicorn server at :8001)

The `acestep api` server (uvicorn) has several non-obvious field names and behaviors that bite first-time users. Verified on the OmniSenter rap-gen session (2026-06-13).

### Field name: `query`, NOT `prompt`

`POST /v1/create_sample` accepts the user description in a field literally called `query`. Sending `prompt`, `caption`, `text`, `description`, or `instrumental_track` is silently ignored and the 5Hz LM gets called with `"NO USER INPUT"`, producing a random J-pop/funk caption unrelated to the user's actual ask.

```bash
# RIGHT: 'query' is the field name
curl -X POST http://127.0.0.1:8001/v1/create_sample \
  -H "Content-Type: application/json" \
  -d '{"query":"boom bap rap instrumental, 90 BPM, dusty drums","duration":20}'

# WRONG (silently ignored):
curl -X POST http://127.0.0.1:8001/v1/create_sample \
  -H "Content-Type: application/json" \
  -d '{"prompt":"boom bap rap instrumental, 90 BPM"}'  # ← produces random J-pop
```

### Two endpoints, two different things

- `POST /v1/create_sample` → calls the 5Hz LM to expand the query, then generates. **Slow** (~60s+ on CPU because the LM is on PyTorch backend when vllm needs CUDA).
- `POST /release_task` → accepts pre-formatted metadata (caption, lyrics, bpm, key_scale, etc.) and **skips the LM entirely** if `thinking: false`. Use this for batch generation.

```bash
# release_task with thinking:false — fastest path
curl -X POST http://127.0.0.1:8001/release_task \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "boom bap rap instrumental, 90 BPM, dusty drums",
    "lyrics": "[Instrumental]",
    "thinking": false,
    "use_format": false,
    "bpm": 90, "key_scale": "F minor", "time_signature": "4",
    "vocal_language": "en",
    "inference_steps": 12, "guidance_scale": 7.0,
    "audio_duration": 30, "audio_format": "wav",
    "task_type": "text2music"
  }'
# Returns: {"data": {"task_id": "uuid-here", "status": "queued"}}
```
### Polling `/query_result` — works partially, but cache-watch is the reliable pattern

`/release_task` is async. The *intended* pattern is to poll `/query_result`
with the task_id list until each task's `status` is `completed` or `failed`:

```bash
curl -X POST http://127.0.0.1:8001/query_result \
  -H "Content-Type: application/json" \
  -d '{"task_ids":["uuid-here"]}'
# Returns: {"data": {"tasks": [{...,"status":"completed", "audio_paths":[...]}, ...]}}
```

**But in practice `/query_result` often returns `{"data":[]}` even after the
task has fully completed and the WAV is sitting in the cache directory.**
The `query_result` endpoint doesn't reliably expose completed tasks — this
was a real bug that cost 75+ min of CPU-bound wall time on the 2026-06-13
rap-gen batch. Verified that the WAV is on disk in the cache but the
endpoint won't acknowledge the task.

**The reliable pattern is to NOT poll, but instead watch the cache directory:**

```python
from pathlib import Path
CACHE = Path('/home/sovthpaw/Models/ace-step/.cache/acestep/tmp/api_audio')

# Snapshot BEFORE posting
baseline = {p.name for p in CACHE.glob('*.wav')}

# Post the task (returns task_id, but we don't care)
task_id = post_release_task(prompt, bpm, key, duration=20)

# Watch for new cache file (ACE-Step on GPU: ~0.7s; on CPU: 4-15s)
deadline = time.time() + 30  # 30s is plenty on GPU
saved = False
while time.time() < deadline:
    new = {p.name for p in CACHE.glob('*.wav')} - baseline
    if new:
        newest = sorted(CACHE.glob('*.wav'), key=lambda p: p.stat().st_mtime, reverse=True)[0]
        shutil.copy(newest, OUT / f'{name}.wav')
        saved = True
        break
    time.sleep(0.5)
```

This is the **only reliable pattern** for batch generation. It cuts wall
time from "20-min poll + timeout" to "1-3 sec watch" on GPU, and works
on CPU too (4-15s per song). Used in `/tmp/rap_gen_v5_smart.py` for the
12-rap-song batch on the OmniStep project.

Polling interval (if you must poll): 10-15s. Each task takes 0.7-300s
depending on GPU vs CPU DiT execution.

### Getting the audio file

Two paths:
- `GET /v1/audio?path=<absolute-path-to-wav-or-mp3>` — serve a file from the ACE-Step cache (`/home/sovthpaw/Models/ace-step/.cache/acestep/tmp/api_audio/`)
- Read directly from the cache directory: the most recent `*.wav` (or `*.mp3`) is the latest generation

### `/v1/init` is required once at startup

By default ACE-Step lazy-loads models on first request. To initialize eagerly (so the first `/v1/create_sample` doesn't pay the model-load cost):

```bash
curl -X POST http://127.0.0.1:8001/v1/init -H "Content-Type: application/json" -d '{}'
# Returns: {"data": {"message": "Model initialization completed", "loaded_model": "acestep-v15-turbo"}}
```

### 5Hz LM is the bottleneck — skip it for batch

The `acestep-5Hz-lm-0.6B` (or 1.7B / 4B) is the LM planner that lives separately from the DiT. The server's PyTorch backend (when vllm can't get CUDA) is **60+ seconds per call** for caption expansion. Always set `thinking: false` on `/release_task` for batch generation, or pre-format the metadata yourself and skip the LM entirely.

### GPU contention forces DiT to CPU

If GPU 0 is held by other long-running inference servers (e.g. Carnice-35A3B, Darwin-28B), ACE-Step's DiT falls back to PyTorch CPU offload. Each 30s song then takes ~10-15 min instead of ~3-4 min on GPU. Mitigation:
- Run ACE-Step on GPU 1 (where it has free VRAM) with `CUDA_VISIBLE_DEVICES=1`
- Or stop the other services first

The DiT CPU-offload log line: `DiT diffusion via PyTorch (cpu)...` (slow path) vs `DiT diffusion via flash_attn (cuda)...` (fast path).

### Cache directory: the recovery trick for timed-out polls

Even when the poll `/query_result` times out (or returns `status: "timeout"`), the audio file is **almost always already on disk** at:

```
/home/sovthpaw/Models/ace-step/.cache/acestep/tmp/api_audio/
```

Filenames are UUIDs (e.g. `6aeb54b9-9c80-b502-bf6d-68207655a365.wav`). The most recent `.wav` (or `.mp3` if the API defaulted to mp3) is the latest generation. **Always fall back to grabbing the most recent cache file on poll timeout** — the model often finishes after your poll deadline expires.

Recovery pattern (Python):
```python
import time
from pathlib import Path
CACHE = Path('/home/sovthpaw/Models/ace-step/.cache/acestep/tmp/api_audio')
snapshot = set(p.name for p in CACHE.glob('*.wav'))

# ... post release_task, poll until status==completed (or timeout) ...

# On timeout: grab the newest cache file
def newest_after(snapshot):
    current = set(p.name for p in CACHE.glob('*.wav'))
    new = current - snapshot
    if not new: return None
    return sorted(CACHE.glob('*.wav'), key=lambda p: p.stat().st_mtime, reverse=True)[0]
```

Verified on the OmniSenter rap-gen batch: 6 songs recovered from cache after the script's 15-min poll timeout, all 5.5 MB valid WAVs at 48kHz stereo.

### `/v1/dataset/auto_label` for music-in

`POST /v1/dataset/auto_label` with JSON body `{"audio_path": "/path/to.wav"}` returns ACE-Step's LM-generated caption + bpm + key + language + lyrics. Useful as a music-in / music-understanding endpoint, **but it requires `app.state.dataset_builder` to be initialized** — which the simple `acestep api` server does NOT set up (only the dataset-training pipeline does). It will return `Internal Server Error: 'State' object has no attribute 'dataset_builder'` if called against the bare API server.

For music-in via ACE-Step, use a separate audio encoder (CLAP, MuQ) instead — see the `evolutionary-model-merging` skill's 4-block OmniStep architecture for the CLAP wiring pattern.

### `ACESTEP_OFFLOAD_DIT_TO_CPU=true` startup flag

When GPU contention is unavoidable, start ACE-Step with:
```
ACESTEP_OFFLOAD_DIT_TO_CPU=true PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
```
The DiT will offload to CPU when VRAM is exhausted (e.g. 0 GB free), gracefully
degrades instead of OOM-crashing. Generation still works, just slower. Set
both flags together — `expandable_segments` prevents fragmentation OOMs
during CPU↔GPU transfers.

### GPU performance: 0.7s per song on RTX 3090, 4-5 min on CPU

ACE-Step v1.5 turbo DiT on an RTX 3090 (24 GB) with no offload produces
a 20-second song in **0.7-0.8 seconds of DiT diffusion + ~0.5s VAE decode**
(~1.3s total wall time). On CPU offload (no GPU available), the same
song takes **4-15 minutes** depending on the system. The 7-10x slowdown is
worth avoiding if at all possible — at 12 songs, GPU finishes in 12s vs
48-180 min on CPU.

To get GPU mode, the GPU must be free. Long-running systemd inference
servers (llama-darwin, llama-apex, omni-va) often hold 20+ GB on each GPU
on a 2× 3090 rig. Two-step strategy for batch jobs:

1. `systemctl --user stop llama-darwin llama-apex omni-va` (frees ~30 GB)
2. Start ACE-Step with `CUDA_VISIBLE_DEVICES=0 ACESTEP_OFFLOAD_DIT_TO_CPU=false`
3. `curl -X POST .../v1/init -d '{}'` to force eager load
4. Run the batch — each song is ~1-2 sec including DiT + VAE + audio save
5. `systemctl --user start llama-darwin llama-apex omni-va` to restore

The systemd services will auto-respawn (PPID 1995 is `systemd --user`),
so stopping them is a temporary disruption (~5-15 min) but the
restart on completion works. Verify they came back with
`systemctl --user status llama-darwin` after you start them.
1. **Turbo mode produces near-silence for HF examples.** `infer_step=8` with `oss_steps="8"` remaps to `num_inference_steps=1`. Use `infer_step=50, oss_steps=None` for shipped examples. Turbo is fine for quick iteration.

2. **LM hallucinates BPM and Key.** Don't rely on auto-labeling for BPM/Key. Use external tools (Key-BPM-Finder at vocalremover.org) first, then let the LM generate captions only.

3. **VRAM management during LoRA training.** The Gradio UI loads both the LM and DiT. If you use the LM for auto-labeling, you may need to restart Gradio without the LM before preprocessing tensors to free VRAM.

4. **Genre Ratio should stay at 0.** LM-generated genres are less descriptive than captions. Captions carry the style information.

5. **Lyrics must be reviewed and cleaned.** Transcription tools produce errors. Remove LRC timestamps. Add structural tags `[Verse]`, `[Chorus]`, etc. for better training.

6. **tensorboard dependency.** LoRA training may fail without tensorboard installed. `pip install tensorboard` before training.

7. **Compressed audio degrades LoRA quality.** Use WAV or FLAC at 44.1kHz+, not MP3, for training data.

8. **2x RTX 3090 (48GB total) is ideal.** 16GB is the minimum but OOMs on longer songs. 20GB+ is comfortable. With 48GB you can run the XL 4B model + 4B LM + LoRA training simultaneously.

9. **`/v1/create_sample` and `/release_task` differ in startup cost.** The first call to either lazy-loads the DiT (~30s on GPU, ~60s on CPU). Subsequent calls are fast. For batch generation, prime the server with one warmup call, then queue the real batch.

10. **Polling timeout ≠ generation failure.** The cache directory pattern (see Http Api Gotchas) catches generations that completed after your poll deadline. Don't lose work to a tight timeout — always check the cache on timeout.

11. **`audio_duration` is a CAP, NOT a target.** ACE-Step generates audio until it runs out of lyrical content. When `thinking: false` (no 5Hz LM), actual duration is determined entirely by how many lyric lines you write — NOT by the `audio_duration` parameter. LINE-TO-DURATION MAP (verified 2026-06-23):
   - 15 lines → ~86 seconds
   - 25 lines → ~160 seconds  
   - 30+ lines → ~213 seconds (3:33) ✅
   - 40+ lines → ~270+ seconds
   Faster genres (slam, punk) need MORE lines — their lines take less time to vocalize. Always verify raw duration before trimming: `(stat_bytes - 44) / 192000`. If <200, the lyrics are too short — pad them or use `thinking: true` to let the LM expand. Source: ACE-Step discussion #95.

## Support Files

- `references/lora-training-deep-dive.md` — full LoRA training workflow details, dataset format, Gradio UI step-by-step, troubleshooting from official tutorial
- `references/model-zoo-and-hardware.md` — complete model zoo specs, GPU selection matrix, performance benchmarks
- `scripts/generate_song.py` — reusable CLI script for the cache-watch generation pattern. Posts to `/release_task` with `thinking:false`, watches cache dir for new WAV, optionally converts to MP3. Usage: `python scripts/generate_song.py --lyrics-file lyrics.txt --style "dark rap, 70 BPM, C minor" --output song.wav --convert-mp3`

## Push to Device & Play (Termux/Android)

After generating a song, the user may want it pushed to their phone
and played immediately. This pattern works for any Android device
running Termux with SSH access (e.g. Surface Duo 2 over Tailscale).

### Prerequisites (one-time setup on the phone)

```bash
# In Termux on the phone:
pkg install openssh termux-media-player
# Set a password and start SSH:
passwd
sshd -p 8022
```

### Push-and-play pipeline

```bash
# 1. Convert WAV → MP3 (smaller for transfer)
ffmpeg -y -i song.wav -codec:a libmp3lame -b:a 192k song.mp3

# 2. Stop any currently playing track
ssh -p 8022 -i ~/.ssh/phone_access droid@<phone-ip> 'termux-media-player stop'

# 3. SCP the MP3 to the phone
scp -P 8022 -i ~/.ssh/phone_access song.mp3 droid@<phone-ip>:~/song.mp3

# 4. Play it
ssh -p 8022 -i ~/.ssh/phone_access droid@<phone-ip> 'termux-media-player play ~/song.mp3'
```

### Notes

- `termux-media-player stop` returns "No track to stop" if nothing is
  playing — this is harmless, not an error.
- The phone SSH host is typically a Tailscale IP (e.g. 100.79.15.54:8022).
- SSH key is at `~/.ssh/phone_access` (Termux uses standard SSH key auth).
- `termux-media-player` supports `play`, `stop`, `pause`, `resume`.
- For batch syncs, see `~/bin/sync-metal-to-duo.sh` which SCPs all MP3s
  from a keep directory to the phone.

### Full end-to-end workflow (study → write → generate → push → play)

1. Study creator style: fetch YouTube transcripts (youtube-content skill),
   extract prose DNA (songwriting-and-ai-music skill section 11)
2. Write lyrics in that register with the user's thematic brief
3. Generate via ACE-Step `/release_task` with `thinking: false` and
   cache-watch pattern (see HTTP API Gotchas above)
4. Convert WAV → MP3 via ffmpeg
5. Push to phone via SCP + play via `termux-media-player`
6. Save lyrics to journal file (e.g. `~/lyrics/journal.md`)

Verified 2026-06-20: 95-second song generated in ~6s on GPU (RTX 3090),
converted in <1s, pushed and playing on Surface Duo 2 within 10s total.

## Related Skills

- `evolutionary-radio` — uses ACE-Step 2B as the radio's voice (queue-fill loop)
- `heartmula` — alternative open-source music model (3B/7B), Suno-like
- `songwriting-and-ai-music` — lyrics writing + Suno prompting techniques
- `comfyui` — ComfyUI can run ACE-Step via custom nodes for visual workflows
