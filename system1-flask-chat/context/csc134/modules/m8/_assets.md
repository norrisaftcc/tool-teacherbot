# M8 — Asset Slotting Notes

Records what slots into M8, per the spine (`_storming/CSC-134-course-spine.md`,
M8's "## M8 — Capstone Miniproject" section — which, unlike every earlier
module, has **no explicit "Assets:" line**) and F-001
(`_lore/findings/F-001-numbering-reconciliation.md` /
`_tracking/numbering-reconciliation-map.md`). **Records intent only —
nothing is moved, renamed, or edited by this pass.**

Tags: **PORT** (adapt an existing asset) · **NEW** (author fresh) ·
**CONTRACT** (build against a frozen `_contracts/` file).

---

## Spine asset table, tagged

The spine's own moduleIdentities summary calls M8 outright: **"NEW —
spec-only, builds on M7 structs/classes."** Unlike M0–M7, the spine's M8
section names no companion readings, no ported labs, no lineage program by
filename. Everything below is therefore either freshly authored, or an
inferred dependency on what an earlier module produces — not a named,
existing M8 asset.

| Candidate asset | Tag | Notes |
|---|---|---|
| Design-document brief (problem statement / user stories / spec / flowchart template) | **NEW** | No existing template found on disk during this scan (`find` for "design doc*", "capstone brief" returned nothing). Deep-build authors this fresh, reusing the user-story form and Mermaid-flowchart convention already taught since M1/M2 — not a new format, a new *use* of an existing one. |
| Git branching / PR walkthrough (relocated from legacy `assignments/m0/02_first_pull_request.md`) | **NEW** (fodder) | **Q4 ruling (A+C), 2026-07-24:** the fork/branch/PR content pulled out of M0 (where it violated ADR-004 student-flow) lands here — branching is a capstone-tier skill. Deep-build mines the legacy M0 file as fodder for an M8 branch/PR beat; the legacy file itself stays frozen (ADR-008). See `modules/m0/_assets.md` flag #1. |
| M7's evolved struct/class program (whatever "Room"/"Hero"/"Monster" — or student-renamed equivalent — artifact M7's Assess beat produces) | **CONTRACT** (indirect, unconfirmed) | The spine states M8 "builds on the structs and classes from M7" but names no specific file. This is a *dependency on M7's own Assess output*, not on a `_contracts/` file directly — flagged as CONTRACT-shaped because M8's Apply/Assess authors will need to know M7's actual finished shape before writing M8's design-doc brief, the same way M6/M7 needed `m5_menu.cpp`'s actual shape before refactoring/extending it. **Unconfirmed lineage** — same caveat M7's own `_assets.md` gave `m5_menu.cpp`: plausible, not locked. |
| `_contracts/m4_gatekeeper.cpp` / `_contracts/m5_menu.cpp` (canonical decision/loop program lineage) | **CONTRACT** | Not named in M8's spine section, but the `_contracts/README.md` states the lineage runs "M6 refactors it into functions; M7 extends it" — if M8's capstone brief offers the gatekeeper→menu lineage as one *example* problem domain (dungeon-themed, matching the running theme), it inherits this frozen program rather than forking it. Deep-build should confirm whether the brief points to this lineage as a sample/reference program or leaves the student's problem fully open — the spine's own framing ("the student is chosen, within a scope boundary TBD," per `_assess-spec.STUB.md`) suggests the latter, not a forced continuation of the exact gatekeeper program. |
| `_contracts/rubric-template.md` (four-column × four-tier rubric) | **CONTRACT** | Every M8 rubric (see `_assess-spec.STUB.md`) inherits this frozen interface, same as every other module. Do not fork it locally — file with the Spine Owner if it seems to not fit the capstone's process-artifact shape (design doc + staged build + defense, rather than a single fixed program). |
| Manifest `M08` entry, "OOP RPG" project (`assignments/m8/project-oop-rpg.md`) | **NEW** (legacy-adjacent) | Named `status: "planned"`, `notes: "A grade milestone"` in the stale `_tracking/course-manifest-csc134.yaml` (line 393–397). **Confirmed not a physical file** — `find` for "project-oop-rpg" and "capstone" returned zero hits anywhere in this repository. Plausibly the ancestor of an M8-shaped deliverable, but the manifest predates the current spine reorg (see "Legacy-content ledger" below) and its whole `M08` entry is titled "Introduction to OOP," which the numbering-reconciliation map splits mostly into M7, not M8. |
| Manifest `M08` entry, "Capstone: Portfolio Defense" (`assignments/m8/capstone-portfolio.md`) | **NEW** (legacy-adjacent) | Named `status: "planned"`, `notes: "Badge requirement"` in the same stale manifest entry (line 399–403). **Confirmed not a physical file** — same zero-hit search result as the row above. Of the manifest's full 8-deliverable `M08` list, this is the one entry whose name ("Capstone," "Portfolio Defense") most plausibly belongs at spine-M8 rather than spine-M7 — its "Badge requirement" note also lines up with the rubric-template's Badge tier being "documentation/reflection above and beyond," a natural fit for MLO 8.4's presentation/defense requirement. Still unconfirmed; a builder call, not decided here. |

---

## Legacy-content ledger (F-001)

