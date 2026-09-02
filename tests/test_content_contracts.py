from __future__ import annotations

import ast
import csv
import json
import re
import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROOMS = ROOT / "rooms"
I18N = ROOT / "i18n"
IMAGES = ROOT / "images"

STANDARD_LAYOUT_FILES = (
    "roomLayouts.csv",
    "startRooms.csv",
    "testRoom.csv",
)

ALLOWED_LAYOUT_CODES = {
    0,
    1,
    2,
    3,
    4,
    6,  # Older undirected NPC marker; currently decodes as generic floor.
    7,
    40,
    *range(50, 54),
    *range(60, 64),
    *range(80, 84),
}

CARD_CLASSES = (
    "CreativityCard",
    "CuriosityCard",
    "JudgementCard",
    "LearningCard",
    "PerspectiveCard",
    "BraveryCard",
    "PerseveranceCard",
    "HonestyCard",
    "ZestCard",
    "GritCard",
    "KindnessCard",
    "LoveCard",
    "SocialCard",
    "CompassionCard",
    "FairnessCard",
    "LeadershipCard",
    "TeamworkCard",
    "ForgivenessCard",
    "HumilityCard",
    "PrudenceCard",
    "RegulationCard",
    "AppreciationCard",
    "GratitudeCard",
    "HopeCard",
    "HumorCard",
    "SpiritualityCard",
)

CARD_CATEGORIES = (
    tuple(range(0, 5)),
    tuple(range(5, 10)),
    tuple(range(10, 14)),
    tuple(range(14, 17)),
    tuple(range(17, 21)),
    tuple(range(21, 26)),
)

SPRITE_SHEETS = {
    "player_sheet.png": ((36, 41), 16),
    "npc_sheet.png": ((36, 41), 16),
    "shopsprite.png": ((46, 46), 21),
    "strength_sheet.png": ((250, 350), 26),
    "card_overlay.png": ((250, 350), 26),
    "xp_sheet.png": ((178, 18), 11),
    "items.png": ((46, 46), 25),
    "item_sheet.png": ((35, 35), 32),
    "item_sheet2.png": ((19, 19), 32),
}


def read_layouts(path: Path) -> list[list[list[int]]]:
    layouts: list[list[list[int]]] = []
    current: list[list[int]] = []

    with path.open(newline="", encoding="utf-8") as handle:
        for line_number, row in enumerate(csv.reader(handle), start=1):
            if not row or all(not cell.strip() for cell in row):
                if current:
                    layouts.append(current)
                    current = []
                continue

            if any(not cell.strip() for cell in row):
                raise AssertionError(f"{path.name}:{line_number} contains an empty tile cell")
            try:
                current.append([int(cell.strip()) for cell in row])
            except ValueError as error:
                raise AssertionError(
                    f"{path.name}:{line_number} contains a non-integer tile code"
                ) from error

    if current:
        layouts.append(current)
    return layouts


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError(f"{path} is not a readable PNG")
    return struct.unpack(">II", header[16:24])


def is_exact_case_file(relative: str) -> bool:
    current = ROOT
    for part in Path(relative).parts:
        entries = {entry.name: entry for entry in current.iterdir()}
        if part not in entries:
            return False
        current = entries[part]
    return current.is_file()


def literal_assignment(tree: ast.AST, name: str):
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == name for target in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError(f"Could not find literal assignment {name}")


class RoomLayoutContracts(unittest.TestCase):
    def test_layout_dimensions(self) -> None:
        for filename in STANDARD_LAYOUT_FILES:
            with self.subTest(filename=filename):
                layouts = read_layouts(ROOMS / filename)
                self.assertTrue(layouts, f"{filename} must contain at least one layout")
                for index, layout in enumerate(layouts):
                    self.assertEqual(
                        len(layout),
                        15,
                        f"{filename} layout {index} must contain 15 rows",
                    )
                    self.assertTrue(
                        all(len(row) == 15 for row in layout),
                        f"{filename} layout {index} must contain 15 columns per row",
                    )

        lift_layouts = read_layouts(ROOMS / "lift.csv")
        self.assertEqual(len(lift_layouts), 1)
        self.assertEqual(len(lift_layouts[0]), 5)
        self.assertTrue(all(len(row) == 5 for row in lift_layouts[0]))

    def test_layout_codes_are_documented(self) -> None:
        for path in sorted(ROOMS.glob("*.csv")):
            for layout_index, layout in enumerate(read_layouts(path)):
                values = {value for row in layout for value in row}
                unknown = values - ALLOWED_LAYOUT_CODES
                self.assertFalse(
                    unknown,
                    f"{path.name} layout {layout_index} has undocumented codes: {sorted(unknown)}",
                )

    def test_standard_rooms_have_centered_edge_entry_points(self) -> None:
        for filename in STANDARD_LAYOUT_FILES:
            for layout_index, layout in enumerate(read_layouts(ROOMS / filename)):
                middle = len(layout) // 2
                edge_values = (
                    layout[0][middle],
                    layout[-1][middle],
                    layout[middle][0],
                    layout[middle][-1],
                )
                self.assertEqual(
                    edge_values,
                    (1, 1, 1, 1),
                    f"{filename} layout {layout_index} must expose four centered doorways",
                )


