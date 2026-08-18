# ADR 0002: Runtime time values use seconds

- Status: Accepted
- Date: 2026-08-11

## Context

The Pygame project updates at a nominal 60 FPS and stores card effects and
cooldowns as frame counts. For example, `8 * 60` represents eight seconds and
is decremented by one per frame.

Kivy calls `update(dt)` with real elapsed seconds. Some copied card values still
contain `* 60`, and some expiry methods compare float timers to exactly `1`.
Those patterns make effects 60 times too long or prevent cleanup from firing.

## Decision

All Kivy duration, cooldown, delay, and countdown values use seconds. They are
decremented by elapsed `dt` unless a documented pause domain applies.

Legacy frame counts are converted as:

```text
seconds = legacy_frames / 60
```

Expiry is detected by crossing zero:

```python
old_timer = timer
timer = max(timer - dt, 0)
if old_timer > 0 and timer <= 0:
    end_effect()
```

## Consequences

- Tuning values are readable without knowing the target frame rate.
- Effects behave consistently during frame drops and at different refresh rates.
- Every remaining `* 60` value must be reviewed rather than mechanically kept.
- Prudence and any future time-stop feature must name which timers it pauses.

