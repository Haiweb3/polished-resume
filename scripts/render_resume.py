#!/usr/bin/env python3

import html
import json
import shutil
import sys
from pathlib import Path


def escape(value):
    return html.escape(str(value), quote=True)


def compact(items):
    return [item for item in items if item]


def format_date_range(start, end):
    start = (start or "").strip()
    end = (end or "").strip()
    if start and end:
        return f"{escape(start)} - {escape(end)}"
    return escape(start or end)


def section(title, body):
    if not body.strip():
        return ""
    return (
        '<section class="section">'
        f'<h2 class="section-title">{escape(title)}</h2>'
        f"{body}"
        "</section>"
    )


def render_education(items):
    rows = []
    for item in items:
      school = escape(item.get("school", ""))
      degree = escape(item.get("degree", ""))
      major = escape(item.get("major", ""))
      left = " ".join(compact([school, degree, major]))
      date_range = format_date_range(item.get("start_date"), item.get("end_date"))
      honors = item.get("honors", [])
      honors_html = ""
      if honors:
          honors_html = f'<p class="text">{" / ".join(escape(x) for x in honors if x)}</p>'
      rows.append(
          '<div class="row">'
          '<div class="row-main">'
          f'<p class="item-title">{left}</p>'
          f"{honors_html}"
          '</div>'
          f'<div class="row-side">{date_range}</div>'
          '</div>'
      )
    return section("教育背景", "".join(rows))


def render_skills(skills):
    labels = [
        ("编程语言", skills.get("languages", [])),
        ("后端框架", skills.get("frameworks", [])),
        ("中间件 & 数据库", skills.get("databases", [])),
        ("分布式 & 运维", skills.get("infrastructure", [])),
        ("工具", skills.get("tools", [])),
        ("其他", skills.get("other", [])),
    ]
    items = []
    for label, values in labels:
        values = [escape(v) for v in values if v]
        if not values:
            continue
        items.append(
            f'<li><span class="label">{escape(label)}:</span> {", ".join(values)}</li>'
        )
    if not items:
        return ""
    return section("技术能力", f'<ul class="skills-list">{"".join(items)}</ul>')


def render_bulleted_rows(title, items, name_key, subtitle_key=None):
    rows = []
    for item in items:
        name = escape(item.get(name_key, ""))
        subtitle = escape(item.get(subtitle_key, "")) if subtitle_key else ""
        title_line = name
        if subtitle:
            title_line += f" <span class=\"item-subtitle\">({subtitle})</span>"
        date_range = format_date_range(item.get("start_date"), item.get("end_date"))
        bullets = item.get("bullets", [])
        bullet_html = "".join(f"<li>{escape(b)}</li>" for b in bullets if b)
        rows.append(
            '<div class="row">'
            '<div class="row-main">'
            f'<p class="item-title">{title_line}</p>'
            f'<ul class="bullet-list">{bullet_html}</ul>'
            '</div>'
            f'<div class="row-side">{date_range}</div>'
            '</div>'
        )
    return section(title, "".join(rows))


def render_experience(items):
    rows = []
    for item in items:
        company = escape(item.get("company", ""))
        role = escape(item.get("role", ""))
        title_line = " - ".join(compact([company, role]))
        date_range = format_date_range(item.get("start_date"), item.get("end_date"))
        bullets = item.get("bullets", [])
        bullet_html = "".join(f"<li>{escape(b)}</li>" for b in bullets if b)
        rows.append(
            '<div class="row">'
            '<div class="row-main">'
            f'<p class="item-title">{title_line}</p>'
            f'<ul class="bullet-list">{bullet_html}</ul>'
            '</div>'
            f'<div class="row-side">{date_range}</div>'
            '</div>'
        )
    return section("工作经历", "".join(rows))


def render_awards(items):
    rows = []
    for item in items:
        name = escape(item.get("name", ""))
        issuer = escape(item.get("issuer", ""))
        note = escape(item.get("note", ""))
        left = " - ".join(compact([name, issuer]))
        date = escape(item.get("date", ""))
        note_html = f'<p class="text">{note}</p>' if note else ""
        rows.append(
            '<div class="row">'
            '<div class="row-main">'
            f'<p class="item-title">{left}</p>'
            f"{note_html}"
            '</div>'
            f'<div class="row-side">{date}</div>'
            '</div>'
        )
    return section("奖项荣誉", "".join(rows))


def build_contact_line(basic, meta):
    parts = compact([
        basic.get("email", "").strip(),
        basic.get("phone", "").strip(),
        meta.get("target_role", "").strip(),
    ])
    return " · ".join(escape(x) for x in parts)


def main():
    if len(sys.argv) != 3:
        print("Usage: render_resume.py <input.json> <output.html>", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1]).resolve()
    output_path = Path(sys.argv[2]).resolve()
    skill_root = Path(__file__).resolve().parent.parent
    template_path = skill_root / "assets" / "template.html"
    css_path = skill_root / "assets" / "base.css"

    data = json.loads(input_path.read_text(encoding="utf-8"))
    template = template_path.read_text(encoding="utf-8")

    basic = data.get("basic", {})
    meta = data.get("meta", {})

    replacements = {
        "{{name}}": escape(basic.get("name", "")),
        "{{title}}": escape(basic.get("title", "")),
        "{{contact_line}}": build_contact_line(basic, meta),
        "{{education_section}}": render_education(data.get("education", [])),
        "{{skills_section}}": render_skills(data.get("skills", {})),
        "{{projects_section}}": render_bulleted_rows("项目经历", data.get("projects", []), "name", "subtitle"),
        "{{experience_section}}": render_experience(data.get("experience", [])),
        "{{awards_section}}": render_awards(data.get("awards", [])),
    }

    html_output = template
    for key, value in replacements.items():
        html_output = html_output.replace(key, value)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_output, encoding="utf-8")
    shutil.copy2(css_path, output_path.parent / "base.css")


if __name__ == "__main__":
    main()
