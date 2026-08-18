# Working on Shoppaileva Saukko

This file is the operating contract for Codex and other coding agents. Read it
before changing the project. Read the relevant document in `docs/` before
changing gameplay, content formats, or architecture.

## Project and source of truth

Shoppaileva Saukko is an in-progress Python/Kivy rewrite of the older Pygame
project at <https://github.com/Llaugo/VahvuusVaris>.

Use sources in this order:

1. The current Kivy code, automated checks, and accepted decision records
2. `docs/GAME_DESIGN.md` for confirmed and explicitly proposed behavior
3. `docs/PORTING_STATUS.md` for what is current, partial, or not ported
4. The Pygame repository as historical behavior and implementation reference

Do not copy Pygame APIs, frame-based timing, drawing code, or serialized object
formats into the Kivy runtime. When the current code, design document, and
legacy behavior disagree in a way that changes player-visible behavior, stop
and ask which behavior is wanted.

## Setup and commands

Run every command from the repository root. Images, fonts, translations, KV,
and room layouts are currently loaded with paths relative to that directory.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python main.py
```

Run the dependency-free automated checks with:

```bash
python3 -m unittest discover -s tests -v
```

For a manual launch in a restricted environment, give Kivy a writable home:

```bash
KIVY_HOME=/tmp/shoppaileva-saukko-kivy python3 main.py
```

See `docs/TESTING.md` for the manual smoke-test checklist. Do not claim that a
visual or interaction change was verified unless the app was actually run and
the relevant flow was exercised.

## Architecture boundaries

- `main.py` owns the app, localization selection, screens, and screen-level
  scheduling.
- `shopper.kv` owns the widget tree and presentation. KV `id` values referenced
  from Python are API names; update both sides together.
- `game.py` owns run/floor state, room traversal, the update loop, and
  coordination between gameplay systems.
- `playerClass.py` owns the active Kivy `Player`. The triple-quoted Pygame code
  below the live implementation is reference-only and must not be called.
- `room.py` and `tile.py` decode room content and own room-local objects.
- `shoppingList.py` and `item.py` own item selection and list progress.
- `strengthMenu.py`, `strengthDeck.py`, and `strengthCard.py` own card selection,
  activation, leveling, active effects, expiry, and reset.
- `const.py` owns tuning data and loads room files. Do not add UI state there.
- `rooms/`, `i18n/`, `images/`, and `fonts/` are content, not generated output.

Prefer completing behavior in the owning module over adding cross-module state
or reaching through several widgets. Do not perform broad renames or formatting
while implementing a feature; the code still contains intentional porting
seams and established mixed-case module names.

## Required invariants

### Time

The Kivy update loop uses seconds. `dt`, card `timer`, card `cooldown`, player
effect durations, and the floor timer must all be expressed in seconds.

The Pygame project used frame counts at 60 FPS. Convert legacy values explicitly
by dividing frame counts by 60. Never copy expressions such as `8 * 60` without
first deciding whether they mean eight seconds or 480 seconds. Detect expiry
with a transition such as `old_timer > 0 and timer <= 0`; a float timer is not
guaranteed to equal exactly `1` or `0` during an update.

### Kivy lifecycle

- Access `self.ids` only after KV has populated the widget, normally in or after
  `on_kv_post`.
- Use Kivy properties for state observed by KV.
- Keep every `Clock.schedule_*` and `Window.bind` paired with an unschedule or
  unbind at the owning lifecycle boundary.
- Keep hitboxes and visuals distinct when resizing a player or sprite.
- A floor or screen transition must reset temporary card/player/room effects.

### Content

- Standard room layouts are 15 x 15; the lift layout is 5 x 5.
- Room CSV files use rows whose cells are all empty as layout separators.
- Use only codes documented in `docs/CONTENT_FORMATS.md`.
- Card IDs are stable integers `0..25`. An ID must continue to map to its class,
  category, individual card image, and translation text.
- Finnish (`fi`) is the complete source locale. Add a Finnish key for every new
  visible string. English and Swedish may remain incomplete until their
  localization milestone, but non-empty JSON files must be valid objects.
- Do not edit binary art or font files unless the task explicitly calls for an
  asset change. Preserve dimensions and frame order when replacing a sheet.

### Repository hygiene

- Preserve unrelated user changes and inspect `git status` before editing.
- Do not commit generated caches, local environments, logs, saves, or OS files.
- Do not stage, commit, push, or delete tracked files unless the user requests it.
- Keep docs synchronized when a change alters a documented contract or feature
  status.

## Definition of done

A gameplay or content change is complete when:

1. The behavior and ownership are consistent with the docs, or the docs and an
   accepted decision record are updated.
2. Active effects also have correct expiry, reset, room-change, and floor-change
   behavior.
3. New strings, card data, room codes, and assets satisfy the content contracts.
4. `python3 -m unittest discover -s tests -v` passes.
5. Relevant manual checks in `docs/TESTING.md` were run, or the handoff clearly
   states why they were not.
6. `git diff` contains no unrelated formatting, generated files, or accidental
   binary changes.

