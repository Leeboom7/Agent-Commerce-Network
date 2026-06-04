# Demo Video Script — Agent Commerce Network

**Duration**: 2:50 (under Devpost 3-minute limit)
**Format**: Screen recording + English voiceover (Chinese subtitles optional)
**Tool**: OBS Studio (free) or Screen Studio

---

## 0:00–0:25 — HOOK: The Problem

| Time | Visual | Voiceover |
|------|--------|-----------|
| 0:00 | Black screen → text fades in: "What if AI agents could form their own economy?" | "Right now, if an AI agent needs a service from another agent, there's no standard way to discover it, negotiate a price, sign a contract, verify delivery, or resolve disputes." |
| 0:12 | Show CLI demo running: `python -m demo.competitive_analysis`. Qwen initialization line visible. | "The Agent Commerce Protocol solves this. 18 economic relationship types. Multi-round negotiation with game-theoretic strategies. Automated verification and arbitration. All powered by Qwen Cloud." |
| 0:22 | Cut to Next.js frontend — the neo-brutalist graph canvas. 5 agent nodes pulsing. | "Let me show you." |

## 0:25–1:10 — WALKTHROUGH: The Agent Economy in Action

| Time | Visual | Voiceover |
|------|--------|-----------|
| 0:25 | Click [RUN DEMO]. Scene advances to "SCENE 1: Agent Registration". 5 nodes appear with reputation scores. | "Five specialized agents register on the network: an Orchestrator, Data Analyst, Report Writer, Fact Checker, and Arbitrator. Each has a reputation score and transaction history." |
| 0:38 | Scene auto-advances to "SCENE 2: Service Discovery". Yellow dashed edges appear from Orchestrator to service agents. Floating "LIVE FEED" card pops in. | "The Orchestrator searches the registry and discovers three service providers. Prices and reputations are visible — the market is transparent." |
| 0:48 | Scene advances to "SCENE 3: Negotiation". Edges labeled with negotiated prices (67.80, 116.70, 37.50 NC). "NEGOTIATION" card shows offer/counter/accept rounds. | "Then agents negotiate. Not just prompt engineering — each agent uses a game-theoretic strategy: BATNA, Concession, Tit-for-Tat, Value-Based. Three bilateral negotiations reach agreement in real time." |
| 1:05 | Scene advances to "SCENE 4: Contract Signing". Edges turn solid black. "ACTIVE CONTRACTS" card appears. | "Agreed terms become signed contracts with machine-verifiable acceptance criteria — format checks, data thresholds, source citations." |

## 1:10–2:00 — THE DRAMA: Delivery, Error, Dispute, Resolution

| Time | Visual | Voiceover |
|------|--------|-----------|
| 1:10 | Scene advances to "SCENE 5: Delivery & Verification". DataAnalyst edge turns green [OK]. ReportWriter edge turns RED [FAIL]. | "Here's where multi-agent collaboration proves its value. The Data Analyst delivers perfectly — verified, accepted, paid. But the Report Writer's delivery contains factual errors." |
| 1:22 | "VERIFICATION RESULTS" card shows 2 errors found. | "The Fact Checker — an independent verification agent — catches two errors: an overstated market share claim and an incorrect release date. A single agent would never catch its own mistakes." |
| 1:35 | Scene advances to "SCENE 6: Dispute & Arbitration". Red dashed edge from Orchestrator to Arbitrator. "ARBITRATION CASE" card appears with ruling. | "The Orchestrator files a dispute. The Arbitrator reviews the evidence — the verification report, the contract terms, the factual errors — and rules: buyer upheld. The seller must revise, with a 10% penalty." |
| 1:50 | Scene advances to "SCENE 7: Settlement & Reputation". All edges colored. "SETTLEMENT LEDGER" card shows final payments. Reputation scores update. | "The seller revises and resubmits. Final settlement: 210 NC total cost. Reputation scores update — the Data Analyst and Fact Checker gain points, the Report Writer takes a hit. The market self-regulates." |

## 2:00–2:30 — PROOF: Single-Agent Baseline

| Time | Visual | Voiceover |
|------|--------|-----------|
| 2:00 | Cut to terminal: `python -m demo.single_agent_baseline`. Side-by-side comparison table appears. | "But does multi-agent collaboration actually help? Let's check the baseline. We ran the same task with a single agent — no specialization, no peer review, no independent verification." |
| 2:12 | Highlight the comparison metrics one by one. | "Single agent: 4 errors, 2 revisions, 320 NC cost, zero verifiability. Multi-agent: 2 errors, 1 revision, 210 NC — that's 50% fewer errors, 34% lower cost, and 100% independently verified output." |
| 2:25 | Show the CONCLUSION line. | "Specialization works. Independent verification works. Economic incentives work. This is not just a demo — it's a measurable efficiency gain." |

## 2:30–2:50 — CLOSE: Architecture + Impact

| Time | Visual | Voiceover |
|------|--------|-----------|
| 2:30 | Cut to architecture diagram (`docs/architecture.svg`). | "Under the hood: a modular Python protocol with 8 implemented relationship types, 4 negotiation strategies, automated verification, binding arbitration, and a reputation system with time decay and transitive trust." |
| 2:40 | Show Qwen integration: the `[QWEN] Qwen Cloud connected` line from the demo output. | "All agent reasoning is powered by Qwen Cloud — Qwen3.7-Max for negotiation and arbitration, Qwen3-Coder for code-related tasks. The protocol is model-agnostic but Qwen-native." |
| 2:47 | Show GitHub repo URL. | "Open source, MIT licensed, 145 tests. Built for the Qwen Cloud Global Hackathon — Track 3: Agent Society." |

---

## Recording Tips

1. **Screen resolution**: 1920x1080, no window decorations for the Next.js app
2. **CLI demo**: Use Windows Terminal with JetBrains Mono font, dark background
3. **Cursor**: Hide mouse cursor during recording, use click animations
4. **Audio**: Record voiceover separately, sync in post. Speak at 140-150 words/minute.
5. **Music**: Optional — subtle electronic/ambient background, very low volume

## Post-Production Checklist

- [ ] Trim to exactly 2:50
- [ ] Add English voiceover
- [ ] Add Chinese subtitles (optional but recommended for Qwen judges)
- [ ] Add GitHub URL overlay at the end
- [ ] Export as MP4, <500MB
- [ ] Upload to YouTube (unlisted) or directly to Devpost
