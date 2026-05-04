# Resume Schema

Use this as the normalized rendering schema for the first version of the skill.

## Top-level structure

```json
{
  "meta": {
    "language": "zh",
    "target_role": "",
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
  "skills": {
    "languages": [],
    "frameworks": [],
    "databases": [],
    "infrastructure": [],
    "tools": [],
    "other": []
  },
  "projects": [],
  "experience": [],
  "awards": []
}
```

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

- Keep all lists already cleaned and display-ready before rendering.
- Use simple strings for date ranges in the renderer if the source is inconsistent.
- Omit empty sections instead of rendering placeholder headings.
- Prefer concise section payloads to protect one-page output quality.
