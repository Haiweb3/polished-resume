# Resume Schema

Normalized rendering schema used by `scripts/render_resume.py`.

## Top-level structure

```json
{
  "meta": {
    "language": "zh",
    "target_role": "",
    "template": "technical",
    "industry": "tech",
    "style_hint": "professional"
  },
  "basic": {
    "name": "",
    "title": "",
    "phone": "",
    "email": "",
    "location": "",
    "website": "",
    "github": "",
    "linkedin": ""
  },
  "education": [],
  "skills": {},
  "projects": [],
  "experience": [],
  "awards": []
}
```

## meta

Two independent axes drive the output:

| Field | Values | Effect |
| --- | --- | --- |
| `language` | `zh`, `en` | Section labels and skill category labels. Defaults to `zh`. Unknown values warn and fall back to `zh`. |
| `template` | `technical`, `modern`, `classic`, `compact`, `creative` | Visual style only (typography, colors, spacing). Defaults to `technical`. |
| `industry` | `tech`, `design`, `business`, `academic`, `marketing` | Skill category keys and section order. Defaults to `tech`. |

`template` and `industry` are orthogonal — any combination is valid.

## skills

The shape of `skills` depends on `meta.industry`:

| Industry | Expected keys |
| --- | --- |
| `tech` | `languages`, `frameworks`, `databases`, `infrastructure`, `tools`, `other` |
| `design` | `software`, `specialties`, `output`, `methodology`, `tools`, `other` |
| `business` | `tools`, `methodologies`, `domains`, `languages`, `certifications`, `other` |
| `academic` | `research_areas`, `methods`, `tools`, `publications`, `languages`, `other` |
| `marketing` | `channels`, `content`, `analytics`, `platforms`, `tools`, `other` |

Empty categories are dropped. Unknown keys are still rendered, with the key itself (Title Cased) used as the label.

## Education item

```json
{
  "school": "",
  "degree": "",
  "major": "",
  "start_date": "",
  "end_date": "",
  "honors": []
}
```

## Project item

```json
{
  "name": "",
  "subtitle": "",
  "start_date": "",
  "end_date": "",
  "bullets": []
}
```

## Experience item

```json
{
  "company": "",
  "role": "",
  "start_date": "",
  "end_date": "",
  "bullets": []
}
```

## Awards item

```json
{
  "name": "",
  "issuer": "",
  "date": "",
  "note": ""
}
```

## Rendering rules

- Keep lists curated and display-ready before rendering.
- Use simple strings for date ranges when the source is inconsistent.
- Empty sections are omitted; no placeholder headings.
- Prefer concise section payloads to protect one-page output.
