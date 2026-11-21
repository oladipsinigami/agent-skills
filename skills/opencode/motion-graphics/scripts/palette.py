#!/usr/bin/env python3
"""Extract a dominant-color palette from an image (logo, screenshot, brand asset).

Usage:
    python palette.py image.png [--colors 6] [--ignore-white] [--ignore-black] [--json]

Prints hex swatches, most-frequent first. Near-white, near-black and fully
transparent pixels are excluded by default because they dominate most logos
and carry no brand information.
"""
import sys
import json
import argparse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--colors", type=int, default=6)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--keep-white", action="store_true")
    ap.add_argument("--keep-black", action="store_true")
    ap.add_argument("--threshold", type=int, default=24,
                    help="how close to white/black counts as near-neutral")
    args = ap.parse_args()

    from PIL import Image

    def rows(img):
        # getdata() is deprecated in Pillow 12+; get_flattened_data is the
        # replacement. Fall back so the script runs on either version.
        try:
            return list(img.get_flattened_data())
        except AttributeError:
            return list(img.getdata())

    im = Image.open(args.image)
    if im.mode in ("RGBA", "LA", "PA"):
        im = im.convert("RGBA")
        px = [p[:3] for p in rows(im) if p[3] > 200]
    else:
        im = im.convert("RGB")
        px = rows(im)

    if not px:
        print("ERROR: image is fully transparent", file=sys.stderr)
        return 1

    t = args.threshold
    filtered = []
    for r, g, b in px:
        if not args.keep_white and r > 255 - t and g > 255 - t and b > 255 - t:
            continue
        if not args.keep_black and r < t and g < t and b < t:
            continue
        filtered.append((r, g, b))

    if not filtered:
        print("ERROR: every pixel was filtered as neutral; lower --threshold "
              "or pass --keep-white/--keep-black", file=sys.stderr)
        return 1

    # Rebuild a small source image so Pillow's quantizer does the clustering.
    src = Image.new("RGB", (len(filtered), 1))
    src.putdata(filtered)
    n = max(1, min(args.colors, len(filtered)))
    q = src.quantize(colors=n, method=Image.MEDIANCUT)
    pal = q.getpalette()
    ranked = sorted(q.getcolors(len(filtered)), reverse=True)

    out = []
    for count, idx in ranked:
        i = idx * 3
        r, g, b = pal[i], pal[i + 1], pal[i + 2]
        out.append({
            "hex": "#%02x%02x%02x" % (r, g, b),
            "rgb": [r, g, b],
            "pixels": count,
            "share": round(count / len(filtered), 4),
        })

    if args.json:
        print(json.dumps({"total_sampled": len(filtered), "swatches": out}, indent=2))
    else:
        for s in out:
            print("%s  rgb(%d,%d,%d)  %5.1f%%  n=%d"
                  % (s["hex"], *s["rgb"], s["share"] * 100, s["pixels"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
