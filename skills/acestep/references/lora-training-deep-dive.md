# ACE-Step LoRA Training — Deep Dive

Condensed from the official tutorial at
https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/LoRA_Training_Tutorial.md
and FM9 guide at https://fm9.ai/ace-step/lora-training

## Dataset Format (Per Song)

Each song in the dataset folder needs:

| File | Required | Notes |
|------|----------|-------|
| `{name}.mp3` / `.wav` / `.flac` / `.ogg` / `.opus` | Yes | Audio file |
| `{name}.lyrics.txt` | Yes | Lyrics with structural tags |
| `{name}.json` | Optional | Annotations: caption, bpm, keyscale, timesignature, language |
| `{name}.caption.txt` | Optional | Free-text caption (can also be in JSON) |

JSON annotation example:
```json
{
  "caption": "A high-energy trap beat with deep 808s and hi-hats",
  "bpm": 140,
  "keyscale": "C minor",
  "timesignature": "4",
  "language": "en"
}
```

## Gradio UI Step-by-Step (Official Tutorial)

### Prerequisite: Disable Service Pre-Init
- Windows (`start_gradio_ui.bat`): `INIT_SERVICE=--init_service true` → `--init_service false`
- Linux/macOS (`start_gradio_ui.sh`): `INIT_SERVICE:=--init_service true` → `--init_service false`

### Step-by-Step

1. **Load Models** (optional) — Select LM model if auto-labeling needed; otherwise skip
2. **Load Data** — LoRA Training tab → enter dataset path → **Scan**
   - Auto-recognizes audio, lyrics, caption, JSON, CSV
3. **Review & Adjust**
   - Duration auto-read from audio
   - Lyrics need `.lyrics.txt`
   - Labeled column shows ✅/❌
   - Uncheck "All Instrumental" if not all instrumental
   - Genre Ratio → **keep at 0** (LM genres less descriptive than captions)
   - Custom Trigger Tag has limited effect
4. **Auto Label** (skip if captions exist)
   - **Get BPM/Key from external tool FIRST** — LM generates hallucinated BPM/Key
   - Key-BPM-Finder at vocalremover.org (local processing, not uploaded)
   - Export CSV, place in dataset folder
5. **Review & Edit** — Edit entry by entry; **click Save after each edit**
6. **Save Dataset** — Export as JSON file
7. **Preprocess Tensors**
   - If VRAM insufficient after LM use → **restart Gradio without LM model**, reload
8. **Start Training** — Monitor loss; should decrease steadily without spiking
9. **Test** — Load LoRA checkpoint, generate with style prompts

## Training Parameters (Recommended from FM9)

| Parameter | Recommended | Range | Note |
|-----------|-------------|-------|------|
| LoRA Rank | 16 | 4-64 | Higher = more capacity, slower |
| LoRA Alpha | 32 | 8-128 | Usually 2× rank |
| Learning Rate | 1e-4 | 5e-5 – 5e-4 | Lower for small datasets |
| Batch Size | 4 | 1-16 | Reduce if OOM |
| Epochs | 50-150 | 20-500 | Monitor for overfitting |
| Warmup Steps | 50 | 0-200 | Stabilizes early training |

The official tutorial used: batch size 1, 500 epochs, on 13 tracks.
FM9 recommends: batch size 4, 100 epochs as a starting point.

## Lyrics Transcription & Cleanup

### Tools
- `acestep-transcriber` (HuggingFace) — self-hosted, no structural tags
- Gemini API — **adds structural tags** `[Verse]`, `[Chorus]`, `[Bridge]`
- Whisper — self-hosted, no structural tags
- ElevenLabs Scribe — paid, generous free tier

### Provided Scripts (in ACE-Step repo)
- `scripts/lora_data_prepare/whisper_transcription.py` — via OpenAI Whisper API
- `scripts/lora_data_prepare/elevenlabs_transcription.py` — via ElevenLabs Scribe API
- Both support `process_folder()` for batch processing

### Cleanup Required
Transcribed lyrics MUST be manually reviewed. Remove LRC timestamps:
```python
import re
def clean_lrc_content(lines):
    result = []
    for line in lines:
        line = line.strip()
        if not line: continue
        cleaned = re.sub(r"\[\d{2}:\d{2}\.\d{1,3}\]", "", line)
        result.append(cleaned)
    while result and not result[-1]: result.pop()
    return result
```

### Structural Tags (Optional but helpful)
Tags like `[Verse]`, `[Chorus]`, `[Bridge]` help the model learn song structure.
Tip: Use Gemini to add structural tags to existing lyrics.

## Stem Separation (for cleaner training data)

```bash
pip install demucs
python -m demucs --two-stems=vocals audio/mixed_track.wav
```

Use Demucs to isolate vocals or instruments for cleaner LoRA training signal.

## Known Issues

1. **tensorboard missing** — LoRA training fails without it. `pip install tensorboard`
2. **torchaudio duration check fails** — Issue #283: some audio formats cause `torchaudio.info()` to fail in the scan step. Convert to WAV first.
3. **Training appears stuck on Windows** — Issue #233: GPU busy indicator shows activity but no progress updates. Check GPU utilization via `nvidia-smi`.
4. **LoRA training error on fresh install** — Issue #129: multiple dependency conflicts. Use `uv sync` from the repo root.
5. **folder scan errors** — Ensure audio filenames don't have special characters.

## Hardware Benchmarks (from official README)

- **<2s per full song** on A100
- **<10s on RTX 3090** (2B turbo)
- **LoRA training**: ~1 hour on RTX 3090 / 12GB from 8 songs
- **Generation**: 10 seconds to 10 minutes (configurable `audio_duration`)
- **Batch**: up to 8 songs simultaneously
