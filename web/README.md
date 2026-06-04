# ACP Frontend — Agent Commerce Network

Neo-Brutalist Next.js frontend for the Agent Commerce Protocol.
Force-directed graph visualization of the autonomous agent economy.

## Quick Start

```bash
npm install
npm run dev
# Open http://localhost:3000
```

## Tech Stack

- Next.js 16 + TypeScript
- Tailwind CSS 4 (neo-brutalist theme)
- React Flow (@xyflow/react) — graph canvas
- Space Grotesk + JetBrains Mono fonts

## Architecture

Single-page canvas app:
- **TopBar** — network status, demo controls [RUN|PAUSE|RESET]
- **Canvas** — React Flow with AgentNode (circle) + ContractEdge (line)
- **Floating Cards** — positioned overlay cards (registry, feed, negotiation, contract, arbitration, ledger, reputation)
- **BottomDock** — protocol version + hackathon info
- **7-scene Demo** — auto-advancing timeline through the full agent commerce lifecycle

## Build

```bash
npm run build
npm start
```
