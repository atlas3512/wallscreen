from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import wps  # noqa: E402

PACK = ROOT / "packs" / "aurora-night" / "aurora-01"
MANIFEST = PACK / "wallpaper.pack.json"


class SchemaTests(unittest.TestCase):
    def test_schema_is_valid_draft_2020_12(self) -> None:
        from jsonschema import Draft202012Validator

        schema = json.loads(wps.SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)

    def test_reference_pack_validates(self) -> None:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(wps.validate_pack(PACK, data), [])

    def test_broken_pack_is_rejected(self) -> None:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        data["id"] = "different-theme.aurora-01"
        errors = wps.validate_pack(PACK, data)
        self.assertTrue(any("id prefix" in error for error in errors))


class GeometryTests(unittest.TestCase):
    def test_crop_keeps_safe_area(self) -> None:
        box = wps.crop_box(
            1000, 500, (1, 1),
            {"x": 0.4, "y": 0.2, "w": 0.2, "h": 0.6},
        )
        # 500x500 crop; x must contain 400..600, y must contain 100..400.
        self.assertEqual(box, (250, 0, 750, 500))

    def test_portrait_override_fits(self) -> None:
        box = wps.crop_box(
            7680, 4320, (9, 16),
            {"x": 0.42, "y": 0.05, "w": 0.16, "h": 0.9},
        )
        x0, y0, x1, y1 = box
        safe = (0.42 * 7680, 0.05 * 4320, 0.58 * 7680, 0.95 * 4320)
        self.assertLessEqual(x0, safe[0] + 1)
        self.assertGreaterEqual(x1, safe[2] - 1)
        self.assertLessEqual(y0, safe[1] + 1)
        self.assertGreaterEqual(y1, safe[3] - 1)


class RenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        wps.ensure_master(PACK, data)

    def test_render_16x9(self) -> None:
        from PIL import Image

        with tempfile.TemporaryDirectory() as tmp:
            records = wps.render_pack(PACK, Path(tmp), ["16:9"])
            self.assertEqual(len(records), 3)
            for record in records:
                target = Path(tmp) / record["path"]
                self.assertTrue(target.is_file())
                with Image.open(target) as image:
                    self.assertEqual(image.format, "JPEG")
                    self.assertEqual(image.size, (record["width"], record["height"]))
                    self.assertEqual(image.mode, "RGB")
            checksums = (Path(tmp) / "checksums.sha256").read_text(encoding="utf-8")
            self.assertEqual(len(checksums.strip().splitlines()), 3)
            index = json.loads((Path(tmp) / "index.json").read_text(encoding="utf-8"))
            self.assertIn("aurora-night.aurora-01", index["packs"])


class AdapterTests(unittest.TestCase):
    def test_all_targets_emit_config(self) -> None:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        chosen = {"path": "aurora-night/aurora-01/dark/16:9/3840x2160.jpg"}
        for target in data["targets"]:
            with self.subTest(target=target):
                filename, text = wps.adapter_config(target, chosen, data)
                self.assertTrue(filename)
                self.assertIn(chosen["path"], text)

    def test_capabilities_cover_all_targets(self) -> None:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        capabilities = wps.load_capabilities()
        for target in data["targets"]:
            self.assertIn(target, capabilities)


if __name__ == "__main__":
    unittest.main()
