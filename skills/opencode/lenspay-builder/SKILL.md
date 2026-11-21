---
name: lenspay-builder
description: Use for building, improving, and debugging Lenspay — a pay-before-access sidecar for Immich using real USDC micropayments on Arc Testnet. Also covers the circle-agent TypeScript x402 payment trace companion. Helps with architecture decisions, real wallet integration (MetaMask + viem), per-share pricing, creator dashboard, payer paywall UI, payment lifecycle transparency, and making the project production-ready for the Lepton hackathon. Knows the full current architecture and relevant references. Make sure to use this skill whenever the user mentions Lenspay, lenspay, pay-before-access, Immich micropayments, Arc Testnet USDC, x402 payment lifecycle, or any Lepton/Canteen hackathon payment project — even if they don't explicitly name the project.
---

# Lenspay Builder

## Overview

This skill helps you build and improve **Lenspay**, a system that adds real USDC micropayments in front of Immich shared links. It also covers the companion **circle-agent** TypeScript app that traces and visualizes the x402 payment lifecycle.

The project comprises **two sub-projects**:

| Project | Stack | Purpose |
|---------|-------|---------|
| **lenspay** | Python 3.9+, FastAPI, httpx, SQLite | Reverse-proxy sidecar that gates Immich shared links behind USDC micropayments |
| **circle-agent** | Node.js 20+, Express, viem, `@circle-fin/x402-batching` | Explainer companion: paywalled server + browser UI that visualizes the full x402 payment lifecycle |

## Core Architecture Knowledge

### Lenspay (Python Backend)

**Backend (Python + FastAPI)** — `src/lenspay/`
- `api.py` — FastAPI app; catch-all route `/s/{share_id}{path}`; checks payment → proxies to Immich via `httpx.AsyncClient` streaming; serves paywall (`/paywall/{share_id}`) and creator dashboard (`/creator-dashboard`, `/api/dashboard`); per-IP token-bucket rate limiter; optional basic-auth
- `payment.py` — `pay(url, share_id, price_usdc)` with idempotency (checks SQLite before calling ARC CLI); parses CLI output (JSON or plain-text)
- `arc_runner.py` — subprocess wrapper for ARC CLI (`arc pay ... --private-key`)
- `config.py` — Pydantic `BaseSettings`; reads from `.env` or env vars; private key from file or env var (never logged)
- `transaction_store.py` — Thread-safe SQLite singleton; `transactions`, `share_prices`, and `creator_settings` tables; supports idempotency, per-share pricing, creator wallet storage

**Key endpoints:**
- `GET /s/{share_id}[/path]` — Main paywall proxy (redirects browsers to paywall, proxies after payment)
- `GET /paywall/{share_id}` — Friendly paywall page (React build or fallback HTML)
- `GET /creator-dashboard` — Creator dashboard (React app)
- `GET /api/dashboard` — JSON with earnings, per-share stats, recent transactions
- `POST /creator/prices` — Set custom price per share
- `POST /creator/wallet` — Save creator EVM wallet address
- `POST /api/pay/{share_id}` — Record on-chain USDC payment from browser
- `GET /api/price/{share_id}` — Get effective price + payment status for a share

### Circle-Agent (TypeScript Companion)

**TypeScript Express server** — `circle-agent/`
- `server.ts` — Express server with `createGatewayMiddleware` from `@circle-fin/x402-batching`; paywalls `/hello-world` at $0.01 USDC; proxies to Circle Gateway API and ArcScan explorer
- `decode-batch.ts` — On-chain `submitBatch()` decoder using viem; fetches Arc Testnet tx, decodes calldata word-by-word, infers buyer→seller net transfers, heuristically matches off-chain settlement UUIDs
- `buyer.ts` — CLI buyer script using `GatewayClient.pay()`
- `public/buyer.html` — Browser UI that walks through the 6-step x402 payment lifecycle

