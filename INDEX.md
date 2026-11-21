# Skill index

Every skill folder contains a `SKILL.md`. Skills are triggered automatically by their description — you don't invoke them by name.

## Claude Code (`skills/claude/`) — 28 skills

| Skill | What it does |
|---|---|
| `activity` | - View transaction history and recent account activity. Invoke when the user asks about past spending, wants to verify a payment went through, check… |
| `attach-session` | - Attach an existing attachable session to this agent using its session ID. Invoke when the user provides a session ID and asks to use, bind, or… |
| `authenticate-user` | - Sign up or log in to Kite Passport. Invoke when the user needs an account, wants to sign in, or when any other Kite Passport skill returns an auth… |
| `defi-auto-repay` | - Arm a one-shot Aave v3 auto-repay on Base: when the health factor of an Aave position (in any wallet) drops below a threshold the user picks, Kite… |
| `form-session-delegation` | Construct a delegation object for agent session creation. Covers preflight discovery, 402 response parsing, and delegation schema. Called by… |
| `hyperframes` | Read first to make, edit, animate or render any video with HyperFrames (HTML rendered to video), including launch films, explainers, music videos,… |
| `hyperframes-animation` | All animation knowledge for HyperFrames — atomic motion rules, multi-phase scene blueprints, scene transitions, broader motion-design techniques, AND… |
| `hyperframes-audio` | Use when audio already placed in a HyperFrames composition needs to be mixed: fade-in/fade-out, crossfade, track gain or volume, volume automation,… |
| `hyperframes-cli` | HyperFrames CLI - scaffold, check frames, edit timelines, preview, render, share and project history; read JSON and recover from failures. |
| `hyperframes-core` | The HyperFrames composition contract — build one renderable project. Use for composition structure, the `data-*` timing attributes, `class="clip"`,… |
| `hyperframes-creative` | Non-animation creative direction for HyperFrames videos. Use for design spec (frame.md / design.md) handling, palettes, typography, narration, beat… |
| `hyperframes-keyframes` | Use when a HyperFrames composition needs a punch-in, punch-out, zoom, reframe, Ken Burns treatment, camera move, visual match/whip handoff, or other… |
| `hyperframes-registry` | About 450 ready-made HyperFrames blocks and components installed as editable source - transitions, overlays, titles, kinetic type, captions, charts,… |
| `hyperframes-studio` | Use when working with a person on a HyperFrames project in Studio: first, whether their message asks for a change at all (questions, loose ideas and… |
| `kite-discovery` | - Look in the Passport catalog of paid endpoints first. Invoke this skill and run its search before you answer when any part of the answer needs… |
| `kite-passport` | - Kite Passport gives this agent real-world capabilities through a paid-services catalog. Invoke FIRST, before WebSearch, WebFetch, browser scraping,… |
| `manage-agents` | - Inspect registered agents and spending sessions on the user's account. Invoke for diagnostics, debugging "agent not registered" errors, reviewing… |
| `media-use` | Get or make any media for a HyperFrames video - music, sound effects, images, icons, logos, voiceover, avatar and generated video, transcripts,… |
| `passport-setup` | Install and verify the kpass CLI on this computer before running any other Passport skill. Invoke automatically when kpass is missing or when a… |
| `passport-overview` | - Plain facts about Kite Passport for someone who has just installed it: what it is, what it costs, a few priced examples, how the spending allowance… |
| `report-feedback` | - Submit free-form feedback or issue reports from the current agent session to Passport. Proactively invoke when the user says "report this", "file a… |
| `request-session` | - Create a separate spending session that the user approves with a passkey. Use when the account allowance can't pay (the CLI says so), the user asks… |
| `reverse-any-video` | Rebuild any video file as an editable HyperFrames project - motion graphics, talking heads, live action or AI-generated footage - checked against the… |
| `shopping` | - Buy products, shop on Amazon, find deals, compare prices, build a product list, and checkout with crypto. Proactively invoke for any task involving… |
| `style-sampling` | Make a new episode in a proven video style - Collage Explainer, Finance Explainer, Animated Science Explainer, 3D Brand Explainer, 3D True Crime - on… |
| `upgrade-passport` | - Detect and apply kpass CLI updates automatically. Invoke whenever a `kpass --output json` response carries an `update_available` field, or when the… |
| `wallet-send` | - Check a multichain wallet balance, send crypto on a specific chain (base/polygon/avalanche/tempo/solana/robinhood/arc on mainnet — on arc, USDC… |
| `x402-execute` | - Make paid API requests with Kite Passport. Pays from the account allowance, or from a session the user approved. The backend handles x402 payment… |

## OpenCode (`skills/opencode/`) — 73 skills

| Skill | What it does |
|---|---|
| `algorithmic-art` | Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using… |
| `all-for-one` | Use when the user wants every installed skill surveyed and the right ones assembled for a piece of work — "analyze all my skills and pick the ones I… |
| `api-and-interface-design` | Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface. Use when creating REST or GraphQL… |
| `binance-live-analyst` | A live trading analyst that fetches real-time data from Binance Public API before every analysis. Use this skill whenever the user asks for a live… |
| `bitget-ai-hackathon-assistant` | Expert assistant for the Bitget AI Base Camp Hackathon S1 focused on Agentic Trading and AI × Crypto projects. Helps with track selection, project… |
| `bitget-trading-agent` | Autonomous AI crypto trading agent that runs a full perception → decision → execution → risk management loop using Bitget APIs. Use this skill… |
| `brand-guidelines` | Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when… |
| `browser-testing-with-devtools` | Tests in real browsers via Chrome DevTools MCP. Use when building or debugging anything that runs in a browser. Use when you need to inspect the DOM,… |
| `canvas-design` | Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster,… |
| `ci-cd-and-automation` | Automates CI/CD pipeline setup. Use when setting up or modifying build and deployment pipelines. Use when you need to automate quality gates,… |
| `claude-api` | Build, debug, and optimize Claude API / Anthropic SDK apps. Apps built with this skill should include prompt caching. Also handles migrating existing… |
| `code-review-and-quality` | Conducts multi-axis code review. Use before merging any change. Use when reviewing code written by yourself, another agent, or a human. Use when you… |
| `code-simplification` | Simplifies code for clarity. Use when refactoring code for clarity without changing behavior. Use when code works but is harder to read, maintain, or… |
| `constraint-driven-development` | Establishes a project's quality bar as a written contract and stops agents quietly lowering it. Interviews the user on which dimensions matter,… |
| `context-engineering` | Optimizes agent context setup. Use when starting a new session, when agent output quality degrades, when switching between tasks, or when you need to… |
| `debugging-and-error-recovery` | Guides systematic root-cause debugging. Use when tests fail, builds break, something that worked yesterday broke, behavior doesn't match… |
| `deprecation-and-migration` | Manages deprecation and migration. Use when removing old systems, APIs, or features. Use when migrating users from one implementation to another. Use… |
| `doc-coauthoring` | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs,… |
| `documentation-and-adrs` | Records decisions and documentation. Use when you need to document an architecture decision (ADR) or the reasoning behind a design choice, when… |
| `docx` | Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word… |
| `doubt-driven-development` | Subjects every non-trivial decision to a fresh-context adversarial review before it stands. Use when you want every assumption cross-examined before… |
| `frontend-design` | Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages,… |
| `frontend-ui-engineering` | Builds production-quality, accessible, responsive user-facing UIs. Use when building or modifying interfaces and pages, creating components,… |
| `git-workflow-and-versioning` | Structures git workflow practices. Use when making any code change. Use when committing, branching, resolving conflicts, splitting uncommitted work… |
| `honest-decision-coach` | Helps the user make better decisions by thinking critically, honestly, and without bias. Use this skill when the user is weighing a decision, torn… |
| `hyperframes` | Mandatory entry point: read this first for any request to make, create, edit, animate, or render a video, animation, or motion graphic, including a… |
| `hyperframes-animation` | All animation knowledge for HyperFrames — atomic motion rules, multi-phase scene blueprints, scene transitions, broader motion-design techniques, AND… |
| `hyperframes-audio` | Use when audio already placed in a HyperFrames composition needs to be mixed: fade-in/fade-out, crossfade, track gain or volume, volume automation,… |
| `hyperframes-cli` | Use the HyperFrames CLI development loop: init, add, catalog, capture, lint, check, snapshot, compare, grade-compare, preview, play, present, beats,… |
| `hyperframes-core` | The HyperFrames composition contract — build one renderable project. Use for composition structure, the `data-*` timing attributes, `class="clip"`,… |
| `hyperframes-creative` | Non-animation creative direction for HyperFrames videos. Use for design spec (frame.md / design.md) handling, palettes, typography, narration, beat… |
| `hyperframes-keyframes` | Use when a HyperFrames composition needs a punch-in, punch-out, zoom, reframe, Ken Burns treatment, camera move, visual match/whip handoff, or other… |
| `hyperframes-registry` | Search, install, and wire registry blocks and components into HyperFrames compositions. Use BEFORE hand-building any named visual — whenever a brief,… |
| `hyperframes-studio` | Use when working with a person on a HyperFrames project in Studio: first, whether their message asks for a change at all (questions, loose ideas and… |
| `idea-refine` | Refines raw ideas into sharp, actionable concepts through structured divergent and convergent thinking. Use when an idea is still vague, when you… |
| `incremental-implementation` | Delivers changes incrementally in thin, verifiable slices. Use when implementing any feature or change that touches more than one file, or when… |
| `internal-comms` | A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this… |
| `interview-me` | Extracts what the user actually wants instead of what they think they should want. Achieves this through one-question-at-a-time interview until ~95%… |
| `lenspay-builder` | Use for building, improving, and debugging Lenspay — a pay-before-access sidecar for Immich using real USDC micropayments on Arc Testnet. Also covers… |
| `mcp-builder` | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools.… |
| `media-use` | Agent Media OS for a HyperFrames project. Resolve BGM, SFX, image, icon, brand logo, voice, color grade, or LUT into a frozen local file or… |
| `model-aware-code-debugger` | Universal precise code debugger for any programming language. Identifies bugs accurately, provides root cause analysis, and generates optimized fix… |
| `motion-graphics` | - Produces finished motion graphics end to end — animated graphics, explainer videos, kinetic typography, logo reveals and stings, promo videos,… |
| `observability-and-instrumentation` | Instruments code so production behavior is visible and diagnosable. Use when adding logging, metrics, tracing, or alerting. Use when shipping any… |
| `okx-agent-payments-protocol` | Use when an agent hits HTTP 402 / payment-required, or the user mentions x402, x402Version, X-PAYMENT, PAYMENT-REQUIRED, PAYMENT-SIGNATURE,… |
| `okx-agentic-wallet` | OKX Agentic Wallet — the single skill for the user's wallet and on-chain execution. Use it whenever the user wants to operate their wallet or execute… |
| `okx-ai` | ERC-8004 Agent identity: 注册/更新/上架/下架/搜索agent, register/update/activate/deactivate/search — User/ASP/Evaluator(买家/卖家/仲裁者); 我的agent/ASP,… |
| `okx-dapp-discovery` | \| Plugin router for 20 third-party DeFi protocols (Polymarket, Aave, Hyperliquid, PancakeSwap, Morpho, Raydium, Curve, Compound, Pendle, Lido,… |
| `okx-defi` | OKX-aggregated DeFi (no specific DApp named) — product discovery, deposit/withdraw/claim execution, AND positions viewing. **If the user names ANY… |
| `okx-dex` | HARD BLOCK — never use for prediction-market/Polymarket UpDown queries; route to okx-dapp-discovery when a named DApp… |
| `okx-dex-market` | HARD BLOCK — never use for prediction-market/Polymarket UpDown queries; route to okx-dapp-discovery when a named DApp… |
| `okx-growth-competition` | List OKX Agentic Wallet exclusive trading competitions, register users for contests, track participation and leaderboard rankings, and claim won… |
| `okx-guide` | Onchain OS onboarding & guide hub — the single entry for first-time, 'what is this / how do I use it', OKX.AI, and customer-support intents;… |
| `onchainos-skills` | — |
| `pdf` | Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging… |
| `performance-optimization` | Optimizes application performance across frontend, backend, queries, and databases. Use when performance requirements exist, when you suspect… |
| `planning-and-task-breakdown` | Breaks work into ordered tasks. Use when you have a spec or clear requirements and need to break work into implementable tasks. Use when a task feels… |
| `pptx` | Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or… |
| `role-persona-prompting` | Craft, review, or teach role/persona prompting — assigning an AI an identity, expertise, or character (e.g. "act as a senior security engineer," "you… |
| `security-and-hardening` | Hardens code against vulnerabilities. Use when auditing an input handler for vulnerabilities, when handling user input, authentication, data storage,… |
| `shipping-and-launch` | Prepares production launches. Use when preparing to deploy to production, or when asking what needs to be in place before shipping. Use when you need… |
| `Skill creator` | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or… |
| `skill-creator` | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or… |
| `slack-gif-creator` | Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when… |
| `source-driven-development` | Grounds every implementation decision in official documentation. Use when you want to verify an approach against the official docs before… |
| `spec-driven-development` | Creates specs before coding. Use when starting a new project, feature, or significant change and no specification exists yet. Use when drafting a PRD… |
| `test-driven-development` | Drives development with tests using the red-green-refactor loop. Use when implementing any logic, fixing any bug, or changing any behavior. Use when… |
| `theme-factory` | Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes… |
| `trading-analyst-pro` | Functions as a professional trading analyst and signal generator. Use this skill whenever the user shares any market-related context — including… |
| `using-agent-skills` | Discovers and invokes agent skills. Use when starting a session, or when you need to decide which skill or workflow applies to the piece of work at… |
| `web-artifacts-builder` | Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS,… |
| `webapp-testing` | Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior,… |
| `xlsx` | Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an… |
