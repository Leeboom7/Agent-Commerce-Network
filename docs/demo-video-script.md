# Demo Video Script - CoAgenta

**Duration**: 2:45-2:55
**Format**: product screencast + concise voiceover
**Core message**: CoAgenta is the commerce layer for autonomous agents. It does not host every runtime; it lets external buyer, seller, verifier, and arbitrator agents transact through AgentServices, connectors, protocol objects, Qwen reasoning, verification, dispute resolution, settlement, and reputation.

## 0:00-0:25 - Product Hook

| Time | Visual | Voiceover |
|------|--------|-----------|
| 0:00 | Open `/`. Show the landing hero and product UI frame. | "What if autonomous agents could connect, hire each other, verify work, and settle value?" |
| 0:08 | Scroll through the commerce story: connect, negotiate, verify, settle. | "CoAgenta turns agent collaboration into a structured economic loop, not a chat transcript." |
| 0:18 | Open `/console`. Show My Agents, active deals, connector health, and credits. | "The operator sees the whole agent network from one SaaS console." |

## 0:25-0:55 - Marketplace and Agent Profile

| Time | Visual | Voiceover |
|------|--------|-----------|
| 0:25 | Open `/marketplace`. Show purchasable AgentService cards. | "Hire Agents is the buyer-side marketplace for external agent services." |
| 0:35 | Open `/agents/dataanalyst-03`. | "Each agent has an economic identity: capabilities, pricing, reputation, connector status, and commerce history." |
| 0:47 | Highlight endpointUrl, agentCardUrl, MCP endpoint, API scopes. | "The runtime is external. CoAgenta coordinates commerce through connector metadata and scoped permissions." |

## 0:55-1:10 - Bounty Board

| Time | Visual | Voiceover |
|------|--------|-----------|
| 0:55 | Open `/bounties`. Show budget, deadline, criteria, proposal count. | "The other side is the Bounty Board: connected agents can discover work and submit proposals." |
| 1:04 | Point to verification requirements and matched agents. | "Every bounty can carry acceptance criteria and verifier expectations before work starts." |

## 1:10-2:25 - Transaction Workbench

| Time | Visual | Voiceover |
|------|--------|-----------|
| 1:10 | Open `/transactions/demo` and click `Run Live Protocol`. | "Now we run the real Python demo through the Next.js API." |
| 1:18 | Show Qwen decision layer. | "Qwen is inside the agent society loop: planner output, negotiation rationale, and arbitration rationale." |
| 1:32 | Show console events: task request, planner, match, offer, counter, agreements. | "The buyer creates a TaskRequest, Qwen decomposes it, the marketplace matches specialist services, sellers offer, the buyer counters, and agreements are created." |
| 1:48 | Show external runtime monitor and artifact/verification events. | "External seller runtimes execute and submit artifacts. The verifier runtime flags two unsupported claims before buyer acceptance." |
| 2:05 | Show dispute and arbitration events. | "The buyer opens a DisputeCase, evidence goes to the arbitrator, and Qwen supports a buyer-upheld ruling with remedy terms." |
| 2:18 | Show settlement and baseline cards. | "The demo ledger settles NC credits and reputation. Compared with a single-agent baseline: 50 percent fewer errors, 34 percent lower cost, and 100 percent verified." |

## 2:25-2:55 - Close

| Time | Visual | Voiceover |
|------|--------|-----------|
| 2:25 | Briefly show terminal or repo. | "The open-source version demonstrates the protocol and connector-first architecture." |
| 2:38 | Return to Workbench Qwen/baseline view. | "For Qwen Cloud Track 3, this shows task division, negotiation, conflict resolution, and measurable gain over a single-agent baseline." |
| 2:50 | End on repo or Devpost title. | "CoAgenta: the commerce layer for autonomous agents. Powered by ACP under the hood." |

## Recording Checklist

- Record at 1920x1080 when possible; verify 1280x720 still reads clearly.
- Use this path: `/` -> `/console` -> `/marketplace` -> `/bounties` -> `/agents/dataanalyst-03` -> `/transactions/demo`.
- Do not imply live escrow or hosted runtimes. Payment is demo `NC` credits.
- If no Qwen key is available, keep `Qwen status: fallback` visible and say it is a deterministic fallback replay.
- Keep the last Workbench shot on the baseline metrics: `50% / 34% / 100%`.
