# AlgoCratic TA System: Design Guidelines

**Maintained by:** Design specialist
**Consumed by:** System 1 (`terminal.css`, templates)
**Workflow:** Designer updates this file → dev implements from spec

---

## Status

✅ Full mockup delivered — see `design/system1/` for source files

---

## Source Files

| File | Purpose |
|------|---------|
| `design/system1/colors_and_type.css` | All design tokens (colors, type, spacing, effects) — **source of truth** |
| `design/system1/kit.css` | All component styles (masthead, sidebar, chat, composer, doc panel) |
| `design/system1/app.jsx` | Top-level layout mockup |
| `design/system1/chat.jsx` | Chat thread + message components |
| `design/system1/sidebar.jsx` | Group switcher sidebar |
| `design/system1/doc-panel.jsx` | Bottom doc panel with tabs |
| `design/system1/chrome.jsx` | Masthead / classification banner |
| `design/system1/assets/af-a-eye.svg` | Brand mark (amber eye logo) |

**Implementation rule:** Copy `colors_and_type.css` and `kit.css` directly into `system1-flask-chat/static/css/`. Do not rewrite — implement HTML that uses the CSS classes defined there.

---

## Design Overview

**Two-mode system:**
- **Terminal Mode** (default): cream-on-navy, JetBrains Mono, 1px hard borders, CRT scan-line texture
- **Poster Mode** (accent): Bungee display + Yellowtail script + rainbow ROYGB extrusion

**Palette summary:**

| Role | Token | Value |
|------|-------|-------|
| Page background | `--ink` / `--bg` | `#0E1F33` (deep navy) |
| Card/raised surface | `--ink-raised` / `--bg-elev` | `#162A44` |
| Primary text | `--cream` / `--fg` | `#F4ECD2` |
| Secondary text | `--cream-soft` | `#E6DDC0` |
| Brand accent / CTA | `--amber` / `--accent` | `#E08236` |
| Success | `--moss` / `--success` | `#7BA15A` |
| Danger | `--rust` / `--danger` | `#A23A2C` |
| Info / links | `--teal` / `--info` | `#5DA9B4` |
| Borders | `--ink-muted` | `#3A4E68` |

**Typography:**

| Role | Font |
|------|------|
| Display / headings | Bungee (single-weight, uppercase) |
| Script accent | Yellowtail |
| Body / UI | Space Grotesk |
| Code / terminal | JetBrains Mono |

**Spacing:** 4px base scale — `--space-1` (4px) through `--space-9` (96px)

---

## Key Layout Components

### App Shell
```
.app (flex column, full viewport)
  .classification-banner  ← "AMBER CLEARANCE" pulsing rust bar
  .masthead               ← brand mark + breadcrumb + right controls
  .main (flex row)
    .sidebar              ← group switcher (280px fixed)
    .workspace            ← chat + optional doc panel
```

### Chat Region (`.chat`)
- `.chat__topbar` — group name, clearance tag, status pill
- `.chat__thread` — scrollable message list with `.msg` items
- `.composer` — message input with `>` prompt glyph, amber focus glow, send button

### Message Types
- `.msg--bot` — amber left border on bubble
- `.msg--user` — right-aligned, amber-tint background
- `.msg--instructor` — teal left border

### Sidebar (`.sidebar`)
- `.group-row` with `.mini-meter` token bar per group
- `.role-toggle` — Student / Instructor toggle
- `.activity` dot — green (active) or rust (alert)

### Admin View
Use `.group-row` cards from the sidebar component + `.doc-md` for conversation log rendering.

---

## Assets

| Asset | Path | Usage |
|-------|------|-------|
| Brand mark | `design/system1/assets/af-a-eye.svg` | Masthead + empty state |

---

## Notes for Dev

- **Do not use the old green-on-dark `#00ff41` palette** — that was a placeholder. Use the token system.
- The `.classification-banner` is the rust-red pulsing bar at the very top — required for AlgoCratic aesthetic.
- Buttons use `[ text ]` bracket wrapping via `::before`/`::after` on `.btn` — don't add brackets in HTML.
- CRT scan-line is applied via `body::before` in `colors_and_type.css` — it's automatic, no extra markup needed.
- All inputs get amber focus glow (`--glow-amber`) automatically via `kit.css` — no extra JS needed.
- The `.composer__prompt` renders the `>` glyph — put it before the textarea in HTML.
