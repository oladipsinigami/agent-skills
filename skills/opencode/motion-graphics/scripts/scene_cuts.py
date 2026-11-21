#!/usr/bin/env python3
"""Measure the pacing of a reference video: find cuts, then report shot lengths.

Usage:
    python scene_cuts.py reference.mp4 [--threshold 10] [--json]

How it works
------------
`ffmpeg -vf scdet` scores every frame for scene change on a 0-100 scale and logs
one line per detected cut:

    lavfi.scd.score: 85.547, lavfi.scd.time: 1

This script parses those lines, diffs the cut times to get per-shot durations,
and reports the pacing statistics you need to match a reference's rhythm.

`--threshold` is passed straight through as `scdet=threshold=N` (valid range
0-100, default 10). Lower it for short-form/social cutting, which has smaller
diffs per cut, and raise it if you are getting false cuts on camera shake or
film grain. Verify against a frame you extracted before trusting a low value.

Emit `--json` to feed the numbers into a later step.

Note: the alternative `select='gt(scene,0.4)'` uses a 0-1 score on a different
scale and, in testing on FFmpeg 9.0.2, missed gradual dissolves that `scdet`
caught. `scdet` is the more reliable of the two.
"""
import sys
import re
import json
import argparse
import subprocess
import statistics

CUT_RE = re.compile(
    r"lavfi\.scd\.score:\s*([0-9.]+),\s*lavfi\.scd\.time:\s*([0-9.]+)")


def ffprobe_info(path):
    out = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries",
        "format=duration:stream=codec_name,width,height,r_frame_rate,"
        "nb_frames,pix_fmt",
        "-of", "json", path,
    ], capture_output=True, text=True).stdout
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {}


def find_cuts(path, threshold):
    vf = "scdet=threshold=%g" % float(threshold)
    proc = subprocess.run(
        ["ffmpeg", "-v", "info", "-i", path, "-vf", vf, "-f", "null", "-"],
        capture_output=True, text=True, errors="replace",
    )
    text = proc.stdout + proc.stderr
    cuts = []
    for m in CUT_RE.finditer(text):
        cuts.append(round(float(m.group(2)), 3))
    return sorted(set(cuts))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--threshold", type=float, default=10.0,
                    help="scdet sensitivity, 0-100 (default 10; lower = more cuts)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not 0 <= args.threshold <= 100:
        print("ERROR: --threshold must be 0-100", file=sys.stderr)
        return 2

    info = ffprobe_info(args.video)
    streams = info.get("streams", [{}])
    v = next((s for s in streams if "width" in s), streams[0]) if streams else {}
    duration = float(info.get("format", {}).get("duration", 0) or 0)

    cuts = find_cuts(args.video, args.threshold)

    fps = None
    if v.get("r_frame_rate"):
        num, _, den = v["r_frame_rate"].partition("/")
        try:
            fps = float(num) / float(den or 1)
        except (ValueError, ZeroDivisionError):
            fps = None

    boundaries = [0.0] + cuts + ([duration] if duration else [])
    shots = [round(boundaries[i + 1] - boundaries[i], 3)
             for i in range(len(boundaries) - 1)]

    report = {
        "file": args.video,
        "duration_s": round(duration, 3),
        "resolution": [v.get("width"), v.get("height")],
        "fps": round(fps, 3) if fps else None,
        "codec": v.get("codec_name"),
        "pixel_format": v.get("pix_fmt"),
        "threshold": args.threshold,
        "cut_points_s": cuts,
        "shot_count": len(shots),
        "shot_lengths_s": shots,
    }
    if shots:
        report["shot_mean_s"] = round(statistics.mean(shots), 3)
        report["shot_median_s"] = round(statistics.median(shots), 3)
        report["shot_min_s"] = round(min(shots), 3)
        report["shot_max_s"] = round(max(shots), 3)
        report["shot_stdev_s"] = (
            round(statistics.pstdev(shots), 3) if len(shots) > 1 else 0.0
        )
        if report["duration_s"]:
            report["cuts_per_minute"] = round(len(cuts) / duration * 60, 2)

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print("file            %s" % report["file"])
    print("duration        %.3f s" % duration)
    print("resolution      %sx%s  %s fps  %s" %
          (v.get("width"), v.get("height"), report["fps"], v.get("codec_name")))
    print("scdet threshold %g" % args.threshold)
    print("shots           %d" % len(shots))
    if shots:
        print("shot length     mean %.2fs  median %.2fs  min %.2fs  max %.2fs  stdev %.2fs"
              % (report["shot_mean_s"], report["shot_median_s"],
                 report["shot_min_s"], report["shot_max_s"], report["shot_stdev_s"]))
        print("cuts/min        %s" % report.get("cuts_per_minute"))
        print("cuts at (s)     %s" % (", ".join("%.2f" % c for c in cuts) or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
