#!/usr/bin/env python3
"""Slam batch song generator — brutal death metal / PeelingFlesh style with 3:33 hard trim.

Usage:
  python3 scripts/generate_slam_batch.py

Requires: ACE-Step API at http://127.0.0.1:8001, ffmpeg, ffprobe
"""
import json, time, shutil, subprocess
from pathlib import Path
from urllib.request import Request, urlopen

ACE_STEP = "http://127.0.0.1:8001/release_task"
CACHE = Path("/home/sovthpaw/Models/ace-step/.cache/acestep/tmp/api_audio")
OUT = Path("/tmp/slam-output")

SONGS = [
    {
        "name": "01_shoot_to_kill",
        "style": "brutal death metal slam, downtuned 8-string guitars in Drop F#, chromatic slam riffs, triggered kick drums, blast beats into slow crushing breakdown, guttural tunnel throat vocals, pig squeal accents, raw brick-wall production, 110 bpm, gangster attitude, street execution energy",
        "bpm": 110,
        "key": "F# minor",
        "time_sig": "4",
        "lyrics": """[Intro - police scanner sample, ambient noise]
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
car peels away"""
    },
    {
        "name": "02_concrete_curb",
        "style": "gangster slam crossover, street attitude, downtuned Drop G# guitars with DJ scratch textures, mid-tempo groove at 105 bpm, hardcore shouted verses, call-and-response breakdown vocals, 808 sub-drops with palm mutes, PeelingFlesh crossover production, barked delivery, police scanner static",
        "bpm": 105,
        "key": "G# minor",
        "time_sig": "4",
        "lyrics": """[Intro - spoken, DJ scratch]
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
walk away car door slam"""
    },
]

OUT.mkdir(parents=True, exist_ok=True)

def post(style, lyrics, bpm, key, time_sig, dur=213):
    p = {"prompt":style,"lyrics":lyrics,"thinking":False,"use_format":False,
         "bpm":bpm,"key_scale":key,"time_signature":time_sig,"vocal_language":"en",
         "inference_steps":50,"guidance_scale":7.0,"audio_duration":dur,
         "audio_format":"wav","task_type":"text2music"}
    r = Request(ACE_STEP, data=json.dumps(p).encode(),
                headers={"Content-Type":"application/json"}, method="POST")
    return json.loads(urlopen(r, timeout=30).read())

def wait_wav(baseline, to=600):
    dl = time.time() + to
    while time.time() < dl:
        ns = {p.name for p in CACHE.glob("*.wav")}
        nf = ns - baseline
        if nf:
            return sorted(CACHE.glob("*.wav"), key=lambda p: p.stat().st_mtime)[-1]
        time.sleep(2)
    return None

def trim_to_mp3(src_wav, out_mp3, target=213):
    subprocess.run(["ffmpeg","-y","-i",str(src_wav),"-t",str(target),
                    "-codec:a","libmp3lame","-b:a","192k",str(out_mp3)],
                   capture_output=True)
    d = subprocess.run(["ffprobe","-v","quiet","-show_entries","format=duration",
                        "-of","csv=p=0",str(out_mp3)], capture_output=True, text=True)
    return float(d.stdout.strip()) if d.stdout.strip() else 0

baseline = {p.name for p in CACHE.glob("*.wav")}

for s in SONGS:
    name = s["name"]
    print(f"GEN: {name}...", flush=True)
    t0 = time.time()
    try:
        resp = post(s["style"], s["lyrics"], s["bpm"], s["key"], s.get("time_sig","4"))
        print(f"  POST OK: task_id={resp.get('data',{}).get('task_id','?')}", flush=True)
    except Exception as e:
        print(f"  FAIL POST: {e}", flush=True)
        continue

    wav = wait_wav(baseline, 600)
    if not wav:
        nf = {p.name for p in CACHE.glob("*.wav")} - baseline
        wav = sorted(CACHE.glob("*.wav"), key=lambda p: p.stat().st_mtime)[-1] if nf else None
    if not wav:
        print(f"  TIMEOUT", flush=True)
        baseline = {p.name for p in CACHE.glob("*.wav")}
        continue

    src = CACHE / wav
    raw_bytes = src.stat().st_size - 44
    actual_dur = raw_bytes / 192000

    tmp = OUT / f"{name}_raw.wav"
    shutil.copy2(src, tmp)
    final = OUT / f"{name}.mp3"
    dur = trim_to_mp3(tmp, final, 213)
    mb = final.stat().st_size / (1024 * 1024) if final.exists() else 0
    elapsed = time.time() - t0
    print(f"  OK {mb:.1f}MB dur={dur:.1f}s (raw={actual_dur:.1f}s) in {elapsed:.1f}s", flush=True)
    baseline = {p.name for p in CACHE.glob("*.wav")}
    time.sleep(3)

print(f"\nDone. Files in {OUT}/", flush=True)
