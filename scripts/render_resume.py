#!/usr/bin/env python3
"""Render a resume JSON spec into a self-contained HTML file.

Two independent axes drive the output:
  meta.template: visual look (technical / modern / classic / compact / creative)
  meta.industry: content semantics (tech / design / business / academic / marketing)
"""

import argparse
import html
import json
import sys
from pathlib import Path


TEMPLATES = ("technical", "modern", "classic", "compact", "creative")

INDUSTRIES = {
    "tech": {
        "skill_keys": ["languages", "frameworks", "databases", "infrastructure", "tools", "other"],
        "section_order": ["education", "skills", "projects", "experience", "awards"],
    },
    "design": {
        "skill_keys": ["software", "specialties", "output", "methodology", "tools", "other"],
        "section_order": ["education", "skills", "projects", "experience", "awards"],
    },
    "business": {
        "skill_keys": ["tools", "methodologies", "domains", "languages", "certifications", "other"],
        "section_order": ["education", "experience", "skills", "projects", "awards"],
    },
    "academic": {
        "skill_keys": ["research_areas", "methods", "tools", "publications", "languages", "other"],
        "section_order": ["education", "experience", "skills", "projects", "awards"],
    },
    "marketing": {
        "skill_keys": ["channels", "content", "analytics", "platforms", "tools", "other"],
        "section_order": ["education", "experience", "skills", "projects", "awards"],
    },
}

LABELS = {
    "zh": {
        "page_label": "个人简历",
        "education": "教育背景",
        "skills": "技术能力",
        "projects": "项目经历",
        "experience": "工作经历",
        "awards": "奖项荣誉",
        "languages": "编程语言",
        "frameworks": "后端框架",
        "databases": "中间件 & 数据库",
        "infrastructure": "分布式 & 运维",
        "tools": "工具",
        "other": "其他",
        "software": "设计软件",
        "specialties": "设计领域",
        "output": "输出能力",
        "methodology": "方法论",
        "methodologies": "方法论",
        "domains": "领域知识",
        "certifications": "认证资质",
        "research_areas": "研究方向",
        "methods": "研究方法",
        "publications": "代表论文",
        "channels": "渠道运营",
        "content": "内容输出",
        "analytics": "数据分析",
        "platforms": "平台工具",
    },
    "en": {
        "page_label": "Resume",
        "education": "Education",
        "skills": "Skills",
        "projects": "Projects",
        "experience": "Experience",
        "awards": "Awards",
        "languages": "Languages",
        "frameworks": "Frameworks",
        "databases": "Databases",
        "infrastructure": "Infrastructure",
        "tools": "Tools",
        "other": "Other",
        "software": "Software",
        "specialties": "Specialties",
        "output": "Deliverables",
        "methodology": "Methodology",
        "methodologies": "Methodologies",
        "domains": "Domains",
        "certifications": "Certifications",
        "research_areas": "Research Areas",
        "methods": "Methods",
        "publications": "Publications",
        "channels": "Channels",
        "content": "Content",
        "analytics": "Analytics",
        "platforms": "Platforms",
    },
}


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


def render_education(items, labels):
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
    return section(labels["education"], "".join(rows))


def render_skills(skills, labels, skill_keys):
    seen = set()
    ordered = list(skill_keys) + [k for k in skills.keys() if k not in skill_keys]
    items = []
    for key in ordered:
        if key in seen:
            continue
        seen.add(key)
        values = [escape(v) for v in (skills.get(key) or []) if v]
        if not values:
            continue
        label = labels.get(key, key.replace("_", " ").title())
        items.append(
            f'<li><span class="label">{escape(label)}:</span> {", ".join(values)}</li>'
        )
    if not items:
        return ""
    return section(labels["skills"], f'<ul class="skills-list">{"".join(items)}</ul>')


def render_bulleted_rows(title, items, name_key, subtitle_key=None):
    rows = []
    for item in items:
        name = escape(item.get(name_key, ""))
        subtitle = escape(item.get(subtitle_key, "")) if subtitle_key else ""
        title_line = name
        if subtitle:
            title_line += f' <span class="item-subtitle">({subtitle})</span>'
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


def render_experience(items, labels):
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
    return section(labels["experience"], "".join(rows))


def render_awards(items, labels):
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
    return section(labels["awards"], "".join(rows))


def build_contact_line(basic, meta):
    parts = compact([
        basic.get("email", "").strip(),
        basic.get("phone", "").strip(),
        meta.get("target_role", "").strip(),
    ])
    return " · ".join(escape(x) for x in parts)


def resolve_language(meta):
    lang = (meta.get("language") or "zh").lower()
    if lang not in LABELS:
        print(f"warning: unknown language {lang!r}, falling back to zh", file=sys.stderr)
        lang = "zh"
    return lang


def resolve_template(meta):
    name = (meta.get("template") or "technical").lower()
    if name not in TEMPLATES:
        print(f"warning: unknown template {name!r}, falling back to technical", file=sys.stderr)
        name = "technical"
    return name


def resolve_industry(meta):
    name = (meta.get("industry") or "tech").lower()
    if name not in INDUSTRIES:
        print(f"warning: unknown industry {name!r}, falling back to tech", file=sys.stderr)
        name = "tech"
    return name


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"error: input file not found: {path}")
    except json.JSONDecodeError as exc:
        sys.exit(f"error: invalid JSON in {path}: {exc.msg} (line {exc.lineno}, col {exc.colno})")


def load_text(path, kind):
    if not path.exists():
        sys.exit(f"error: {kind} file not found: {path}")
    return path.read_text(encoding="utf-8")


def render_sections(data, labels, industry):
    sections = {
        "education": render_education(data.get("education", []), labels),
        "skills": render_skills(data.get("skills", {}), labels, industry["skill_keys"]),
        "projects": render_bulleted_rows(
            labels["projects"], data.get("projects", []), "name", "subtitle"
        ),
        "experience": render_experience(data.get("experience", []), labels),
        "awards": render_awards(data.get("awards", []), labels),
    }
    return "\n".join(sections[name] for name in industry["section_order"])


def render(data, skill_root):
    basic = data.get("basic") or {}
    meta = data.get("meta") or {}

    if not basic.get("name"):
        print("warning: basic.name is empty; header will render without a name", file=sys.stderr)

    lang = resolve_language(meta)
    template_name = resolve_template(meta)
    industry_name = resolve_industry(meta)
    labels = LABELS[lang]
    industry = INDUSTRIES[industry_name]

    template_dir = skill_root / "assets" / "templates" / template_name
    template = load_text(template_dir / "template.html", f"template {template_name!r}")
    css = load_text(template_dir / "style.css", f"stylesheet for {template_name!r}")

    sections_html = render_sections(data, labels, industry)

    replacements = {
        "{{lang}}": "en" if lang == "en" else "zh-CN",
        "{{name}}": escape(basic.get("name", "")),
        "{{title}}": escape(basic.get("title", "")),
        "{{page_label}}": escape(labels["page_label"]),
        "{{contact_line}}": build_contact_line(basic, meta),
        "{{inline_css}}": css,
        "{{sections}}": sections_html,
    }

    output = template
    for key, value in replacements.items():
        output = output.replace(key, value)
    return output


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Render a resume JSON spec into a self-contained HTML file."
    )
    parser.add_argument("input", help="path to the resume JSON spec")
    parser.add_argument("output", help="path to write the rendered HTML")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    skill_root = Path(__file__).resolve().parent.parent

    data = load_json(input_path)
    output = render(data, skill_root)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
