---
name: motion-graphics
description: >-
  Produces finished motion graphics end to end — animated graphics, explainer
  videos, kinetic typography, logo reveals and stings, promo videos, UI/product
  demos, data visualisation, lower thirds, slideshows and looping backgrounds.
  Runs a short intake, writes a storyboard and motion spec, builds it in
  HyperFrames (Apache-2.0, free, no account) or Remotion, renders a preview and
  then the final file, and runs a QA checklist before delivering. Use this
  whenever the user asks to "animate this logo", "make an explainer", "kinetic
  text", "motion graphic", "promo video", "product demo video", "app walkthrough",
  "match this video's style", "turn these screenshots into a video", or asks for
  any video, animation, motion, sting, intro, outro, or animated title. Also use
  it for "animate my logo", "make a reel/tiktok/short out of this", "visualise
  these numbers", "make this chart move", or any request where the deliverable is
  something that moves. The whole stack is free forever — no paid tiers,
  credits, API keys, watermarks, or per-render fees.
license: MIT
---

# Motion graphics

You are making a finished motion-graphics piece: an explainer, a kinetic-type
promo, a logo sting, a product demo, an animated chart. Not a screenshot, not a
slide, not a storyboard — a video file.

This skill is opinionated about craft and ruthless about cost. Follow the order:
intake, brief, storyboard, spec, build, preview, QA, deliver. Do not skip to code.

---

## The hard rule: $0 forever

Every tool this skill uses is free for commercial use. No paid tiers, trials,
credits, API keys, watermarks, or per-render fees. If you find yourself reaching
for something that needs an account, stop.

Default renderer is **HyperFrames** (Apache-2.0). Optional second is **Remotion**
(source-available, free only for teams of 3 or fewer). Everything else is
supporting: FFmpeg, GSAP, Pillow, rembg.

Never use: After Effects, Canva, any SaaS renderer, Remotion Lambda/Cloud Run,
HyperFrames cloud render, or rembg's **default** model (it requires a paid
commercial licence — see `references/tooling.md` §8).

---

## Step 0 — Check the environment

Before anything else, confirm you can actually render. Do this once per session.

```bash
node --version            # need 22 or newer
ffmpeg -version           # need FFmpeg on PATH
npx hyperframes doctor    # reports FFmpeg, Chrome, cache
npx hyperframes browser ensure
```

**If FFmpeg is missing**, stop and tell the user. On Windows: download a 64-bit
build from gyan.dev, extract, add `bin` to PATH. On macOS: `brew install ffmpeg`.
On Debian/Ubuntu: `sudo apt install ffmpeg`.

**If Chromium cannot be installed** (no network, sandbox restriction), say so
plainly and fall back to **Manim**, which renders headlessly through a software
rasteriser and ships ffmpeg via PyAV:

```bash
pip install manim
manim render -qm scene.py SceneName     # 1280x720 @ 30fps, no display needed
```

Manim is right for mathematical and diagrammatic pieces. It is wrong for
typographic or UI work — if the piece is typographic and there is no Chromium,
tell the user you cannot produce the quality they want and why.

If you set environment variables to keep runs quiet and offline, use these:

```bash
export HYPERFRAMES_NO_TELEMETRY=1
export HYPERFRAMES_NO_UPDATE_CHECK=1
export HYPERFRAMES_SKIP_SKILLS=1
```

---

## Step 1 — Intake

Ask these in **one batch**, not one at a time. **Skip any question the user's
message already answers.** Use selectable options where your interface supports
them.

**Q1 — Visual type.** What kind of motion graphic is this?
- Kinetic typography (text is the subject)
- Logo reveal / sting
- Explainer / infographic
- Data visualisation / charts
- UI / product demo
- Social short-form (vertical, punchy)
- Lower third / title / overlay
- Slideshow / photo-driven
- Looping / abstract background
- Other / not sure — recommend one

**Q2 — Images.** Will this include images (logo, product shots, screenshots,
photos)? If yes: how many, what is each for, and where are the files? If no, we
design with shapes, type and icons only — say so, it is a perfectly good answer.

