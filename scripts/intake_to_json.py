#!/usr/bin/env python3
"""Convert a filled markdown resume intake into normalized resume JSON."""

import argparse
import json
import re
import sys
from pathlib import Path

from render_resume import ValidationError, normalize_resume


FIELD_MAP = {
    "basic info": ("section", "basic"),
    "target": ("section", "target"),
    "education": ("list", "education"),
    "experience": ("list", "experience"),
    "projects": ("list", "projects"),
    "skills": ("section", "skills"),
    "awards": ("section", "awards"),
}

BASIC_FIELDS = {
    "name": "name",
    "title": "title",
    "phone": "phone",
    "email": "email",
    "location": "location",
    "website": "website",
    "github": "github",
    "linkedin": "linkedin",
}

TARGET_FIELDS = {
    "target role": "target_role",
    "language": "language",
    "style hint": "style_hint",
    "template": "template",
    "industry": "industry",
    "section order": "section_order",
}
PLACEHOLDER_VALUES = {
    "language": {"zh / en"},
    "style_hint": {"professional / modern / concise"},
    "template": {"technical / modern / classic / compact / creative"},
    "industry": {"tech / design / business / academic / marketing"},
    "section_order": {"education, skills, projects, experience, awards"},
}

SKILL_FIELDS = {
    "languages": "languages",
    "frameworks": "frameworks",
    "databases": "databases",
    "infrastructure": "infrastructure",
    "tools": "tools",
    "other": "other",
    "software": "software",
    "specialties": "specialties",
    "output": "output",
    "methodology": "methodology",
    "methodologies": "methodologies",
    "domains": "domains",
    "certifications": "certifications",
    "research areas": "research_areas",
    "methods": "methods",
    "publications": "publications",
    "channels": "channels",
    "content": "content",
    "analytics": "analytics",
    "platforms": "platforms",
}
KNOWN_FIELD_LABELS = set(BASIC_FIELDS) | set(TARGET_FIELDS) | set(SKILL_FIELDS) | {
    "school",
    "degree",
    "major",
    "start",
    "end",
    "honors",
    "company",
    "role",
    "summary",
    "achievements",
    "name",
    "subtitle",
    "details",
    "award",
    "issuer",
    "date",
    "note",
}


def strip_code_fence(text):
    lines = text.splitlines()
    if len(lines) >= 2 and lines[0].strip().startswith("```") and lines[-1].strip() == "```":
        return "\n".join(lines[1:-1])
    return text


def split_value(value):
    if not value:
        return []
    parts = re.split(r"[,\n/]+", value)
    return [part.strip() for part in parts if part.strip()]


def parse_section_order(value):
    return [part.strip().lower() for part in re.split(r"[,\n>/-]+", value) if part.strip()]


def clean_placeholder(field_name, value):
    value = value.strip()
    if value in PLACEHOLDER_VALUES.get(field_name, set()):
        return ""
    return value


def parse_list_items(lines, start_index):
    items = []
    index = start_index
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        if stripped.startswith("## ") or stripped.startswith("### "):
            break
        if stripped.startswith("-"):
            value = stripped[1:].strip()
            key, sep, _ = value.partition(":")
            if sep and key.strip().lower() in KNOWN_FIELD_LABELS:
                break
            if value:
                items.append(value)
        index += 1
    return items, index


