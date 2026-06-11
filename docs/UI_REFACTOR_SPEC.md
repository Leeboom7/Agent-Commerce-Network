# CoAgenta UI Refactoring Spec: Infrastructure Grade

**Date**: 2026-06-11
**Target Maturity**: Linear / Vercel / Stripe (High-Density, High-Precision Infrastructure)

## 1. Vision & Core Metaphor
The current CoAgenta UI leans towards a warm, soft, "lifestyle SaaS" aesthetic (oat/cocoa colors, pill-shaped headers, soft drop shadows, floating cards). This contradicts the core product offering: an **Agent Commerce Network** involving contracts, arbitration, verification, and ledger settlements. 

To achieve the "Top-Tier SaaS" feel, we must pivot the metaphor from a "friendly cafe" to an **"infrastructure-grade financial/dev terminal"**. It needs to feel fast, deterministic, rigorous, and completely trustworthy.

### Keyword Shifts:
*   **From:** Warm, Floating, Friendly, Spacious, Decorative.
*   **To:** Cool/Neutral, Grounded, Precise, Dense, Functional.

---

## 2. Competitive UI Analysis (The Baselines)

### Linear
*   **Strengths:** Absolute grid adherence, lack of arbitrary floating elements, ultra-high information density without feeling cluttered.
*   **Takeaway for CoAgenta:** Ditch the enormous "fat cards" for Agents and Bounties. Move towards tight lists (table-row-like cards) with strict left-to-right reading order. Badges, IDs, and statuses should be ultra-compact.

### Vercel
*   **Strengths:** The "developer-first" pristine black-and-white look. Minimalist borders (`1px solid #eaeaea`), deep focus on state visibility (tiny colored dots for status), flat design with very subtle inner shadows on buttons to provide tactility. 
*   **Takeaway for CoAgenta:** Replace colored backgrounds with pure white or `zinc-50`. Use 1px borders everywhere to create structure instead of relying on shadows. Make primary buttons sharp and confident (pure black or strict blue).

### Stripe Dashboard
*   **Strengths:** Unparalleled typography hierarchy, tabular numerals for currency/numbers, exceptional micro-interactions.
*   **Takeaway for CoAgenta:** Whenever dealing with "NC credits", prices, dates, or IDs (e.g., `DataAnalyst-03`), we MUST use a Monospace font with tabular alignment. This instantly signifies "financial grade".

---

## 3. The New Visual Foundation

### 3.1 Color Palette (Tailwind v4 Setup)
We are stripping out the `--cg-oat`, `--cg-honey-cream`, and `--cg-cocoa` variables. We will adopt a strict grayscale palette with one piercing accent color.
*   **Background (App):** `#FAFAFA` (Zinc-50) – A clinical, clean canvas.
*   **Surface (Cards/Panels):** `#FFFFFF` (Pure White)
*   **Borders:** `#E4E4E7` (Zinc-200) – Used heavily to define all boundaries.
*   **Text Primary:** `#18181B` (Zinc-900)
*   **Text Secondary:** `#71717A` (Zinc-500)
*   **Text Tertiary/Placeholder:** `#A1A1AA` (Zinc-400)
*   **Status Colors (Muted but crisp):**
    *   *Verified/Success:* Green-600 (`#16A34A`), bg: Green-50 / Border: Green-200
    *   *Dispute/Danger:* Red-600 (`#DC2626`), bg: Red-50 / Border: Red-200
    *   *Pending/Warning:* Amber-600 (`#D97706`), bg: Amber-50 / Border: Amber-200
    *   *System/Protocol:* Indigo-600 (`#4F46E5`), bg: Indigo-50 / Border: Indigo-200

### 3.2 Typography
*   **Heading Font:** Can remain *Space Grotesk* for brand identity (Landing Page H1s), but must decrease tracking (`tracking-tight`) to look sharper. Inside the Console, consider a more neutral font like *Inter* or *Geist/Geist Sans* if available.
*   **Data Font (CRITICAL):** *JetBrains Mono* or *Geist Mono*.
    *   *Usage Rule:* Every single Agent ID, Contract hash, price (250 NC), timestamp, status badge, and parameter key MUST be in this monospace font. It immediately elevates the "developer tool" feel.

### 3.3 Shape & Geometry (Borders & Shadows)
*   **Corner Radius (Border Radius):** Move from abstract circles (`rounded-full`) to precise geometry. 
    *   Buttons: `rounded-md` (6px) or `rounded-lg` (8px). 
    *   Cards: `rounded-xl` (12px).
*   **Drop Shadows:** Eliminate large offset blur shadows (`var(--cg-shadow)`). Replace with:
    *   Card Default: Pure 1px border, NO shadow.
    *   Card Hover/Interactive: `shadow-sm` (0 1px 2px rgba(0,0,0,0.05)) + slight negative Y transform (`-translate-y-[1px]`).
    *   Modal/Dropdowns: `shadow-xl` with a 1px border ring.
*   **Inner Shadows (The SaaS Polish):**
    *   Primary Buttons (Black): `box-shadow: inset 0 1px 0 rgba(255,255,255,0.15);` (Gives it a crisp, 3D machined edge).
    *   Secondary Buttons (White): 1px border + `box-shadow: 0 1px 2px rgba(0,0,0,0.05);`

---

## 4. Component Refactoring Guidelines

### 4.1 The Navigation (Navbar)
*   **Old:** Floating horizontal pill (`.cg-header`). Looks like a Dribbble shot, not a real tool.
*   **New:** Full-width header spanning 100% of the viewport. `bg-white/80`, `backdrop-blur-md`, with a sharp `border-b border-zinc-200`.

### 4.2 Data Cards & Service Listings (Marketplace / Bounties)
*   **Old:** Tall, chunky cards with lots of empty space.
*   **New:** High-density rows.
    *   Layout: Flex-row. Left side contains the icon and name. Middle contains tags (Mono font). Right side contains the Price and CTA.
    *   If using cards (grid), make them squat and wide. Title on top, rigid horizontal separator (`border-t`), meta data on bottom.

### 4.3 Tags & Badges
*   **Old:** Big pill shapes, rounded-full.
*   **New:** Tiny, sharp, `rounded-md`. Size `text-xs`. Font `font-mono`. Example: `<span class="inline-flex items-center px-1.5 py-0.5 rounded-md border border-zinc-200 text-zinc-600 bg-zinc-50 font-mono text-xs">verified</span>`

### 4.4 Dashboards / Console
*   Do not let the content float in an infinite background. Use an outer container with a 1px border and a subtle gray background (`bg-zinc-50`) to frame the workspace, creating a clear "stage" for the data.

---

## 5. Execution Plan (Phased Steps)

1.  **CSS & Configuration Purge (`globals.css`)**
    *   Delete the `.cg-*` warm variables.
    *   Implement the strictly typed Tailwind v4 inline theme mappings for the new grayscale/mono palette.
    *   Define structural base CSS (body background to `zinc-50`).
2.  **Layout Reset (`layout.tsx`, Components)**
    *   Rewrite the `<AppHeader>` to be a full-width structured top bar.
    *   Adjust main container constraints (standardize `max-w-6xl` or full-width with padding).
3.  **Component Upgrades (`src/components/ui/`)**
    *   Update `Button`, `Card`, and `Badge` abstractions to use the new border logic and typography.
4.  **Page-by-Page Density Refactor**
    *   `app/page.tsx` (Landing): Sharpen typography, use tighter layout grids.
    *   `app/marketplace/...` & `app/bounties/...`: Convert chunky cards into rigorous data lists or dense grid items.

---
*Prepared as the blueprint for the UI code overhaul.*