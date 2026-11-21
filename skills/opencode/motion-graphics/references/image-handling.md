# Handling user images

Logos, screenshots, product shots, photos. Most of the problems here are
resolution and alpha, and both are cheap to fix if you check first.

## 1. Check before you use it

```bash
ffprobe -v error -show_entries stream=width,height,codec_name,pix_fmt -of json input.png
```

Or in Python:

```python
from PIL import Image
im = Image.open(path)
print(im.size, im.mode)   # mode RGBA means it has alpha
```

Two things to check: **resolution** and **whether it has an alpha channel**.

## 2. Resolution

A source image needs to be at least as large as the area it occupies in the final
frame, and ideally larger, because it will be scaled and compressed.

| Final frame | Minimum source | Comfortable |
|---|---|---|
| 1080p (1920×1080) | 1920 px on the long edge | 2560–3840 px |
| 4K (3840×2160) | 3840 px | 5760+ px |
| 1080×1920 vertical | 1920 px tall | 2560 px tall |

DPI is irrelevant — only pixels matter for video. A 300 DPI image that is 400 px
wide is a 400 px image.

**If it is too small, do not silently scale it.** Options, in order of preference:

1. **Crop tighter.** If the important part is a smaller region, crop to it and
   the effective resolution improves.
2. **Upscale with Real-ESRGAN** (BSD-3-Clause, no Python needed):

   ```bash
   ./realesrgan-ncnn-vulkan -i small.png -o big.png -n realesrgan-x4plus
   ./realesrgan-ncnn-vulkan -i small.png -o big.png -s 2 -t 512
   ```

   The NCNN executable is not MIT-licensed separately — BSD-3-Clause. It has not
   been updated since April 2022; the maintained fork is
   `upscayl/upscayl-ncnn`. Test whichever you pick.
3. **Rescale with a good filter** as a last resort:

   ```bash
   ffmpeg -i small.png -vf scale=1920:-1:flags=lanczos big.png
   ```

   This interpolates; it does not add detail. It is better than nothing and much
   worse than upscaling.

**Tell the user when you upscaled.** A soft image is a legitimate outcome; a soft
image presented as sharp is not.

## 3. Formats

- **PNG** — use for anything with hard edges, text, screenshots, logos. Lossless,
  supports alpha. Preferred for UI work.
- **JPEG** — photographs only. No alpha. Never re-encode a JPEG repeatedly.
- **WebP** — good compression and alpha support; fine as an input.
- **SVG** — ideal for logos; scales without loss. Convert to PNG at the final
  render resolution before use, or embed directly in a HyperFrames composition.
- **HEIC** — common from phones. Convert first: `ffmpeg -i IMG.heic out.png` or
  PIL with `pillow-heif`. Verify which is available; do not assume.

## 4. Background removal

`rembg` is MIT-licensed code, but **the models carry their own licences and the
default is a trap**: the default model is now `bria-rmbg`, whose licence requires
a paid agreement for commercial use.

**Always pass `-m u2netp`** (Apache-2.0 upstream via U-2-Net, 4.6 MB download):

```bash
pip install rembg
rembg i -m u2netp input.png output.png     # single file
rembg p -m u2netp ./in/ ./out/             # batch directory
```

`u2net` and `isnet-general-use` are also Apache-2.0 and give better edges at
higher memory cost.

**Verified on a modest machine:** the default model failed with an ONNX Runtime
error asking for an 822 MB buffer. `u2netp` succeeded. So the small model is both
the correct licence answer and the practical one.

If the CLI fails with `ModuleNotFoundError: filetype` / `watchdog` / `asyncer`,
`pip install` those — rembg's install can leave them unresolved.

Edge quality: `u2netp` gives firm, slightly blocky edges and struggles on hair.
Add alpha matting (`-a`, needs `pymatting`) and feather one pixel afterwards if
the cut looks harsh:

```bash
ffmpeg -i cut.png -vf "gblur=sigma=0.6" -pix_fmt rgba feathered.png
```

## 5. Alpha and matting

- An RGBA PNG's alpha channel is a matte. Most pipelines expect
  **straight (non-premultiplied) alpha**.
- Compositing a premultiplied image over a dark background produces dark fringes;
  over a light one, light fringes. If you see halos on a cut-out, the source is
  premultiplied — un-premultiply before use.
- Feathering too much makes edges look like a cheap drop shadow. 0.5–1 px at
  1080p is enough.
- HyperFrames renders to MP4 as `yuv420p`, which has no alpha. For transparency
  render `--format webm` or `--format mov` and composite later.

## 6. Chroma key (green screen)

If the source has a clean solid background, ffmpeg can key it without any model:

```bash
ffmpeg -i greenscreen.mp4 -vf "chromakey=0x00FF00:0.35:0.15" -c:v libx264 -pix_fmt yuv420p out.mp4
```

Experiment with similarity and blend. `colorkey` is the simpler sibling;
`lumakey` keys on brightness. A matte built by hand and feathered will look
better than a model on a genuinely clean background.