class LocalizationContracts(unittest.TestCase):
    def test_source_locale_contains_runtime_keys(self) -> None:
        finnish = json.loads((I18N / "fi.json").read_text(encoding="utf-8"))
        self.assertIsInstance(finnish, dict)

        key_pattern = re.compile(r'(?:app|utils|self)\.tr\(\s*f?["\']([^"\']+)["\']')
        required: set[str] = set()
        for path in [*ROOT.glob("*.py"), ROOT / "shopper.kv"]:
            for key in key_pattern.findall(path.read_text(encoding="utf-8")):
                if "{" not in key:
                    required.add(key)
        required.update(f"strengths.card{card_id}_info" for card_id in range(26))

        missing = required - set(finnish)
        self.assertFalse(missing, f"fi.json is missing runtime keys: {sorted(missing)}")
        self.assertTrue(all(isinstance(value, str) for value in finnish.values()))

    def test_non_empty_locale_files_are_json_objects(self) -> None:
        for path in sorted(I18N.glob("*.json")):
            with self.subTest(locale=path.stem):
                source = path.read_text(encoding="utf-8").strip()
                if not source:
                    # Empty files are allowed only as documented unsupported placeholders.
                    self.assertNotEqual(path.stem, "fi")
                    continue
                self.assertIsInstance(json.loads(source), dict)


class CardAndItemContracts(unittest.TestCase):
    def test_card_categories_cover_every_stable_id_once(self) -> None:
        flattened = [card_id for category in CARD_CATEGORIES for card_id in category]
        self.assertEqual(flattened, list(range(26)))
        self.assertEqual(len(flattened), len(set(flattened)))

    def test_card_classes_factory_images_and_text_align(self) -> None:
        source = (ROOT / "strengthCard.py").read_text(encoding="utf-8")
        tree = ast.parse(source, filename="strengthCard.py")
        defined_classes = {
            node.name for node in tree.body if isinstance(node, ast.ClassDef)
        }
        self.assertTrue(set(CARD_CLASSES).issubset(defined_classes))

        factory = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "createStrengthCard"
        )
        mapping: dict[int, str] = {}
        for node in ast.walk(factory):
            if not isinstance(node, ast.If) or not isinstance(node.test, ast.Compare):
                continue
            compare = node.test
            if not (
                isinstance(compare.left, ast.Name)
                and compare.left.id == "n"
                and len(compare.ops) == 1
                and isinstance(compare.ops[0], ast.Eq)
                and len(compare.comparators) == 1
                and isinstance(compare.comparators[0], ast.Constant)
                and isinstance(compare.comparators[0].value, int)
            ):
                continue
            returns = [item for item in node.body if isinstance(item, ast.Return)]
            if not returns or not isinstance(returns[0].value, ast.Call):
                continue
            call = returns[0].value
            if isinstance(call.func, ast.Name):
                mapping[compare.comparators[0].value] = call.func.id

        self.assertEqual(mapping, dict(enumerate(CARD_CLASSES)))

        finnish = json.loads((I18N / "fi.json").read_text(encoding="utf-8"))
        for card_id, class_name in enumerate(CARD_CLASSES):
            with self.subTest(card_id=card_id, class_name=class_name):
                image = IMAGES / "cards" / f"card{card_id}.png"
                self.assertTrue(image.is_file())
                self.assertEqual(png_dimensions(image), (250, 350))
                self.assertIn(f"strengths.card{card_id}_info", finnish)

    def test_gratitude_card_never_uses_the_active_overlay(self) -> None:
        tree = ast.parse((ROOT / "strengthCard.py").read_text(encoding="utf-8"))
        gratitude = next(
            node
            for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == "GratitudeCard"
        )
        setting = next(
            node
            for node in gratitude.body
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "showActiveOverlay"
                for target in node.targets
            )
        )
        self.assertIs(ast.literal_eval(setting.value), False)

    def test_item_rarity_is_cumulative_and_covers_floor_distance(self) -> None:
        tree = ast.parse((ROOT / "const.py").read_text(encoding="utf-8"))
        distributions = literal_assignment(tree, "itemRarity")
        floor_size = literal_assignment(tree, "floorSize")

        expected_distances = 2 * (floor_size // 2) + 1
        self.assertEqual(len(distributions), expected_distances)
        for distance, row in enumerate(distributions):
            with self.subTest(distance=distance):
                self.assertEqual(len(row), 5)
                self.assertEqual(row, sorted(row))
                self.assertTrue(all(0 <= value <= 1 for value in row))
                self.assertEqual(row[-1], 1)


class AssetContracts(unittest.TestCase):
    def test_static_asset_references_exist_with_exact_case(self) -> None:
        pattern = re.compile(
            r'(?P<path>(?:images|fonts|rooms|i18n)/[A-Za-z0-9_./-]+'
            r'\.(?:png|ttf|csv|json))'
        )
        missing: list[str] = []
        for source_path in [*ROOT.glob("*.py"), ROOT / "shopper.kv"]:
            source = source_path.read_text(encoding="utf-8")
            for relative in pattern.findall(source):
                if not is_exact_case_file(relative):
                    missing.append(f"{source_path.name}: {relative}")
        self.assertFalse(missing, "Missing static assets:\n" + "\n".join(missing))

    def test_sprite_sheet_geometry(self) -> None:
        for filename, (frame_size, frame_count) in SPRITE_SHEETS.items():
            with self.subTest(filename=filename):
                width, height = png_dimensions(IMAGES / filename)
                self.assertEqual(height, frame_size[1])
                self.assertEqual(width, frame_size[0] * frame_count)

    def test_navigation_stone_art_size_matches_its_widget_bounds(self) -> None:
        tree = ast.parse((ROOT / "navigationStone.py").read_text(encoding="utf-8"))
        art_size = literal_assignment(tree, "STONE_ART_SIZE")
        self.assertEqual(png_dimensions(IMAGES / "stone.png"), art_size)


if __name__ == "__main__":
    unittest.main()