**Q3 — Reference video.** Is there a reference video whose style you want matched?
If yes: give me the file (or a direct link to the media file, not a streaming
page), and tell me what to take from it — pacing, transitions, typography,
colours, camera moves, or everything. If no, we use the default preset for the
chosen type.

**Only if still unknown after those three**, ask briefly: duration · aspect ratio
and platform · brand colours and fonts · the actual text/script · music or
voiceover · preferred output format.

Do not ask more than four rounds of questions total. A creator who says "make me
a 6 second logo sting for my company, here's the logo, vertical" has given you
everything you need.

If the user picks "not sure" on type, **recommend one and say why**. Do not ask
another question.

---

## Step 2 — Restate the brief

Before building, write the brief back in 3–5 lines and get a quick confirmation.
Skipping this is how you end up redoing a 40-second render.

```markdown
## Brief
- **Type:** 6s logo sting, landscape 1920x1080 @ 30fps
- **Images:** company logo (SVG, supplied) — one asset, mark + wordmark
- **Style:** no reference; default preset for logo reveal
- **Palette:** brand navy #143cb4 + off-white
- **Deliverable:** MP4, 1080p, ~2-5 MB
```

If the user says "yes / looks right / go", proceed. If they amend it, amend the
brief and re-read it back.

---

## Step 3 — Storyboard / shot list

Write a shot list with **timestamps, on-screen text, and motion notes** per scene.
This is the single highest-leverage artefact in the whole process: it is cheap to
change and it prevents a bad render.

```markdown
## Storyboard — "Acme logo sting" (6s, 1920x1080, 30fps)

| # | Time | On screen | Motion |
|---|---|---|---|
| 1 | 0.0–0.9 | brand navy field | scale 1.08 → 1.0, power2.inOut |
| 2 | 0.9–1.8 | mark revealed by mask wipe | clip-path wipe L→R, power2.out, 900ms |
| 3 | 1.8–2.4 | wordmark fades in below | opacity + y 24→0, power3.out, 500ms |
| 4 | 2.4–5.6 | full lockup held | static; 3.2s hold |
| 5 | 5.6–6.0 | fade to black | opacity → 0, 280ms |
```

Check the reading time of every text card against `references/motion-principles.md`
§4 before you accept the storyboard. A 20-word card holding 1.8 seconds is a bug,
not a style choice.

---

## Step 4 — Motion spec

Write this **before any code**. It is what makes the piece feel designed rather
than assembled.

```markdown
## Motion spec
- Easing: power3.out in, power2.in out, power2.inOut on-screen
  (cubic-bezier 0.33,1,0.68,1 / 0.32,0,0.67,1 / 0.65,0.35,0.35,1)
- Entrance 600ms · exit 280ms · scene hold 2.5s min
- Stagger 30ms per item, capped at 8 items
- Overshoot: back.out(1.4) on the mark only
- Palette: #143cb4 navy, #f8fafc off-white, #0b0d12 deep navy
- Type: display 160px/800/-0.03em · supporting 56px/500
- Safe area: 90% of frame
- fps: 30
```

Read `references/motion-principles.md` for the numbers and the reasoning behind
each. Read `references/visual-types.md` for the preset for your chosen type — use
it unless the brief or a reference says otherwise, and say which you did.

---

## Step 5 — Choose the renderer

**Default: HyperFrames.** Apache-2.0, renders locally with no account, no key, and
no watermark. HTML + GSAP means real easing with no build step.

**Choose Remotion only if** the user prefers React, or the project already is a
React project.

Before choosing Remotion, **ask how many people are on the team.** Remotion's Free
License covers individuals and companies of up to **3 employees**. At 4 or more it
is not free and you must fall back to HyperFrames. If you do use it, pin the
version and tell the user to check `LICENSE.md` before upgrading — a licence
change is planned for 5.0.

