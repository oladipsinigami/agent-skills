# Tooling: what to install, what to render with, what each licence allows

Everything here is free for commercial use. Versions were verified on 2026-10-09
against the npm registry, PyPI, and each project's own LICENSE file. Re-check
before relying on a version for a long-running project — these numbers rot.

## The working environment this was tested on

| | |
|---|---|
| OS | Windows 11 (win32) |
| Node | v24.18.0 |
| npm | 11.16.0 |
| Python | 3.14.5 |
| FFmpeg | 9.0.2 ("Lei", gyan.dev build) |
| Chrome (system) | present, but HyperFrames uses its own bundled browser |

A full end-to-end render was completed in this environment: a 3-second
1920×1080 30fps MP4 with a GSAP timeline, rendered in 18.6 s and verified with
ffprobe (h264, yuv420p, 90 frames, 1920×1080). It also rendered to WebM, GIF, a
transparent-capable WebM, and an MP4 with a mixed AAC audio track.

---

## 1. HyperFrames — the default renderer

Apache-2.0. Local rendering is free, needs no account, no API key, and produces
**no watermark**. (Verified from the README, the quickstart page, and the
authentication guide, which all state local rendering uses no HeyGen credits.)

### Install

```bash
# No install needed — this is the route to prefer in an agent harness
npx hyperframes <command>

# Or install once
npm install -g hyperframes
```

**Node.js 22 or newer is required** (`engines` in package.json, and stated in the
README). FFmpeg is a separate required system dependency.

On Windows, if FFmpeg is not already on PATH: download a 64-bit Windows build
from gyan.dev, extract it, and add its `bin` directory to PATH. Confirm with
`ffmpeg -version`.

Verified on 2026-10-09: **v0.8.143**. It is pre-1.0 and releases roughly daily,
so do not assume semver stability. Pin it if reproducibility matters:
`npx hyperframes@0.8.143 render ...`.

### Environment variables worth setting

HyperFrames ships telemetry **on by default** and it fingerprints the OS, kernel,
CPU/memory shape, whether it is running in Docker or gVisor, and the name of the
detected coding agent. It also runs a daily background update check, and `init`
reaches out to GitHub to install skills. For a deterministic, quiet, offline
run set all three:

```bash
export HYPERFRAMES_NO_TELEMETRY=1
export HYPERFRAMES_NO_UPDATE_CHECK=1
export HYPERFRAMES_SKIP_SKILLS=1
```

### The browser

HyperFrames renders through Chromium via Puppeteer. It **downloads its own
browser** rather than using the system one:

```bash
npx hyperframes browser ensure     # find it, or download it
npx hyperframes browser path       # print the executable path
npx hyperframes browser clear      # drop the cache
```

If this machine has no network access at render time, the browser is already
cached at `~/.cache/hyperframes/chrome/chrome-headless-shell/`, so renders still
work. `npx hyperframes doctor` reports whether HyperFrames can see FFmpeg and
Chrome — run it first when something fails.

### Commands actually used in this skill

```bash
# Authoring structure
npx hyperframes init my-video        # scaffold (use --non-interactive)
npx hyperframes catalog --query "logo reveal"   # search ~400 hosted blocks
npx hyperframes add <block-name> --no-clipboard

# Before rendering — this catches real contract errors
npx hyperframes check
npx hyperframes check --snapshots --at 1.5,4,7.25

# Preview frames without a full render
npx hyperframes snapshot . --at 0.5,1.5,2.9

# Render
npx hyperframes render --output out.mp4 --fps 30
npx hyperframes render --quality draft --output preview.mp4     # cheap preview
npx hyperframes render --format webm --output overlay.webm      # alpha
npx hyperframes render --format gif --output loop.gif
npx hyperframes render --no-browser-gpu --output sw.mp4         # software raster
```

`check` flags worth knowing: `--json`, `--samples` (default 9), `--at-transitions`,
`--tolerance`, `--timeout`, `--strict`, `--no-contrast`, `--caption-zone`.

`render` flags worth knowing: `-c/--composition` (default `index.html`),
`-f/--fps`, `-q/--quality` (`draft`, `looks`, `delivery`/`high`, `standard`),
`--resolution`, `--workers/-w` (1–24), `--crf`, `--video-bitrate`,
`--gif-loop`, `--hls-segment-seconds`, `--low-memory-mode`, `--gpu`,
`--browser-timeout` (seconds, default 60), `--player-ready-timeout` (ms).

`init --resolution` presets, verified: `landscape` 1920×1080, `portrait`
1080×1920, `landscape-4k` 3840×2160, `portrait-4k` 2160×3840, `square`
1080×1080, `square-4k` 2160×2160. Aliases `1080p`, `4k`, `uhd`.

### Composition anatomy

The root element carries the composition; timed children carry `class="clip"`:

