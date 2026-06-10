# Hackathon-Winning Demo Research

Date: 2026-06-05
Updated: 2026-06-09

This note records the demo strategy for Agent Commerce Network's Qwen Cloud Hackathon submission.

## Executive Judgment

The previous Agent Network Graph and Agent Commerce Theater were clearer than a static diagram, but they still read as "circles, lines, text cards." Track 3 needs more than a relationship map. Judges must see a process unfold:

1. Buyer Agent posts a valuable task.
2. Specialist agents receive work packages.
3. Seller agents quote prices.
4. Buyer counters and accepts.
5. Agreements lock terms.
6. Sellers execute and upload artifacts.
7. Verifier opens the artifact and checks claims.
8. Failed claims become a dispute case.
9. Arbitrator issues a ruling.
10. Ledger settles payment and reputation.
11. Baseline proof shows measurable gain.

The current direction is **Connector-First Agent Commerce App + Transaction Workbench**:

- Marketplace first: judges see purchasable `AgentService` cards before any abstract graph.
- Agent Profile second: judges see identity, capabilities, pricing, reputation, and external runtime metadata.
- Connector page third: judges see that ACN does not host every runtime; it coordinates external runtimes through REST/OpenAPI, agent cards, MCP metadata, and scoped API keys.
- Transaction Workbench fourth: judges run the Python demo through `POST /api/demo/run` and see protocol events, Qwen decisions, runtime monitor, settlement, and baseline metrics.
- Optional replay/theater surfaces may remain, but they are no longer the primary judging path.

The core design rule is: **every animation must correspond to a protocol event.** No decorative motion.

## External Findings

### 1. Judges may judge from submission materials alone

The Qwen Cloud Devpost rules indicate that judges can evaluate based on text, images, and video. The demo video is therefore a primary judging surface, not a supplement.

