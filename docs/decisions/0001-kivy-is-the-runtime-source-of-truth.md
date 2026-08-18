# ADR 0001: Kivy is the runtime source of truth

- Status: Accepted
- Date: 2026-08-11

## Context

Shoppaileva Saukko is a rewrite of the Pygame project VahvuusVaris. Much of the
legacy behavior is useful and some Kivy files still contain copied or inactive
Pygame-era code. The frameworks use different event loops, widgets, coordinate
objects, rendering, collision primitives, and persistence assumptions.

Without an explicit boundary, a port can accidentally call an unavailable
Pygame API or treat historical behavior as a current requirement.

## Decision

The current Kivy repository is authoritative for runtime architecture and
implemented behavior. Accepted design documents and decision records are
authoritative for intended behavior.

<https://github.com/Llaugo/VahvuusVaris> is a historical behavior and domain
reference. Code may be studied there, but must be reimplemented through the
current Kivy ownership boundaries. Pygame types, frame-loop assumptions,
drawing code, and Pickle object graphs must not be copied into live Kivy code.

When legacy behavior conflicts with current Kivy behavior and the design docs do
not settle the difference, the behavior is an open product question.

## Consequences

- Porting work starts with a Kivy domain/API design, not a pasted method.
- `docs/PORTING_STATUS.md` must distinguish class presence from playability.
- Inactive legacy code can be removed once its useful behavior is documented.
- Some ports take longer initially but avoid mixing incompatible frameworks.