Other renderers: **Manim** for mathematical/diagrammatic work, and as the fallback
when no Chromium is available. **MoviePy** only for trivial compositing. Do not
use Lottie as a rendering path — see `references/tooling.md` §6 for why.

Full install commands, verified versions and licences: `references/tooling.md`.

---

## Step 6 — Build

### With HyperFrames

```bash
npx hyperframes init my-video --non-interactive   # scaffold
# or write index.html by hand
```

A composition is a root element with `data-composition-id`, `data-width`,
`data-height`, `data-duration`, containing timed children with `class="clip"`:

```html
<div class="clip" data-composition-id="acme-sting" data-start="0" data-duration="6"
     data-width="1920" data-height="1080"
     style="left:0; top:0; width:1920px; height:1080px;">

  <div id="field" class="clip" data-start="0" data-duration="6"
       style="position:absolute; inset:0; background:#143cb4;"></div>

  <div id="mark" class="clip" data-start="0.9" data-duration="4.7"
       style="position:absolute; left:50%; top:44%; transform:translate(-50%,-50%);">
    <img src="./logo.svg" style="width:240px; height:auto;" />
  </div>

  <div id="wordmark" class="clip" data-start="1.8" data-duration="3.8"
       style="position:absolute; left:50%; top:62%; transform:translate(-50%,-50%);
              font-family:Inter,Arial,sans-serif; font-size:56px; font-weight:500;
              color:#f8fafc; letter-spacing:-0.01em; white-space:nowrap;">
    Acme
  </div>
</div>
```

Motion is one paused GSAP timeline registered under the composition id:

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"></script>
<script>
  var tl = gsap.timeline({ paused: true });
  window.__timelines = window.__timelines || {};
  tl.from("#field", { scale: 1.08, duration: 0.9, ease: "power2.inOut" }, 0);
  tl.from("#mark",  { opacity: 0, duration: 0.9, ease: "power2.out" }, 0.9);
  tl.from("#wordmark", { opacity: 0, y: 24, duration: 0.5, ease: "power3.out" }, 1.8);
  window.__timelines["acme-sting"] = tl;
</script>
```

**Contract rules the renderer enforces.** Violating any of these produces a lint
error or a broken render:

- Exactly one `data-composition-id` on the root, and the same string as the key in
  `window.__timelines`.
- `data-width` and `data-height` on the root.
- Animate **child** elements, not the clip elements themselves. `autoAlpha` on a
  clip element is rejected — the framework owns clip visibility.
- One finite, **paused** timeline. No `Date.now()`, no `requestAnimationFrame`,
  no unseeded `Math.random()`, no mid-render fetching.
- Keep `data-start`/`data-duration` from overlapping unless overlap is intended.
  `data-track-index` is display-only and does **not** prevent overlap.
- If nothing registers a timeline, add `data-no-timeline` to the root, or every
  render pays a flat 45-second penalty.

**Prefer relative timing** so the shot list stays true when durations shift:

```html
<div class="clip" data-start="intro + 0.5" data-duration="1.2">
```

### With images

Read `references/image-handling.md` before compositing anything. The two things
that most often ruin a render are a source image that is too small and an image
with the wrong alpha handling. Both are cheap to check and expensive to discover
at 4K.

### With a reference video

Read `references/reference-video-analysis.md` and run the analysis scripts. Then
build to the spec you wrote from the reference, not to the reference.

---

## Step 7 — Lint, preview, then final

**Never go straight to the final render.**

```bash
npx hyperframes check                       # contract, layout, contrast, motion
npx hyperframes check --snapshots --at 1.0,2.5,4.5
npx hyperframes render --quality draft --output preview.mp4    # cheap preview
```

Read `check`'s output. A clean lint pass is not the same as a good render — but a
lint failure means the render will be wrong.

If `check` reports "Browser session never ran", that is a failure, not a pass.
Layout, motion and contrast results are placeholders in that state.

**Look at the preview.** Extract frames and actually look at them:

```bash
npx hyperframes snapshot . --at 1.0,2.5,4.5
hyperframes check --caption-zone
```

Check: is the text legible, does anything collide, is it inside the safe area,
does the timing feel right, does it match the brief. Fix what is wrong, re-preview.

**Then the final render:**

```bash
npx hyperframes render --output out.mp4 --fps 30
npx hyperframes render --format webm --output overlay.webm    # if you need alpha
```

---

## Step 8 — QA

Run the mechanical checks and the design checks. Report failures honestly.

```bash
python scripts/qa.py out.mp4 --expect-fps 30 --expect-duration 6.0 \
  --expect-size 1920x1080 --max-mb 50 --still 2.5 --still-out review.png
