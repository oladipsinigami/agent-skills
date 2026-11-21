# Routing map

Grouped by job so you can jump to a cluster instead of scanning every row of
`index.md`. This is a starting map, not the full list — use `index.md` or
`inventory.py --search` when the build needs something not listed here.

Names marked ⚙ need an external CLI or binary that is not installed by
default. Select them, then tell the user what to install.

## Before writing code

| Skill | Use when |
| --- | --- |
| `brainstorming` | Requirements are fuzzy and you are about to invent features |
| `interview-me` | The ask is underspecified; one-question-at-a-time intent extraction |
| `grill-me` | User wants their plan stress-tested before committing |
| `honest-decision-coach` | User is torn between options and wants a verdict |
| `idea-refine` | Idea is vague and needs diverging then converging |
| `spec-driven-development` | No spec exists; needs PRD/scope first |
| `planning-and-task-breakdown` | Clear requirements that need ordered tasks |
| `writing-plans` | Multi-step work needs a plan before touching code |
| `doubt-driven-development` | Stakes are high; every assumption deserves a cross-exam |
| `constraint-driven-development` | Quality bar needs to be written down and defended |

## While writing code

| Skill | Use when |
| --- | --- |
| `incremental-implementation` | Change spans several files or feels too big to land at once |
| `test-driven-development` | Implementing logic or fixing a bug, where tests prove it works |
| `systematic-debugging` | A bug, failing test, or unexpected behaviour |
| `model-aware-code-debugger` | Debugging where you want model-specific fix prompts |
| `source-driven-development` | Library/framework correctness matters; verify against real docs |
| `api-and-interface-design` | Designing endpoints, type contracts, or module boundaries |
| `security-and-hardening` | Untrusted input, auth, sessions, third-party integrations, deps |
| `performance-optimization` | Slow code, N+1 queries, Core Web Vitals, profiling |
| `observability-and-instrumentation` | Production behaviour must be visible and diagnosable |
| `deprecation-and-migration` | Removing old systems, zero-downtime schema changes |
| `ponytail` | Any coding task where the laziest working solution is the right one |
| `caveman` | Output is too verbose and needs compressing without losing accuracy |

## Reviewing and verifying

| Skill | Use when |
| --- | --- |
| `code-review-and-quality` | Multi-axis review before anything merges |
| `verification-before-completion` | About to claim done, fixed, or passing |
| `receiving-code-review` | Feedback arrived and needs technical scrutiny, not blind action |
| `requesting-code-review` | Major feature finished and needs eyes on it |
| `code-simplification` | Code works but is hard to read or extend |
| `ponytail-review` | Diff-level over-engineering audit |
| `ponytail-audit` ⚙ | Whole-repo over-engineering audit |
| `archify-review` | Triage by value, cost, and impact |

## Frontend and UI

| Skill | Use when |
| --- | --- |
| `frontend-design` | Building pages/components with real design quality |
| `frontend-ui-engineering` | Accessible, responsive, production-grade UI |
| `ui-ux-pro-max` ⚙ | Design intelligence, styles, palettes, stack-specific UI |
| `ui-styling` | shadcn/ui, Tailwind, dark mode, design systems |
| `impeccable` ⚙ | Design direction pass: audit, polish, bolder, quieter, harden |
| `interface-kit` | Accessible, performant UI implementation details |
| `design` | Logos, brand identity, banners, icons, social assets |
| `design-system` | Token architecture and component specs |
| `brand` / `brand-guidelines` | Voice and identity; Anthropic brand styling |

## Diagrams, docs, and artifacts

| Skill | Use when |
| --- | --- |
| `archify` ⚙ | Architecture/workflow/sequence/data-flow diagrams as HTML+SVG |
| `graphify` ⚙ | Knowledge graph of a codebase or docs corpus |
| `understand` ⚙ and `understand-*` ⚙ | Interactive codebase graphs, diffs, onboarding, Figma |
| `documentation-and-adrs` | Recording architecture decisions and rationale |
| `doc-coauthoring` | Structured spec/proposal writing workflow |
| `content-research-writer` | Long-form researched content with citations |
| `deslopify` | Strip AI-writing tells from any text |
| `internal-comms` | Status reports, leadership updates, incident reports |
| `slides` / `theme-factory` / `artifacts-builder` ⚙ | Presentations, theming, complex HTML artifacts |

## Testing in the real world

| Skill | Use when |
| --- | --- |
| `webapp-testing` ⚙ | Playwright against a local app, screenshots, browser logs |
| `browser-testing-with-devtools` ⚙ | Chrome DevTools MCP for DOM, console, network, profiling |
| `langsmith-fetch` ⚙ | Debugging LangChain/LangGraph via execution traces |
| `mcp-builder` | Building an MCP server in Python or TypeScript |
| `claude-api` | Anthropic SDK apps, prompt caching, model migration |

## Git, CI, and shipping

| Skill | Use when |
| --- | --- |
| `git-workflow-and-versioning` | Branching, atomic commits, PRs, releases |
| `using-git-worktrees` | Feature work needs isolation from the main workspace |
| `finishing-a-development-branch` | Implementation done; deciding how to integrate |
| `ci-cd-and-automation` | Setting up or changing pipelines and quality gates |
| `shipping-and-launch` | Pre-launch checklist, staged rollout, rollback |
| `subagent-driven-development` / `dispatching-parallel-agents` | Independent tasks worth fanning out |
| `executing-plans` | Running a plan inline as the implementer |
| `loop-factory` | Spec-driven inbox → active → archive task loop |

## File formats

| Skill | Use when |
| --- | --- |
| `pdf` / `docx` / `pptx` / `xlsx` | Those formats are the input or the deliverable |
| `file-organizer` | Deduplicating and restructuring files |
| `invoice-organizer` | Sorting receipts and invoices for tax |

## Domain-specific

| Skill | Use when |
| --- | --- |
| `trading-analyst-pro` / `binance-live-analyst` / `bitget-trading-agent` | Trading signals, live market data, automated execution |
| `use-*`, `pay-via-agent-wallet`, `lenspay-builder`, `accept-agent-payments` | Circle wallets, USDC, bridging, swaps, on-chain payments |
| `connect` / `connect-apps` | Real actions in Gmail, Slack, GitHub, Notion, 1000+ apps |
| `you-web` / `you-research` / `you-finance` / `you-free` | Web search, cited synthesis, finance data |

## Recurring selection conflicts

**Two skills for the same job.** Prefer the more specific one; if both are
equally specific, say which you picked and why. `frontend-design` and
`impeccable` overlap heavily — `frontend-design` builds, `impeccable`
critiques and refines. `ui-ux-pro-max` and `ui-styling` both cover component
work; `ui-styling` is the concrete shadcn/Tailwind implementation guide.

**A process skill fighting a speed skill.** `ponytail` (do less) and
`incremental-implementation` (thin slices) usually agree. `brainstorming`
(diverge first) and `ponytail` (just build it) genuinely conflict — ask the
user which they want rather than guessing.

**Skill bodies that need external tools.** `graphify`, `impeccable`,
`understand*`, `ui-ux-pro-max`, `archify`, `ponytail-audit`, `webapp-testing`,
`browser-testing-with-devtools`, `langsmith-fetch`, `artifacts-builder`. Load
these, then tell the user what to install.

**Overlapping index entries.** Two `skill-creator` skills exist with the same
purpose, and `artifacts-builder` / `web-artifacts-builder` are near-identical.
Pick one explicitly and mention the duplicate rather than loading both.