# ADR 0003: Content contracts are executable

- Status: Accepted
- Date: 2026-08-11

## Context

Rooms, translations, cards, items, and sprite sheets are connected through
numeric IDs, filenames, dimensions, and string keys. Many mistakes load only at
runtime and may affect a randomly selected room or card far into a run.

## Decision

Stable content rules are documented in `docs/CONTENT_FORMATS.md` and enforced by
dependency-free tests where practical. The tests may parse source and content
without importing Kivy.

A content-format change updates code, documentation, fixtures/assets, and tests
in the same change. Tests should validate contracts rather than freeze ordinary
content, so adding another valid room or translating more keys does not require
rewriting unrelated assertions.

## Consequences

- Common CSV, JSON, asset-path, and frame-geometry mistakes fail quickly.
- Numeric IDs must be treated as persistent data, not incidental list indexes.
- Visual correctness still requires a manual Kivy run.
- New content systems should expose validation rules that can run headlessly.

