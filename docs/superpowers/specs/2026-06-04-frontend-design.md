# ACP Frontend — Design Spec

**Date**: 2026-06-04
**Status**: Approved

## Context

The Agent Commerce Network has a complete Python backend (35 modules, 145 tests) but only a basic Streamlit dashboard. For the Qwen Cloud Hackathon submission, we need a frontend that makes the Agent Commerce Protocol **visually unforgettable**.

The design goal: an interface that feels like **watching an autonomous agent economy live** — not a SaaS dashboard.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Tech Stack | Next.js 14 + TypeScript + Tailwind + shadcn/ui | Production-grade, interview-recognizable |
| Visual Style | Neo-Brutalist | 3px black borders, offset shadows, primary colors. Most distinctive hackathon aesthetic |
| Interaction Model | Force-directed graph + floating cards | Agents as nodes, contracts as edges, info as draggable cards |
| Graph Library | @xyflow/react (React Flow) | Production-ready, customizable nodes/edges, built-in drag |
| API Integration | Next.js API routes → FastAPI backend | Clean separation, WebSocket for live events |

## Visual System

### Colors
- Background: #FFFDF7 (paper white)
- Card: #FFFFFF (pure white)
- Text Primary: #111111 (true black)
- Text Secondary: #555555 (dark gray)
- Accent Yellow: #FFE033 — highlights, negotiations, active state
- Accent Red: #FF5E5E — disputes, failures, penalties
- Accent Green: #22C55E — completed, verified, success
- Accent Purple: #7C3AED — info, arbitration
- Invert: #111111 — code blocks, protocol data

### Typography
- Headings/Labels: Space Grotesk (700 for headings, 500 for subtext)
- Protocol data/IDs: JetBrains Mono

### Signature Elements
- All cards: 3px solid black border + 5px offset black shadow
- Status pills: heavy border, solid color fill
- Tabs: borders connect/disconnect from content
- Node pulses on state changes

## Architecture

```
route: /                    → full app (single page canvas)
route: /api/agents          → agent list, reputation, status
route: /api/contracts       → active contracts
route: /api/negotiations    → negotiation sessions
route: /api/ledger          → transaction history
route: /api/demo/run        → trigger demo scenario (POST)
route: /api/ws              → WebSocket for live events
```

### Component Tree
```
App
├── Canvas (fullscreen React Flow)
│   ├── AgentNode[]          — circle, size=reputation, color=status
│   ├── ContractEdge[]       — line, style=relationship, animated
│   └── FloatingCards[]      — draggable, hard shadow
│       ├── RegistryCard     — agent list, online status
│       ├── FeedCard         — live event stream
│       ├── NegotiationCard  — bilateral negotiation view
│       ├── ContractCard     — state machine visualization
│       ├── ArbitrationCard  — case timeline
│       ├── LedgerCard       — transaction log
│       └── ReputationCard   — leaderboard
├── TopBar
│   ├── NetworkStatus        — "NETWORK: LIVE // 5 AGENTS"
│   ├── DemoControl          — [RUN DEMO] [PAUSE] [RESET]
│   └── SimClock             — simulated time
└── BottomDock
    └── MiniFeed             — scrolling protocol messages
```

### Floating Card Behavior
- Appearance: scale(0) → scale(1) spring animation, shadow 0→5px
- Dragging: follow mouse, shadow shifts directionally
- Dismissal: click X, scale(1) → scale(0.8) + fade
- Dispute pulse: border color #000 → #FF5E5E pulsing
- Stack: z-index by recency, last interacted on top

## Demo Flow

1. **Idle state**: 5 nodes softly pulsing on canvas
2. **User clicks [RUN DEMO]**:
   - Nodes rearrange (force simulation)
   - Edges appear as contracts form (gold dashed → solid)
   - Floating cards pop in sequence:
     a. RegistryCard — shows all 5 agents
     b. NegotiationCard — Data Analyst negotiation (offer/counter/accept)
     c. NegotiationCard — Report Writer negotiation
     d. NegotiationCard — Fact Checker negotiation
     e. ContractCard — 3 contracts go active
     f. FeedCard — verification events
     g. ArbitrationCard — dispute filed, ruling issued
     h. LedgerCard — payments processed
     i. ReputationCard — scores updated
   - Disputed node (ReportWriter) pulses red
   - Credit flow animations along edges
3. **End state**: All cards visible, network frozen in final state
4. **User can**: drag cards, click nodes, explore at will

## Implementation Plan

### Phase 1: Scaffold (Next.js project)
- Initialize Next.js 14 with TypeScript, Tailwind, shadcn/ui
- Configure Space Grotesk + JetBrains Mono fonts
- Set up global CSS with neo-brutalist base styles
- Create FastAPI backend routes in `api/` directory

### Phase 2: Graph Canvas
- Implement AgentNode component (circle, label, reputation ring)
- Implement ContractEdge component (line, status-dependent style)
- Set up React Flow with force layout
- Node click → info card popup

### Phase 3: Floating Cards
- Build draggable card wrapper (motion/react or custom)
- Implement each card: Registry, Feed, Negotiation, Contract, Arbitration, Ledger, Reputation
- Card animation system (enter, exit, drag)

### Phase 4: Demo Integration
- Wire up [RUN DEMO] button to FastAPI backend
- Sequence card appearances along demo timeline
- Implement PAUSE/RESET controls
- WebSocket for live event streaming

### Phase 5: Polish
- Responsive tweaks (focus on desktop — demo target)
- Loading states, error boundaries
- Build for production

## Verification

1. `npm run build` succeeds without errors
2. Frontend renders all 5 agent nodes + 3 contract edges after demo
3. All 7 floating cards appear in correct sequence
4. Cards are independently draggable
5. Neo-brutalist style is consistent (borders, shadows, fonts, colors)
6. Demo runs end-to-end: click RUN → see complete lifecycle → final state
