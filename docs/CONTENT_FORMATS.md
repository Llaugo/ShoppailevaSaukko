# Content formats

This document is the content contract for room layouts, localization, cards,
items, and sprite sheets. Update it with any format change.

## Room CSV files

`utils.readLayout` reads CSV rows as integers. One file may contain multiple
layouts. A separator is a CSV row for which every cell is empty or whitespace;
comma-only rows therefore count as separators.

| File | Layout size | Purpose |
| --- | ---: | --- |
| `rooms/roomLayouts.csv` | 15 x 15 | General lazily generated rooms |
| `rooms/startRooms.csv` | 15 x 15 | Candidate central room for each floor |
| `rooms/testRoom.csv` | 15 x 15 | Development-only room fixture |
| `rooms/lift.csv` | 5 x 5 | Between-floor lift/checkpoint room |

All rows within one layout must have the same width. Do not put a blank row
inside a layout. Standard rooms should leave a traversable doorway at the center
of each outer edge so floor-boundary logic can close only the unavailable exits.

### Raw layout codes

Raw codes are decoded by `Room.setRoom`; they are not the same as sprite-sheet
frame numbers.

| Raw code | Meaning | Current Kivy behavior |
| ---: | --- | --- |
| 0 | Wall | Runtime wall frame 9; lift wall frame 19 |
| 1 | Floor / outer doorway | Random floor frame 1-3; edge doorway frame 8; lift floor frame 4 |
| 2 | Shelf | Random shelf frame 10-18; may spawn an item |
| 3 | Lift/exit tile | Runtime frame 0 and assigned to `Room.exit` |
| 4 | Guaranteed crate | Runtime crate frame 5 and a `Crate` child |
| 40 | Probabilistic crate | Crate with `crateProbability`, otherwise ordinary floor |
| 50-53 | Cart with direction 0-3 | Currently rendered as floor; entity not ported |
| 60-63 | NPC with direction 0-3 | Currently rendered as floor; entity not ported |
| 6 | Older undirected NPC marker | Present in existing content; currently falls back to generic floor |
| 7 | Water | Runtime water frame 20 and added to `Room.waters` |
| 80-83 | Advert with direction 0-3 | Currently renders advert frame 7; entity behavior not ported |

Do not add new uses of legacy single-digit cart/NPC/advert codes. The comments
in `const.py` that describe `5`, `6`, and `8` are older than the encoded marker
scheme and should be reconciled when those systems are ported. Other positive
values currently fall through to a generic frame, but that fallback is not a
supported extension mechanism.

Direction suffixes preserve legacy orientation values `0..3` (as down, right, up, left). Their visual and
movement meaning must be covered by tests when the entity systems are ported;
do not infer a new direction order from filename or list position alone.

## Localization JSON

Locale files live at `i18n/<language-code>.json` and contain one flat JSON
object:

```json
{
  "menu.newgame": "Uusi peli",
  "game.item_button": "Poimi\nesine"
}
```

Keys use lower-case dot-separated namespaces. Current namespaces are `menu`,
`strengths`, `item`, and `game`. The runtime returns the key itself when the
selected JSON object lacks a value.

Rules:

- Finnish (`fi.json`) is the source locale and must contain every runtime key.
- Add player-visible text through translation keys, not inline Python or KV
  literals, except temporary debug text.
- Card descriptions use `strengths.card<ID>_info` for IDs `0..25`.
- Products use `item.item<1..25>`; the key, not its localized value, should be
  used by future save data.
- A non-empty locale file must be a valid UTF-8 JSON object.
- English currently uses obsolete key names and Swedish is an empty placeholder.
  Do not advertise either as supported until keys match Finnish.

## Card identity and categories

Card IDs are permanent and are used in class construction, categories, image
filenames, selection offsets, and translations.

| Category index | Category | Global IDs | Cover card |
| ---: | --- | --- | ---: |
| 0 | Wisdom and knowledge | 0-4 | 0 |
| 1 | Courage | 5-9 | 5 |
| 2 | Humanity | 10-13 | 10 |
| 3 | Justice | 14-16 | 14 |
| 4 | Temperance | 17-20 | 17 |
| 5 | Spirituality | 21-25 | 21 |

Each ID requires:

- `images/cards/card<ID>.png`;
- a matching class returned by `createStrengthCard(ID)`;
- `strengths.card<ID>_info` in the source locale;
- membership in exactly one selection category.

Append new IDs only after a deliberate format/version decision. Reordering
existing cards would silently corrupt saved selections.

## Items and rarity

There are five rarity tiers with five products in each tier. `const.shop()`
returns tiers from most common to rarest. `images/items.png` contains the 25
product frames in the same flattened order.

`const.itemRarity[distance]` is a cumulative probability distribution from the
most common tier to the rarest. Each row must:

- contain five values;
- be non-decreasing;
- contain values between 0 and 1;
- end at exactly 1.

The current 9 x 9 floor has a maximum Manhattan distance of eight from its
center, matching the nine distribution rows.

## Sprite sheets

`SpriteSheet` assumes one horizontal row of fixed-size frames and extracts frame
`n` from `(n * frame_width, 0, frame_width, frame_height)`.

| Asset | Frame size | Frames | Purpose |
| --- | ---: | ---: | --- |
| `images/player_sheet.png` | 36 x 41 | 16 | Four directions x four walk frames |
| `images/npc_sheet.png` | 36 x 41 | 16 | Legacy/future NPC animation similar to player animation |
| `images/shopsprite.png` | 46 x 46 | 21 | Room tile frames 0-20 |
| `images/strength_sheet.png` | 250 x 350 | 26 | Combined card art |
| `images/card_overlay.png` | 250 x 350 | 26 | Card state overlays |
| `images/xp_sheet.png` | 178 x 18 | 11 | Card experience/level strip. Put and updated individually for every card |
| `images/items.png` | 46 x 46 | 25 | Shopping-list product images |
| `images/item_sheet.png` | 35 x 35 | 32 | Item shine animations |
| `images/item_sheet2.png` | 19 x 19 | 32 | Alternate/legacy item animation |

Sheet width must be an exact multiple of frame width and sheet height must equal
frame height. If frame order changes, update all numeric mappings in the same
change.

Individual card PNGs and button state PNGs are used directly by KV. Preserve
their filenames unless every reference and automated check is updated.