Source: [Qwen Cloud Devpost rules](https://qwencloud-hackathon.devpost.com/rules)

Implication:

- The UI must explain itself inside a 3-minute video.
- Screenshots should include negotiation, delivery, failed verification, dispute resolution, and final baseline proof.
- Do not rely on a spoken explanation to make the process understandable.

### 2. Track 3 requires process evidence

Track 3 asks for multiple agents with distinct capabilities to collaborate through task division, dialogue or negotiation, conflict resolution, and measurable efficiency gain over a single-agent baseline.

Source: [Qwen Cloud Devpost rules](https://qwencloud-hackathon.devpost.com/rules)

Implication:

- A graph is insufficient.
- Negotiation must show offer, counter, and accept.
- Delivery must show seller execution, artifact packaging, upload, and verifier review.
- Conflict resolution must show evidence transfer and ruling.
- The final scene must show measurable gain, not just a claim.

### 3. Qwen usage and technical depth matter more than visual polish alone

Qwen's official hackathon page lists Innovation & AI Creativity, Technical Depth & Engineering, Problem Value & Impact, and Presentation & Documentation as judging criteria.

Source: [Qwen Cloud Hackathon page](https://www.qwencloud.com/challenge/hackathon)

Implication:

- The UI should visibly expose Qwen-style reasoning moments.
- Until the API key is available, use a deterministic cached reasoning trace.
- After coupon/key arrival, add live Qwen calls for planner and arbitration rationale while preserving cached fallback for recording.

### 4. Devpost favors product screencasts

Devpost video guidance recommends showing what the app does through a clear screencast, with a fast elevator pitch, rehearsal, and edited dead time.

Sources:

- [Devpost video-making best practices](https://help.devpost.com/article/84-video-making-best-practices)
- [Devpost: 6 tips for making a winning hackathon demo video](https://info.devpost.com/blog/6-tips-for-making-a-hackathon-demo-video)

Implication:

- The video should show the actual UI replay, not a separate trailer.
- The most important shots are live negotiation, delivery/verification, dispute/ruling, and baseline proof.
- A visible console plus visual process board is stronger than cards alone because it communicates that agents are executing.

## Reference Pattern From Other Hackathon Demos

The useful pattern across strong agent hackathon submissions is not "more animation." It is **observable work**:

- AgentPlace-style marketplace demos show customer/contractor agents negotiating and tracking jobs end to end.
- BidBot-style negotiation demos show parallel agent calls, live call logs, and changing result cards.
- BountyBot-style task demos show post, agent attempts, comparison, and winner selection.
- Autopsy/AUTO-OPS-style operations demos show agent loops through a live console and timeline.

The shared lesson: judges understand faster when they can see the state machine running.

## UI Architecture

Use a multi-page product screencast optimized for recording:

```text
Marketplace
  AgentService cards for research, writing, verification, arbitration

Agent Profile
  external runtime type, connector status, endpointUrl, agentCardUrl, MCP endpoint, API scopes

Connectors
  platform boundary, REST/OpenAPI/MCP bridge, adapter loop, secret boundary

Transaction Workbench
  Qwen decision layer
  live protocol console
  commerce object timeline
  external runtime monitor
  settlement and baseline proof
```

## Qwen Strategy

Qwen must be visible in three core decisions:

- Planner: decomposes the buyer request into specialist work packages.
- Negotiation rationale: compares proposal price, reputation, delivery risk, and remedy terms.
- Arbitration rationale: reads agreement criteria, failed claims, evidence bundle, and remedy options.

When `QWEN_API_KEY` is absent, the UI must display `Qwen status: fallback`. When the key is present, `demo.web_api` attempts live Qwen calls and still keeps deterministic fallback for reliable recording.

## Animation Strategy

Use animations only for protocol causality:

- `task-split`: Buyer decomposes task into work packages.
- `offer-slide`: seller proposal enters negotiation.
- `counter-write`: buyer writes counteroffer terms.
- `accept-stamp`: proposal becomes accepted.
- `artifact-pack`: seller execution and packaging.
- `upload-flight`: artifact moves to buyer inbox.
- `claim-scan`: verifier scans acceptance criteria.
- `case-transfer`: dispute evidence moves to arbitrator.
- `ruling-stamp`: arbitrator issues remedy.
- `ledger-count`: settlement and reputation update.

Avoid:

- decorative particles;
- full-screen graph as the main visual;
- random layout;
- animation that does not represent a business state transition.

## Recommended Video Structure

Target: 2:45 to 2:55, English voiceover, optional Chinese subtitles.

- 0:00-0:20: hook and problem.
- 0:20-0:55: Buyer Agent decomposes task and discovers specialist services.
- 0:55-1:25: live offer, counter, accept, and agreement snapshot.
- 1:25-2:05: sellers execute, artifacts upload, verifier catches two failed claims.
- 2:05-2:25: dispute case enters arbitrator, ruling issued, ledger settles.
- 2:25-2:45: baseline proof cards.
- 2:45-2:55: architecture/Qwen/repo close.

## Acceptance Bar

The UI is good enough for submission only if:

- Silent viewing for 15 seconds makes it clear that a buyer agent is hiring specialist agents.
- The negotiation phase visibly shows at least offer, counter, and accepted states.
- The delivery phase visibly shows seller execution and artifact upload.
- The verification phase visibly shows a verifier opening/checking the artifact and catching failed claims.
- The dispute phase visibly shows evidence entering an arbitrator and a ruling coming out.
- The final proof visibly shows 50% fewer errors, 34% lower cost, and 100% verified output.

## Final Recommendation

Do not lead with the graph or theater. Demote it to an optional support view.

The winning demo should be:

- marketplace-first, because judges need to understand what is bought;
- connector-first, because the product direction is BYOA runtime integration rather than hosting every agent;
- execution-console backed, because judges need to see agents doing work;
- protocol-object based, because business state transitions are clearer than a graph;
- negotiation-visible, because Track 3 explicitly mentions dialogue and negotiation;
- conflict-centered, because disagreement resolution is a judging requirement;
- baseline-backed, because measurable gain is mandatory;
- Qwen-explicit, because Track 3 judging rewards technical depth and the sponsor stack.
