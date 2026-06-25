---
name: llmc-song-pipeline
description: "Standardized LLMC song creation pipeline: lyric writing → ACE-Step generation → MP3 conversion → Discord delivery → playlist integration. Enforces naming, format, and delivery conventions."
version: 1.0.0
tags: [music, llmc, ace-step, song-forge, discord, pipeline, mc-baldiee]
triggers:
  - generate songs
  - llmc batch
  - create song
  - song forge
  - batch generate
---

# LLMC Song Pipeline — Standardized

The definitive pipeline for batch song creation. Every time the user asks for songs, follow this exact process.

## 1. Lyric Writing

### Style: Mc.Baldiee Cosmic Prose
Load the `mc-baldiee-prose` skill for the full style guide. Core rules:

- **Direct 2nd-person address** — speak TO the listener
- **Cosmic/natural metaphors ONLY** — oceans, stars, rivers, storms, embers, tides, fire, sky, bone, ash, lighthouses, serpents, compasses. Never literal.
- **Reframing declarations** — take the "weak" thing and reveal its power
- **The "does not apologize" pattern** — in pre-choruses and bridges
- **No explicit morality** — never say "you should." Paint the image.
- **Body/soul imagery** — ribs, bones, veins, marrow as containers of spirit
- **The -ing motif** — preserve and extend gerund chains from the user's lines

### Structural Tags (ACE-Step compatible)
```
[Verse 1]      — Story, scene-setting, the observation
[Pre-Chorus]   — The "does not apologize" pattern, tension ramp
[Chorus]       — The emotional core, the hook, the reframe
[Verse 2]      — Deepen the theme, new angle
[Pre-Chorus]   — Variation on the pattern
[Chorus]       — Repeat for memorability
[Bridge]       — The turn. Break rhyme for raw impact.
[Outro]        — Resolution, echo opening lines, the thesis
```

### Duration Rule
ACE-Step's `audio_duration` parameter is a CAP, not a target. Actual duration is determined by **lyric line count** when `thinking: false`:

| Lines | Duration |
|-------|----------|
| 15    | ~86s     |
| 25    | ~160s    |
| 30+   | ~213s (3:33) ✅ |
| 40+   | ~270s    |
| 60+   | ~300s (5:00) |

**For 3:33+ minimum: write 40+ lines per song.** 60+ lines reliably hits 300s (5:00).

### Anti-Repetition Rules
- Every song must have a **completely distinct lyrical theme** — no shared metaphors between songs
- Do not reuse imagery across songs (if song 1 uses lighthouses, song 2 cannot)
- Do not reuse chorus structures or hook patterns
- Vary the metaphor system per song: one song = rivers, next = eclipses, next = serpents, etc.
- The user has noticed LLMC tends to be repetitive — actively counter this

## 2. Song Naming Convention

**Title format:** `NN_descriptive_title_snake_case`

- `NN` = zero-padded order number (01, 02, 03...)
- Title in snake_case (underscores for spaces)
- Example: `01_the_architects_hands`, `04_anti_icon`

**Display title:** Title Case with spaces — "The Architect's Hands", "Anti-Icon"

## 3. File Structure

Every song produces exactly **3 files**, all named with the song's snake_case title:

```
output/
├── 01_the_architects_hands.mp3          # The song (192kbps MP3)
├── 01_the_architects_hands.wav           # Raw WAV (for re-processing)
├── 01_the_architects_hands_lyrics.txt    # Lyrics + metadata header
├── 02_the_river_forgets_the_mountain.mp3
├── 02_the_river_forgets_the_mountain.wav
├── 02_the_river_forgets_the_mountain_lyrics.txt
└── ...
```

### Lyrics File Format
Every lyrics file MUST have this header:
```
LLMC — [Title in Title Case]
Theme: [one-line theme description]
Style: [full style prompt used for ACE-Step]
BPM: [bpm] | Key: [key] | Duration: ~[duration]s ([min] min)
============================================================

[Full lyrics with structural tags]
```

## 4. Style Prompt Diversity

Each song in a batch gets a **different style prompt**. Rotate through:

| Style | BPM range | Key | Characteristics |
|-------|-----------|-----|-----------------|
| Dark cinematic rap | 70-80 | C minor, D minor | Deep 808s, haunting piano, orchestral strings, trap production |
| Dark ambient spoken word | 60-65 | D minor, A minor | Drone, no drums, VHS dreamcore, ethereal reverb |
| Cinematic orchestral | 75-90 | Bb minor, D minor | Sweeping strings, french horns, gothic, choir, crescendo |
| Industrial dark trap | 130-140 | F minor, G minor | Distorted bass, menacing 808s, GHOSTEMANE-style, horror |
| Cinematic boom bap | 85-95 | E minor, A minor | Dusty drums, jazz piano, upright bass, noir atmosphere |

Never use the same style prompt for two songs in the same batch.

## 5. ACE-Step Generation

### API: POST http://127.0.0.1:8001/release_task

```python
payload = {
    "prompt": style_prompt,        # Style tags (NOT "query")
    "lyrics": lyrics,              # Full lyrics with [Verse], [Chorus] tags
    "thinking": False,             # Skip LM planner — fastest path
    "use_format": False,
    "bpm": bpm,
    "key_scale": key_scale,
    "time_signature": "4",
    "vocal_language": "en",
    "inference_steps": 50,         # Full quality. NEVER use 8 (turbo = silence)
    "guidance_scale": 7.0,
    "audio_duration": 300,         # CAP — actual duration from line count
    "audio_format": "wav",
    "task_type": "text2music"
}
```

