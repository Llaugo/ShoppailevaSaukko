# Testing and verification

## Automated checks

The repository checks use Python's standard-library `unittest`, so content and
source contracts can be validated before Kivy is installed:

```bash
python3 -m unittest discover -s tests -v
```

The suite checks:

- Python source parses without creating bytecode caches;
- room CSV dimensions, separators, entry points, and raw codes;
- Finnish contains every statically referenced and card-generated key;
- non-empty locale files are valid JSON objects;
- card IDs, classes, categories, and card images stay aligned;
- active card overlays loop at a duration-independent rate;
- card-level thresholds remain float-safe;
- Appreciation shelf selection and rarity bonuses remain valid and capped;
- source-keyed timed speed effects compose, refresh, and expire;
- referenced static assets exist with exact case;
- sprite sheets retain their frame geometry;
- item rarity tables remain valid cumulative distributions;
- Python `ids` references have matching KV IDs.

These tests deliberately avoid importing Kivy. Widget construction may create a
window, depend on a graphics provider, and write Kivy state outside the project.
Logic should gradually be extracted into pure functions or data objects so it
can receive deterministic unit tests.

## Manual launch

Set up and run from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python main.py
```

If Kivy cannot write its normal user configuration in a sandbox:

```bash
KIVY_HOME=/tmp/shoppaileva-saukko-kivy python main.py
```

## Baseline smoke checklist

Run this checklist after changing screens, KV, input, rooms, player collision,
items, cards, or floor transitions.

1. The menu opens without missing font, KV, translation, or image errors.
2. New game opens the strength menu.
3. Each category opens and one card can be selected.
4. Randomize selects one card in every category.
5. Start opens gameplay with six visible cards.
6. `W`, `A`, `S`, and `D` move and animate the player.
7. Walls, shelves, and crates block movement without trapping the player.
8. Crossing each available edge enters a room and places the player on the
   opposite edge.
9. Standing on an item reveals the pickup button; picking it up updates feedback
   and the shopping list correctly.
10. Curiosity removes a reachable crate and handles no-target activation.
11. Zest increases speed and returns it to normal after expiry/reset.
12. Humility changes both visible size and hitbox, then restores both.
13. Appreciation adds exactly one collectible item to an empty shelf, uses the
    expected rarity bonus at levels 1-3, reduces cooldown from 30 to 27 to 24
    seconds, preserves the item when revisiting the room, and rejects a full
    room without consuming selection, experience, or cooldown.
14. Gratitude drops one visible stone with matching visual/trigger bounds,
    rejects an overlapping duplicate without a cooldown, preserves stones when
    revisiting a room, applies the expected boost without overriding Zest, and
    never replaces its cooldown overlay with the active animation.
15. Standing on the lift shows the lift button; floor transition does not leave
    a selected, active, or cooldown overlay in an invalid state.
16. Resize the window to 1000 x 500 and at least one non-2:1 shape. The world,
    buttons, cards, and text remain reachable.
17. Leave and re-enter the game screen once. Input is not duplicated and only
    one update loop is active.

Current known incomplete flows—Continue, settings, information, timeout,
victory, NPC/cart behavior, water effects, darkness, and adverts—should be
tested only as part of a task that ports them. Update this checklist when they
become playable.

## Feature test recipe

For a timed card or player effect, record at least:

- initial state;
- activation in valid context;
- activation in invalid context;
- state during the effect;
- natural expiry across a `dt` step that skips past zero;
- manual reset;
- room change;
- floor/lift change;
- overlapping effect behavior;
- level 2 and level 3 upgrade behavior.

Prefer fixed random seeds for non-visual logic. Do not make tests depend on the
specific random room or item chosen unless randomness is the subject of the
test.