## 7. Ken Burns, parallax, 2.5D

**Do not use ffmpeg `zoompan` for Ken Burns.** It steps visibly and its motion is
effectively linear. If you need a smooth move, use one of:

**Preferred — a paused timeline plus frame capture.** Build the move in HyperFrames
with GSAP easing and render it. You get real easing for free:

```js
var tl = gsap.timeline({ paused: true });
tl.fromTo("#photo", { scale: 1.0 }, { scale: 1.08, duration: 3, ease: "power2.inOut" }, 0);
```

**Parallax** — separate the image into layers (foreground, mid, background) and
move each at a different rate. Manual masking in Pillow:

```python
from PIL import Image
base = Image.open("scene.png").convert("RGBA")
# Paint an alpha mask: 255 = background layer, 0 = foreground layer
mask = Image.open("mask.png").convert("L")
bg  = base.copy(); bg.putalpha(mask)           # moves slowest
fg  = base.copy(); fg.putalpha(Image.eval(mask, lambda v: 255 - v))  # moves fastest
```

2.5D depth from a single image is a nice-to-have, not a requirement — if you
cannot separate layers reliably, a single slow push-in is a better result than a
bad parallax.

**Verified Pillow per-frame approach** if you must do it frame by frame:

```python
from PIL import Image
src = Image.open("photo.png")
w, h = src.size
for i in range(90):                       # 3s at 30fps
    t = i / 89.0
    zoom = 1.0 + 0.08 * t                 # scale 1.0 -> 1.08
    cw, ch = int(w / zoom), int(h / zoom) # crop window shrinks = zoom in
    x = (w - cw) // 2
    y = (h - ch) // 2
    frame = src.crop((x, y, x + cw, y + ch)).resize((w, h), Image.LANCZOS)
    frame.save("frames/kb_%04d.png" % i)
```

This is linear zoom. Apply an easing function to `t` if you can.

## 8. Logo treatment and clear space

**Clear space rule of thumb when no brand guideline exists:** reserve margin equal
to the cap height of the logo's most prominent letterform (or the height of a
distinctive mark element) on all four sides. Half that for the absolute minimum
acceptable spacing.

**Minimum size:** a logo should stay legible — if its smallest text element drops
below roughly 8–10 px cap height at 1080p, it is too small and will be unreadable
after compression.

**Never do these:**
- stretch, squash, or rotate the logo to fit
- recolour it unless explicitly told to
- place it on a background with insufficient contrast
- put it inside the bottom 35% of a vertical frame
- animate the logo itself with scale or rotation; animate what surrounds it

If the logo is supplied as vector, keep it vector as long as possible and only
rasterise at the final render resolution.

## 9. Extract a brand palette from a logo

```bash
python scripts/palette.py logo.png --colors 6
```

It prints hex swatches ranked by frequency, excluding near-white, near-black and
transparent pixels by default, because those dominate most logos and carry no
brand information. Flags: `--colors N`, `--json`, `--keep-white`, `--keep-black`,
`--threshold` (how close to neutral counts as neutral, default 24).

Verified: on a logo with five colours on white, it returns the five brand colours
and drops the white.

## 10. Licensing cautions — say this to the user

Do not lecture, but do state it once, plainly:

- They need the rights to any image they supply. Stock photos, press images, and
  other companies' logos all carry restrictions.
- A logo is a trademark as well as (sometimes) a copyright asset. Using a brand's
  logo in a promotional video implies endorsement in many jurisdictions.
- Fonts embedded in a supplied logo are themselves licensed works; extracting the
  type from a logo and reusing it as headline text is usually not permitted. Use
  an open-licensed font that is visually similar (see the asset list in
  `tooling.md` §11 for options).
- AI-generated and stock imagery still carry licence terms. Check them before
  publishing.

## 11. Free fonts and music

**SIL Open Font License (OFL-1.1)** — free for commercial use and embedding, with
no attribution string appearing in the rendered video. Note that OFL fonts often
have a **Reserved Font Name** (Inter is one), so derivatives must be renamed.

Verified OFL-1.1: **Inter** (rsms/inter — the GitHub release is more current than
the Google Fonts copy), **Bebas Neue**, **Roboto** (the current
`googlefonts/roboto-3-classic` repo; the old `roboto-2` was Apache-2.0 and is now
archived), **Open Sans**.

**CC0 1.0 music** — no attribution required, commercial use permitted. Verified
CC0 sources: Internet Archive items tagged Musopen (e.g. the item
`musopen-chopin`), and OpenGameArt's CC0 collection (verify each track
individually — the collection page mixes licences).

**Do not use:** ccMixter (CC BY-NC 4.0 site-wide, many NonCommercial tracks),
Free Music Archive (licence varies per track and is set by the rightsholder),
Open Music Archive (public domain *or* CC BY-SA — BY-SA requires attribution and
share-alike), or Pixabay (a proprietary Pixabay Content License, not CC0, which
restricts standalone resale and commercial use of recognisable brands).
