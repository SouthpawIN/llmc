# LLMC — Song Forger & Creative Music Agent

![LLMC](https://v3b.fal.media/files/b/0a9fe98d/3gpcxPgerAOI5bEpZTsSI_9rTvA7HD.png)

## What LLMC Does

LLMC is a creative music agent — "an LLM that's also an MC." It collaborates with the user to write lyrics in the Mc.Baldiee prose register (metaphorical, cosmic, never explicit) and generates full songs via ACE-Step, a local music generation model. The workflow: discuss themes → write lyrics → generate songs → deliver to Discord → add to Evolutionary Radio playlist.

- **Writes lyrics** in Mc.Baldiee style — lighthouse metaphors, cosmic imagery, implicit truths through concrete scenes
- **Generates songs** via ACE-Step API (local, GPU-accelerated, ~2-3s per track on RTX 3090)
- **Tracks everything** in a lyric journal — every version, every session, every song
- **Delivers** to Discord as two-message format: audio file + lyrics with metadata
- **Builds playlists** for Evolutionary Radio — every batch feeds the radio's track queue

## Quick Start

### Install
```bash
hermes profile install https://github.com/SouthpawIN/llmc
```

### Verify
```bash
hermes profile list
```

### Run
```bash
hermes chat --profile llmc
```

## Example Prompts

- *"Write a song about the moment you realize you've outgrown someone — not angry, just distant, like watching a ship disappear over the horizon"*
- *"I've got these lines: 'the architect's hands were never shaking / the blueprint was wrong from the start.' Build a full song around them."*
- *"Generate a batch of 3 songs — dark cinematic rap, completely distinct themes. No shared metaphors between songs."*
- *"What's in the lyric journal from last session? Let me see what we wrote."*
- *"Push the latest batch to Discord and add it to the Evolutionary Radio playlist."*
- *"Change the style — give me an industrial dark trap track, GHOSTEMANE-style distortion, 140 BPM."*

## Key Features
- **Mc.Baldiee prose register** — metaphorical, cosmic, never explicit. Translates themes into imagery.
- **ACE-Step integration** — local music generation at `http://127.0.0.1:8001`, GPU-accelerated, 50 inference steps for full quality
- **Anti-repetition system** — every song in a batch has completely distinct lyrical themes, no shared metaphors
- **Batch workflow** — theme discussion → lyric writing → song generation → Discord delivery → playlist integration
- **Style diversity** — 5 preset styles (dark cinematic rap, ambient spoken word, orchestral, industrial trap, boom bap), rotated per batch
- **Duration mastery** — ACE-Step's audio_duration is a cap, actual duration from line count. 60+ lines reliably hits 300s (5:00)
- **File naming convention** — `NN_song_name.mp3`, matching lyrics file, consistent across batches

## Workflow

```
User theme → LLMC (discuss + write lyrics) → ACE-Step (generate WAV) → ffmpeg (MP3) → Discord (2 messages) → Evolutionary Radio (playlist)
```

## Song Delivery Format

Every song is delivered to Discord as two separate messages:

**Message 1 — The Song:**
```
🎵 **LLMC — [Title]**
*Theme: [one-line theme]*
*[BPM] BPM, [Key] | ~[duration]s ([min] min) ✅*

MEDIA:/path/to/song.mp3
```

**Message 2 — The Lyrics:**
```
📜 Lyrics: [Title]
MEDIA:/path/to/lyrics.txt
```

## Style Presets

| Style | BPM | Key | Character |
|-------|-----|-----|-----------|
| Dark cinematic rap | 70-80 | C/D minor | Deep 808s, haunting piano, orchestral strings, trap |
| Dark ambient spoken word | 60-65 | D/A minor | Drone, no drums, VHS dreamcore, ethereal reverb |
| Cinematic orchestral | 75-90 | B♭/D minor | Sweeping strings, french horns, gothic choir |
| Industrial dark trap | 130-140 | F/G minor | Distorted bass, menacing 808s, GHOSTEMANE-style |
| Cinematic boom bap | 85-95 | E/A minor | Dusty drums, jazz piano, upright bass, noir |

## Integration with Other Agents

LLMC is a creative specialist. It collaborates with:

- **Senter** — routes music requests to LLMC from Discord or CLI
- **Anser** — catches music-related Discord questions and plans song projects
- **Frieza** — manages the Evolutionary Radio infrastructure that plays LLMC's tracks
- **Kashik** — documents LLMC's workflow patterns and anti-repetition strategies for the fleet's institutional memory

## Configuration
`~/.hermes/profiles/llmc/config.yaml`

Key settings:
- `ace_step_url` — ACE-Step API endpoint (default: `http://127.0.0.1:8001`)
- `output_dir` — where songs land (default: `~/music/output/llmc-playlist/`)
- `lyric_journal_path` — journal file path (default: `~/lyrics/journal.md`)
- `default_style` — fallback style prompt (default: dark cinematic rap)
- `discord_channel` — where songs are delivered

## Troubleshooting

**ACE-Step not generating:** Check the API is running (`curl http://127.0.0.1:8001/health`). If it's down, ACE-Step needs ~10GB free VRAM. Stop turbofit-carnice temporarily if needed, restart ACE-Step on the freed GPU, generate, then restart Carnice.

**Songs too short:** ACE-Step's `audio_duration` is a cap, not a target. Write 40+ lines for 3:33+, 60+ lines for 5:00. Line count determines actual duration.

**Repeated imagery across songs:** The anti-repetition rules are strict — each song in a batch needs a completely different metaphor system. If song 1 uses lighthouses, song 2 cannot. Vary the metaphor system per song.

---

*Part of the multi-agent fleet by SouthpawIN*
