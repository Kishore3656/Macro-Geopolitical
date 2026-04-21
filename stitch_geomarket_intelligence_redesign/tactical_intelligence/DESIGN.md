# Design System Strategy: The Sovereign Intelligence Framework

## 1. Overview & Creative North Star
**The Creative North Star: "The Tactical Archive"**

This design system moves away from the "SaaS dashboard" aesthetic and toward a high-stakes, military-grade intelligence environment. The objective is to evoke the feeling of a sophisticated, encrypted terminal where every pixel is a deliberate piece of data. 

We achieve this through **"Monastic Brutalism"**: a marriage of stark, technical monospaced utility and the authoritative, archival elegance of serif typography. The layout rejects the standard 12-column grid in favor of **Intentional Asymmetry**. Heavy side panels anchor the experience, while the central workspace breathes through deep, ink-black voids. This is not just an interface; it is a proprietary tool for high-consequence decision-making.

---

## 2. Colors & Surface Architecture

The palette is a "Midnight Tonal Scale," designed to minimize ocular fatigue during long-duration surveillance while maintaining aggressive high-contrast "Amber" focal points.

### The "No-Line" Rule
Traditional 1px borders are a crutch. In this system, boundaries are established through **Tonal Shifts**. To define a section, transition from `surface_dim` (#111319) to `surface_container_low` (#191b22). This creates a "machined" look where components appear to be recessed or milled into the interface rather than pasted on top.

### Surface Hierarchy (The Layering Principle)
Treat the UI as a series of physical "intel folders" stacked on a dark desk:
- **Base Layer:** `surface_container_lowest` (#0c0e14) — The infinite void.
- **Navigation/Panels:** `surface_container` (#1e1f26) — The primary structural frame.
- **Data Cards:** `surface_container_high` (#282a30) — The active focus.
- **Hover/Interaction:** `surface_container_highest` (#33343b) — Immediate feedback.

### The "Amber Pulse" & Signature Textures
- **The Core Accent:** `primary` (#ffb867) is reserved for "Live" status and critical CTAs.
- **Signature Gradient:** Use a subtle vertical gradient from `primary_container` (#d4840a) to `on_primary_fixed_variant` (#673d00) for large-scale data visualizations or primary action buttons to add a "phosphor glow" reminiscent of vintage radar screens.

---

## 3. Typography: The Editorial Authority

The typographic system creates a tension between **Technical Precision** and **Archival Narrative**.

- **The Logo (Barlow Condensed):** Provides a compressed, industrial strength.
- **The Intelligence (Newsreader/Lora):** Serif is used for headlines and body text to provide an "Editorial/Intelligence Report" feel. It suggests that the data has been analyzed and curated, not just spat out by a machine.
- **The Data (Space Grotesk / IBM Plex Mono / JetBrains Mono):** Monospaced fonts are used for all labels, coordinates, and "Big Numbers." This ensures that numerical values align perfectly in columns, facilitating rapid scanning of fluctuating market data.

**Key Rule:** Never use Serif for data. Never use Mono for narrative.

---

## 4. Elevation & Depth: Tonal Layering

We do not use standard "Drop Shadows." They feel soft and consumer-grade. Instead, we use **Ambient Depth**.

- **The Ghost Border:** If high-density data requires containment, use `outline_variant` (#534435) at **15% opacity**. This creates a "whisper" of a line that disappears into the background.
- **Tactical Glass:** For floating command menus or tooltips, use `surface_container_high` with a **12px Backdrop Blur**. This maintains the "Military HUD" aesthetic, allowing the map or data beneath to remain partially visible.
- **Amber Gloom:** For "Live" indicators, use an `on_primary` outer glow with a 20px spread at 10% opacity, pulsing on a 2-second linear loop.

---

## 5. Components

### Buttons: Tactical Actuators
- **Primary:** Solid `primary_container` (#d4840a). 0px border radius. Typography: `label-md` (All Caps). 
- **Secondary:** Ghost-style. `outline` (#a08d7b) border at 20% opacity. Text color: `on_surface`.
- **States:** On hover, the button should not grow; it should "invert," switching the background and text colors instantly with no transition, mimicking a mechanical switch.

### Data Cards: The Intelligence Unit
- **Forbid Dividers:** Do not use horizontal lines to separate card content. Use **16px/24px/32px vertical steps** of white space.
- **Header:** Use a `surface_container_highest` (#33343b) top-bar (2px height) to indicate the card is "Active."

### Inputs: The Terminal Prompt
- **Style:** Underline only. Use `outline_variant` (#534435) as the base.
- **Focus:** The underline shifts to `primary` (#ffb867) with a "blinking cursor" in the label to reinforce the terminal aesthetic.

### Collapsible Panels: The Sliding Bellows
Side panels must use a **Cubic-Bezier (0.4, 0, 0.2, 1)** transition. They should feel heavy and hydraulic. When collapsed, they leave behind a "Tab Strip" using `IBM Plex Mono` vertical text.

---

## 6. Do’s and Don’ts

### Do
- **DO** use absolute zero (`0px`) border radius. Hard corners represent precision.
- **DO** use `JetBrains Mono` for all currency and coordinate values.
- **DO** allow for "Dead Space." High-end intelligence tools don't need to fill every corner; whitespace (or "dark space") signifies clarity of thought.
- **DO** use `tertiary` (#9dd3aa) for "Positive" market trends and `error` (#ffb4ab) for "Negative" alerts.

### Don’t
- **DON'T** use soft rounded corners (pill shapes). They undermine the "Military-Grade" promise.
- **DON'T** use standard blue for links. Use `primary` (Amber) or `secondary` (Silver).
- **DON'T** use 100% white (#FFFFFF). All "white" text should be `on_surface` (#e2e2eb) to prevent retina-burn in dark environments.
- **DON'T** use drop shadows to create depth. Use background color shifts.