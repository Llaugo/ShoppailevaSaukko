from __future__ import annotations

import unittest

from cardAnimation import advanceActiveOverlay


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


if __name__ == "__main__":
    unittest.main()
