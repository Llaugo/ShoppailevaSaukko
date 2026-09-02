import random


def itemDistanceWithBonus(roomDistance, rarityBonus, maxDistance):
    """Return a capped item-rarity distance for an Appreciation spawn."""

    if roomDistance < 0 or rarityBonus < 0 or maxDistance < 0:
        raise ValueError("Item distance values cannot be negative")
    return min(roomDistance + rarityBonus, maxDistance)


def chooseEmptyShelf(shelves, chooser=None):
    """Choose an unoccupied shelf, or return None when every shelf is full."""

    emptyShelves = [shelf for shelf in shelves if shelf.item is None]
    if not emptyShelves:
        return None
    if chooser is None:
        chooser = random.choice
    return chooser(emptyShelves)