```

It exits non-zero on failure, so it can gate a build. Then do the visual pass from
`references/qa-checklist.md` — text legibility, safe zones, audio sync, banding,
loop seams, file size per platform.

If something fails: fix it, re-render, re-run QA. Do not deliver a file you know
is broken.

---

## Step 9 — Deliver

Present the output file(s) and a short note on what can be tweaked.

```markdown
## Delivered
- **out.mp4** — 1920x1080, 30fps, 6.0s, 2.1 MB, h264
- QA: 9 passed, 0 failed, 1 warning (no audio, as intended)

**What you can tweak:**
- Hold length on the lockup (scene 4) — currently 3.2s
- Logo position — currently centred at 44% vertical
- Palette — swap #143cb4 for any brand colour and the whole field follows
- Export a 1080x1920 vertical version by changing data-width/height
```

Keep that to a handful of specific, cheap-to-change levers. It is what turns a
render into a working relationship.

---

## Reference files

Read these when you need them, not up front.

| File | Read it when |
|---|---|
| `references/motion-principles.md` | Writing the motion spec. Easing curves with numbers, durations, stagger, reading time, safe areas, aspect ratios, the 12 principles as controls. |
| `references/visual-types.md` | Choosing or refining a default preset. Nine types with structure, pacing, common mistakes, and a spec each. |
| `references/tooling.md` | Installing anything, or before you rely on a version or licence. Verified versions, install commands, render flags, licences, and the traps. |
| `references/image-handling.md` | The user supplied images. Resolution, background removal (and which rembg model is safe), alpha, Ken Burns, logo clear space, palette extraction, licensing. |
| `references/reference-video-analysis.md` | The user supplied a reference video. The FFmpeg procedure for cuts, pacing, palette, motion intensity, and what not to copy. |
| `references/qa-checklist.md` | Before delivering. Mechanical checks, visual checks, and the common fixes. |

## Scripts

Tested, and no placeholders:

| Script | Use |
|---|---|
| `scripts/qa.py` | QA a rendered video. Frame rate, duration, resolution, black/frozen frames, audio, loudness, file size. Exits non-zero on failure. |
| `scripts/scene_cuts.py` | Measure a reference's pacing. Finds cuts with `scdet`, reports shot-length distribution and cuts/min. |
| `scripts/palette.py` | Extract a brand palette from an image, dropping neutrals and transparency. |

```bash
python scripts/qa.py out.mp4 --expect-fps 30 --expect-duration 6.0
python scripts/scene_cuts.py reference.mp4 --threshold 1
python scripts/palette.py logo.png --colors 6
```

## Things that will bite you

- **A composition with no registered timeline costs 45 seconds per render.** Add
  `data-no-timeline`.
- **`data-track-index` does not prevent overlap.** The render never reads it.
- **`autoAlpha` on a clip element is rejected.** Animate a child.
- **rembg's default model is not free for commercial use.** Always `-m u2netp`.
- **rembg's default model also fails on modest machines** with an 822 MB ONNX
  allocation error. `u2netp` is both the licence-safe and the working choice.
- **ffmpeg `zoompan` steps visibly.** Use a paused GSAP timeline for Ken Burns.
- **`hyperframes beats` reports nothing on non-percussive audio.** It needs real
  onsets.
- **MP4 has no alpha.** Render WebM or MOV if you need transparency.
- **Remotion is only free for teams of 3 or fewer.** Ask before choosing it.
