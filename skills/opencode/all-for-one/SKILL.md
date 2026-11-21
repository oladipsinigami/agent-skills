---
name: all-for-one
description: Use when the user wants every installed skill surveyed and the right ones assembled for a piece of work — "analyze all my skills and pick the ones I need", "which skills should I use for this build", "what do I have installed", "help me choose the right skills", "audit my skill library", "why isn't the right skill triggering", or any request to survey, list, compare, or route across the whole skill collection before starting work. Fires even when the user names only the task ("build me a dashboard") and does not mention skills at all, because the point of this skill is to decide the tooling before acting. Not for a single obvious skill use where the description already names it outright.
---

# All for one

One pass over the whole skill library, then a deliberate shortlist for the
build in front of us. The value here is the selection, not the listing — a
wall of 140 skill names helps nobody. The job is to work out what the build
actually needs, then load exactly those skills and say why.

## Why this exists

Without a deliberate pass, two failure modes show up constantly. Either the
agent loads nothing and improvines badly on work that has a proven skill for
it, or it loads fifteen overlapping skills and the instructions fight each
other while context fills with text nobody reads. Both waste the user's time.
Reading the library first, then committing to a short list, avoids both.

## Step 1 — Survey the library

Run the bundled inventory rather than trusting your memory of what is
installed. Skills get added and removed constantly, and a stale mental model
is how you end up recommending a skill that was deleted three weeks ago.

```bash
python <skill-dir>/scripts/inventory.py
```

Options worth knowing: `--json` for structured output, `--search "<term>"` to
filter, `--out <path>` to write the full table to a file when the list is long
enough to be worth paging through.

If the script cannot run (no Python, locked-down environment), fall back to
reading `references/index.md`, which is the same survey pre-generated. Tell the
user it is a snapshot rather than live output, because it goes stale.

Report the shape of the library, not every row: roughly how many skills, which
categories dominate, and whether anything looks stale or duplicated. Duplicate
names are worth flagging, because two skills claiming the same job will
compete for triggering and you have to pick one deliberately.

## Step 2 — Analyze the build

Before touching skills, understand the work. A selection built on a vague read
of the request will miss.

Establish, from the conversation and the repo:

- **The deliverable** — what exists at the end. A deployable app, a document,
  a diagram, a passing test suite.
- **The domain** — frontend, backend, data, docs, trading, on-chain, research.
  This decides which category of skill applies.
- **The stage** — discovery, planning, implementation, review, or shipping.
  The right skill differs sharply across these, and loading a
  discovery-time skill during implementation is mostly wasted context.
- **The friction** — what is likely to go wrong. Performance, accessibility,
  security, unclear requirements, unfamiliar framework, flaky tests. This is
  often where the most valuable skill is hiding, because it is the thing the
  user did not think to ask for.
- **Constraints** — existing stack, libraries already in `package.json`, what
  the user said not to touch. Skills that recommend a different stack than the
  one already in the repo cause friction, not value.

If the request is genuinely ambiguous in a way that changes the selection, ask
one focused question. Do not interrogate — resolve ambiguity with a single
question, then commit.

## Step 3 — Match and justify

Read `references/routing.md` for the category map. It groups the common skills
by job so you can jump to the right cluster instead of scanning 140 rows.

Produce a shortlist with three tiers:

- **Core** (1–3 skills) — directly on the critical path of this build. These
  get loaded.
- **Supporting** (0–3) — useful for a specific phase, loaded when that phase
  starts rather than all at once.
- **Deliberately skipped** — the near-misses you considered and ruled out, with
  the reason. Naming these matters: it shows the selection was a decision, and
  it stops the user asking "why didn't you use X?" later.

Then actually load the core skills with the `skill` tool. A shortlist you never
load is just a document. Load them now, because the skill bodies are what
change how you execute.

Present the shortlist to the user in a compact table before or alongside
loading:

| Skill | Why this build | When |
| --- | --- | --- |
| `frontend-design` | Landing page from scratch, no design system exists | now |
| `verification-before-completion` | Claims about the build need evidence | now |
| `performance-optimization` | Only if the page gets heavy | later |

Keep it tight. If the table runs past about six rows, the shortlist is too
broad and you should cut it — most builds genuinely need two or three.

## Step 4 — Apply and note the gap

Work the build using the loaded skills. While doing so, keep an eye out for
moments where a skill would have helped but was not in the shortlist. Add it
then rather than re-running the whole survey.

Close by telling the user what you loaded, what you deferred, and anything you
noticed while surveying that they may want to act on separately — a stale
skill, a duplicate pair, a skill that references a CLI which is not installed.
That last one is worth checking explicitly: several skills ship a body that
depends on an external binary, so the skill loads and then quietly cannot do
its job. `graphify` needs its Python package, `impeccable` needs its engine,
the `understand-*` family needs its viewer toolchain. Mention these when they
are selected, not when they fail.

## Keeping the index fresh

Regenerate the reference files whenever the library changes:

```bash
python <skill-dir>/scripts/inventory.py --json --out <skill-dir>/references/index.json
python <skill-dir>/scripts/inventory.py --out <skill-dir>/references/index.md
```

Both writes are safe to run at any time — the script only reads skill
directories and rewrites these two files.

## Notes

This skill composes with `using-agent-skills` and `using-superpowers`, which
cover general skill-discovery discipline. Where they overlap, prefer their
guidance on a normal task and use this one when the user wants an explicit
survey-and-shortlist across the whole library.

The library is large enough that blindly loading everything would be actively
harmful — the descriptions alone would swamp the context window and dilute
every instruction in it. Select, then load.