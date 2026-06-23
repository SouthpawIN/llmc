---
name: slam-song-forge
description: "End-to-end brutal death metal / slam AND metallic hardcore / beatdown song generation pipeline. PeelingFlesh gangster slam + Kublai Khan-style hardcore. Lyrics to ACE-Step generation to 3:33 MP3 output to Discord push."
version: 1.1.0
tags: [slam, death-metal, brutal-deathcore, peelingflesh, hardcore, beatdown, kublai-khan, metallic-hardcore, music, ace-step, generation, beats, metal]
triggers:
  - generate slam songs
  - make death metal songs
  - create slam album
  - brutal death metal
  - PeelingFlesh style
  - slam deathcore
  - gangster slam
  - make hardcore songs
  - beatdown hardcore
  - Kublai Khan style
  - metallic hardcore
  - Nomad style
  - 3:33 songs
---

# SLAM Song Forge v1.1 — PeelingFlesh Gangster Slam + Kublai Khan Beatdown Hardcore

Brutal death metal / slam pipeline AND metallic hardcore / beatdown pipeline. Two genre DNAs, one tool. ACE-Step generation → 3:33 MP3 trim → Discord push.

**Genre 1: PeelingFlesh Gangster Slam** — downtuned guitars, blast beats, guttural growls, DJ scratches, gangster swagger.
**Genre 2: Kublai Khan Beatdown Hardcore** — beefy hardcore chords, shouted strained vocals, personal struggle, crushing breakdowns.

See `references/kublai-khan-dna.md` for full Kublai Khan / Nomad album research.

## Architecture

```
Slam DNA (PeelingFlesh genre analysis) → ACE-Step /release_task → Cache-watch WAV
  → ffmpeg trim to 3:33 → MP3 → Discord push
```

## Genre DNA — PeelingFlesh Gangster Slam

### What Is Slam?

