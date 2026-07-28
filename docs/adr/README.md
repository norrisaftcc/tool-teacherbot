# Architecture Decision Records

Each ADR captures one significant architectural decision: the context that
forced the choice, the option we picked, and what living with it will cost.

## Conventions

- Files are numbered sequentially: `NNNN-short-title.md` (zero-padded to 4).
- Every ADR uses the template below.
- Status starts `Proposed`, moves to `Accepted` when merged, `Superseded by
  NNNN` when a later ADR replaces it, or `Deprecated` when withdrawn.
- Once `Accepted`, an ADR is immutable except for the Status line and links
  to superseding records — corrections happen in a new ADR.

## Index

| ID | Title | Status |
|----|-------|--------|
| [0001](0001-pivot-teacherbot-to-csc134-haiku.md) | Serve /csc114 and /csc134 as skins; run CSC 134 on Haiku | Accepted |
| [0002](0002-per-skin-persona-and-windowed-corpus.md) | Per-skin persona, and window the corpus to one module | Accepted |
| [0003](0003-local-model-backend-for-dev-and-eval.md) | A local (Ollama) model backend for development and evaluation | Accepted |

## Template

```markdown
# ADR-NNNN: <Short imperative title>

- **Status:** Proposed | Accepted | Superseded by NNNN | Deprecated
- **Date:** YYYY-MM-DD
- **Deciders:** <names or roles>

## Context

What is the situation, what forces are in play, and what constraints matter.
Keep it factual — no argument yet.

## Decision

The choice being made, in one or two sentences. Then the shape of what will
be built.

## Consequences

Positive, negative, and neutral effects. Include what this makes harder as
well as easier.

## Alternatives Considered

The other options we weighed and why we did not pick them.
```
