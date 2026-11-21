# Agent Skills

A personal library of **101 agent skills** for [Claude Code](https://claude.com/claude-code) and [OpenCode](https://opencode.ai). Each skill teaches an agent a repeatable workflow — building a deck, reviewing a pull request, designing a landing page, analysing a chart, running a payment.

Skills are triggered automatically by their description. You don't run commands; you just ask for the work.

## What's inside

| Collection | Install to | Count |
|---|---|---|
| `skills/claude/` | `~/.claude/skills/` | 28 |
| `skills/opencode/` | `~/.config/opencode/skills/` | 73 |

Some skills appear in both collections — they are independent copies, install whichever you need.

Highlights by area:

- **Engineering** — code review, debugging, TDD, spec-driven development, security hardening, performance, CI/CD, git workflow, observability
- **Design & frontend** — frontend design, UI engineering, design systems, accessibility, UI/UX intelligence
- **Documents & files** — `docx`, `pdf`, `pptx`, `xlsx` (create, edit, extract)
- **Video & motion** — HyperFrames suite, motion graphics, demo videos, media sourcing
- **Crypto & payments** — Kite Passport, OKX onchain suite, Circle/USDC wallets, x402 payments, trading analysis
- **Thinking & planning** — brainstorming, spec writing, planning, decision coaching, adversarial review

See [`INDEX.md`](INDEX.md) for the full list with one-line descriptions.

## Install

**macOS / Linux**

```bash
git clone <this-repo-url> agent-skills
cd agent-skills
./install.sh
```

**Windows (PowerShell)**

```powershell
git clone <this-repo-url> agent-skills
cd agent-skills
.\install.ps1
```

The installers copy the skill folders into the right place for each agent. They don't touch anything else. To install only one collection, pass it as an argument:

```bash
./install.sh claude      # Claude Code only
./install.sh opencode    # OpenCode only
```

Restart the agent (or start a new session) and the skills are available.

### Manual install

```bash
cp -r skills/claude/*   ~/.claude/skills/
cp -r skills/opencode/* ~/.config/opencode/skills/
```

## Requirements

Everything is plain markdown plus optional helper scripts. Prompt-only skills (design, writing, planning, review) work immediately.

Skills that shell out to a tool need that tool installed:

| Skills | Needs |
|---|---|
| `hyperframes*`, `motion-graphics`, `media-use`, `reverse-any-video` | Node.js + `hyperframes` CLI |
| `kite-*`, `passport-*`, `wallet-send`, `shopping`, `x402-execute` | `kpass` CLI + your own account |
| `okx-*` | `onchainos` CLI + your own OKX login |
| `docx`, `pdf`, `pptx`, `xlsx` | Python 3 + the libraries named in each `SKILL.md` |
| `browser-testing-with-devtools` | Chrome DevTools MCP server |

## No credentials included

This repo contains **no** API keys, wallets, sessions, or tokens. Every credential-using skill asks you to sign in on first run, against your own account.

## Updating

```bash
git pull
./install.sh          # re-copy; existing folders are overwritten
```

## Adding a skill

Create `skills/opencode/<my-skill>/SKILL.md` with YAML frontmatter:

```markdown
---
name: my-skill
description: What it does and when to use it. Be specific — this line is how the agent decides to trigger it.
---

# My skill

Instructions...
```

Commit and push. The description matters more than the body: it is the only thing the agent sees before deciding to load the skill.

## Provenance

Skills were collected from a mix of public collections (Anthropic's skills, HyperFrames, OKX, Circle/Kite tooling) and personal work. Check the individual `SKILL.md` and any `LICENSE`/`ATTRIBUTION` files inside a skill folder before redistributing it.
