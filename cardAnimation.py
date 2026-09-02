import math


ACTIVE_OVERLAY_FIRST_FRAME = 5
ACTIVE_OVERLAY_FRAME_COUNT = 4
ACTIVE_OVERLAY_FRAMES_PER_SECOND = 8
ACTIVE_OVERLAY_LOOP_SECONDS = (
    ACTIVE_OVERLAY_FRAME_COUNT / ACTIVE_OVERLAY_FRAMES_PER_SECOND
)


def advanceActiveOverlay(phase, dt):
    """Advance an active-overlay loop by elapsed seconds and return its frame."""

    if dt < 0:
        raise ValueError("Card animation cannot be updated with negative time")
    phase = (phase + dt) % ACTIVE_OVERLAY_LOOP_SECONDS
    frameOffset = math.floor(phase * ACTIVE_OVERLAY_FRAMES_PER_SECOND)
    return phase, ACTIVE_OVERLAY_FIRST_FRAME + frameOffset
