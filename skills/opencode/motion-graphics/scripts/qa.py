#!/usr/bin/env python3
"""QA a rendered video against the motion-graphics checklist.

Usage:
    python qa.py render.mp4 [--expect-fps 30] [--expect-duration 3.0]
                            [--expect-size 1920x1080] [--json]
                            [--still 1.5 --still-out frame.png]

Checks the things that are cheap to check mechanically and that most often go
wrong: frame-rate consistency, black/frozen frames, duration drift, audio
loudness, and file size. It deliberately does NOT judge design.
"""
import sys
import re
import json
import argparse
import subprocess


def run(cmd):
    # ffmpeg writes its filter reports (blackdetect, ebur128, ...) to stderr, so
    # both streams have to be captured.
    p = subprocess.run(cmd, capture_output=True, errors="replace")
    return p.stdout + p.stderr


def ffprobe(path):
    out = run(["ffprobe", "-v", "error", "-show_format", "-show_streams",
               "-of", "json", path])
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {}


def parse_ratio(s):
    if not s:
        return None
    num, _, den = s.partition("/")
    try:
        return float(num) / float(den or 1)
    except (ValueError, ZeroDivisionError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--expect-fps", type=float, default=None)
    ap.add_argument("--expect-duration", type=float, default=None,
                    help="seconds; flags drift beyond 1 frame")
    ap.add_argument("--expect-size", default=None, help="WxH")
    ap.add_argument("--max-mb", type=float, default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--still", type=float, default=None,
                    help="extract a frame at this many seconds for review")
    ap.add_argument("--still-out", default="qa-still.png")
    args = ap.parse_args()

    info = ffprobe(args.video)
    if not info:
        print("ERROR: ffprobe could not read %s" % args.video, file=sys.stderr)
        return 1

    streams = info.get("streams", [])
    v = next((s for s in streams if "width" in s), None)
    a = next((s for s in streams if s.get("codec_type") == "audio"), None)
    fmt = info.get("format", {})

    fps = parse_ratio(v.get("r_frame_rate")) if v else None
    nb_frames = None
    if v and v.get("nb_frames"):
        try:
            nb_frames = int(v["nb_frames"])
        except ValueError:
            nb_frames = None
    duration = float(fmt.get("duration", 0) or 0)
    size_bytes = int(fmt.get("size", 0) or 0)

    checks, warnings = [], []

    def ok(name, detail=""):
        checks.append({"name": name, "pass": True, "detail": detail})

    def bad(name, detail):
        checks.append({"name": name, "pass": False, "detail": detail})

    def warn(name, detail):
        warnings.append({"name": name, "detail": detail})

    # --- frame rate consistency -------------------------------------------------
    if fps:
        ok("frame_rate", "%g fps" % fps)
    else:
        warn("frame_rate", "could not determine fps")
    if v and v.get("pix_fmt"):
        ok("pixel_format", v["pix_fmt"])

    if nb_frames and fps and duration:
        expected = duration * fps
        drift = abs(nb_frames - expected)
        if drift <= 0.5:
            ok("frame_count_matches_duration",
               "%d frames == %.3fs x %g fps" % (nb_frames, duration, fps))
        else:
            bad("frame_count_matches_duration",
                "%d frames but %.3fs x %g fps = %.1f (drift %d frames)"
                % (nb_frames, duration, fps, expected, round(drift)))

    if args.expect_fps and fps:
        if abs(fps - args.expect_fps) < 0.01:
            ok("expected_fps", "%g fps as requested" % args.expect_fps)
        else:
            bad("expected_fps", "got %g fps, asked for %g" % (fps, args.expect_fps))

    # --- duration ---------------------------------------------------------------
    if args.expect_duration and duration:
        frame = 1.0 / fps if fps else 1.0 / 30.0
        drift = duration - args.expect_duration
        if abs(drift) <= frame:
            ok("duration", "%.3fs (requested %.3fs)" % (duration, args.expect_duration))
        else:
            bad("duration",
                "%.3fs vs requested %.3fs (off by %.3fs = %d frames)"
                % (duration, args.expect_duration, drift, round(abs(drift) / frame)))

    # --- resolution -------------------------------------------------------------
    if args.expect_size and v:
        want = args.expect_size.lower().replace(" ", "")
        got = "%sx%s" % (v.get("width"), v.get("height"))
        if want == got:
            ok("resolution", got)
        else:
            bad("resolution", "got %s, expected %s" % (got, want))

    # --- black frames -----------------------------------------------------------
    bl = run(["ffmpeg", "-v", "info", "-i", args.video,
              "-vf", "blackdetect=d=0.1:pix_th=0.10", "-f", "null", "-"])
    black = re.findall(r"black_start:([0-9.]+)\s+black_end:([0-9.]+)", bl)
    if black:
        bad("no_black_frames", "black at %s"
            % ", ".join("%s-%ss" % b for b in black[:6]))
    else:
        ok("no_black_frames", "none detected")

    # --- frozen frames ----------------------------------------------------------
    fz = run(["ffmpeg", "-v", "info", "-i", args.video,
              "-vf", "freezedetect=n=0.001:d=0.5", "-f", "null", "-"])
    freezes = re.findall(r"freeze_start:\s*([0-9.]+)", fz)
    if freezes:
        bad("no_frozen_frames", "freeze starts at %s"
            % ", ".join("%ss" % f for f in freezes[:6]))
    else:
        ok("no_frozen_frames", "none detected")

    # --- audio ------------------------------------------------------------------
    if a:
        ok("has_audio", "%s" % a.get("codec_name"))
        loud = run(["ffmpeg", "-nostats", "-i", args.video,
                    "-filter_complex", "ebur128", "-f", "null", "-"])
        m = re.search(r"I:\s*(-?[0-9.]+)\s*LUFS", loud)
        if m:
            lufs = float(m.group(1))
            if -24.0 <= lufs <= -9.0:
                ok("loudness", "%.1f LUFS integrated (reasonable for web)" % lufs)
            else:
                warn("loudness", "%.1f LUFS integrated; broadcast/web target "
                                 "is about -16 LUFS (EBU R128 default is -23)"
                      % lufs)
    else:
        warn("no_audio", "no audio stream found")

    # --- file size --------------------------------------------------------------
    mb = size_bytes / (1024 * 1024)
    if args.max_mb:
        if mb <= args.max_mb:
            ok("file_size", "%.1f MB (limit %.1f MB)" % (mb, args.max_mb))
        else:
            bad("file_size", "%.1f MB exceeds %.1f MB limit" % (mb, args.max_mb))
    else:
        if v:
            kbps = (size_bytes * 8 / 1000) / duration if duration else 0
            ok("file_size", "%.1f MB, %.0f kbps average" % (mb, kbps))

    # --- still for human review -------------------------------------------------
    still_path = None
    if args.still is not None:
        still_path = args.still_out
        run(["ffmpeg", "-v", "error", "-ss", str(args.still), "-i", args.video,
             "-frames:v", "1", "-y", still_path])

    passed = sum(1 for c in checks if c["pass"])
    failed = [c for c in checks if not c["pass"]]

    if args.json:
        print(json.dumps({
            "file": args.video, "passed": passed, "failed": len(failed),
            "checks": checks, "warnings": warnings, "still": still_path,
        }, indent=2))
    else:
        print("QA: %s" % args.video)
        if v:
            print("  %sx%s  %s  %g fps  %.3fs  %s"
                  % (v.get("width"), v.get("height"), v.get("codec_name"),
                     fps or 0, duration, v.get("pix_fmt")))
        for c in checks:
            print("  [%s] %-28s %s" % ("PASS" if c["pass"] else "FAIL",
                                       c["name"], c["detail"]))
        for w in warnings:
            print("  [WARN] %-28s %s" % (w["name"], w["detail"]))
        if still_path:
            print("  still written to %s" % still_path)
        print("  %d passed, %d failed, %d warnings"
              % (passed, len(failed), len(warnings)))

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
