# ACE-Step Duration: Lyrics Length = Actual Duration

Verified 2026-06-23 against ACE-Step discussion #95 and live generation on RTX 3090.

## The Rule

`audio_duration` is a **CAP**, not a target. ACE-Step generates audio until it
runs out of lyrical content. The DiT doesn't pad silence to fill the cap.

## Verified Line-to-Duration Map

Tested with `thinking: false` (`/release_task` endpoint), 4B XL SFT DiT, 50 inference steps:

| Lines | Raw Duration | Genre | Notes |
|-------|-------------|-------|-------|
| 15 | 86s | Slam death metal | Barked one-liners, minimal syllables |
| 30 | 213s | Slam death metal | 3 verses + 3 breakdowns + intro/outro |

## Duration Formula

```
# ACE-Step outputs 48kHz stereo 16-bit WAV
# 1 second = 48,000 × 2 channels × 2 bytes = 192,000 bytes
actual_duration = (file_size_bytes - 44) / 192000

# Target: >= 200 seconds for 3:33 after ffmpeg trim
```

## Two Paths to Correct Duration

| Path | `thinking` | Speed | Mechanism |
|------|-----------|-------|-----------|
| LM Planner | `true` | ~120s | 5Hz LM plans structure, respects `audio_duration` |
| Dense Lyrics | `false` | ~15s | 30-40 lines → ~213s, no LM needed |

Path B (dense lyrics + `thinking: false`) is faster and verified correct.
Path A (LM + `thinking: true`) is safer when you're unsure about line count.

## Genre Factor

Faster vocal delivery (slam, punk, speed metal) consumes fewer seconds per line.
Slower delivery (ballads, doom) fills more. For 3:33:

| Genre | Min Lines Needed |
|-------|-----------------|
| Rap (80-90 BPM) | 25-30 |
| Slam/Punk (110-180 BPM) | 30-40 |
| Ballad/Doom (60-80 BPM) | 20-25 |

## Discard Policy

If `actual_duration < 200`, the track is too short. Don't ffmpeg-extend with
silence — regenerate with more lyrics. The listener will hear the missing
content even if ffmpeg pads the container.