def parse_intake(text):
    lines = strip_code_fence(text).splitlines()
    data = {
        "meta": {
            "language": "zh",
            "target_role": "",
            "template": "technical",
            "industry": "tech",
            "style_hint": "professional",
        },
        "basic": {},
        "education": [],
        "skills": {},
        "projects": [],
        "experience": [],
        "awards": [],
    }

    section_name = None
    current_item = None
    current_item_bucket = None
    current_multiline_key = None
    current_award = None
    index = 0

    while index < len(lines):
        raw_line = lines[index]
        line = raw_line.strip()

        if not line or line == "# Resume Input" or line.startswith("Use this template"):
            index += 1
            continue

        if line.startswith("## "):
            heading = line[3:].strip().lower()
            section_type = FIELD_MAP.get(heading)
            if not section_type:
                raise ValidationError(f"unsupported intake section heading: {line}")
            section_name = heading
            current_item = None
            current_item_bucket = None
            current_multiline_key = None
            current_award = None
            index += 1
            continue

        if line.startswith("### "):
            if section_name not in ("education", "experience", "projects"):
                raise ValidationError(f"unexpected subsection outside repeatable section: {line}")
            current_item = {}
            current_item_bucket = section_name
            data[section_name].append(current_item)
            current_multiline_key = None
            current_award = None
            index += 1
            continue

        if line.startswith("-"):
            body = line[1:].strip()
            key, sep, value = body.partition(":")
            key_name = key.strip().lower()
            value = value.strip()
            if not sep:
                if current_multiline_key and current_item is not None:
                    current_item.setdefault(current_multiline_key, []).append(body)
                    index += 1
                    continue
                raise ValidationError(f"could not parse line: {raw_line}")

            if section_name == "basic info":
                mapped = BASIC_FIELDS.get(key_name)
                if mapped:
                    data["basic"][mapped] = value
            elif section_name == "target":
                mapped = TARGET_FIELDS.get(key_name)
                if mapped == "section_order":
                    cleaned = clean_placeholder(mapped, value)
                    data["meta"][mapped] = parse_section_order(cleaned) if cleaned else []
                elif mapped:
                    data["meta"][mapped] = clean_placeholder(mapped, value)
            elif section_name == "skills":
                mapped = SKILL_FIELDS.get(key_name)
                if mapped:
                    data["skills"][mapped] = split_value(value)
            elif section_name == "education":
                if current_item is None:
                    current_item = {}
                    data["education"].append(current_item)
                education_fields = {
                    "school": "school",
                    "degree": "degree",
                    "major": "major",
                    "start": "start_date",
                    "end": "end_date",
                    "honors": "honors",
                }
                mapped = education_fields.get(key_name)
                if mapped == "honors":
                    current_item[mapped] = split_value(value)
                elif mapped:
                    current_item[mapped] = value
            elif section_name == "experience":
                if current_item is None:
                    current_item = {}
                    data["experience"].append(current_item)
                experience_fields = {
                    "company": "company",
                    "role": "role",
                    "start": "start_date",
                    "end": "end_date",
                    "summary": "summary",
                    "achievements": "bullets",
                }
                mapped = experience_fields.get(key_name)
                if mapped == "bullets":
                    bullets = split_value(value)
                    if not bullets:
                        bullets, index = parse_list_items(lines, index + 1)
                    current_item[mapped] = bullets
                    current_multiline_key = "bullets"
                    continue
                elif mapped:
                    current_item[mapped] = value
                    current_multiline_key = None
            elif section_name == "projects":
                if current_item is None:
                    current_item = {}
                    data["projects"].append(current_item)
                project_fields = {
                    "name": "name",
                    "subtitle": "subtitle",
                    "start": "start_date",
                    "end": "end_date",
                    "details": "bullets",
                }
                mapped = project_fields.get(key_name)
                if mapped == "bullets":
                    bullets = split_value(value)
                    if not bullets:
                        bullets, index = parse_list_items(lines, index + 1)
                    current_item[mapped] = bullets
                    current_multiline_key = "bullets"
                    continue
                elif mapped:
                    current_item[mapped] = value
                    current_multiline_key = None
            elif section_name == "awards":
                award_fields = {
                    "award": "name",
                    "issuer": "issuer",
                    "date": "date",
                    "note": "note",
                }
                mapped = award_fields.get(key_name)
                if mapped:
                    if mapped == "name" or current_award is None:
                        current_award = {}
                        data["awards"].append(current_award)
                    current_award[mapped] = value
            else:
                raise ValidationError(f"unsupported intake section: {section_name}")

            index += 1
            continue

        if current_multiline_key and current_item is not None:
            current_item.setdefault(current_multiline_key, []).append(line)
            index += 1
            continue

        index += 1

    finalize_items(data)
    normalized = normalize_resume(data)
    apply_meta_defaults(normalized)
    return normalized


def finalize_items(data):
    for item in data["experience"]:
        summary = item.pop("summary", "").strip()
        bullets = item.get("bullets", [])
        if summary:
            item["bullets"] = [summary] + bullets

    for award in data["awards"]:
        for key in ("name", "issuer", "date", "note"):
            award.setdefault(key, "")


def apply_meta_defaults(data):
    meta = data["meta"]
    meta["language"] = meta["language"] or "zh"
    meta["template"] = meta["template"] or "technical"
    meta["industry"] = meta["industry"] or "tech"
    meta["style_hint"] = meta["style_hint"] or "professional"


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Convert a filled markdown resume intake into normalized resume JSON."
    )
    parser.add_argument("input", help="path to the markdown intake file")
    parser.add_argument("output", help="path to write the normalized resume JSON")
    return parser.parse_args(argv)


def load_text(path):
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        sys.exit(f"error: input file not found: {path}")


def main(argv=None):
    args = parse_args(argv)
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()

    try:
        data = parse_intake(load_text(input_path))
    except ValidationError as exc:
        sys.exit(f"error: invalid intake in {input_path}: {exc}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