**The x402 Payment Lifecycle:**
```
Step 1: Buyer signs EIP-712 TransferWithAuthorization (off-chain, no gas)
Step 2: Merchant middleware POSTs to Circle facilitator → settlement UUID
Step 3: Settlement queued (status: "received", balance optimistically debited)
Step 4: Circle relayer batches multiple payments (~10 min on testnet)
Step 5: On-chain submitBatch(calldataBytes, signature)
Step 6: Settlement marked "completed" (updatedAt ≈ block timestamp ±2s)
```

## Key Technical Decisions

- **Real on-chain USDC payments on Arc Testnet** — not mock (except demo mode)
- **Creator connects wallet** → that address receives payments
- **Per-share custom pricing** stored in SQLite (with sensible default in `.env`)
- **Idempotency** via transaction records — same share_id never charged twice
- **ARC CLI as subprocess** — simple but requires `arc` on `$PATH`
- **Zero-touch Immich integration** — sidecar pattern, no Immich source code changes needed
- **Friendly UI** for both creators and payers (React + Tailwind)

## When to Use This Skill

Use this skill when you need help with:

- Implementing or debugging real MetaMask + USDC payments on Arc Testnet
- Designing or improving the creator dashboard (wallet connection + price management + earnings view)
- Improving the payer paywall UI (states, friendliness, wallet connection flow, payment confirmation)
- Making architectural decisions (backend vs frontend payment logic, proxy flow, idempotency)
- Adding features like transaction history, earnings aggregation, per-share analytics
- Implementing or debugging the x402 payment lifecycle (EIP-712 signing, settlement, batch decoding)
- Working with the circle-agent decode-batch.ts on-chain transaction decoder
- Preparing the project for hackathon submission (traction, demo flow, documentation)
- Understanding how to get real usage and distribution

## Instructions

When helping with Lenspay or circle-agent:

1. **Always consider real usage and traction** — The Lepton hackathon heavily values genuine payments flowing and real people using the project. Prioritize features that help get real users and real transactions.

2. **Prioritize simplicity + friendliness** — Both the creator dashboard and payer paywall should feel clean and approachable. Assume users may be non-technical. Error messages should be human-readable, not raw hex or stack traces.

3. **Focus on real Arc Testnet payments** — Use viem/wagmi for wallet connection and real USDC transfers. Avoid mocks when possible. When debugging, check that the user has actual Arc Testnet USDC (from the Circle faucet).

4. **Support per-share pricing** — Creators should be able to set different prices for different share_ids, with a sensible default. The `POST /creator/prices` endpoint handles this; the creator dashboard should expose it clearly.

5. **Maintain clean separation**:
   - Backend handles proxy logic, price checking, and transaction storage
   - Frontend handles wallet connection and user interaction
   - The paywall frontend should call `/api/pay/{share_id}` after the on-chain transfer completes

6. **When suggesting code**, prefer practical solutions that can be implemented quickly while still being production-minded. Reference existing files in the project rather than reinventing them.

7. **For circle-agent work**, understand the x402 lifecycle intimately:
   - The Gateway middleware (`@circle-fin/x402-batching/server`) handles EIP-712 authorization
   - Settlement UUIDs bridge off-chain authorization and on-chain batch settlement
   - `decode-batch.ts` uses a ±10s timestamp heuristic to match settlements to on-chain entries
   - The browser UI should walk users through all 6 steps with live links and status indicators

## Current Priorities (as of July 2026)

- Get real MetaMask + USDC payment flow working end-to-end (both lenspay and circle-agent)
- Improve creator experience (wallet connection + price setting + earnings visibility)
- Make payer paywall UI friendly and clear (connection states, loading, success, error)
- Ensure idempotency works correctly
- Improve the circle-agent browser UI for the 6-step payment lifecycle
- Prepare a solid demo and submission for the Lepton hackathon

Use this skill to move Lenspay from demo toward something genuinely usable.