### Cache-Watch Pattern (CRITICAL)

The `/query_result` endpoint is unreliable. **Always watch the cache directory:**

```python
from pathlib import Path
import time, shutil

CACHE = Path('/home/sovthpaw/Models/ace-step/.cache/acestep/tmp/api_audio')

# 1. Snapshot BEFORE posting task
baseline = {p.name for p in CACHE.glob('*.wav')}

# 2. Post task
post_release_task(...)

# 3. Watch for NEW file (not any file — must be NEW since baseline)
deadline = time.time() + 300
while time.time() < deadline:
    current = {p.name for p in CACHE.glob('*.wav')}
    new_files = current - baseline
    if new_files:
        # Get the NEWEST file that wasn't in baseline
        new_wavs = [p for p in CACHE.glob('*.wav') if p.name in new_files]
        newest = max(new_wavs, key=lambda p: p.stat().st_mtime)
        break
    time.sleep(1)
```

**PITFALL:** If you sort ALL files by mtime without filtering to `new_files`, you may grab a stale file from a previous session. ALWAYS filter to `current - baseline` first, THEN sort by mtime.

### VRAM Management

ACE-Step needs ~10GB free VRAM. On a dual-GPU system with turbofit services:

1. Check `nvidia-smi --query-gpu=index,memory.free --format=csv,noheader`
2. If both GPUs are full, stop `turbofit-carnice` (frees ~20GB on GPU 1)
3. Kill existing ACE-Step process
4. Restart on freed GPU: `CUDA_VISIBLE_DEVICES=1 ... python -m uvicorn acestep.api_server:app --port 8001`
5. Call `POST /v1/init` to eagerly load models
6. Generate songs
7. **Restart Carnice** when done: `systemctl --user start turbofit-carnice.service`

Never stop `turbofit-darwin-28b-reason` — the active session runs through it.

### Batch Generation

For 8+ songs, post tasks **one at a time** and wait for each cache file before posting the next. ACE-Step processes tasks sequentially, but posting all at once makes it impossible to match output files to songs.

If you must batch-post (for speed), record the exact timestamp of each POST and match cache files by creation time in order.

## 6. MP3 Conversion

```bash
ffmpeg -y -i song.wav -codec:a libmp3lame -b:a 192k song.mp3
```

## 7. Discord Delivery (MANDATORY FORMAT)

Every song MUST be delivered to Discord as **two separate messages**:

### Message 1: The Song
```
🎵 **LLMC — [Title in Title Case]**
*Theme: [one-line theme]*
*[BPM] BPM, [Key] | ~[duration]s ([min] min) ✅*

MEDIA:/path/to/NN_song_name.mp3
```

### Message 2: The Lyrics
```
📜 Lyrics: [Title in Title Case]

MEDIA:/path/to/NN_song_name_lyrics.txt
```

### Send command
```bash
hermes send -t discord:[CHANNEL_ID] "🎵 **LLMC — Title**
*Theme: ...*
*70 BPM, C minor | ~300s (5:00) ✅*

MEDIA:/path/to/song.mp3"
```

### Final Message: Batch Summary
```
🎵 **LLMC Batch Complete — N/N songs**

All songs: [duration]s each — all meet 3:33+ minimum ✅

• **Song Title** — theme (BPM, Key)
• **Song Title** — theme (BPM, Key)
...

*Style: Mc.Baldiee cosmic prose + [other influences]*
*Influences: [all influences listed]*
```

## 8. Playlist Integration

Copy each MP3 to the playlist directory:
```bash
cp song.mp3 ~/music/output/llmc-playlist/llmc_NN_song_name.mp3
```

This feeds Evolutionary Radio's track queue.

## 9. Lyric Journal Update

After every batch, append to `~/lyrics/journal.md`:

```markdown
### Entry N — [DATE]: LLMC Batch — [N] Songs ([brief description])

**Session brief:**
- [What the user asked for]

**Influences compiled:**
- [All influences]

**Songs generated:**
1. **Title** — theme (BPM, key, style)
2. **Title** — theme (BPM, key, style)
...

**Technical notes:**
- [Line counts, duration results, GPU status, any issues]
```

## 10. Post-Generation Cleanup

1. **Restart Carnice** if it was stopped
2. **Verify all songs** meet 3:33 minimum: `(wav_size - 44) / 192000 >= 213`
3. **Verify all files** exist: MP3, WAV, lyrics TXT for each song
4. **Verify playlist** has all songs
5. **Verify Discord** received all songs + lyrics + summary

## Pitfalls

1. **Cache file matching** — always filter to `current - baseline` before sorting by mtime. Grabbing the newest file without filtering picks up stale files from previous sessions.
2. **Turbo mode = silence** — `inference_steps: 8` produces -27dB noise. Always use 50.
3. **Don't batch-post without tracking** — if you post all tasks at once, you can't match outputs to songs by timestamp alone (multiple files appear at once).
4. **`audio_duration` is a CAP** — 30 lines won't give you 300s just because you set `audio_duration: 300`. You need 60+ lines.
5. **Field name `prompt` not `query`** — `/release_task` uses `prompt`. `/v1/create_sample` uses `query`. Don't mix them up.
6. **GPU contention** — if turbofit services hold all VRAM, ACE-Step falls back to CPU (4-15 min per song vs 2-3s on GPU). Always free VRAM first.
