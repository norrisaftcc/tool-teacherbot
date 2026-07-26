# M0 — Asset-Slotting Notes

> **SKELETON ONLY.** Records intent and provenance; reconciles nothing;
> ports/moves/renames nothing. Per `_tracking/skeleton-plan.md` §3 and the
> layout spec's `nonClobberPolicy`: legacy `assignments/` is frozen this pass
> and is recorded here as a porting *source*, never edited or moved.

---

## Namespace note (read this first)

This scaffold was built at **`modules/m0/`**, not `assignments/m0/`. The
authoritative layout spec (mirrored in `_tracking/skeleton-plan.md`, dated
2026-07-24, "Status: Authoritative for the M0–M8 scaffolding fan-out") states:

> "Canonical spine skeleton lives in a NEW top-level `modules/` tree...
> Legacy `assignments/` is FROZEN this pass — a porting *source* only, never
> a scaffold target."

and its non-clobber rule (2): *"Never touch anything outside `modules/mN/`.
No builder creates, edits, moves, renames, or deletes any file under
`assignments/`..."*

The build request that launched this pass said to "scaffold `assignments/m0/`."
That instruction conflicts with the authoritative spec above. Per this
project's own operating principle — contracts are law; if one seems wrong,
file the issue with the spine owner, never fork the interface locally — this
build followed the authoritative `modules/m0/` location instead. It flags the
conflict here rather than silently complying with either side.
**No files were created, edited, or touched under `assignments/m0/`.** If the
spine owner intends `assignments/m0/` to be the real target after all, that is
a namespace ruling (open question 2 in `_tracking/skeleton-plan.md`). This pass
should not resolve that unilaterally by writing there.

---

## Asset-slotting table

| Asset | Tag | Slots into | Note |
|---|---|---|---|
| `assignments/m0/01_workspace_setup.md` | `PORT` | M0 Apply/Learn | Legacy tutorial: Codespaces setup, customization, first compile. Content already matches spine M0's Apply beat closely. Stays exactly as-is on disk (frozen); port operation (copy/adapt into a real M0 Apply-beat file under `modules/m0/`) is a deep-build-pass action, not this skeleton pass. |
| `assignments/m0/02_first_pull_request.md` | `DO NOT PORT` (frozen provenance) | — (superseded) | **RESOLVED Q4 (A+C):** not ported. Deep-build authors a fresh **Mail-Run M0 lab** (commit/push + Postmark Rule, no PR); the fork/branch/PR walkthrough relocates to the **M8 capstone**. See "Numbering flags" #1 below. |
| `assignments/m0/README.md` | *(legacy, not ported)* | — | Legacy module overview. Per non-clobber rule 3, stays exactly as-is; the canonical overview is `modules/m0/_overview.md`, not a replacement for this file. Note: this README's own "Next Module" link points to `../m1/` framed as "Variables and Basic I/O" — that is the drifted numbering (legacy `assignments/m1` = spine M3 content, per `_tracking/numbering-reconciliation-map.md` row 6/manifest-delta). Recorded, not fixed — out of scope for this module's skeleton. |
| Chapter 1 — Introduction to C++ Programming (partial) | `PORT` | M0 Learn | Per spine asset table (`_storming/CSC-134-course-spine.md` line 359: "Chapter 1 — Intro to C++ → M0 (partial)") and spine's own M0 "Assets" line (line 114). Physical source file not located under `assignments/m0/`; likely lives in `_past_work/` — deep-build pass should confirm exact path before porting. |
| Toolchain guidance | `PORT` | M0 Apply | Per spine's M0 "Assets" line ("toolchain guidance"). Likely overlaps with `01_workspace_setup.md` above — deep-build pass should confirm whether these are the same asset or two. |
| M0 Assess rubric shape | `CONTRACT` | M0 Assess | Inherits `_contracts/rubric-template.md` (four columns × four tiers) — instantiated (as a stub) in `_assess-spec.STUB.md` in this folder. |

---

## Legacy-content ledger

Content on disk under a drifted/legacy number that this module's deep-build
pass should be aware of:

- **`assignments/m0/*`** (all three files) — legacy numbering here **already
  matches** spine M0 per `_tracking/numbering-reconciliation-map.md` row 11's
  reconciliation logic (M0 is the one legacy folder that isn't part of the
  M1/M2/M3 drift — see that map's rows 1–11 and its manifest-delta table).
  No renumbering is needed for this folder; the only open item is the
  PR-workflow content mismatch flagged below, which is a *workflow-convention*
  finding, not a numbering one.
- No other drifted content elsewhere in the repo has been identified as
  destined for M0. (Compare: `assignments/m1/*` and `assignments/m2/*` are
  spine-M3 content, not M0 — recorded for M3's own `_assets.md`, not repeated
  here.)

---

## Numbering / reconciliation flags

1. **`assignments/m0/02_first_pull_request.md` vs. ADR-004.** Flagged in
   `_tracking/numbering-reconciliation-map.md` row 10 and restated as open
   question 5 in `_tracking/skeleton-plan.md`. The file teaches
   fork → branch → commit → PR to students in their first module; ADR-004's
   student flow is commit + push directly, no branches, no PRs before the
   capstone. **RESOLVED (2026-07-24, Q4 ruling — A+C):** do NOT port this file.
   The legacy file stays frozen provenance (ADR-008). Deep-build **authors a
   fresh Mail-Run M0 lab** in `modules/m0/` — pull → commit → push, framed with
   the Postmark Rule ([[ADR-007-postmark-rule]]) and the Mail Run
   ([[ADR-006-mail-run-and-import-direction]]), no branch and no PR (ADR-004
   student flow). The branch/PR walkthrough content is **not discarded — it
   relocates to the M8 capstone**, where branching is an age-appropriate
   capstone-tier skill. Applies existing ADRs (004/006/007/008); no new ADR.
2. **Namespace conflict** between this task's literal instruction
   ("scaffold `assignments/m0/`") and the authoritative
   `_tracking/skeleton-plan.md` / layout-spec ruling (`modules/m0/` is
   canonical, `assignments/` is frozen). Resolved in favor of the
   authoritative spec for this build — see "Namespace note" above. Flagging
   for the spine owner in case the launching instruction reflects an intended
   supersession of `skeleton-plan.md` that this pass wasn't told about
   explicitly.
3. **Chapter 1 (Intro to C++) exact file path** unconfirmed — spine cites it
   as an M0 asset but it was not found under `assignments/m0/` in this pass.
   Deep-build pass should locate it under `_past_work/` before treating it as
   ready to port.
