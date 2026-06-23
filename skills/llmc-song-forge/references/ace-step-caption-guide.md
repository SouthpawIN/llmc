# ACE-Step Caption & Lyrics Format Guide

Summarized from official docs (INFERENCE.md, Tutorial.md) — June 2026.

## Caption (MOST critical input)

Be specific. Combine these dimensions:
- **Style/genre**: southern hip-hop, dark R&B, boom bap, progressive metal trap
- **Instruments**: piano, 808s, snare, strings, synth, guitar
- **Emotion**: aggressive, vulnerable, haunting, triumphant
- **Timbre/texture**: warm tape saturation, vinyl crackle, metallic reverb, analog warmth
- **Era/production**: 2008 Cash Money, 90s East Coast, Hans Zimmer cinematic
- **Vocals**: falsetto, chest voice, whispered, screamed, conversational
- **Rhythm**: double-time hi-hats, half-time drums, swing, syncopated
- **Dynamic arc**: whisper-to-scream, building, explosive chorus, fade out

Bad: "dark rap"
Good: "southern hip-hop, crisp snare on the three, sub-bass 808s with slow pitch glide, warm tape saturation, confident conversational delivery, 2008 Cash Money production, sparse piano stab on upbeats, building from minimalist verse to full-spectrum chorus"

## Lyrics Structure

### Section Tags (REQUIRED — with modifiers)
```
[Intro - spoken, sparse beat]
[Verse 1 - conversational, low energy]
[Pre-Chorus - building, melodic]
[Chorus - explosive, full beat, anthemic]
[Verse 2 - intense, rapid flow]
[Bridge - whispered, reverb-heavy]  OR  [Bridge - spoken, strings alone]
[Outro - soft, fading]
```

### Vocal/Energy Tags (use within sections)
- `[whispered]`, `[falsetto]`, `[raspy vocal]`, `[chest voice]`, `[screamed]`
- `[high energy]`, `[building energy]`, `[low energy]`
- Uppercase = intensity. (parentheses) = backing vocals / ad-libs.

### Syllable Control
- **6-10 syllables per line** — match line lengths across verses
- Avoid: adjective stacking, rhyme chaos, blurred section boundaries, mixed metaphors
- ONE core metaphor per song. Don't switch metaphors mid-verse.

### Avoid AI-Flavored Lyrics
- No adjective stacking: "beautiful painful endless dark night"
- No rhyme chaos: forcing rhymes at the cost of meaning
- No blurred boundaries: don't make the chorus indistinguishable from the verse
- No mixed metaphors: stick to ONE domain per song (metal/forging, water/river, architecture)

## Metadata

- `bpm`: 30-300. LM auto-infers. Set manually only for specific needs.
- `keyscale`: e.g. "F# minor", "D minor". Auto-detected.
- `timesignature`: "4" for standard, "6" for triplet feel ballads.
- `duration`: -1.0 = auto from lyrics (only works with `thinking: true`)

## Key Takeaway

The caption describes WHAT you want to hear.
The lyrics describe WHEN you want to hear it.
The metadata anchors both.

**NEVER use `thinking: false`** — it skips the LM planner and duration is ignored.