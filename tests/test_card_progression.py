from __future__ import annotations

import unittest

from cardProgression import advanceCardLevel


class CardProgressionTests(unittest.TestCase):
    def test_tenth_uses_reach_levels_despite_float_rounding(self) -> None:
        level = 1
        levelUpUses = []

        for use in range(1, 21):
            level, leveledUp = advanceCardLevel(level, 0.1, 3)
            if leveledUp:
                levelUpUses.append(use)

        self.assertEqual(levelUpUses, [10, 20])
        self.assertEqual(level, 3)

    def test_level_is_capped_and_does_not_repeat_level_up(self) -> None:
        level, leveledUp = advanceCardLevel(2.95, 0.1, 3)
        self.assertEqual(level, 3)
        self.assertTrue(leveledUp)

        level, leveledUp = advanceCardLevel(level, 0.1, 3)
        self.assertEqual(level, 3)
        self.assertFalse(leveledUp)

    def test_zero_experience_does_not_cross_a_rounded_boundary(self) -> None:
        level, leveledUp = advanceCardLevel(1.9999999995, 0, 3)

        self.assertEqual(level, 1.9999999995)
        self.assertFalse(leveledUp)


if __name__ == "__main__":
    unittest.main()
