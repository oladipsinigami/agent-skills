# QA checklist

Run this on **every** render, including previews. Report failures honestly — a
render with a known defect that you describe is more useful than one you call
finished.

Mechanical checks are scripted in `scripts/qa.py`. Design checks need your eyes
on extracted frames.

## 1. Mechanical — run the script

```bash
python scripts/qa.py out.mp4 \
  --expect-fps 30 \
  --expect-duration 6.0 \
  --expect-size 1920x1080 \
  --max-mb 50 \
  --still 1.5 --still-out review.png
```

It exits non-zero if any check fails, so it can gate a build.

| Check | What it catches |
|---|---|
| `frame_rate` | wrong fps |
| `pixel_format` | unexpected format |
| `frame_count_matches_duration` | dropped frames, VFR, duration drift |
| `expected_fps` | you asked for one fps and got another |
| `duration` | the composition ran short or long, off by more than one frame |
| `resolution` | wrong output size |
| `no_black_frames` | accidentally blank opening/ending, bad fades |
| `no_frozen_frames` | a stalled render, a held frame, a decode failure |
| `has_audio` / `no_audio` | audio missing when you expected it |
| `loudness` | audio far too quiet or too hot |
| `file_size` | over a platform limit |

Worth knowing: `blackdetect` uses `d=0.1:pix_th=0.10` — a frame that is 90% black
counts. A deliberately dark scene can trip it, so read the result rather than
trusting it blindly.

`freezedetect=n=0.001:d=0.5` flags any half-second stretch with effectively no
change. Deliberate holds (a logo sting's final frame, an end card) will trip it.
That is a warning about your design, not necessarily a bug.

## 2. Design — look at actual frames

Extract frames at every scene boundary and check each one. Use `hyperframes
snapshot` if you are working in HyperFrames:

```bash
hyperframes snapshot . --at 0.5,1.5,2.9,4.0,5.5
```

Or with ffmpeg:

```bash
ffmpeg -v error -ss 1.5 -i out.mp4 -frames:v 1 -y review-1.5s.png
```

### Text legibility
- Is every text element readable at the size the platform will display it? Check
  on a real phone for vertical formats.
- Does text fit its line without wrapping or clipping? Anything over 42 characters
  per line is suspect.
- Is there enough contrast? `hyperframes check` tests WCAG AA automatically
  (it passed 7/7 text checks on the test render). Target 4.5:1 for body text,
  3:1 for large text.
- Does text collide with anything during a transition? Check the mid-transition
  frames, not just the start and end states.
- Is the font actually the font you asked for? A missing font falls back
  silently. `hyperframes check` reports loaded vs unused font faces.

### Safe zones
- Landscape: is everything important inside 90% of the frame?
- Vertical: is everything clear of the top 14% and bottom 35%, and 6% on the
  sides?
- Does anything overlap where a platform's UI sits?

### Frame-rate consistency
- Did you actually render at the fps you intended? The script checks it.
- Is any motion fast enough to strobe or alias? Fast horizontal movement at
  24–30 fps can flicker.
- If you mixed clips of different frame rates, check the seams.

### Audio sync (if there is audio)
- Does audio start with the video, not before or after? A lead-in offset of more
  than ~50 ms is noticeable.
- Do cuts land on beats, if the brief asked for beat-synced cutting?
- Is the loudness sane? The script warns outside roughly -24 to -9 LUFS.
  **-16 LUFS** is the usual web target; **-23 LUFS** is the EBU R128 default.
- Are there clicks at the edit points? Add 20–50 ms crossfades.

### Banding and compression artifacts
- Gradients are the risk area. A large, slowly-shifting background gradient at
  `yuv420p` can band visibly. Add a tiny amount of noise (dither) or increase
  bitrate.
- Text on solid colour is the other risk. At low bitrate, edges crawl.
- Check the file's average bitrate. The script reports it. If it is under about
  1 Mbps at 1080p30, raise `--quality` or `--video-bitrate`.

```bash
# Extract the worst-case frame (usually a gradient or a text card) and inspect
ffmpeg -v error -ss <time> -i out.mp4 -frames:v 1 -y suspect.png
```

### Loop seams (if looping)
- Extract the first and last frame and compare them. They should be nearly
  identical.
- A visible jump at the seam is the single most common failure in looping
  backgrounds.

```bash
ffmpeg -v error -i loop.mp4 -vf "select='eq(n,0)+eq(n,N-1)'" -vsync vfr seam_%02d.png
```

Then diff the two images. In Pillow:

```python
from PIL import Image, ImageChops
a = Image.open("seam_00.png").convert("RGB")
b = Image.open("seam_01.png").convert("RGB")
diff = ImageChops.difference(a, b)
print("mean diff:", sum(i * c for i, c in enumerate(diff.histogram())) / (a.size[0] * a.size[1]))
```

### File size per platform
- Instagram Reels / Stories: **max 4 GB**
- TikTok: max 10 minutes, ~500 MB, bitrate at least 516 kbps
- X/Twitter: 2:20 standard, 1280×720 recommended
- LinkedIn: max 5 GB, 3 s minimum
- YouTube: up to 256 GB / 12 hours

These are platform ceilings, not targets. A 30-second 1080p30 promo should be
well under 100 MB.

### Colour space
- If this will be graded or intercut with other footage, check the colour space
  and range. A mismatch shows as washed-out or crushed blacks.
- HyperFrames defaults are fine for SDR web delivery; `--hdr` is MP4-only.

## 3. If something fails

Fix it and re-render. Do not ship a render you know is broken while promising to
fix it later — say what is wrong, fix it, and re-run QA on the new file.

Common fixes:

| Failure | First thing to try |
|---|---|
| Text clipped | shorten the line or reduce the type size; check the container width |
| Wrong fps | pass `--fps` to `render` explicitly |
| Wrong duration | check the root `data-duration`; remember a variable override cannot change it |
| Blank first/last frame | check clip `data-start`/`data-duration` for gaps at the boundaries |
| Hard render failure | run `hyperframes doctor`, then `hyperframes check` and read the lint errors |
| Banding | raise `--quality` or `--crf`; add slight noise to gradients |
| Audio too quiet | `data-volume` is linear-ish; 1 = 0 dB, up to 3.98 = +12 dB |
