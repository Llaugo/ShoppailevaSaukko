from __future__ import annotations

import unittest

from itemLogic import chooseEmptyShelf, itemDistanceWithBonus


class FakeShelf:
    def __init__(self, item=None):
        self.item = item


class AppreciationItemLogicTests(unittest.TestCase):
    def test_rarity_bonus_is_added_to_room_distance(self) -> None:
        self.assertEqual(itemDistanceWithBonus(2, 1, 8), 3)
        self.assertEqual(itemDistanceWithBonus(2, 2, 8), 4)
        self.assertEqual(itemDistanceWithBonus(2, 3, 8), 5)

    def test_rarity_distance_is_capped_at_the_best_distribution(self) -> None:
        self.assertEqual(itemDistanceWithBonus(7, 3, 8), 8)
        self.assertEqual(itemDistanceWithBonus(8, 1, 8), 8)

    def test_negative_distance_values_are_rejected(self) -> None:
        for values in ((-1, 1, 8), (1, -1, 8), (1, 1, -1)):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    itemDistanceWithBonus(*values)

    def test_only_an_empty_shelf_can_be_chosen(self) -> None:
        occupied = FakeShelf(object())
        firstEmpty = FakeShelf()
        secondEmpty = FakeShelf()

        chosen = chooseEmptyShelf(
            [occupied, firstEmpty, secondEmpty],
            chooser=lambda shelves: shelves[-1],
        )

        self.assertIs(chosen, secondEmpty)

    def test_full_or_missing_shelf_list_returns_none(self) -> None:
        self.assertIsNone(chooseEmptyShelf([]))
        self.assertIsNone(chooseEmptyShelf([FakeShelf(object())]))


if __name__ == "__main__":
    unittest.main()
