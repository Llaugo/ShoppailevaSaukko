# Kivy porting status

Last reviewed: 2026-08-18

The current repository is a Kivy rewrite of
<https://github.com/Llaugo/VahvuusVaris>. The legacy project is a behavioral
reference, not runtime code. A status of **not ported** means the current class
may still exist but calls an API that does not exist in the live Kivy objects.

## Status vocabulary

- **Playable:** the main path is implemented in live Kivy code.
- **Partial:** some state or rendering exists, but the full design loop does not.
- **Not ported:** only markers, card shells, or legacy reference code exist.
- **Infrastructure:** support exists but has not been integrated into a complete
  player-visible flow.

## Core systems

| System | Status | Current source | Important gap |
| --- | --- | --- | --- |
| App and screen manager | Partial | `main.py`, `shopper.kv` | Continue destination is absent; settings/info are placeholders |
| Strength selection | Playable | `strengthMenu.py` | Needs localization completion and manual aspect-ratio checks |
| Gameplay rendering/scaling | Playable | `game.py`, `shopper.kv` | Duplicate key binding; mobile movement absent |
| Floor matrix and lazy rooms | Playable | `game.py` | Starts from `testRoom`, not a production start layout |
| Room CSV decoding | Playable | `roomLayout.py`, `room.py` | Decoder docs in `const.py` are stale for encoded markers |
| Player movement/collision | Playable | live top section of `playerClass.py` | No water, NPC, cart, flight, strength, or push state |
| Items and rarity | Playable | `item.py`, `const.py` | Randomness is not injectable for deterministic tests |
| Shopping list | Playable | `shoppingList.py` | Completion is not connected to victory |
| Floor/lift transition | Partial | `game.py` | No entry lock, timeout, victory, defeat, or full checkpoint policy |
| Save/continue | Not ported | legacy `SaveLoadManager.py` | Needs a versioned Kivy data schema |
| Localization | Partial | `main.py`, `i18n/` | Finnish complete to the current extent of the game; English mismatched; Swedish empty |
| Automated content checks | Infrastructure | `tests/` | Does not replace interactive Kivy testing |

## Environment systems

| System | Status | What exists | What must be ported |
| --- | --- | --- | --- |
| Crates | Playable | Spawn, collision, interaction range, removal | Failure feedback and broader test coverage |
| Water | Partial | Tile decoding and room water list | Movement effect, swimming, cleaning, expiry |
| Darkness/light | Not ported | Tuning value and legacy card calls | Room mask/state, temporary and permanent light |
| Adverts | Partial | Directional markers render one tile frame | Entity/state, direction, push, rotate, destroy, block |
| Carts | Not ported | Encoded layout markers become floor | Entity, collision, owner, weight/push rules |
| NPC shoppers | Not ported | Encoded layout markers become floor | Entity, movement, collision, targeting |
| Trade | Not ported | Legacy design and unused art | Data transaction and Kivy UI |
| Navigation stones | Playable | Room-owned Kivy widgets using `images/stone.png` | Verify exact-size trigger during manual play |
| Bird's-eye view | Not ported | Legacy implementation only | Kivy multi-room view and darkness policy |

## Strength cards

All 26 Kivy card classes and images exist. Only the rows marked playable have
their required API in the live Kivy `ShopperGame`, `Player`, and `Room` classes.

| ID | Class | Category | Status | Missing or next verification |
| ---: | --- | --- | --- | --- |
| 0 | `CreativityCard` | Wisdom | Not ported | `ShopperGame.jumpGap`; collision-safe Kivy teleport |
| 1 | `CuriosityCard` | Wisdom | Playable | Verify range and failure cooldown reset |
| 2 | `JudgementCard` | Wisdom | Not ported | `showItemNames`; float-safe expiry |
| 3 | `LearningCard` | Wisdom | Not ported | permanent darkness clearing |
| 4 | `PerspectiveCard` | Wisdom | Not ported | bird's-eye view; float-safe expiry |
| 5 | `BraveryCard` | Courage | Not ported | player strength and cart pushing |
| 6 | `PerseveranceCard` | Courage | Not ported | water collision and `Player.swim` |
| 7 | `HonestyCard` | Courage | Not ported | advert entities and `rotateAdverts` |
| 8 | `ZestCard` | Courage | Playable | Verify overlapping speed effects and resets |
| 9 | `GritCard` | Courage | Not ported | advert entities and `destroyAdvert` |
| 10 | `KindnessCard` | Humanity | Not ported | NPC collision timer and level-3 contact behavior |
| 11 | `LoveCard` | Humanity | Not ported | NPC talk targeting, battery UI, flight |
| 12 | `SocialCard` | Humanity | Not ported | cart/NPC ownership view and reset |
| 13 | `CompassionCard` | Humanity | Not ported | NPC targeting and position swap |
| 14 | `FairnessCard` | Justice | Not ported | NPC permission and temporary cart access |
| 15 | `LeadershipCard` | Justice | Not ported | NPC/cart pathing and owner action |
| 16 | `TeamworkCard` | Justice | Not ported | NPC inventory, trade rules, Kivy trade UI |
| 17 | `ForgivenessCard` | Temperance | Not ported | water removal in interaction range |
| 18 | `HumilityCard` | Temperance | Playable | Verify hitbox/visual reset at every transition |
| 19 | `PrudenceCard` | Temperance | Not ported | pause domains, `stopTime`, float-safe expiry |
| 20 | `RegulationCard` | Temperance | Not ported | advert pushing/block state and expiry |
| 21 | `AppreciationCard` | Spirituality | Not ported | room-level item creation and full-shelf failure |
| 22 | `GratitudeCard` | Spirituality | Playable | Verify room persistence, level tuning, and Zest overlap |
| 23 | `HopeCard` | Spirituality | Not ported | directional darkness beam and reset |
| 24 | `HumorCard` | Spirituality | Not ported | water collision and `Player.swim` |
| 25 | `SpiritualityCard` | Spirituality | Not ported | radial darkness light and reset |

## General card-port checklist

Before changing a card from not ported to playable:

1. Port the underlying world capability to its owning Kivy class.
2. Convert all legacy frame durations to seconds.
3. Replace exact timer comparisons with transition-based expiry.
4. Define whether failed targeting consumes cooldown or experience.
5. Keep card range visible only while that card is selected and usable.
6. Test effect overlap with Zest, Humility, and Prudence where relevant.
7. Reset state on natural expiry, deck reset, room transition, floor transition,
   and leaving the game screen.
8. Update this table and add an automated or documented manual check.

## Legacy code embedded in the Kivy tree

`playerClass.py` contains an inactive triple-quoted copy of the old Pygame
player implementation after the live Kivy methods. It is useful for identifying
intended capabilities but refers to undefined Pygame types and old room fields.
Do not uncomment it piecemeal. Port one capability at a time into the live Kivy
class, with seconds-based timing and Kivy collision primitives.

Several card classes are similarly close copies of their legacy versions. Their
presence does not imply playability; use the tables above.
