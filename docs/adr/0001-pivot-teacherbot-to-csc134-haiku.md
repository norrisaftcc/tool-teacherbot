# ADR-0001: Serve /csc114 and /csc134 as skins; run CSC 134 on Haiku

- **Status:** Accepted
- **Date:** 2026-07-25
- **Deciders:** norrisaftcc (product), Claude Code (implementation)

## Context

Teacherbot (the Flask app in `system1-flask-chat/`) already serves one
real cohort — **CSC 114**, Summer 2026 pilot — landed in PRs #6/#7/#8
on main:

- Cohort credentials live in a single `auth.py::GROUPS` table.
- Per-cohort framing lives in `context/<cohort>_context.md` (hand-authored
  header) plus `context/<cohort>/` (vendored corpus).
- Corpus is pulled with `scripts/sync_csc114_corpus.py` +
  `scripts/csc114_manifest.yaml`, cloning
  `norrisaftcc/course-csc114-template` at a pinned ref.
- `claude_handler.py` hardcodes `MODEL = 'claude-sonnet-4-6'` at module
  scope. All cohorts share it.
- Routing is flat: one `/`, one `/login`, one `/chat`, one `/admin`.
  A student picks their cohort by typing its ID on the login form.

We now need to onboard **CSC 134** *and* change how cohorts are surfaced.
The product intent is that CSC 114 and CSC 134 are separately branded
entry points — **"skins"** — reachable at their own URLs, not one login
form that fans out. Requirements:

- Two URL-addressable skins: `/csc114/…` and `/csc134/…`. Each has its
  own login, chat, and admin surface. Root `/` becomes a picker (or
  redirects).
- Each skin has its own passcode, its own cohort header + vendored
  corpus, and its own visual copy (title, tagline, colors are
  potentially different, though the design kit is shared).
- CSC 134 runs on **Claude Haiku**. CSC 114 stays on Sonnet. Model is a
  per-skin property, not per-request or per-env.
- Same backing database. Logs remain queryable per cohort so a single
  admin surface (or a per-skin admin surface — pick in the impl PR) can
  read them.
- The AlgoCratic Futures spike from PR #1 (branch
  `claude/add-teacherbot-demo-rKeS2`) stays untouched. It's not on main
  and is not part of this pivot.

Trusted-workflow constraints: Issues → ADRs → PRs, one substantive
change per PR, no unrelated cleanup.

## Decision

Restructure `system1-flask-chat/` so each cohort is a **skin** exposed
under its own URL prefix, and land CSC 134 as the second skin, pinned
to Haiku.

Shape:

1. **Skin registry, not a flat GROUPS table.** Replace `auth.py::GROUPS`
   with a `SKINS` mapping keyed by cohort slug. Each skin declares:
   passcode, model, cohort header path, corpus dir, display name /
   tagline, and any visual tokens that vary from the design kit
   default. `auth.py` grows `authenticate_skin(slug, password)` and
   `load_skin_context(slug)`.

   ```python
   SKINS = {
       'csc114': {
           'password':    '2026su',
           'model':       'claude-sonnet-4-6',
           'display':     'CSC 114 — AI/ML Fundamentals',
           'header_file': 'csc114_context.md',
           'corpus_dir':  'csc114/',
           'tagline':     'Summer 2026 pilot cohort.',
       },
       'csc134': {
           'password':    '<TBD>',
           'model':       'claude-haiku-4-5-20251001',
           'display':     'CSC 134 — <official title TBD>',
           'header_file': 'csc134_context.md',
           'corpus_dir':  'csc134/',
           'tagline':     '<TBD>',
       },
   }
   ```

2. **URL-prefixed blueprint per skin.** Replace the single flat
   `routes.py` blueprint with a `skin_blueprint(slug)` factory
   registered once per skin at its URL prefix. Each blueprint owns:

   - `GET  /<slug>/`             → skin login page
   - `POST /<slug>/login`        → sets session skin + auth flag
   - `GET  /<slug>/chat`         → chat UI, skinned
   - `POST /<slug>/api/chat`     → JSON chat, model taken from skin
   - `GET  /<slug>/admin`        → admin console scoped to this cohort
   - `GET  /<slug>/logout`

   Root `/` renders a picker listing the registered skins as tiles.

3. **Session scoped to skin.** Login writes `session['skin'] = slug`.
   Every skin-guarded route asserts the session skin matches the URL
   slug — a student logged into `csc114` who navigates to `/csc134/chat`
   is bounced to `/csc134/`. Prevents cross-skin session bleed and
   makes the admin scoping trivial.

4. **Per-skin model wiring.** `claude_handler.get_claude_response`
   takes an explicit `model` argument. The chat route reads it from the
   skin registry via the URL slug (not from the session — URL is the
   source of truth) and passes it through. Module-level `MODEL`
   constant becomes a fallback default only.

5. **Templates: shared base, skin-scoped copy.** Templates stay in one
   `templates/` tree but read a `skin` context dict (display, tagline,
   colors) from the blueprint. No per-skin template forks unless a
   skin needs a genuinely different page shape — none do in v1.

