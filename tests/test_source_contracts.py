from __future__ import annotations

import ast
import re
import unittest
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]


class PythonSourceContracts(unittest.TestCase):
    def test_python_sources_compile_without_importing_kivy(self) -> None:
        paths = sorted(ROOT.glob("*.py")) + sorted((ROOT / "tests").glob("*.py"))
        self.assertTrue(paths)
        for path in paths:
            with self.subTest(path=path.name):
                source = path.read_text(encoding="utf-8")
                compile(source, str(path), "exec", dont_inherit=True)

    def test_python_id_references_exist_in_kv(self) -> None:
        kv_source = (ROOT / "shopper.kv").read_text(encoding="utf-8")
        kv_ids = set(re.findall(r"^\s*id:\s*([A-Za-z_]\w*)", kv_source, re.MULTILINE))

        referenced: set[str] = set()
        for path in ROOT.glob("*.py"):
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Attribute):
                    continue
                if not isinstance(node.value, ast.Attribute) or node.value.attr != "ids":
                    continue
                if node.attr != "get":
                    referenced.add(node.attr)

        missing = referenced - kv_ids
        self.assertFalse(missing, f"Python references KV ids that do not exist: {sorted(missing)}")


class DocumentationContracts(unittest.TestCase):
    def test_local_markdown_links_resolve(self) -> None:
        markdown_paths = [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "ROADMAP.md"]
        markdown_paths.extend(sorted((ROOT / "docs").rglob("*.md")))
        link_pattern = re.compile(r"!?\[[^]]*\]\(([^)]+)\)")
        missing: list[str] = []

        for path in markdown_paths:
            source = path.read_text(encoding="utf-8")
            for raw_target in link_pattern.findall(source):
                target = raw_target.strip().split("#", 1)[0]
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                resolved = path.parent / unquote(target.strip("<>"))
                if not resolved.exists():
                    missing.append(f"{path.relative_to(ROOT)}: {raw_target}")

        self.assertFalse(missing, "Broken local Markdown links:\n" + "\n".join(missing))


if __name__ == "__main__":
    unittest.main()
