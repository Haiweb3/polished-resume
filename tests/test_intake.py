"""Tests for scripts/intake_to_json.py."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INTAKE = ROOT / "scripts" / "intake_to_json.py"

sys.path.insert(0, str(ROOT / "scripts"))
import intake_to_json  # noqa: E402


SAMPLE_INTAKE = """# Resume Input

## Basic Info
- Name: Jane Doe
- Title: Senior Backend Engineer
- Phone: +1 555 000 0000
- Email: jane@example.com
- Location: San Francisco, CA
- Website: https://janedoe.dev
- GitHub: github.com/janedoe
- LinkedIn: linkedin.com/in/janedoe

## Target
- Target Role: Staff Engineer
- Language: en
- Style Hint: concise
- Template: modern
- Industry: tech
- Section Order: experience, projects, skills, education, awards

## Education
### Education 1
- School: Example University
- Degree: BS
- Major: Computer Science
- Start: 2015
- End: 2019
- Honors: Dean's List, Scholarship

## Experience
### Experience 1
- Company: Acme
- Role: Senior Engineer
- Start: 2022
- End: Present
- Summary: Led platform modernization across billing services.
- Achievements:
  - Reduced API latency by 42%.
  - Introduced event-driven retries for failed payment webhooks.

## Projects
### Project 1
- Name: Resume Engine
- Subtitle: Internal Tool
- Start: 2023
- End: 2024
- Details:
  - Built HTML-to-PDF export workflow.
  - Added template switching for multiple resume styles.

## Skills
- Languages: Python, Go, SQL
- Frameworks: FastAPI / gRPC
- Infrastructure: AWS, Docker

## Awards
- Award: Engineering Excellence
- Issuer: Acme
- Date: 2024
- Note: Recognized for platform migration leadership.
"""


def run_cli(args):
    return subprocess.run(
        [sys.executable, str(INTAKE), *args],
        capture_output=True,
        text=True,
    )


class IntakeParserTests(unittest.TestCase):
    def test_parse_intake_returns_normalized_resume(self):
        data = intake_to_json.parse_intake(SAMPLE_INTAKE)
        self.assertEqual(data["meta"]["language"], "en")
        self.assertEqual(data["meta"]["template"], "modern")
        self.assertEqual(data["meta"]["section_order"][0], "experience")
        self.assertEqual(data["basic"]["github"], "github.com/janedoe")
        self.assertEqual(data["experience"][0]["bullets"][0], "Led platform modernization across billing services.")
        self.assertIn("Reduced API latency by 42%.", data["experience"][0]["bullets"])
        self.assertEqual(data["projects"][0]["bullets"][0], "Built HTML-to-PDF export workflow.")
        self.assertEqual(data["awards"][0]["issuer"], "Acme")

    def test_cli_writes_json_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            intake_path = Path(tmp) / "resume.md"
            output_path = Path(tmp) / "resume.json"
            intake_path.write_text(SAMPLE_INTAKE, encoding="utf-8")

            result = run_cli([str(intake_path), str(output_path)])

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            data = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(data["basic"]["name"], "Jane Doe")
            self.assertEqual(data["skills"]["languages"], ["Python", "Go", "SQL"])

    def test_invalid_intake_exits_with_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            intake_path = Path(tmp) / "resume.md"
            output_path = Path(tmp) / "resume.json"
            intake_path.write_text("## Unknown\n- Foo: Bar\n", encoding="utf-8")

            result = run_cli([str(intake_path), str(output_path)])

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid intake", result.stderr.lower())

    def test_template_placeholders_are_not_kept_as_values(self):
        template_text = (ROOT / "references" / "intake-template.md").read_text(encoding="utf-8")
        data = intake_to_json.parse_intake(template_text)
        self.assertEqual(data["meta"]["language"], "zh")
        self.assertEqual(data["meta"]["template"], "technical")
        self.assertEqual(data["meta"]["industry"], "tech")
        self.assertEqual(data["education"], [])
        self.assertEqual(data["experience"], [])


if __name__ == "__main__":
    unittest.main()
