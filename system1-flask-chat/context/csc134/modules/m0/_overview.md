# M0 — Welcome to Programming

> **Canonical home.** This file, and the other three `_`-prefixed files beside
> it in `modules/m0/`, are the spine-true scaffold for Module 0. `assignments/m0/`
> is legacy source material (frozen, not authoritative) — see `_assets.md` in
> this folder for exactly which legacy files port in and which are flagged for
> a reconciliation ruling before they port.
>
> **SKELETON ONLY.** This is structure, not authored lesson content. The deep
> build (Learn / Practice / Apply / Assess beats) happens in a later pass.

---

## Spine header

| Field | Value |
|---|---|
| Module | **M0** |
| Title | Welcome to Programming |
| Phase | A |
| Weeks | ~Week 1 |
| Spine source | `_storming/CSC-134-course-spine.md`, "## M0 — Welcome to Programming" (line 102) |

## Big idea

*(Verbatim from the spine.)*

> Why are we even in this building, in front of computers? What is a program,
> what is this field, and why does this still matter when an AI can write code?

**Reframed for our audience.** The systems idea (software runs inside a system
of people + processes + technology) is kept, but tilted toward the transfer
majority: computation as the universal problem-solving instrument underneath
CS and engineering. The AI stance is stated head-on in our terms — AI can
write C++; verifying and collaborating with it requires you to read C++, and
building that fluency is an explicit goal of this course. "Prompt and hope"
is not an engineering skill.

---

## LPAA beat map

*(One-liners from the spine — not the authored beats themselves.)*

| Beat | One-liner |
|---|---|
| **Learn** | Read "Welcome to Programming" (short); what a program is; what this field is. |
| **Practice** | Exit ticket — what makes something a "program"? Classify a few everyday systems. |
| **Apply** | Instructor-led environment setup — GitHub account, Codespaces vs. local VSCode + MinGW/MSYS2, "hello world" compiles and runs on *your* setup. |
| **Assess** | A short reflection (a program you used today: its inputs, its process, its outputs) + proof the toolchain runs. |

---

## Make-gradient position

**M0 sits before the Apply-beat gradient begins.** The gradient
(`_contracts/rubric-template.md`, "Make-gradient note") is defined for
C++-authoring modules: **M2–M4 type-in-100%**, **M5–M7 finish-the-80%**,
**M8 spec-only**. M0 has no C++ program to gradient-position yet — its Apply
beat is instructor-led *environment setup*, not code construction. Treat M0's
Apply beat as **pre-gradient**: the "100%" here is the toolchain steps, walked
together, ending in one working `hello world` compile per student.

---

## User story (fill-in — skeleton slot, not authored)

> As a student **arriving in CSC-134 with no assumed prior programming
> experience**, I want ______, so that ______.

**Note on the template mismatch:** the layout spec's standard phrasing is
*"As a student finishing M{N-1}..."* M0 is the entry module — there is no
M-1 to have finished. The line above substitutes the natural entry-point
framing ("arriving in CSC-134...") and is left as a fill-in for the deep-build
pass, same as every other module's user story.

---

## Contract touch

M0 does not touch a frozen `_contracts/` interface (no `m4_gatekeeper.cpp` /
`m5_menu.cpp` involvement at this stage). Its only inherited contract is
`_contracts/rubric-template.md`, instantiated in `_assess-spec.STUB.md`.

---

## Numbering flag

Per `_tracking/numbering-reconciliation-map.md` (row 10) and
`_tracking/skeleton-plan.md` (open question 5): `assignments/m0/02_first_pull_request.md`
teaches the full fork → branch → PR workflow. That contradicts ADR-004's
student-flow rule (commit + push only, no branches/PRs before the capstone).
This scaffold does not resolve that — see `_assets.md` for the flagged detail.
It is recorded here as a pending reconciliation, not actioned.