6. **Data model change.** `Group.name` continues to hold the slug —
   existing rows for `csc114` are unaffected. New rows for `csc134`
   are created on first login just as before. Conversation and Message
   tables need no changes. An admin scoped to `/<slug>/admin` filters
   by `Group.name == slug`.

7. **Corpus for CSC 134.** New `scripts/csc134_manifest.yaml` pointed
   at `norrisaftcc/course-csc134-template` at a pinned ref, mirroring
   the CSC 114 manifest schema. Sync script is either generalized to
   `scripts/sync_course_corpus.py <manifest>` or copy-pasted as
   `sync_csc134_corpus.py` — the implementation PR picks whichever
   diff is smaller; prefer generalization if it costs <20 lines.

8. **Cohort header for CSC 134.**
   `system1-flask-chat/context/csc134_context.md`, hand-authored,
   mirrors the CSC 114 header shape.

9. **Tests.** Extend the sync-script test to cover CSC 134's manifest.
   Add route tests covering: root picker lists both skins, each skin's
   login round-trips, `/api/chat` under each skin passes the correct
   model into a mocked `claude_handler`, and cross-skin session
   isolation (log into csc114, hit csc134 chat, expect redirect).

### What we deliberately do not change

- Design kit (`static/css/{colors_and_type,kit}.css`) — shared.
- Database schema — reused as-is.
- The pedagogical system prompt — same wording for both skins in v1.
  If Haiku-on-CSC-134 needs a divergent prompt, that becomes ADR-0002.
- Render deployment story — same single service serves both prefixes.
- The AlgoCratic spike on PR #1 — untouched.

## Consequences

**Positive.**
- Each skin is a shareable link (`/csc114/`, `/csc134/`) that instructors
  can hand to their sections without explaining a cohort ID.
- Per-skin model unlocks the CSC 134 cost profile (Haiku) without
  affecting CSC 114, and enables future A/B by changing one dict value.
- Session-scoped-to-skin plus URL-anchored model means the two cohorts
  cannot accidentally see each other's chats or costs.
- Refactor is a one-time cost that pays off for every subsequent
  cohort — the third skin is a dict entry plus a manifest, not a code
  change.

**Negative.**
- The blueprint-per-skin refactor touches `routes.py`, `auth.py`, and
  every template. Non-trivial diff, must land as one PR to keep the
  session/URL contract atomic.
- Existing single-`/login` bookmarks and any docs pointing at them
  break. Mitigation: root `/` becomes the picker, so old links
  redirect somewhere useful.
- Two `<cohort>_manifest.yaml` files today; more if more cohorts land.
  Refactor candidate for ADR-0002.
- Haiku is weaker than Sonnet at multi-step reasoning. Shared prompt
  may need to diverge later (ADR-0003 candidate).

**Neutral.**
- No streaming responses in v1 (already the case).
- No new external dependencies.

## Alternatives Considered

1. **Add CSC 134 to the flat `GROUPS` table, keep one `/login`.**
   Smallest possible diff, but does not deliver the "two skinned entry
   points" product intent. Rejected.
2. **Fork `system1-flask-chat/` into `csc114-teacherbot/` and
   `csc134-teacherbot/` siblings.** Cleanest isolation, worst
   maintenance. Every future route, template, or logging change is a
   double-edit. Rejected.
3. **Subdomains (`csc114.teacherbot.example`, `csc134.…`) instead of
   URL prefixes.** More Render/DNS setup, no product benefit over
   prefixes at this stage. Rejected for v1; revisit if a skin needs
   real domain-level isolation.
4. **Per-request model via query string or header.** Trivially bypassed,
   makes cost attribution ambiguous. Rejected.

## Open Questions

- **Passcode for CSC 134.** Placeholder in the implementation PR;
  the real value is set out-of-band before students log in.
- **Ref to pin in `csc134_manifest.yaml`.** Implementation PR pins
  whatever's at `norrisaftcc/course-csc134-template@main` at sync
  time; instructor bumps via manifest edit + re-sync.
- **Admin surface.** Per-skin `/<slug>/admin` is the v1 default. A
  cross-skin instructor overview page (list both cohorts side by
  side) is a follow-up PR if the instructor asks for it — do not
  build speculatively.
- **Official course title for CSC 134.** Cosmetic; picker tile and
  `display` field. Placeholder OK for the implementation PR.
- **Root `/` behavior.** Picker page listing registered skins with
  brief taglines is the v1 default. If a plain redirect to a
  designated "primary" skin is preferred, flag before the impl PR.

## Follow-ups

- ADR-0002 (conditional): Generalize `sync_*_corpus.py` when a third
  cohort or fourth manifest lands.
- ADR-0003 (conditional): Diverge the pedagogical system prompt per
  skin if the Haiku-on-CSC-134 experience needs it.
- ADR-0004 (conditional): Subdomain-per-skin routing if a cohort needs
  domain-level isolation.
