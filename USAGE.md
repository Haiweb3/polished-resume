# Using Polished Resume

This repository can be used in two ways:

1. As a local rendering tool that turns structured JSON into HTML and PDF.
2. As a Codex / Claude skill that helps turn raw resume material into a polished final document.

## 1. Install the repository

Clone the repo:

```bash
git clone https://github.com/Haiweb3/polished-resume.git
cd polished-resume
```

Requirements:

- Python 3.10+
- Node.js
- Google Chrome or Chromium

If Chrome is installed in a non-standard location:

```bash
export CHROME_PATH="/path/to/Google Chrome"
```

## 2. Prepare the input

The renderer expects JSON. Start from one of these:

- `assets/sample_resume.json`
- `assets/samples/*.json`
- `references/intake-template.md`
- `references/schema.md`

Recommended flow:

1. Collect the candidate's raw source material.
2. If the source is messy, first put it into `references/intake-template.md`.
3. Rewrite it into concise resume bullets.
4. Normalize it into the JSON schema.
5. Set `meta.template` and `meta.industry`.

Minimal example:

```json
{
  "meta": {
    "language": "en",
    "template": "modern",
    "industry": "tech",
    "target_role": "Senior Backend Engineer"
  },
  "basic": {
    "name": "Jane Doe",
    "title": "Backend Engineer",
    "email": "jane@example.com",
    "phone": "+1 555 000 0000",
    "location": "San Francisco, CA",
    "website": "https://janedoe.dev",
    "github": "github.com/janedoe",
    "linkedin": "linkedin.com/in/janedoe"
  },
  "experience": [
    {
      "company": "Acme",
      "role": "Senior Engineer",
      "start_date": "2022.03",
      "end_date": "Present",
      "bullets": [
        "Led migration of the billing API to event-driven workflows, cutting reconciliation time by 63%.",
        "Designed observability and retry controls for payment webhooks across 12 partner integrations."
      ]
    }
  ],
  "projects": [],
  "education": [],
  "skills": {
    "languages": ["Python", "Go", "SQL"],
    "frameworks": ["FastAPI", "gRPC"],
    "infrastructure": ["AWS", "Docker", "Kubernetes"]
  },
  "awards": []
}
```

## 3. Render HTML

If you are starting from a markdown intake file, convert it first:

```bash
python3 scripts/intake_to_json.py ./resume-intake.md ./out/resume.json
```

Then render:

```bash
python3 scripts/render_resume.py ./out/resume.json ./out/resume.html
```

What the renderer does:

- validates and normalizes the resume schema
- inlines CSS into the HTML
- escapes HTML-sensitive content
- drops empty sections
- falls back on unknown `language`, `template`, and `industry`

Input guardrails:

- `skills` can be an object or a flat list of strings
- `bullets` and `honors` can be either a string or a list of strings
- invalid schema shape exits with a clear error instead of a Python traceback

You can also override section order:

```json
{
  "meta": {
    "section_order": ["experience", "projects", "skills", "education", "awards"]
  }
}
```

Valid section names are:

- `education`
- `skills`
- `projects`
- `experience`
- `awards`

## 4. Export PDF

```bash
node scripts/export_pdf.js ./out/resume.html ./out/resume.pdf
```

If the export succeeds, you will get a stable A4 PDF suitable for review and delivery.

## 5. Use as a skill

### Codex

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/Haiweb3/polished-resume.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/polished-resume"
```

### Claude Code

```bash
mkdir -p "${CLAUDE_HOME:-$HOME/.claude}/skills"
git clone https://github.com/Haiweb3/polished-resume.git \
  "${CLAUDE_HOME:-$HOME/.claude}/skills/polished-resume"
```

Then ask the host agent to use the skill on:

- a markdown intake form
- an old resume
- scattered experience / education / projects / skills notes

Recommended prompt pattern:

```text
Use polished-resume to turn these materials into a one-page modern tech resume in English.
```

Be explicit about:

- target role
- language
- template
- industry
- whether you are starting from an intake form or a previous resume
- whether you want one page or denser content

## 6. Check the output

After PDF export, verify:

- page count
- section order
- no clipped bullets
- no awkward line wraps in the header
- no weak or repetitive bullets

If layout is crowded, shorten content before reducing type size.
