import math


ACTIVE_OVERLAY_FIRST_FRAME = 5
ACTIVE_OVERLAY_FRAME_COUNT = 4
ACTIVE_OVERLAY_FRAMES_PER_SECOND = 8
ACTIVE_OVERLAY_LOOP_SECONDS = (
    ACTIVE_OVERLAY_FRAME_COUNT / ACTIVE_OVERLAY_FRAMES_PER_SECOND
)
LEVEL_EPSILON = 1e-9


def advanceActiveOverlay(phase, dt):
    """Advance an active-overlay loop by elapsed seconds and return its frame."""

    if dt < 0:
        raise ValueError("Card animation cannot be updated with negative time")
    phase = (phase + dt) % ACTIVE_OVERLAY_LOOP_SECONDS
    frameOffset = math.floor(phase * ACTIVE_OVERLAY_FRAMES_PER_SECOND)
    return phase, ACTIVE_OVERLAY_FIRST_FRAME + frameOffset


def advanceCardLevel(level, amount, maxLevel):
    """Add experience and report whether a whole card level was crossed."""

    if amount < 0:
        raise ValueError("Card experience cannot be negative")
    newLevel = min(level + amount, maxLevel)
    nextWholeLevel = math.floor(level + LEVEL_EPSILON) + 1
    leveledUp = (
        nextWholeLevel <= maxLevel
        and newLevel + LEVEL_EPSILON >= nextWholeLevel
    )
    return newLevel, leveledUp