```html
<div class="clip" data-composition-id="my-video" data-start="0" data-duration="6"
     data-width="1920" data-height="1080"
     style="left:0; top:0; width:1920px; height:1080px;">

  <div id="headline" class="clip" data-start="0.4" data-duration="2.2">
    Hello
  </div>

</div>
```

Motion is one paused GSAP timeline registered under the composition id:

```js
var tl = gsap.timeline({ paused: true });
window.__timelines = window.__timelines || {};
tl.from("#headline", { opacity: 0, y: 60, duration: 0.9, ease: "power3.out" }, 0.4);
window.__timelines["my-video"] = tl;
```

Determinism rules the renderer enforces: no `Date.now()`, no
`requestAnimationFrame`, no unseeded `Math.random()`, no mid-render fetching,
fps/width/height fixed before frame 0, and one finite timeline. Time is
`floor(frame) / fps`, never a clock.

Relative timing works, which makes shot lists easy to keep in sync:

```html
<div class="clip" data-start="scene1 + 0.5" data-duration="1.2">
```

### Known limitations, verified

- **A composition that never registers a timeline costs a flat 45 s penalty on
  every render.** If you are not animating, add `data-no-timeline` to the root.
- `data-track-index` is Studio-display only. The render never reads it and it
  does not prevent overlap — you must keep `data-start`/`data-duration` from
  overlapping by hand unless overlap is what you want.
- Animate **child** elements, not the clip element itself. `check` rejects
  `autoAlpha` on a clip element because the framework owns clip visibility.
- GIF has no audio and limited transparency. WebM and MOV carry alpha.
- Large raw-frame paths (`png-sequence`, `gif`, HDR, layered shader transitions)
  can need tens of GB on disk. Streaming is the default for single-worker
  MP4/MOV.
- `hyperframes check` reports "Browser session never ran" if the page is not
  render-ready inside `--timeout` (default 3000 ms). Layout, motion and contrast
  results are then placeholders, not a pass. Treat that as a failure.
- Render only strips metadata with `ffmpeg -i out.mp4 -map_metadata -1 -c copy`.
  What it writes (`hyperframes_renderer`, `hyperframes_version`) is container
  metadata, not a visible watermark.

### Audio

`<audio>` and `<video data-has-audio="true">` are mixed into the output. Useful
attributes: `data-volume` (1 = 0 dB), `data-fade-in`, `data-fade-out` (seconds,
linear, anchored to clip edges), `data-media-start`, `data-playback-rate`.

Tag the music so `beats` can find it:

```html
<audio id="bgm" data-timeline-role="music" data-start="0" data-duration="6"
       src="./bgm.mp3" data-volume="0.5" data-fade-in="0.4" data-fade-out="0.8"></audio>
```

`npx hyperframes beats . --json` writes `beats/<audio-path>.json` with
`{time, strength}` per beat. **Verified limitation:** on a pure sine tone it
reports "No beats detected" — it needs real percussive content to find onsets.
Free local TTS (Kokoro) and MusicGen exist in the CLI but download models;
HeyGen-hosted voices and music are paid and out of scope for this skill.

---

## 2. Remotion — the optional second renderer

**This is not open source.** The npm `license` field literally reads
`SEE LICENSE IN LICENSE.md`, and Remotion's own FAQ says it is "source-available
software, but it is not open source software according to the Open Source
Initiative's Open Source Definition."

Free License eligibility, verified from LICENSE.md:

- an individual
- a for-profit organisation with **up to 3 employees**
- a non-profit or not-for-profit organisation
- someone evaluating whether Remotion is a good fit, not yet using it commercially

Contracts count towards the headcount from Remotion 5.0 onward — under the
current licence a company could staff entirely with contractors and stay free,
and that closes in 5.0.

**Before choosing Remotion, ask the user how many people are on the team.** If
the answer is 4 or more, Remotion is not free for them and you must fall back to
HyperFrames.

Local rendering needs **no API key and no account** under the current licence.
Never use Remotion Lambda, Cloud Run, or Vercel — all are billed. Remotion Studio
is free locally but needs a paid seat if you are not Free-License eligible.

### Install

```bash
npx create-video@latest --yes --blank my-video    # non-interactive
cd my-video
npx remotion render
```

Current stable: **v4.0.534**. **Remotion 5.0 is not released** — the migration
page says so explicitly, and the v5 code sits behind a compile-time flag set to
`false`. No release date is published.

Requirements: Node 16+ (rises to 22 in 5.0), Bun 1.0.3+ if you use Bun. macOS 15
or later is stated as required; older macOS versions are unsupported. Linux needs
glibc 2.35+ and extra packages. Alpine and nixOS are unsupported. Remotion
downloads its own Chrome Headless Shell into `node_modules/.remotion/`.

### Render

