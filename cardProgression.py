import math


LEVEL_EPSILON = 1e-9


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
