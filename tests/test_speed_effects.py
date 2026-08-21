from __future__ import annotations

import unittest

from speedEffects import TimedSpeedEffects


class TimedSpeedEffectsTests(unittest.TestCase):
    def test_strongest_effect_wins_and_weaker_effect_remains(self) -> None:
        effects = TimedSpeedEffects(400)
        effects.setEffect("gratitude", 520, 2)
        effects.setEffect("zest", 600, 1)

        self.assertEqual(effects.speed, 600)
        effects.update(1.1)
        self.assertEqual(effects.speed, 520)
        self.assertAlmostEqual(effects.remaining("gratitude"), 0.9)

        effects.update(1)
        self.assertEqual(effects.speed, 400)

    def test_refresh_replaces_only_the_named_effect_duration(self) -> None:
        effects = TimedSpeedEffects(400)
        effects.setEffect("gratitude", 520, 1)
        effects.update(0.8)
        effects.setEffect("gratitude", 520, 1)

        self.assertEqual(effects.speed, 520)
        self.assertEqual(effects.remaining("gratitude"), 1)
        effects.update(1.1)
        self.assertEqual(effects.speed, 400)

    def test_clearing_one_source_does_not_clear_another(self) -> None:
        effects = TimedSpeedEffects(400)
        effects.setEffect("gratitude", 520, 2)
        effects.setEffect("zest", 600, 2)

        effects.clearEffect("zest")
        self.assertEqual(effects.speed, 520)
        effects.clear()
        self.assertEqual(effects.speed, 400)

    def test_update_crossing_zero_expires_effect(self) -> None:
        effects = TimedSpeedEffects(400)
        effects.setEffect("gratitude", 520, 0.25)

        effects.update(0.5)
        self.assertEqual(effects.remaining("gratitude"), 0)
        self.assertEqual(effects.speed, 400)


if __name__ == "__main__":
    unittest.main()
