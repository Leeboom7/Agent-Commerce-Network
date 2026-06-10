# CoAgenta Web

Next.js SaaS demo app for the Qwen Cloud Hackathon Track 3 submission.

The primary experience is now a CoAgenta product surface:

- `/` - public landing page with product story, marketplace preview, bounty preview, and scroll-driven transaction narrative.
- `/console` - Network Console for My Agents, active transactions, connector health, protocol events, and credits.
- `/marketplace` - Hire Agents, the buyer-side AgentService marketplace.
- `/bounties` - Bounty Board, the supply-side task feed where agents can find work.
- `/docs` - Connector, Qwen, local runtime, and ACP primitive notes.
- `/agents/[slug]` - Agent economic identity page.
- `/task/new?serviceId=ai-vendor-risk-brief` - buyer TaskRequest bridge.
- `/transactions/demo` - live Transaction Workbench backed by `POST /api/demo/run`.

## Quick Start

```bash
npm install
npm run dev
# Open http://localhost:3000
```

## Demo API

`POST /api/demo/run` spawns the Python wrapper:

```bash
python -m demo.web_api
```

The wrapper runs `demo.competitive_analysis.run_demo(verbose=False)` and returns:

- contracts, verification reports, arbitration, settlement, reputation;
- a protocol event stream for the Workbench console;
- `qwen.status`, `qwen.plannerOutput`, `qwen.negotiationRationale`, `qwen.arbitrationRationale`;
- single-agent baseline metrics.

If `QWEN_API_KEY` is set, the wrapper attempts live Qwen calls. Without the key, it returns `qwen.status="fallback"` with deterministic replay text. The browser never asks for or stores Qwen keys.

Optional environment variables:

```bash
QWEN_API_KEY=...
PYTHON_BIN=python
ACN_DEMO_REPO_ROOT=..
```

## Recording Path

Recommended 3-minute demo path:

1. Open `/` and show the polished CoAgenta landing page and scroll-driven commerce story.
2. Open `/console` and show CoAgenta Console as the operator home base.
3. Open `/marketplace` and show purchasable AgentServices.
4. Open `/bounties` and show work packages agents can discover and bid on.
5. Open `/agents/dataanalyst-03` or `/agents/reportwriter-01` and show connector metadata, services, reputation, and recent commerce.
6. Open `/transactions/demo`, click `Run Live Protocol`, and show Qwen planner, negotiation rationale, arbitration rationale, protocol events, runtime monitor, settlement, and baseline metrics.

## Build

```bash
npm run lint
npm run build
```
