# Polished Resume

[![ci](https://github.com/Haiweb3/polished-resume/actions/workflows/ci.yml/badge.svg)](https://github.com/Haiweb3/polished-resume/actions/workflows/ci.yml)

A skill for generating polished PDF resumes with an `HTML -> PDF` pipeline. Works with **Claude Code / Claude Skills** and **Codex**.

Instead of fighting Word, this skill treats structured resume data as the source of truth, renders a clean HTML layout with a chosen template, and exports a stable A4 PDF via headless Chrome.

## What it does

- Normalizes raw resume materials into a structured spec
- Rewrites content into tighter, result-oriented bullets
- Renders one of **5 visual templates × 5 industry presets** to HTML
- Exports the final resume to PDF

## Templates & industries

Two independent axes — pick any combination.

| Template | Look |
| --- | --- |
| `technical` (default) | Times serif, blue section headers, dense |
| `modern` | Sans-serif, generous whitespace, minimal accent |
| `classic` | Garamond/Georgia serif, B&W, formal |
| `compact` | Smaller font, tight spacing for senior people |
| `creative` | Colored hero band, pill section titles |

| Industry | Skill categories |
| --- | --- |
| `tech` (default) | Languages / Frameworks / Databases / Infrastructure / Tools |
| `design` | Software / Specialties / Deliverables / Methodology / Tools |
| `business` | Tools / Methodologies / Domains / Languages / Certifications |
| `academic` | Research Areas / Methods / Tools / Publications / Languages |
| `marketing` | Channels / Content / Analytics / Platforms / Tools |

Set them in your JSON:

```json
{
  "meta": {
    "language": "zh",
    "template": "modern",
    "industry": "design"
  }
}
```

## Requirements

- Python 3.10+
- Node.js
- Google Chrome or Chromium

If Chrome is not in the default location, set:

```bash
export CHROME_PATH="/path/to/Google Chrome"
```

## Install

### As a Claude Code / Claude Skill

```bash
mkdir -p "${CLAUDE_HOME:-$HOME/.claude}/skills"
git clone https://github.com/Haiweb3/polished-resume.git \
  "${CLAUDE_HOME:-$HOME/.claude}/skills/polished-resume"
```

### As a Codex skill

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/Haiweb3/polished-resume.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/polished-resume"
```

The frontmatter in `SKILL.md` is the universal Anthropic skill format — the same checkout works for both hosts.

## Quick start

```bash
cp assets/sample_resume.json /tmp/my_resume.json
# edit /tmp/my_resume.json with your data; pick template + industry in meta

python3 scripts/render_resume.py /tmp/my_resume.json /tmp/resume.html
node scripts/export_pdf.js /tmp/resume.html /tmp/resume.pdf
```

The HTML is self-contained (CSS is inlined), so you can also open `/tmp/resume.html` directly in a browser.

### Industry samples

Each industry preset ships with a realistic example under `assets/samples/`:

```bash
python3 scripts/render_resume.py assets/samples/design.json /tmp/design.html
python3 scripts/render_resume.py assets/samples/business.json /tmp/business.html
python3 scripts/render_resume.py assets/samples/academic.json /tmp/academic.html
python3 scripts/render_resume.py assets/samples/marketing.json /tmp/marketing.html
```

## Input format

The renderer expects structured JSON. Start from:

- `assets/sample_resume.json` — minimal tech sample
- `assets/samples/*.json` — per-industry examples
- `references/schema.md` — full schema reference
- `references/intake-template.md` — markdown intake for new candidates

## Project layout

```text
polished-resume/
├── SKILL.md
├── README.md
├── assets/
│   ├── sample_resume.json
│   ├── samples/                  # one per industry
│   │   ├── design.json
│   │   ├── business.json
│   │   ├── academic.json
│   │   └── marketing.json
│   └── templates/                # one folder per visual template
│       ├── technical/
│       ├── modern/
│       ├── classic/
│       ├── compact/
│       └── creative/
├── references/
│   ├── schema.md
│   ├── intake-template.md
│   ├── writing-rules.md
│   └── template-notes.md
├── scripts/
│   ├── render_resume.py
│   └── export_pdf.js
└── tests/
    └── test_render.py
```

## Preview

![Preview](assets/preview.png)

## Testing

```bash
python3 -m unittest discover -s tests
```

CI runs on every push and pull request across Python 3.10 / 3.11 / 3.12.

## Scope

Current version:

- 5 templates × 5 industries
- A4 one-page bias (except `compact`)
- HTML -> PDF only

Not included yet:

- DOCX export
- direct Markdown parser
- ATS-specific keyword tuning

## License

MIT