**Like M7, M8 has no legacy `assignments/mN/` folder collision to record.**
As of this scan, `assignments/` contains only `m0/`, `m1/`, and `m2/` — there
is no `assignments/m8/` (nor `m3/`–`m7/`) holding drifted content under this
module's own number on disk. M8's asset problem is not "content sitting
under the wrong folder number"; it is "the stale course manifest names two
project-shaped deliverables under a manifest module (`M08`) whose *title*
doesn't match the spine's M8 at all, and neither deliverable exists as a
file yet" — confirmed by direct search (`find . -iname "*capstone*" -o
-iname "*project-oop*"` returned zero hits under any path in this repo).

| Named asset | Expected legacy home (if any) | Status |
|---|---|---|
| Design-document brief/template | None found | Not-yet-authored (NEW, no legacy source) |
| `project-oop-rpg.md` (manifest `M08`) | `assignments/m8/` per the manifest's own `file:` field — but `assignments/m8/` does not exist | Not-yet-imported (F-001); manifest's `M08` title mismatches spine-M8, see below |
| `capstone-portfolio.md` (manifest `M08`) | `assignments/m8/` per the manifest's own `file:` field — but `assignments/m8/` does not exist | Not-yet-imported (F-001); manifest's `M08` title mismatches spine-M8, see below |

This ledger **records** the absence and the mismatch. It does not author
replacement content, and it does not search outside this repository (e.g.,
an instructor's local drive or an LMS) — that search, if needed, is a
deep-build task.

### Pending reconciliation — do not resolve here

- **Manifest `M08` ("Introduction to OOP") is not the same module as spine
  M8 ("Capstone Miniproject").** Per `_tracking/numbering-reconciliation-map.md`
  §2: "Classes/OOP half → M7 (struct→class arc). Capstone-shaped deliverables
  (`project-oop-rpg`, `capstone-portfolio`) → M8 Capstone, but M8's actual
  shape is 'design doc before code,' not a reading+lab+project ladder."
  Meaning: **six of the manifest's eight `M08` deliverables** (the reading,
  the two tutorials, the two "First Classes"/"Class Relationships" labs)
  belong to **M7**, not this module — see M7's own `_assets.md`, which
  already flags this split from its side. Only the two project-shaped
  entries above plausibly belong here, and even those don't match spine-M8's
  actual required shape (a design-doc-gated, staged, self-authored capstone,
  not a pre-titled "OOP RPG" project brief). Deep-build should treat the
  manifest's two `M08` project entries as, at most, thematically suggestive
  prior art — not a ready-to-port spec.
- **F-001's open AI-permission-line question** (spine, AI collaboration
  policy section: "currently permitted-and-logged on labs; formally owned at
  the capstone (Assess)... to be pinned down in the AI ladder companion
  doc") lands squarely on M8's Badge tier and MLO 8.4. This is a scope/policy
  ruling, not an asset-numbering fix, but it directly blocks
  `_assess-spec.STUB.md`'s Badge-tier row from being finalized — flagged
  here because it is the single biggest open dependency for this module's
  deep-build.
- **Whether ADR-004's "no branches" student-flow rule holds through M8, or
  whether the capstone is where student branching is deliberately
  introduced,** given the spine's own parenthetical calling branching "a
  capstone-tier topic (M8), out of alpha depth" elsewhere in the build
  materials. `_assess-spec.STUB.md`'s Submission-column row flags this as
  TBD; it is not decided here.

---

## Numbering flags for the Spine Owner

1. **Task-instruction / layout-spec conflict, surfaced during this build
   (same pattern already flagged by M7's `_assets.md`).** This scaffold pass
   was instructed to "Scaffold `assignments/m8/`," but the authoritative
   layout spec states plainly that canonical scaffolds land in `modules/mN/`
   and that "legacy `assignments/` is frozen and never a scaffold target."
   The precedent already on disk (`modules/m0/` through `modules/m7/`, each
   built the same way) confirms the layout spec, not the shorthand
   instruction, is load-bearing. **This pass built `modules/m8/`, matching
   the existing canonical tree and the layout spec, and did not create or
   touch any `assignments/m8/` path.** Flagging again since this is now the
   second consecutive module build to receive the same mismatched
   instruction — worth fixing the instruction template upstream rather than
   re-flagging per module.
2. **Manifest `M08`'s title ("Introduction to OOP") and most of its
   deliverables do not describe spine-M8 at all** — they describe spine-M7
   content, per the numbering-reconciliation map's own finding (§2, already
   cross-referenced in M7's `_assets.md`). Only 2 of the manifest's 8 `M08`
   entries (`project-oop-rpg.md`, `capstone-portfolio.md`) are even
   plausible candidates for this module, and neither is confirmed to match
   spine-M8's actual required shape (design doc before code, staged build,
   presentation/defense). This needs the same manifest-rebuild ruling the
   reconciliation map already calls for — not re-litigated here, just
   reaffirmed from M8's side of the split.
3. **M8 is the first (and only) module in the spine with no named
   companion assets at all** — no ported reading, no ported lab, no
   contract-lineage program named directly in its own spine section. Worth
   the Spine Owner confirming this is deliberate ("NEW — spec-only" per the
   moduleIdentities summary) rather than an omission, since every other
   module (M0–M7) names at least one concrete existing or ported asset.
4. The open AI-permission-line question and the open branching-at-capstone
   question (both under "Pending reconciliation" above) are the two
   heaviest unresolved dependencies for M8's deep-build — both are policy
   rulings, not numbering fixes, and both were surfaced by the spine and
   its companion build materials, not invented by this scan.