A brutal death metal subgenre characterized by:
- **Downtuned guitars** (7-string, 8-string, Drop G/F#), palm-muted chugs
- **Blast beats** alternating with slow, crushing breakdown grooves
- **Guttural vocals** — deep growls, pig squeals, tunnel throat
- **Minimal melody** — focus on rhythmic groove and heaviness, not melody
- **Slam riffs** — chromatic, syncopated, pit-call breakdowns
- **Production** — brick-walled, triggered drums, raw but massive

### PeelingFlesh's Unique Crossover

What makes PeelingFlesh distinct is the **hip-hop / gangster crossover**:

| Element | Pure Death Metal | PeelingFlesh Slam |
|---------|-----------------|-------------------|
| Attitude | Satanic / gore | Street dominance / gangster swagger |
| Features | Other metal vocalists | DJ scratches, hardcore shoutouts |
| Lyrics | Occult, gore, philosophy | Boasting, threats, street violence, dark humor |
| Structure | Technical riff-salad | Groove-focused, pit-call breakdowns |
| Vocal delivery | Pure growl | Growl + hardcore shout + occasional spoken |
| Samples | Horror movie clips | Police scanner, street dialogue, skits |

### The 3 Registers (Slam Edition)

**Register 1: Brutal Death Growl**
- Deep guttural delivery, low-register tunnel throat
- Technical riff backing, blast beats
- Lyrical content: violence, gore, body horror imagery
- Delivery tags: `[guttural]`, `[tunnel throat]`, `[low growl]`

**Register 2: Hardcore Shout / Gangster Swagger**
- Mid-register barked vocals, call-and-response
- Groove-metal backing, two-step beats, breakdowns
- Lyrical content: dominance, threats, street credibility
- Delivery tags: `[shouted]`, `[barked]`, `[crowd call]`

**Register 3: Spoken Skit / Sample Drop**
- Clean spoken word over ambient or sparse beat
- Police scanner samples, street dialogue, moralistic outro
- Lyrical content: narrative framing, dark ironic humor
- Delivery tags: `[spoken]`, `[clean]`

### Blend Rules

| Dimension | Brutal Death | Gangster Swagger | Spoken/Skit |
|-----------|-------------|------------------|-------------|
| Vocal style | Low growl, pig squeal | Mid bark, hardcore shout | Clean spoken |
| Riff style | Chromatic slam riffs, blast beats | Groove metal, two-step | Sparse, ambient |
| Hook style | Repeated phrase (growled) | Call-response chant | N/A (narration) |
| Emotional tone | Violent, crushing | Dominant, confrontational | Ironic, narrative |

## Lyric Structure — Slam Format

Slam songs use a DIFFERENT structure than rap. Key differences:
- **Breakdowns replace bridges** — the mosh-call is the emotional peak
- **Shorter verse sections** — 4-6 lines rather than 8-12
- **Repeated slam calls** — single phrases growled repeatedly
- **No melodic choruses** — the hook is a grooved breakdown, not sung

```
[Intro - spoken sample, ambient]       — atmospheric intro, skit, sample
[Riff Drop - explosive, guttural]      — first massive riff, "OOOOH"
[Verse 1 - growled, mid-tempo groove]  — 4-6 lines, dense imagery
[Breakdown - slow, crushing]           — THE pit call, repeated phrase
[Verse 2 - blast beats, intense]       — 4-6 lines, escalate violence
[Breakdown - grooved, crowd call]      — second wave, call-response
[Skit/Interlude - spoken, sparse]      — DJ scratch, sample drop
[Outro - slow, crushing fade]          — final breakdown, fade to noise
```

### Slam Lyric Content — Thematic Domains

**DO write about:**
- Street violence and dominance ("my guns bigger than yours")
- Body horror and gore ("skin blunt", "full of lead")
- Confrontational challenges ("who the fuck you think you is")
- Dark ironic humor (cheese board parables, absurd threats)
- Code violations, rule-breaking, anti-authority

**DON'T write about:**
- Satanic occultism (that's black metal, not slam)
- Viking mythology (that's folk metal)
- Emotional vulnerability (wrong genre entirely)
- Love, relationships, heartbreak (save that for LLMC forge)
- Political commentary (slam is visceral, not intellectual)

### Slam Lyric Techniques

1. **One-word slam calls** — "BREEE", "OOOH", "WHAT", "GO", "MOVE"
2. **Repeated violation phrases** — "concrete curb enforcement" (3-4x)
3. **"My X better than your X" chains** — PeelingFlesh signature
4. **Audio samples as narrative** — police scanner, street dialogue
5. **Absurd moral parables** — cheese board trap, booty shirt warning
6. **G-code / rulebook framing** — street codes, violation systems

## Beat Diversity Templates (Slam Edition)

**NEVER use the same BPM, key, or riff style twice in a batch.**

| Style | BPM | Key | Tags |
|-------|-----|-----|------|
| Classic Slam | 110 | Drop F# | downtuned 8-string chugs, chromatic slam riffs, triggered kicks, guttural tunnel throat, raw brick-wall production |
| Blast Beat Assault | 180 | Drop G | blast beats, tremolo picking, pig squeal highs, technical death metal, chaotic, relentless |
| Groove Slam | 95 | Drop F | mid-tempo groove, palm-muted chugs, hardcore two-step, barked crowd calls, swinging breakdown |
| Deathcore Crossover | 130 | Drop A | djent staccato riffs, deathcore breakdowns, layered growls, atmospheric pads, syncopated chugs |
| Street Slam | 105 | Drop G# | gangster swagger, DJ scratch textures, 808 sub-drops with guitars, hardcore shouts, police scanner samples |
| Beatdown Hardcore | 85 | Drop E | slow crushing beatdown, single-note chugs, fight riffs, gang vocals, minimal drums, maximum weight |
| Technical Brutal Death | 160 | C# standard | technical riffs, sweep picking, gravity blasts, dual vocal trade-offs, complex time signatures |
| Slam-Grind | 200 | Drop G | grindcore speed, slam breakdowns, micro-songs, noise textures, chaotic blast-to-groove switches |
| Doom Slam | 60 | Drop F | funeral doom pace, massive slow riffs, reverb-drenched growls, crushing atmosphere, sub-bass resonance |
| Industrial Slam | 115 | Drop G | industrial percussion, distorted synth bass, glitch textures, metallic clang, mechanical groove |

**NEVER use the same beat style twice in one batch.**

## ACE-Step Generation Pipeline

### Prerequisites
- ACE-Step API running at `http://127.0.0.1:8001`
- GPU with ~9GB+ free VRAM
- ffmpeg installed for trim + convert

### Key Differences from Rap Pipeline

1. **Style prompt is METAL-FOCUSED** — describe guitars, drums, vocal style for death metal
2. **BPM range is higher** — 85-200 for slam vs 65-90 for rap
3. **Key selection matters less** — slam uses low tunings (Drop F-G), ACE-Step may not nail the guitar tone but gets the energy
4. **Vocal language: "en"** even though it's guttural — ACE-Step needs to know it's English lyrics
5. **Structure tags use `[Breakdown]` instead of `[Bridge]`**

### Style Prompt Template (Slam)

```
brutal death metal slam, downtuned 8-string guitars in Drop F,
palm-muted chromatic chugs, triggered kick drums at 110 bpm,
blast beats alternating with slow crushing breakdowns,
guttural tunnel throat vocals, pig squeal highs,
raw brick-wall production, PeelingFlesh style gangster slam,
DJ scratch textures, police scanner samples
```

### Pipeline Steps (same as LLMC forge)

```python
payload = {
    "prompt": "<slam style tags>",
    "lyrics": "<lyrics with slam structure tags>",
    "thinking": False,
    "use_format": False,
    "bpm": 110,
    "key_scale": "Drop F#",       # Low tuning — ACE-Step may re-map
    "time_signature": "4",         # Most slam is 4/4
    "vocal_language": "en",
    "inference_steps": 50,         # FULL QUALITY
    "guidance_scale": 7.0,
    "audio_duration": 213,         # Target 3:33
    "audio_format": "wav",
    "task_type": "text2music",
}
```

### CRITICAL: Lyric Length Drives Duration (NOT audio_duration)

**ACE-Step's `audio_duration` param is a CAP, not a target.** The model generates
audio until it runs out of lyrical content. When `thinking: false` (no 5Hz LM to
expand), the actual duration is determined entirely by how many lyric lines you write.

LINE-TO-DURATION MAP (verified 2026-06-23):
- 15 lines → ~86 seconds (1:26)
- 25 lines → ~160 seconds (2:40)
- 30+ lines → ~213 seconds (3:33) ✅
- 40+ lines → ~270+ seconds (4:30+)

**RULE: For 3:33 target, write 30-40 lines MINIMUM.** Slam's barked one-liners
take less time than rap bars — you need MORE slam lines for the same duration.

```bash
# Verify actual duration before trimming
RAW_BYTES=$(stat -c%s input.wav)
DURATION=$(echo "scale=1; ($RAW_BYTES - 44) / 192000" | bc)
echo "Actual: ${DURATION}s"  # Must be >= 200 for 3:33 target
```

### CRITICAL: 3:33 Trim

```bash
ffmpeg -y -i input.wav -t 213 -codec:a libmp3lame -b:a 192k output.mp3
ffprobe -v quiet -show_entries format=duration -of csv=p=0 output.mp3
```

### Cache Directory
```
/home/sovthpaw/Models/ace-step/.cache/acestep/tmp/api_audio/
```

## Sample Songs (Edit These)

### Track 01 — "Shoot 2 Kill" (Classic Slam)

```
Style: brutal death metal slam, downtuned 8-string guitars in Drop F#, chromatic slam riffs, triggered kick drums, blast beats into slow crushing breakdown, guttural tunnel throat vocals, pig squeal accents, raw brick-wall production, 110 bpm, gangster attitude, street execution energy
BPM: 110
Key: F# minor
Time: 4/4

[Intro - police scanner sample, ambient noise]
This morning shortly before 1am... suspect pulled her out the car...
shoved her to the ground... drove away in her vehicle...
(shoot to kill)

[Riff Drop - explosive, full band, guttural]
SHOOT TO KILL
NO WITNESS NO APPEAL
LEAVE NO TRACE LEAVE NO FEAR
BREEE

[Verse 1 - mid-tempo groove, growled]
Concrete evidence buried under fresh cement
Body count rising and I haven't even paid the rent
Street coroner on payroll chalk lines on every curb
This is G-code enforcement and you just broke every word
No statute of limitations on a street code violation
The sentence is the same whether rat or hesitation

[Breakdown - slow crushing repeated]
SHOOT TO KILL
SHOOT TO KILL
GET BACK
MOVE

[Verse 2 - blast beats, intense]
No ambulance is coming when the violation's this severe
Talking through your teeth but all I hear is volunteer
For the body bag collection for the concrete curb parade
You can run your mouth but you can't outrun the blade
Barrel pressed to temple like a signature in lead
Street coroner's report another snitch pronounced dead

[Breakdown - grooved pit call]
EVERYBODY ON THE FLOOR
STREET EXECUTION
GET DOWN
BREEE BREEE

[Verse 3 - tunnel throat, chugging riff]
Empty casings on the pavement tell the story that I wrote
Floating down the river with a brand new concrete coat
Witness elimination isn't personal it's business
Termination clause activated by any sign of sickness
No court no judge no jury when the verdict's on the street
Just the cold efficiency of making enemies obsolete

[Breakdown - slowest heaviest]
SHOOT TO KILL
LAST WARNING
SHOOT TO KILL
NO SURVIVORS

[Outro - slow feedback fade, guttural whisper]
Shoot to kill
sirens fade
car peels away
```

### Track 02 — "Concrete Curb Enforcement" (Street Slam)

```
Style: gangster slam crossover, street attitude, downtuned Drop G# guitars with DJ scratch textures, mid-tempo groove at 105 bpm, hardcore shouted verses, call-and-response breakdown vocals, 808 sub-drops with palm mutes, PeelingFlesh crossover production, barked delivery, police scanner static
BPM: 105
Key: G# minor
Time: 4/4

[Intro - spoken, DJ scratch]
Yo check the code book
Section 4 paragraph 2 curb enforcement protocol
scratch scratch

[Riff Drop - gangster groove, shouted]
MY CAR FAST MY DRIP BETTER
MY CLOTHES FIT BETTER MY HOES BETTER
MY WHOLE SQUAD THICKER THAN YOUR WHOLE BLOCK
BREEE

[Verse 1 - barked, swinging groove]
My tattoos better I'm stronger than you
My shit thicker than yours my guns bigger than yours
I talk better than you I hustle better
I can get a dollar quicker than you
I breathe better than you my teeth straighter
My whole existence is just naturally greater

[Breakdown - slow, crowd call]
CONCRETE CURB ENFORCEMENT
who the fuck you think you is
CONCRETE CURB ENFORCEMENT
your gangster level is real low

[Verse 2 - growled, building intensity]
Supreme G-code violation you need to check your shit
Talking big game but your paperwork don't fit
The streets have rules and you didn't read the manual
Now your face is getting intimate with the pavement understandable
Citation issued by the curb police no appeals accepted
Your dental records are about to get unexpectedly collected

[Skratch Solo - DJ cut, beat drops out]
wiki wiki wah
CURB CHECK

[Verse 3 - hardcore shout, two-step beat]
My car faster than your car that's just basic math
Consequences of the violation walking down the bloody path
Enforcement officer on duty badge is made of brass knuckles
When the code gets broken all you hear is pavement chuckles
No fine no ticket no court date just gravity
The curb is the judge and the sentence is fatality

[Breakdown - pit call, gang vocals]
EVERYBODY DOWN
CURB CHECK
MOVE MOVE MOVE
FACE TO CONCRETE
LET'S GO

[Outro - spoken, DJ scratch fade, footsteps]
Enforcement complete
Section 4 paragraph 3 no witnesses
scratch scratch fade
walk away car door slam
```

### Track 03 — "The G Code" (Technical Slam)

```
Style: technical brutal death metal, sweep picking arpeggios, gravity blasts at 160 bpm, dual vocal trade-offs between low guttural and high pig squeal, complex time signature shifts, Despised Icon influence, surgical precision, raw technicality
BPM: 160
Key: C# minor
Time: 4/4 (with occasional 5/4 breakdown)

[Intro - technical riff, sweep picked arpeggios]
The code is written in blood
Every article every clause
You broke all of them
Every single one

[Riff Drop - gravity blast, dual vocals]
ARTICLE ONE NEVER TALK TO AUTHORITIES
ARTICLE TWO NEVER LEAVE A WITNESS BREATHING
ARTICLE THREE THE CODE DOES NOT ABSOLVE
PIG SQUEAL

[Verse 1 - guttural, technical riffing]
You violated every statute in the book we wrote in scars
Ink made from the plasma of informants behind bars
The G-code isn't guidelines it's the law of the concrete
And your sentence is delivery to the morgue on a back street
Every clause carved in flesh by the ones who came before
You thought the code was flexible now you're bleeding on the floor

[Breakdown - slow, syncopated, 5/4]
G CODE VIOLATION
guilty
G CODE VIOLATION
sentenced
THE CODE IS ABSOLUTE

[Verse 2 - pig squeal highs, blast beats]
No appeal process no parole board no clemency
Just the cold precision of the penalty for treachery
The code doesn't bend for excuses or apologies
It only breaks the breaker that's the fundamental policy
Your name is written in the ledger of the terminated
Every crossed-out line is someone who negotiated

[Skratch break - DJ cut over syncopated chugs]
wiki wah
CODE CHECK
wiki wiki wah
VIOLATION CONFIRMED

[Verse 3 - dual vocal trade-off, gravity blasts]
Article four states the witness pool gets shallow fast
Article five requires that no evidence will last
You memorized the code but you never understood the weight
Of every word written by the men who sealed your fate
The G-code isn't paper it's the pavement and the knife
And violation penalty is forfeiture of life

[Breakdown - slowest crushing, gang vocals]
THE G CODE IS WRITTEN IN BLOOD
watch your back
THE G CODE DOES NOT FORGET
no exceptions
THE G CODE

[Outro - technical riff decay, spoken whisper]
The code remains
You don't
fade to silence
```

### Track 04 — "Weight of Nothing" (KK Beatdown Hardcore)

```
Style: metallic hardcore beatdown, beefy distorted guitar chords, pinch harmonics, grid-rigid drum grooves, massive crushing breakdowns, strained shouted monotone vocals, venomous delivery, crunchy ballsy guitar tone, crisp clear production, Kublai Khan style, 88 bpm, Drop C tuning, hardcore punk energy
BPM: 88
Key: C minor
Time: 4/4

[Intro - feedback swell, single guitar chug]
I've carried this weight
Long enough to know it's not getting lighter

[Riff Drop - full band, shouted]
THE WEIGHT OF NOTHING
IS HEAVIER THAN EVERYTHING I'VE EVER HELD

[Verse 1 - barked, mid-tempo groove]
Every morning same reflection staring back at me
Same hollow eyes same tired lies same misery
Built this prison with my own two hands and locked the door
Now I'm screaming at the walls but I've heard it all before

[Breakdown - slow, crushing, single chugs]
NOTHING
IS HEAVIER
THAN WHAT YOU CARRY
ALONE

[Verse 2 - shouted, building intensity]
You said you'd stand beside me when the weight came crashing down
But when the ceiling caved you were nowhere to be found
Learned the hard way trust is just another word for debt
And everyone collects eventually — I just haven't yet

[Breakdown - grooved, pit call]
CARRY IT
CARRY IT
CARRY IT UNTIL YOUR SPINE BREAKS

[Verse 3 - strained, desperate]
There's no lesson in the suffering no wisdom in the pain
Just the same four walls closing in again and again
They say what doesn't kill you makes you stronger — that's a lie
What doesn't kill you leaves you wishing that you'd died

[Breakdown - slowest, heaviest]
THE WEIGHT
OF
NOTHING

[Outro - feedback, spoken whisper]
It's still here
It's always here
(amp hum fade)
```

### Track 05 — "No Kin" (KK Metallic Hardcore)

```
Style: aggressive metallic hardcore, gnarly low-pitched chordal riffs, pinch harmonics, tight mixing, double-bass drum sections, busy kit fills, shouted strained vocals, personal betrayal energy, Hatebreed influence, 90 bpm, Drop C#, raw intensity
BPM: 90
Key: C# minor
Time: 4/4

[Intro - dissonant chord, building tension]
Blood means nothing
When the knife is in their hand

[Riff Drop - explosive, shouted]
NO KIN
NO BLOOD
NO LOYALTY LEFT IN THIS ROOM

[Verse 1 - barked, driving groove]
Family portrait hanging crooked on a burning wall
Every face I trusted lined up waiting for the fall
The ones who share your name are the first to use it wrong
Been singing this betrayal since the day that I was born

[Breakdown - slow, crushing]
YOU CALLED ME BROTHER
WITH A BLADE BEHIND YOUR BACK

[Verse 2 - strained, building]
Empty chairs at every table every holiday
Same excuses different faces I believed them anyway
But the math is simple when you finally do the count
Love divided by betrayal always comes out zero amount

[Breakdown - grooved, gang vocal feel]
BLOOD IS THICKER
BUT IT SPILLS THE SAME
BLOOD IS THICKER
BUT IT SPILLS THE SAME

[Verse 3 - shouted, fast]
You want forgiveness you can find it in the ground
Six feet under every promise that you ever let down
I dug this grave for the person I was supposed to be
Turns out the only corpse in it was your memory of me

[Breakdown - pit call, heaviest]
NO KIN
NO BLOOD
NO ONE

[Outro - ringing chord, fade]
Just me
Just me
(feedback)
```

### Track 06 — "River Walker" (KK Sludgy Doom Hardcore)

```
Style: sludgy metallic hardcore, slower heavier arrangement, wider sonic space, doom-influenced beatdown, spoken-word vocals, calmer atmosphere breaking into crushing heaviness, Kublai Khan River Walker style, 75 bpm, Drop B, cinematic, introspective
BPM: 75
Key: B minor
Time: 4/4

[Intro - clean guitar, atmospheric, spoken]
There's a river that runs through every town I've ever left
It doesn't ask where I'm going
It doesn't care where I've been

[Riff Drop - massive, slow, shouted]
I WALK ALONE
I ALWAYS HAVE

[Verse 1 - strained, mid-tempo]
Packed my life into a bag that I could throw away
Nothing worth remembering nothing worth the words to say
The road doesn't judge me for the person I became
It just stretches out in front of me and swallows every name

[Breakdown - crushing, slow single notes]
RIVER
WALKER
DRIFTING
ALWAYS DRIFTING

[Verse 2 - shouted, building]
Every town the same — same faces different streets
Same hollow conversations same defeat
They say roots keep you grounded but I've seen what roots become
Just another way to choke you when the growing season's done

[Bridge - clean interlude, spoken]
The water doesn't remember your face
It only knows direction
It only knows forward

[Breakdown - heaviest, doom pace]
I KEEP WALKING
BECAUSE STOPPING
MEANS
DROWNING

[Verse 3 - shouted, desperate]
Maybe one day I'll find a place where the river meets the sea
Where the current finally slows and lets go of me
But until that day I'll carry what I've always carried
A heart too heavy to stay and legs too tired to bury

[Outro - clean guitar return, spoken]
The river doesn't end
It just becomes something else
Something wider
Something deeper
(walking footsteps, water ambience, fade)
```

Slam requires specific vocal descriptions in the style prompt. ACE-Step needs direction to produce harsh vocals:

| What You Want | Style Prompt Keywords |
|--------------|----------------------|
| Low guttural growls | `guttural vocals`, `tunnel throat`, `low death growl`, `brutal vocal delivery` |
| Pig squeals | `pig squeal highs`, `inhale vocals`, `high-register brutal vocals` |
| Hardcore shouts | `barked vocals`, `hardcore shouted delivery`, `crowd call vocals`, `mid-register aggression` |
| Gang vocals | `gang vocals`, `multiple vocal layers`, `call-and-response vocals` |
| Spoken skits | `spoken word`, `clean narration`, `sample dialogue` |

**CRITICAL — ACE-Step Vocal Sweet Spot:** ACE-Step is primarily designed for sung/rapped vocals. **Hardcore shouted/strained delivery (Kublai Khan style) is its vocal sweet spot** — these produce the cleanest, most convincing heavy music results. Death metal guttural growls and pig squeals are at the edge of capability; expect hardcore-level harshness, not Dying Fetus-level gutturals. When the user asks for heavy music, steer toward hardcore/beatdown over pure death metal for best fidelity. The PeelingFlesh hardcore-shout crossover style actually works in your favor here.

## Verified Generation Results

Verified on ACE-Step v15 turbo (2026-06-23, GPU0 with 14GB free):

| Track | Genre | Lines | Raw Duration | Trim Result | Gen Time |
|-------|-------|-------|-------------|-------------|----------|
| Shoot 2 Kill | PeelingFlesh Slam | 35 | 240.0s (4:00) | 213.0s (3:33) ✅ | 17.0s |
| Concrete Curb | PeelingFlesh Slam | 35 | 213.0s (3:33) | 213.0s (3:33) ✅ | 11.0s |
| Weight of Nothing | KK Beatdown | 35 | 240.0s (4:00) | 213.0s (3:33) ✅ | 17.0s |
| No Kin | KK Hardcore | 35 | 240.0s (4:00) | 213.0s (3:33) ✅ | 64.7s |
| River Walker | KK Doom HC | 35 | 213.0s (3:33) | 213.0s (3:33) ✅ | 8.6s |

All tracks ~4.9MB MP3 at 192kbps. 35+ lines consistently hits or exceeds 3:33 target.

## Pitfalls

### Genre-Specific

**For PeelingFlesh Slam:**

1. **ACE-Step vocal limitations** — ACE-Step's vocal sweet spot is hardcore shouted/strained delivery (see Kublai Khan section). Death metal gutturals and pig squeals are at the edge of capability. The PeelingFlesh hardcore-shout crossover helps — barked/shouted sections will sound more convincing than pure growls. Set expectations: you'll get hardcore-level harshness, not Dying Fetus-level gutturals.

2. **Pig squeals** — Hardest vocal technique for ACE-Step. Use `pig squeal` in the style prompt but expect mixed results. The hardcore shout register is more reliable.

**For Kublai Khan Beatdown:**

3. **Shouted vocals shine** — ACE-Step handles KK-style strained/shouted delivery excellently. This is the model's vocal sweet spot for heavy music. When the user wants heavy/aggressive music, default to KK hardcore style over PeelingFlesh slam for best vocal fidelity.

4. **Spoken word sections** — ACE-Step handles clean spoken word well. KK tracks with spoken intros/outros (River Walker style) produce atmospheric results. Use `spoken word`, `clean narration` in the style prompt.

**For Both:**

5. **Guitar tone** — ACE-Step generates audio from prompt, not real instruments. The "downtuned 8-string" or "crunchy ballsy guitar tone" tags give direction but results may be synth-guitar approximations. Rhythmic focus (chugs, breakdowns) translates better than technical lead playing.

6. **Key specification** — ACE-Step's `key_scale` expects standard notation like "F minor". Map Drop F → "F minor", Drop C → "C minor", etc. The guitar tuning concept doesn't translate — just use the root note in minor.

7. **Blast beats** — Specify `blast beats` and high BPM (160-200) for slam, but ACE-Step can generate fast percussion. KK beatdown at 75-90 BPM produces more natural-sounding drum patterns.

### Pipeline

6. **Same pitfalls as LLMC forge apply** — see that skill's Pitfalls section for: block quantization, turbo=silence, cache-watch over polling, GPU contention, MEDIA: over hermes send, lyric length limits.

## Discord Push

Same as LLMC forge — use MEDIA inline:

```
MEDIA:/absolute/path/to/song.mp3
```

## Related Skills

- `llmc-song-forge` — the rap pipeline this was forked from
- `acestep` — full ACE-Step usage reference
- `songwriting-and-ai-music` — general songwriting craft
- `evolutionary-radio` — infinite generative radio (could use this as a genre channel)

## Support Files

- `scripts/generate_slam_batch.py` — batch generator for slam/hardcore tracks
- `references/peelingflesh-dna.md` — full PeelingFlesh genre analysis
- `references/kublai-khan-dna.md` — Kublai Khan TX / Nomad album genre analysis + ACE-Step compatibility notes
