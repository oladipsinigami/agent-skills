#!/usr/bin/env python3
"""Inventory every installed OpenCode skill and emit a compact routing index.

Skills are discovered in the global dirs OpenCode actually reads, plus the
project-local ones. Frontmatter is parsed properly so folded (>) and literal
(|) YAML scalars come through as real text instead of a bare marker.

Usage:
    python inventory.py                 # markdown table
    python inventory.py --json          # machine-readable
    python inventory.py --search "ui"   # filter by substring
"""

import argparse
import io
import json
import os
import re
import sys

GLOBAL_DIRS = [
    os.path.expanduser("~/.config/opencode/skills"),
    os.path.expanduser("~/.agents/skills"),
    os.path.expanduser("~/.claude/skills"),
]
LOCAL_DIRS = [
    os.path.expanduser("~/.config/opencode/skill"),
    ".opencode/skills",
    ".agents/skills",
    ".claude/skills",
]

# Directories whose skills the user set up deliberately. Prefer these when the
# same name shows up twice so an install never shadows tuned local copies.
PREFERRED = GLOBAL_DIRS[:2]


def parse_frontmatter(text):
    """Return (name, description) from YAML frontmatter.

    Handles plain scalars, and folded (>) / literal (|) blocks with an optional
    chomping indicator, which is how several real skills write long
    descriptions.
    """
    if not text.startswith("---"):
        return None, ""
    end = text.find("\n---", 3)
    if end == -1:
        return None, ""
    block = text[3:end]
    lines = block.splitlines()

    name = ""
    desc = ""
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("name:"):
            name = line[5:].strip().strip("\"'")
            i += 1
        elif line.startswith("description:"):
            head = line[12:].strip()
            if head in (">", "|", ">-", "|-", ">+", "|+"):
                chunk = []
                i += 1
                while i < len(lines):
                    nxt = lines[i]
                    # A block scalar ends at the first line that is not indented.
                    if nxt.strip() and not nxt.startswith((" ", "\t")):
                        break
                    chunk.append(nxt.strip())
                    i += 1
                desc = " ".join(p for p in chunk if p)
            else:
                desc = head.strip("\"'")
                i += 1
        else:
            i += 1
    return name, re.sub(r"\s+", " ", desc).strip()


def first_sentence(text, limit=180):
    if not text:
        return "(no description)"
    text = re.sub(r"^(Use (this skill )?(when|whenever)|Triggers?( on)?:?)\s*", "", text)
    cut = re.split(r"(?<=[.!?])\s", text, maxsplit=1)[0]
    if len(cut) > limit:
        cut = cut[: limit - 1].rsplit(" ", 1)[0] + "…"
    return cut


def keywords(desc, limit=12):
    stop = {
        "use", "when", "the", "and", "for", "this", "skill", "that", "with",
        "you", "are", "a", "an", "to", "of", "in", "on", "it", "is", "or",
        "any", "user", "users", "should", "can", "will", "be", "do", "not",
        "use. ", "skill.", "triggers", "trigger", "also", "make", "sure",
    }
    words = re.findall(r"[a-z][a-z0-9+.#-]{2,}", desc.lower())
    counts = {}
    for w in words:
        if w in stop:
            continue
        counts[w] = counts.get(w, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ", ".join(w for w, _ in ranked[:limit])


def discover():
    found = {}
    for scope, dirs in (("global", GLOBAL_DIRS), ("local", LOCAL_DIRS)):
        for d in dirs:
            if not os.path.isdir(d):
                continue
            for entry in sorted(os.listdir(d)):
                skill_md = os.path.join(d, entry, "SKILL.md")
                if not os.path.isfile(skill_md):
                    continue
                try:
                    with io.open(skill_md, encoding="utf-8", errors="replace") as f:
                        head = f.read(8000)
                except Exception as exc:
                    found.setdefault(
                        entry,
                        {"name": entry, "path": skill_md, "dir": os.path.dirname(skill_md),
                         "scope": scope, "desc": "unreadable: %s" % exc, "keywords": ""},
                    )
                    continue
                name, desc = parse_frontmatter(head)
                name = name or entry
                try:
                    rel = os.path.relpath(os.path.dirname(skill_md))
                except ValueError:
                    rel = os.path.dirname(skill_md)
                record = {
                    "name": name,
                    "dir": entry,
                    "path": skill_md,
                    "location": rel,
                    "scope": scope,
                    "desc": desc,
                    "keywords": keywords(desc),
                }
                prev = found.get(name)
                # Keep the first hit, preferring non-PREFERRED scopes only as a
                # last resort; never let a later install replace an earlier one.
                if prev is None:
                    found[name] = record
                elif prev["scope"] == "local" and record["scope"] == "global":
                    found[name] = record
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--search", default="")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    skills = discover()
    if args.search:
        needle = args.search.lower()
        skills = {
            k: v for k, v in skills.items()
            if needle in v["name"].lower()
            or needle in v["desc"].lower()
            or needle in v["keywords"]
        }

    ordered = sorted(skills.values(), key=lambda s: s["name"].lower())

    if args.json:
        payload = {
            "count": len(ordered),
            "skills": [
                {
                    "name": s["name"],
                    "scope": s["scope"],
                    "location": s["location"],
                    "description": s["desc"],
                    "keywords": s["keywords"],
                }
                for s in ordered
            ],
        }
        text = json.dumps(payload, indent=2, ensure_ascii=False)
    else:
        rows = ["# Installed skills (%d)" % len(ordered), ""]
        rows.append("| Skill | Scope | What it does | Signal words |")
        rows.append("| --- | --- | --- | --- |")
        for s in ordered:
            summary = first_sentence(s["desc"]).replace("|", "/")
            rows.append(
                "| `%s` | %s | %s | %s |"
                % (s["name"], s["scope"], summary, s["keywords"])
            )
        text = "\n".join(rows) + "\n"

    if args.out:
        with io.open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        sys.stderr.write("wrote %s (%d skills)\n" % (args.out, len(ordered)))
    else:
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
        sys.stdout.write(text)


if __name__ == "__main__":
    main()