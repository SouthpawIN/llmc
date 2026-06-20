---
name: lyric-journal
description: "Active lyric notebook — tracks every line, version, and edit. Collaborative editing where the user's voice always wins."
version: 1.0.0
tags: [lyrics, journal, notebook, songwriting, collaboration]
triggers:
  - lyric journal
  - writing lyrics
  - tracking lyrics
  - lyric notebook
---

# Lyric Journal

An active lyric notebook that lives at `~/lyrics/journal.md`. Every line the user writes is tracked, versioned, and preserved. Edits are collaborative — the user's voice always wins.

## Core Rules

1. **Favor what the user writes** — their lines stay theirs
2. **Edit WITH them, not OVER them** — suggest, don't overwrite
3. **Track versions** — when a line evolves, keep the original above the new version
4. **Build with "yes, and..." energy** — find the interesting angle, push concepts further
5. **Flag meter/rhyme opportunities** but NEVER force them
6. **Their voice always wins** — if they want a line that breaks meter, keep it

## Journal Format

The journal file (`~/lyrics/journal.md`) uses this structure:

```markdown
# Lyric Journal

> [User]'s active lyric notebook. Every line lives here.
> Edits are collaborative — their voice always wins.

---

## Entries

### Entry N — YYYY-MM-DD: [Title/Theme]

**Raw ([User]'s lines):**
\```
[original lines exactly as written]
\```

**Sonic notes:**
- [rhyme patterns, internal rhymes, sonic connections found in the raw lines]
- [meter observations — syllable counts, stress patterns]

**Questions for [User]:**
- [clarifying questions about intent, not edits]

**Possible directions (not edits — just "yes, and"):**
- [where the motif could go, not what it should be]

---

### Entry N+1 — YYYY-MM-DD: [Draft/Tightened]

**Draft M — [description]:**

Rhyme map: [section] = [rhyme pairs] · [section] = [rhyme pairs]

\```
[Verse 1]
[lyrics with structural tags]
[Chorus]
[lyrics]
\```

**Changes from Draft M-1 → Draft M:**
- [what changed and why]
```

## Workflow

### When the user drops new lyrics:
1. Append a new Entry to the journal with their raw lines
2. Analyze sonic patterns (rhymes, internal rhymes, meter, motifs)
3. Note what's working — be specific about WHY it works
4. Ask questions, don't make assumptions about intent
5. Offer "yes, and" directions, not corrections

### When tightening/editing:
1. Create a new Entry (don't overwrite the previous one)
2. Map the rhyme scheme explicitly
3. Show what changed and why
4. Keep Draft 1 above Draft 2 — version history matters

### When generating a song:
1. The lyrics from the latest draft go to ACE-Step
2. Structural tags ([Verse], [Chorus], etc.) must be in place
3. Note the style prompt used
4. Record which version was generated

## Analysis Checklist

When analyzing raw lyrics, check for:
- [ ] End rhymes (perfect, slant, assonance)
- [ ] Internal rhymes (words rhyming mid-line)
- [ ] Repeated sounds/consonance
- [ ] Syllable count per line (meter consistency)
- [ ] Stress patterns (da-DUM vs DUM-da)
- [ ] Motifs/recurring images
- [ ] The -ing test: are there gerund chains? Preserve them.
- [ ] The "does not apologize" opportunity: is there a natural metaphor to use?
- [ ] The reframe opportunity: is there a "weak" thing to reveal as powerful?

## Pitfalls

1. **Don't overwrite the user's lines.** Ever. If they wrote it, it stays in the journal.
2. **Don't force rhyme.** If a line breaks meter but hits harder, keep it.
3. **Don't be precious about rules.** Craft serves art, not the other way around.
4. **Don't lose versions.** Every draft is preserved. The evolution IS the art.
