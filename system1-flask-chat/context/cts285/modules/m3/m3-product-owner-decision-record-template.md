# M3 Product Owner Decision Record

## This record is normally generated for you

The **M3.5 — Product Owner Sprint Simulation** generates this decision record automatically after you complete both rounds — your initial release slice and your revised plan after the capacity/complication change. In the normal workflow, you do not write this file from a blank page — you copy the Markdown the simulation produces into `docs/decisions/m3-product-owner-decision-record.md`.

Use this template only if:

- your generated record is missing a section and you need to see what shape it should have, or
- your browser lost the simulation state (for example, localStorage was cleared) and you need to reconstruct the record from your own notes/memory of the decisions you made.

Do not use this template to invent decisions you did not actually make in the simulation. If you cannot reconstruct your decisions honestly, redo the simulation and generate a fresh record.

Replace all bracketed prompts with your own content and delete the brackets before submitting.

## Record contents

### Student
[Your name]

### Date completed
[Date]

### Simulation
M3.5 — Product Owner Sprint Simulation

### Purpose
Make a constrained portfolio selection and revise it under a changed capacity and release-critical requirement — different from individual item triage, and different from M2 evidence investigation.

## Round 1 — Initial release slice

**Capacity:** 13 effort points

List every candidate item and whether you included it in the release slice.

| Item | Value | Relative Effort | Dependency | Risk / Uncertainty | Included? | Reasoning |
|---|---|---|---|---|---|---|
| [Item name] | [High / Medium / Low] | [Smaller / Medium / Larger] | [Dependency or "None"] | [Risk/uncertainty note or "None"] | [Yes / No] | [Why this item belongs in — or was deferred from — the initial slice] |

[Add one row per candidate item. The simulation presents eight candidate items — list all eight, included or not.]

**Round 1 summary:** [1-3 sentences explaining the overall shape of your initial release slice and the biggest tradeoff you made to stay within 13 points.]

## Complication

**New capacity:** 10 effort points
**New constraint:** an accessibility defect becomes release-critical.

[State in your own words what this complication forced you to reconsider.]

## Round 2 — Revised release slice

List only the items whose inclusion changed, plus the release-critical item and any item you deliberately kept and want to defend.

| Item | Round 1 Status | Round 2 Status (Keep / Remove / Add / Still Defer) | Reasoning |
|---|---|---|---|
| [Accessibility defect item] | [Not included / Included] | Add | [Why this must be in the release now that it is release-critical] |
| [Item name] | [Included / Not included] | [Keep / Remove / Add / Still Defer] | [Why, given the reduced capacity and the new release-critical requirement] |

[Add one row per item whose status you reconsidered in Round 2.]

**Round 2 summary:** [1-3 sentences naming the specific tradeoff you made to fit the release-critical item into the reduced 10-point capacity.]

## Summary

[2-4 sentences: what does this decision record show about how you balance value, effort, dependency, risk, and capacity under a changing constraint? How does this compare to what backlog triage taught you about individual item readiness?]

## Final check

- [ ] All eight candidate items appear in the Round 1 table with an include/defer decision and reasoning.
- [ ] The complication (10-point capacity, release-critical accessibility defect) is stated in your own words.
- [ ] Round 2 shows a real tradeoff — something had to move, wait, or be removed to make room for the release-critical item.
- [ ] This file is saved as `docs/decisions/m3-product-owner-decision-record.md`, committed, and synced to GitHub.