```bash
npx remotion render <entry> <composition-id> out.mp4
npx remotion still  <entry> <composition-id> still.png
npx remotion compositions <entry> --quiet      # list ids only
```

Codecs: `h264` (default), `h265`, `av1`, `vp8`, `vp9`, `prores`, `h264-mkv`,
`mp3`, `aac`, `wav`, `png`. GIF via `--number-of-gif-loops` and `--every-nth-frame`.
Audio flags: `--audio-codec`, `--audio-bitrate`, `--muted`, `--enforce-audio-track`.

Before upgrading Remotion, read `LICENSE.md` in the repo. A licence change is
planned for 5.0, and the project's own licence FAQ is the authority on which
terms apply to you.

---

## 3. FFmpeg

**LGPL v2.1 or later** by default. If you build FFmpeg with any `--enable-gpl`
component, the GPL applies to the whole binary. It is explicitly not available
under proprietary terms. ffmpeg.org/legal.html is the authority.

Current stable: **9.0.2** ("Lei", 2026-09-18). An 8.1.3 branch is also current.

FFmpeg is required by HyperFrames and auto-downloaded by MoviePy, so install it
system-wide anyway.

Filters verified as present and correctly spelled in 9.0.2:
`select`, `scdet`, `showinfo`, `signalstats`, `palettegen`, `paletteuse`,
`blackdetect`, `freezedetect`, `drawtext`, `crop`, `zoompan`, `ebur128`,
`mpdecimate`, `tblend`. See `references/reference-video-analysis.md` for the
tested syntax.

---

## 4. GSAP

**Version 3.13+ is free, including commercial use, including all former
Club-only plugins** — SplitText, MorphSVG, DrawSVG, MotionPath, CustomEase,
ScrollTrigger, Flip, GSDevTools and the rest. The licence is Webflow's
proprietary "Standard No-Charge GSAP License", not MIT, but it costs nothing and
permits commercial use. The Webflow acquisition closed in fall 2024 and the
change took effect 2025-04-30 with the 3.13 release.

Current version: **3.15.0**.

```bash
npm install gsap
```

The old private `npm.greensock.com` registry is no longer maintained. Use public
npm with 3.13 or newer.

**One clause to respect:** the Standard License prohibits using GSAP in tools
that let users build visual animations without code where that competes with
Webflow's visual animation builder. Generating animation code from a prompt is
explicitly not prohibited — their own FAQ addresses this. If you ever turn this
skill into a hosted no-code editor, get written consent.

---

## 5. Manim

**MIT** (dual: © 2018 3Blue1Brown LLC and © Manim Community Developers).
Current version **0.22.0**. Requires Python 3.11+; cp314 wheels exist.

```bash
pip install manim
manim render -qm scene.py SquareToCircle   # 1280x720 @ 30fps
manim render -qh scene.py SceneName        # 1920x1080 @ 60fps
manim render --format webm -t scene.py Scene   # transparent -> webm/mov
manim render --format png-sequence scene.py Scene
```

Quality presets: `-ql` 854×480@15, `-qm` 1280×720@30, `-qh` 1920×1080@60,
`-qp` 2560×1440@60, `-qk` 3840×2160@60.

**Runs headless with no display.** The default renderer is Cairo, a software
rasteriser; ffmpeg ships via the PyAV dependency, so there is no separate ffmpeg
install. Avoid `-p` (preview) and `-l` (live preview) — those need GUI paths.
Transparent MP4 is rejected because MP4 has no alpha; use `--format mov` or
`webm`.

Pick Manim when the piece is genuinely mathematical or diagrammatic — plots,
geometry, LaTeX-quality equations, derivation steps. It is the wrong tool for
typographic or UI work.

Known limitations: no LaTeX needed unless you use `Tex`/`MathTex`; the project is
mid-refactor and is not accepting new feature contributions; Windows installs can
fail on missing MSVC build tools for `manimpango`.

---

## 6. Lottie

**lottie-web 5.13.0 — MIT. `@dotlottie/player-component` 2.7.12 — MIT.**
lottie-web does not support image sequences, video, or audio; masks carry a large
performance cost; only rectangles, ellipses and stars exist among shapes.

Honest assessment of headless Lottie → video: **there is no well-maintained
one-command open-source renderer.** `puppeteer-lottie` was last published
2020-07-18 and the LottieFiles fork is archived. `rlottie` is officially
deprecated.

The one credible path is **ThorVG v1.1.2 (MIT)**, whose CLI tools ship
`tvg-lottie2gif` (GIF output — pipe to ffmpeg for MP4). It renders without a
display server by design and uses a CPU/SIMD rasteriser. It needs a from-source
build with meson/ninja and the Lottie loader plus GIF saver enabled,
`-Dextra=lottie_exp` for expressions.

