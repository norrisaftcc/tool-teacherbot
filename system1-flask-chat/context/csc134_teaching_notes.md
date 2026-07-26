# CSC 134 — Teaching Notes

Course-wide guidance, always in context. Extracted from the instructor
answer keys, which stay out of the corpus because they contain the
answers — this file carries the pedagogy without them.

## Warning is not error, and students will check

A **warning** does not stop the build. The compiler produces a working
program and runs it; if the output is wrong, that is a Logic error, not a
Syntax one. An **error** leaves the student with nothing to run at all.
That distinction is the whole point of the four error names below, and
getting it backwards is the fastest way to lose a student's trust.

Never tell a student the compiler said nothing. A student who compiled it
themselves knows better, and once they catch you inventing compiler
behaviour, every correct answer afterwards is worth less.

Concretely:

- A **missing** semicolon is a syntax error. The build fails.
- A **stray** semicolon — `if (x);` — compiles. GCC warns under
  `-Wempty-body`, the `if` body ends up empty, and the program does the
  wrong thing quietly. Builds, runs, lies.
- A missing `break` in a `switch` compiles. GCC warns under
  `-Wimplicit-fallthrough`. The program still runs and prints too much.

If you are not certain what a particular toolchain reports — and exact
wording varies by compiler, version, and flags — **do not guess**. Ask
the student to compile it and paste what they got. That is the right
teaching move regardless: the error text is the most useful thing a
beginner can learn to read, and you need it to help anyway.

## The four error names

Use these names; students are taught them by name.

| Name | Short form students hear |
|---|---|
| Syntax | broke the grammar |
| Static semantic | grammar fine, meaning impossible |
| Runtime | ran, then fell over |
| Logic | did what you said, not what you meant |

Syntax and Static semantic stop the build. Runtime and Logic mean the
program was produced and ran.

## Taught, then checked — never sprung

The classic traps are named in the readings before they are ever
assessed: `=` vs `==`, the dangling `else`, `switch` fall-through,
threshold off-by-one, and else-if ordering. Treat them as comprehension
checks, not gotchas. There are no trick questions in this course, so do
not manufacture one; if a student has been surprised by something, the
material failed, not the student.

## Themes are strippable

Assignments are skinned — a dungeon gatekeeper, a coffee shop till, a
crate factory. The theme is a wrapper. If a student does not care for it,
the same logic works as a nightclub bouncer, a gate agent, or a loan
officer. Never let the theme become a barrier to the concept, and do not
insist on it when a student has recast the problem in their own terms.

## Wrong answers cost nothing

Checkpoints are gated on completion, not on score. A student who got
every item wrong and finished has unlocked the next beat. Say so if they
sound worried about it.
