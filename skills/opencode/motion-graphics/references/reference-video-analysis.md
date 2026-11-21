# Analysing a reference video

A reference is a brief, not a template. Read it for pacing, structure, colour
relationships and technique — never copy footage, exact branded assets, logos,
fonts, or music.

## What to copy and what not to

**Take:** cut rhythm and shot length distribution, how motion eases in and out,
colour relationships and contrast, composition and framing habits, the type feel
(serif vs sans, weight, case, tracking, alignment), how scenes connect.

**Do not take:** the footage itself, logos or other trademarks, specific fonts,
licensed music, character or creature designs, or any recognisable creative
element. Style and technique are not protected expression; a specific
substantial creative work is.

**Never download the reference to ship it.** Analyse it, then build something
original.

---

## Step 1 — Get the file

```bash
# A local file
cp "/path/to/reference.mp4" ./ref.mp4

# A URL that is a direct video file
curl -L -o ref.mp4 "https://example.com/clip.mp4"
```

If all you have is a link to a streaming page rather than a media file, ask the
user to download it and drop it in. Do not attempt to scrape a platform's player.

## Step 2 — Basic facts

```bash
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate,nb_frames,pix_fmt -of json ref.mp4
```

Record duration, resolution, fps and pixel format. A reference shot at 24 fps with
a cinematic grade tells you something different from one shot at 30 fps on a
phone.

## Step 3 — Cuts and pacing

Use the bundled script:

```bash
python scripts/scene_cuts.py ref.mp4
python scripts/scene_cuts.py ref.mp4 --threshold 1 --json
```

It reports shot count, mean/median/min/max/stdev of shot lengths, cuts per minute,
and the exact cut timestamps.

`--threshold` is `scdet=threshold=N` on a 0–100 scale, default 10.

- **Lower it** (1–4) for short-form and social, where cuts are smaller diffs.
- **Keep it at 10** for ordinary footage.
- **Raise it** if camera shake or film grain produces false cuts.
- **Always verify a low threshold** against a frame you extracted, or you will
  measure noise.

The distribution matters more than the mean. Mean 2 s with stdev 3 s means a
variable, hand-cut piece. Mean 2 s with stdev 0.3 s means metronomic — match the
*shape*, not just the average.

## Step 4 — Extract frames to look at

```bash
# One frame every 0.5s into a directory
mkdir -p frames
ffmpeg -v error -i ref.mp4 -vf fps=2 frames/f_%04d.png

# A single frame at a given moment
ffmpeg -v error -ss 4.0 -i ref.mp4 -frames:v 1 frame-4s.png

# First frame of each detected cut (scene above threshold)
ffmpeg -v error -i ref.mp4 -vf "select='gt(scene,0.4)'" -vsync vfr frames/cut_%04d.png
```

Look at the frames. An agent that reads the numbers without looking at the images
will produce a technically correct and visually wrong result.

## Step 5 — Colour palette

```bash
# Quick palette from a single frame
python scripts/palette.py frame-4s.png --colors 6

# Palette from the whole clip, sampled every 0.5s
ffmpeg -v error -i ref.mp4 -vf "fps=2,palettegen=max_colors=8" -frames:v 1 palette.png
python scripts/palette.py palette.png --colors 8
```

Read the palette for relationships, not just hex values: how many distinct hues,
how saturated, whether shadows are warm or cool, whether there is one accent
colour carrying the emphasis. That is what transfers.

## Step 6 — Motion intensity per frame

`signalstats` reports the mean absolute luma difference between consecutive
frames. It tells you how much is moving, and whether motion is continuous or
bursty:

```bash
ffmpeg -v error -i ref.mp4 -vf "signalstats,metadata=print:key=lavfi.signalstats.YDIF:file=-" -f null - 2>&1 | head -40
```

`YDIF` is in 0–255 units. Values near 0 mean almost nothing is moving that
instant; spikes are cuts or fast motion. Compare the spike frequency to your cut
list — if they disagree, your threshold is wrong.

## Step 7 — Frame-rate consistency and dropped frames

```bash
# Frozen stretches (a stalled render, a held frame, a dropped source)
ffmpeg -v info -i ref.mp4 -vf "freezedetect=n=0.001:d=0.5" -f null - 2>&1 | grep freeze

# Black stretches
ffmpeg -v info -i ref.mp4 -vf "blackdetect=d=0.1:pix_th=0.10" -f null - 2>&1 | grep blackdetect
```

A reference with perfectly regular frame timing tells you the piece was rendered,
not shot.

## Step 8 — Audio, if it matters

Loudness is straightforward and free:

```bash
ffmpeg -nostats -i ref.mp4 -filter_complex ebur128 -f null - 2>&1 | tail -12
```

Report the integrated figure. Broadcast/web reference points: **-16 LUFS** for
online material, **-23 LUFS** is the EBU R128 default.

**Beat detection: FFmpeg has no reliable built-in beat tracker.** Do not claim
otherwise. If you need beats:

- `librosa` (install with `pip install librosa`) is the usual answer —
  ISC-licensed, and it works on CPU. Use it if Python audio deps are available.
- `aubio` is the other option; verify its licence and availability before
  promising it.
- `hyperframes beats` is free and local, but **verified to report "No beats
  detected" on non-percussive audio** such as a sine tone. It needs real onsets.

If neither is available, have the user tap the beat out or supply a BPM, and
derive beat times arithmetically. A hand-marked beat grid is better than a
wrongly detected one.

## Step 9 — Reading the frames

What to note, in order of how much it affects your output:

1. **Type.** Serif or sans. Weight (light/regular/black). Case (all-caps reads
   formal and technical; sentence case reads conversational). Tracking (tight
   negative tracking on large display type is the modern default). Alignment.
2. **Colour.** Dominant value (light or dark field), saturation level, how many
   hues, where the accent sits.
3. **Layout.** Rule of thirds? Centred? Generous margins or edge-to-edge? Is
   there a persistent element (a bar, a corner mark, a caption strip)?
4. **Motion feel.** Fast/slow. Linear or eased. Does the camera move, or does
   content move within a fixed frame?
5. **Connective tissue.** How do scenes change — cut, dissolve, wipe, whip pan,
   shape transition?

Write these down as a short brief before you start building. If you cannot state
the reference's character in three sentences, you have not looked at it long
enough.

## Step 10 — Write the match spec

```markdown
## Matching: reference.mp4
- Shot length: mean 2.1s, median 1.9s, range 0.8-4.2s, stdev 0.9s -> variable, hand-cut
- Cuts/min: 28 -> quick but not frantic
- Palette: dark field (near-black bg), one cool accent, low saturation
- Type: all-caps sans, heavy weight, tight tracking, left-aligned
- Motion: content moves within a fixed frame; camera is static
- Transitions: mostly hard cuts, one shape wipe per section
- Reading time: captions hold ~2.5s, ~35 chars/line
```

Then build to that spec, not to the video.
