"""Smoke tests for scripts/render_resume.py.

Covers:
- every template renders the bundled sample without raising
- every industry sample renders cleanly
- bad inputs produce a friendly error instead of a stack trace
- language switching produces translated section titles
"""

import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RENDER = ROOT / "scripts" / "render_resume.py"
SAMPLE = ROOT / "assets" / "sample_resume.json"

sys.path.insert(0, str(ROOT / "scripts"))
import render_resume  # noqa: E402


def render_to_string(data):
    return render_resume.render(data, ROOT)


def run_cli(args, **kwargs):
    return subprocess.run(
        [sys.executable, str(RENDER), *args],
        capture_output=True,
        text=True,
        **kwargs,
    )


class TemplateSmokeTests(unittest.TestCase):
    def setUp(self):
        self.sample = json.loads(SAMPLE.read_text(encoding="utf-8"))

    def test_default_render_has_sections(self):
        html = render_to_string(self.sample)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("教育背景", html)
        self.assertIn("技术能力", html)
        self.assertIn("项目经历", html)

    def test_every_template_renders(self):
        for tmpl in render_resume.TEMPLATES:
            with self.subTest(template=tmpl):
                data = copy.deepcopy(self.sample)
                data["meta"]["template"] = tmpl
                html = render_to_string(data)
                self.assertIn("<style>", html)
                self.assertIn("</html>", html)
                self.assertGreater(html.count("<section"), 0)

    def test_unknown_template_falls_back_to_technical(self):
        data = copy.deepcopy(self.sample)
        data["meta"]["template"] = "does-not-exist"
        html = render_to_string(data)
        self.assertIn("</html>", html)


class IndustrySmokeTests(unittest.TestCase):
    def test_every_industry_sample_renders(self):
        samples_dir = ROOT / "assets" / "samples"
        samples = sorted(samples_dir.glob("*.json"))
        self.assertGreaterEqual(len(samples), 4)
        for sample_path in samples:
            with self.subTest(sample=sample_path.name):
                data = json.loads(sample_path.read_text(encoding="utf-8"))
                html = render_to_string(data)
                self.assertIn("</html>", html)
                self.assertGreater(html.count("<section"), 0)

    def test_unknown_industry_falls_back_to_tech(self):
        data = json.loads(SAMPLE.read_text(encoding="utf-8"))
        data["meta"]["industry"] = "does-not-exist"
        html = render_to_string(data)
        self.assertIn("</html>", html)

    def test_custom_section_order_is_respected(self):
        data = json.loads(SAMPLE.read_text(encoding="utf-8"))
        data["meta"]["section_order"] = ["experience", "projects", "skills", "education", "awards"]
        html = render_to_string(data)
        self.assertLess(html.index("工作经历"), html.index("项目经历"))
        self.assertLess(html.index("项目经历"), html.index("技术能力"))


class LanguageTests(unittest.TestCase):
    def test_english_labels(self):
        data = json.loads(SAMPLE.read_text(encoding="utf-8"))
        data["meta"]["language"] = "en"
        html = render_to_string(data)
        self.assertIn("Education", html)
        self.assertIn("Skills", html)
        self.assertNotIn("教育背景", html)

    def test_unknown_language_falls_back_to_zh(self):
        data = json.loads(SAMPLE.read_text(encoding="utf-8"))
        data["meta"]["language"] = "fr"
        html = render_to_string(data)
        self.assertIn("教育背景", html)


class NormalizationTests(unittest.TestCase):
    def test_string_bullets_are_normalized_to_single_item(self):
        data = {
            "basic": {"name": "Test User"},
            "experience": [{"company": "Acme", "role": "Engineer", "bullets": "Built export flow"}],
        }
        html = render_to_string(data)
        self.assertIn("<li>Built export flow</li>", html)
        self.assertNotIn("<li>B</li>", html)

    def test_skills_list_is_mapped_to_other(self):
        data = {
            "basic": {"name": "Test User"},
            "skills": ["Python", "SQL"],
        }
        html = render_to_string(data)
        self.assertIn("Python, SQL", html)

    def test_contact_line_renders_extended_fields(self):
        data = {
            "meta": {"target_role": "Staff Engineer"},
            "basic": {
                "name": "Test User",
                "email": "test@example.com",
                "location": "Shanghai",
                "website": "https://example.com",
                "github": "github.com/test",
            },
        }
        html = render_to_string(data)
        self.assertIn("test@example.com", html)
        self.assertIn("Shanghai", html)
        self.assertIn("https://example.com", html)
        self.assertIn("github.com/test", html)
        self.assertIn("Staff Engineer", html)

    def test_empty_section_items_are_dropped(self):
        data = {
            "basic": {"name": "Test User"},
            "education": [{"school": "", "degree": "", "major": "", "start_date": "", "end_date": ""}],
        }
        html = render_to_string(data)
        self.assertNotIn("教育背景", html)


class CliErrorTests(unittest.TestCase):
    def test_missing_input_exits_with_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "out.html")
            result = run_cli(["/no/such/file.json", out])
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not found", result.stderr.lower())

    def test_invalid_json_exits_with_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = os.path.join(tmp, "bad.json")
            Path(bad).write_text("{not json", encoding="utf-8")
            out = os.path.join(tmp, "out.html")
            result = run_cli([bad, out])
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid json", result.stderr.lower())

    def test_invalid_schema_exits_with_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = os.path.join(tmp, "bad.json")
            Path(bad).write_text(
                json.dumps({"basic": {"name": "Test"}, "skills": 42}),
                encoding="utf-8",
            )
            out = os.path.join(tmp, "out.html")
            result = run_cli([bad, out])
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid resume schema", result.stderr.lower())

    def test_happy_path_writes_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "out.html")
            result = run_cli([str(SAMPLE), out])
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertTrue(Path(out).exists())
            self.assertGreater(Path(out).stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()
