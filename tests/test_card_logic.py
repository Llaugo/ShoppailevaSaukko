from __future__ import annotations

import unittest

from cardLogic import advanceActiveOverlay, advanceCardLevel


class ActiveOverlayAnimationTests(unittest.TestCase):
    def test_animation_advances_at_eight_frames_per_second(self) -> None:
        phase, frame = advanceActiveOverlay(0, 0)
        self.assertEqual(frame, 5)

        phase, frame = advanceActiveOverlay(phase, 0.125)
        self.assertEqual(frame, 6)
        phase, frame = advanceActiveOverlay(phase, 0.125)
        self.assertEqual(frame, 7)
        phase, frame = advanceActiveOverlay(phase, 0.125)
        self.assertEqual(frame, 8)

    def test_animation_loops_after_half_a_second(self) -> None:
        phase, frame = advanceActiveOverlay(0.375, 0.125)

        self.assertEqual(phase, 0)
        self.assertEqual(frame, 5)

    def test_large_dt_keeps_the_same_time_based_rate(self) -> None:
        directPhase, directFrame = advanceActiveOverlay(0, 1.375)

        steppedPhase = 0
        steppedFrame = 5
        for _ in range(11):
            steppedPhase, steppedFrame = advanceActiveOverlay(
                steppedPhase,
                0.125,
            )

        self.assertAlmostEqual(directPhase, steppedPhase)
        self.assertEqual(directFrame, steppedFrame)


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
