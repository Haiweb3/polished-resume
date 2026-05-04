# Polished Resume

A Codex skill for generating polished resumes with an `HTML -> PDF` pipeline.

Instead of writing directly to Word, this skill treats structured resume data as the source of truth, renders a clean HTML layout, and exports a stable A4 PDF with headless Chrome.

## What it does

- turns raw resume materials into a normalized resume spec
- rewrites content into tighter, result-oriented bullets
- renders a clean technical-resume HTML template
- exports the final resume to PDF

## Why this approach

Most resume generators either:

- write directly into Word and fight formatting
- over-focus on form fields and under-invest in layout quality

This skill uses HTML as the layout source of truth so the visual result is easier to control, easier to iterate, and easier to keep consistent.

## Included

- `SKILL.md`: skill instructions and workflow
- `references/`: schema, intake template, writing rules, template notes
- `assets/`: HTML template, CSS, sample resume JSON, preview image
- `scripts/render_resume.py`: JSON -> HTML renderer
- `scripts/export_pdf.js`: HTML -> PDF exporter via headless Chrome

## Requirements

- Python 3
- Node.js
- Google Chrome or Chromium

If Chrome is not installed in the default location, set:

```bash
export CHROME_PATH="/path/to/Google Chrome"
```

## Install as a Codex skill

Clone this repository into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/Haiweb3/polished-resume.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/polished-resume"
```

After that, Codex can discover the skill from:

```text
${CODEX_HOME:-$HOME/.codex}/skills/polished-resume
```

## Quick start

The fastest way to try it is:

1. Copy the sample JSON.
2. Replace the sample fields with your own resume data.
3. Render HTML.
4. Export PDF.

Example:

```bash
cp assets/sample_resume.json /tmp/my_resume.json

# Edit /tmp/my_resume.json with your own data first

python3 scripts/render_resume.py /tmp/my_resume.json /tmp/resume.html
node scripts/export_pdf.js /tmp/resume.html /tmp/resume.pdf
```

The final file will be written to:

```text
/tmp/resume.pdf
```

## Input format

The renderer currently expects structured JSON.

Start from:

- `assets/sample_resume.json`
- `references/schema.md`
- `references/intake-template.md`

Recommended flow:

1. Draft your resume content in `references/intake-template.md`
2. Convert it into the JSON shape from `references/schema.md`
3. Save that JSON to a file
4. Run the renderer and exporter

## Minimal workflow

Render HTML:

```bash
python3 scripts/render_resume.py input.json output.html
```

Export PDF:

```bash
node scripts/export_pdf.js output.html output.pdf
```

## Example project layout

```text
polished-resume/
├── SKILL.md
├── README.md
├── assets/
│   ├── template.html
│   ├── base.css
│   └── sample_resume.json
├── references/
│   ├── schema.md
│   ├── intake-template.md
│   ├── writing-rules.md
│   └── template-notes.md
└── scripts/
    ├── render_resume.py
    └── export_pdf.js
```

## Preview

![Preview](assets/preview.png)

## Scope

Current version:

- optimized for concise technical resumes
- one-page A4 bias
- single template
- `HTML -> PDF` only

Not included yet:

- DOCX export
- multiple templates
- direct Markdown parser
- ATS-specific branching

## License

MIT