**Recommendation: treat Lottie as a playback format, not a rendering path.** If a
user hands you a `.json` or `.lottie`, the pragmatic route is to embed it in a
HyperFrames composition with `lottie-web` and render that. Do not promise
standalone Lottie→MP4 conversion.

---

## 7. Python: Pillow and MoviePy

**Pillow 12.3.0 — MIT-CMU** (note: the SPDX id is `MIT-CMU`, not plain MIT).
Python 3.10+, with cp314 wheels. Used for frame compositing, alpha masks, and
text rendering via `ImageFont.truetype()` / `ImageDraw`.

**MoviePy 2.2.1 — MIT.** Requires Python 3.9+, but its CI only tests 3.9–3.11 and
there is no 3.13 or 3.14 classifier — **treat it as unsupported on Python 3.14**
(which is what this environment runs). MoviePy 2.x renders text through Pillow,
so it no longer needs ImageMagick. ffmpeg is auto-downloaded by `imageio-ffmpeg`.
`preview()` needs ffplay and does not work headless.

Use MoviePy only for simple compositing and concatenation. For anything driven by
easing curves, HyperFrames with GSAP is both easier and more correct.

---

## 8. rembg — background removal

**MIT** for the code. **The models carry their own licences, and this is a trap.**

Verified from the rembg 2.0.85 README:

- The **default model is now `bria-rmbg`**, and "RMBG-2.0 is released under a
  BRIA license that requires a paid agreement for commercial use."
- `u2net` and `u2netp` come from U-2-Net, which is **Apache-2.0** — free for
  commercial use.
- `isnet-general-use` comes from DIS, also **Apache-2.0**.
- `u2net_cloth_seg` is MIT.

**Always pass an explicit model. Never let it default.**

```bash
pip install rembg
rembg i -m u2netp input.png output.png      # 4.6 MB model, Apache-2.0
rembg p -m u2netp ./in/ ./out/               # batch
```

**Verified on this machine:** the default model failed with an ONNX Runtime
allocation error asking for an 822 MB buffer. `-m u2netp` succeeded and produced
a clean RGBA result (corner alpha 0, centre alpha 254). So `u2netp` is both the
correct licence answer and the only reliable one on a modest machine. It
downloads from GitHub on first use into `~/.rembg/models/`.

If the CLI fails with `ModuleNotFoundError` for `filetype`, `watchdog`, or
`asyncer`, install those packages — the rembg install can leave them unresolved.

Edges from `u2netp` are firm and can look blocky on hair. Add alpha matting with
`-a` (needs `pymatting`) and consider a one-pixel feather afterwards.

---

## 9. Real-ESRGAN — upscaling

**BSD-3-Clause.** Code is BSD-3-Clause; the codec patents are your own
responsibility, exactly as with Remotion.

The portable NCNN/Vulkan executable needs no Python, no PyTorch and no CUDA:

```bash
./realesrgan-ncnn-vulkan.exe -i input.jpg -o output.png -n realesrgan-x4plus
./realesrgan-ncnn-vulkan -i input.jpg -o output.png -s 2 -t 512
```

Model names: `realesr-animevideov3` (default), `realesrgan-x4plus`,
`realesrgan-x4plus-anime`, `realesrnet-x4plus`. Flags: `-s` (2/3/4), `-t` tile
size (0 = auto, lower it if you run out of VRAM), `-j` thread counts.

**Prefer upscaling a source image over scaling it in the render.** An upscaled
PNG still holds detail; `scale` in ffmpeg only interpolates.

---

## 10. What to avoid, and why

| Do not use | Reason |
|---|---|
| After Effects, Canva, any SaaS renderer | Paid or subscription; breaks the $0 rule and needs a GUI |
| Remotion default model path in rembg | BRIA licence requires a paid commercial agreement |
| Remotion Lambda / Cloud Run / Vercel | Billed per render |
| HyperFrames cloud render | Needs a HeyGen account; 4K is billed at 1.5× |
| Pixabay "free" music | Pixabay Content License, not CC0; restricts standalone resale and branded use |
| Anything with an API key, credit system, trial, or watermark | Violates the hard rule |

---

## Unverified

- Whether Remotion 5.0 keeps the 3-employee threshold. The documented 5.0 licence
  changes are that contractors count toward headcount and that the company
  licence binds to the new Terms and Conditions. No source says the number moves,
  but none says it stays. Treat the current licence as authoritative for ≤4.x only.
- Remotion's `--concurrency` numeric default and range. The docs render it through
  a component that does not resolve to a number.
- Real-ESRGAN's NCNN executable has not been updated since April 2022; the
  maintained fork is `upscayl/upscayl-ncnn`. Test before relying on either.
- Whether a specific prebuilt FFmpeg binary on your system was compiled with
  `--enable-libfreetype` / `--enable-libfontconfig`, which `drawtext` needs. Check
  `ffmpeg -filters | grep drawtext` and test with a real font file.
