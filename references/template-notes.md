# Template Notes

Each template lives in `assets/templates/<name>/` and ships its own `template.html` + `style.css`.

## Available templates

| Name | Look | Best for |
| --- | --- | --- |
| `technical` | Times serif, blue section headers, dense | Engineering / backend / infra |
| `modern` | Sans-serif, lots of whitespace, minimal accent | Internet product / design / startup |
| `classic` | Garamond / Georgia serif, B&W, centered header | Finance / law / traditional enterprise |
| `compact` | Smaller font, tight spacing | Senior people with multi-page content |
| `creative` | Colored hero band, pill section titles, dotted bullets | Brand / marketing / consumer roles |

All templates share the same data contract: `{{lang}}`, `{{name}}`, `{{title}}`, `{{page_label}}`, `{{contact_line}}`, `{{inline_css}}`, `{{sections}}`.

## Layout assumptions

- A4 page size across all templates.
- One-page bias except for `compact`, which assumes content density.
- Mixed Chinese + English content is supported by all templates.
- The renderer hands the template already-curated content; templates don't reshape data.

## When content overflows

Adjust content first:

- cut low-value awards
- shorten skills
- merge similar bullets
- reduce project detail

If content is already tight, switch to `compact`. Avoid hand-editing template CSS for a single resume; that breaks reproducibility.

## Adding a new template

1. Create `assets/templates/<name>/template.html` with the standard placeholders.
2. Create `assets/templates/<name>/style.css`.
3. Add `<name>` to `TEMPLATES` in `scripts/render_resume.py`.
4. Add a `with self.subTest(template=...)` row in `tests/test_render.py` if any new placeholder is introduced (the existing loop already covers visual variants).

## What to defer

- DOCX export
- ATS-specific branching
- Photo-heavy variants
- Sidebar layouts that break the single-column data flow
