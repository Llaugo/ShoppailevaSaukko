# Development roadmap

Last reviewed: 2026-08-11

This roadmap orders work by dependency and testability. It is not a release
promise. `docs/PORTING_STATUS.md` is the detailed inventory; this file describes
the next coherent milestones.

## Milestone 0: Codex-ready foundation

- [x] Document agent instructions and source-of-truth rules
- [x] Document current architecture, intended game loop, and content formats
- [x] Inventory the Kivy port against the legacy Pygame project
- [x] Add dependency metadata and repository ignore rules
- [x] Add dependency-free checks for source, layouts, translations, card assets,
  sprite sheets, and tuning data
- [ ] Remove already tracked generated caches and OS files in a dedicated cleanup
  change

Done when a new contributor or Codex task can set up the project, identify
authoritative code, and run checks without reverse-engineering the repository.

## Milestone 1: Stable Kivy vertical slice

- [ ] Use a production start-room layout instead of `testRoom`
- [ ] Start the first playable floor with the intended floor number
- [ ] Implement shopping-list victory and floor-timeout defeat
- [ ] Confirm and implement lift availability rules
- [ ] Make room, floor, and game transitions reset every temporary effect
- [ ] Fix invalid/incomplete menu destinations without introducing placeholder
  crashes
- [ ] Audit keyboard bindings so each event is handled once
- [ ] Verify Curiosity, Zest, and Humility through activation, expiry, failure,
  room transition, and floor transition
- [ ] Add deterministic logic tests for list generation, rarity selection, and
  floor generation where those systems can be separated from Kivy widgets

Done when a player can start a run, explore and collect items, win or lose, and
return to the menu without an exception or leaked scheduled callback.

## Milestone 2: Environment interactions

- [ ] Define reusable timed-effect and interaction-result patterns
- [ ] Port water collision and swimming
- [ ] Port darkness and temporary/permanent light effects
- [ ] Port advert direction, pushing, rotation, destruction, and blocking
- [ ] Port room item-name reveal and item creation
- [ ] Port jump/teleport with collision-safe landing
- [x] Port navigation stones without Pygame rectangle dependencies
- [ ] Complete the cards that depend only on these environment systems

Done when environment markers in all production room layouts have visible,
testable behavior and their associated cards no longer call missing APIs.

## Milestone 3: NPCs, carts, and social cards

- [ ] Port NPC movement, collision, and interaction targeting
- [ ] Port carts, ownership, pushing strength, and owner highlighting
- [ ] Port talking, permission, leadership, swapping, and love charging
- [ ] Port the trade model and Kivy trade UI
- [ ] Complete all NPC/cart-dependent strength cards
- [ ] Test combinations of simultaneous player and card effects

Done when every NPC/cart marker produces a working entity and every social card
has explicit success, failure, expiry, and reset behavior.

## Milestone 4: Persistence, screens, and localization

- [ ] Decide and document a versioned, non-Pickle Kivy save schema
- [ ] Save only stable game data rather than Kivy widget instances
- [ ] Implement continue, overwrite confirmation, and give-up flows
- [ ] Implement settings and game-information screens
- [ ] Decide the supported language set for the first release
- [ ] Complete English and Swedish or hide unsupported language choices
- [ ] Add translation-key parity checks for supported locales

Done when a run can be saved and restored across application versions according
to the documented compatibility policy and every offered locale is complete.

## Milestone 5: Mobile readiness and release

- [ ] Choose and implement touch movement controls
- [ ] Test representative phone, tablet, and desktop aspect ratios
- [ ] Add accessibility checks for text size, contrast, and input targets
- [ ] Add continuous integration for automated checks
- [ ] Define supported Python/Kivy/platform versions
- [ ] Package reproducible desktop builds, then evaluate mobile packaging
- [ ] Add release licensing and attribution material

Done when a clean checkout can be tested and packaged reproducibly for each
supported platform.

## Candidate later work

- Tutorial floor
- Achievements
- Balance telemetry and seeded run replay
- Additional room sets, items, and card progression content

