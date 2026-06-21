# LLMC — LLM + MC. Your Lyric & Song Companion

A Hermes Agent profile — an LLM that's also an MC. Collaborates with you to write metaphorical, prophetic lyrics (Mc.Baldiee style) and forge them into songs via ACE-Step.

## Install

```bash
hermes profile install github.com/SouthpawIN/llmc
```

Then launch:
```bash
hermes -p llmc
```

## What it does

1. **Chat about themes** — describe a feeling, a situation, an idea
2. **Write lyrics** — Mc.Baldiee prose register: metaphorical, cosmic, never explicit
3. **Generate the song** — ACE-Step v1.5 on local GPU (~6s per song)
4. **Push to Discord** — MP3 + lyrics sent to your channel
5. **Build a playlist** — tracks feed into Evolutionary Radio

## Skills Included

| Skill | Description |
|-------|-------------|
| `mc-baldiee-prose` | Prose DNA extracted from 6 Mc.Baldiee videos — metaphorical, prophetic, never explicit |
| `lyric-journal` | Active lyric notebook — tracks every line, version, and edit |
| `song-forge` | End-to-end pipeline: lyrics → ACE-Step → MP3 → Discord → playlist |

## Requirements

- Hermes Agent >= 0.12.0
- ACE-Step v1.5 API running locally (GPU recommended)
- ffmpeg for audio conversion
- Discord bot token (for sharing songs)

## Style

Default genre: dark cinematic rap. Adjustable per song.

The prose style follows Mc.Baldiee's cosmic spoken-word videos:
- Direct 2nd-person address
- Cosmic/natural metaphors only (oceans, stars, rivers, fire, bone)
- Reframing declarations ("Tears are not surrender. They are the tide's confession.")
- The "does not apologize" pattern ("The river does not apologize for flowing.")
- No explicit morality — paint images that imply truths

## License

MIT
