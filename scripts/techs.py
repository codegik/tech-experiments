#!/usr/bin/env python3
"""Maintain the tech list in README.md.

The list lives between the <!-- techs:start --> and <!-- techs:end --> markers:
one `## Category` heading per group, each followed by a table whose rows are
`| [Name](https://url) | One-line description | YYYY-MM-DD |`.
Categories and rows are kept in case-insensitive alphabetical order.
"""
import argparse
import datetime
import os
import re
import sys
from pathlib import Path

START = "<!-- techs:start -->"
END = "<!-- techs:end -->"
HEADER = "| Tech | What it is | Added |"
DIVIDER = "|---|---|---|"
ROW = re.compile(r"^\| \[([^\]]+)\]\((https?://[^)\s]+)\) \| ([^|]+) \| (\d{4}-\d{2}-\d{2}) \|$")


def readme_path() -> Path:
    return Path(os.environ.get("TECHS_FILE", Path(__file__).resolve().parent.parent / "README.md"))


def split(text: str):
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError(f"README must contain exactly one {START} and one {END}")
    head, rest = text.split(START)
    body, tail = rest.split(END)
    return head, body, tail


def parse(body: str):
    """Return ([(category, [row dicts])], errors)."""
    cats, errors, current = [], [], None
    for n, line in enumerate(body.strip("\n").splitlines(), 1):
        if not line.strip():
            continue
        if line.startswith("## "):
            current = (line[3:].strip(), [])
            cats.append(current)
        elif line in (HEADER, DIVIDER):
            if current is None:
                errors.append(f"line {n}: table before any '## Category' heading")
        elif m := ROW.match(line):
            if current is None:
                errors.append(f"line {n}: row before any '## Category' heading")
                continue
            current[1].append({"name": m[1], "url": m[2], "desc": m[3].strip(), "date": m[4]})
        else:
            errors.append(f"line {n}: not a valid row: {line}")
    return cats, errors


def validate(cats):
    errors, names, urls = [], {}, {}
    key = lambda s: s.casefold()
    titles = [c for c, _ in cats]
    if titles != sorted(titles, key=key):
        errors.append("categories are not in alphabetical order")
    if len(set(map(key, titles))) != len(titles):
        errors.append("duplicate category heading")
    for cat, rows in cats:
        if not rows:
            errors.append(f"category '{cat}' has no techs")
        order = [r["name"] for r in rows]
        if order != sorted(order, key=key):
            errors.append(f"category '{cat}' is not in alphabetical order")
        for r in rows:
            for seen, field in ((names, "name"), (urls, "url")):
                k = key(r[field].rstrip("/"))
                if k in seen:
                    errors.append(f"duplicate {field} '{r[field]}' (in '{seen[k]}' and '{cat}')")
                seen[k] = cat
            try:
                datetime.date.fromisoformat(r["date"])
            except ValueError:
                errors.append(f"'{r['name']}': invalid date {r['date']}")
    return errors


def render(cats) -> str:
    out = []
    for cat, rows in cats:
        out += [f"## {cat}", "", HEADER, DIVIDER]
        out += [f"| [{r['name']}]({r['url']}) | {r['desc']} | {r['date']} |" for r in rows]
        out.append("")
    return "\n" + "\n".join(out)


def load():
    text = readme_path().read_text()
    head, body, tail = split(text)
    cats, errors = parse(body)
    return head, cats, tail, errors + validate(cats)


def cmd_check(_args) -> int:
    try:
        _, cats, _, errors = load()
    except ValueError as e:
        errors = [str(e)]
        cats = []
    if errors:
        print("\n".join(f"error: {e}" for e in errors), file=sys.stderr)
        return 1
    print(f"ok: {sum(len(r) for _, r in cats)} techs in {len(cats)} categories")
    return 0


def cmd_list(_args) -> int:
    _, cats, _, _ = load()
    for cat, rows in cats:
        for r in rows:
            print(f"{cat}\t{r['name']}\t{r['url']}")
    return 0


def cmd_add(a) -> int:
    for field in ("name", "desc", "category"):
        v = getattr(a, field)
        if "|" in v or "\n" in v or not v.strip():
            print(f"error: --{field} must be non-empty, single-line, without '|'", file=sys.stderr)
            return 1
    if not re.match(r"^https?://\S+$", a.url):
        print("error: --url must be an http(s) URL", file=sys.stderr)
        return 1
    head, cats, tail, errors = load()
    if errors:
        print("\n".join(f"error: {e}" for e in errors), file=sys.stderr)
        return 1
    key = lambda s: s.casefold()
    for cat, rows in cats:
        for r in rows:
            if key(r["name"]) == key(a.name) or key(r["url"].rstrip("/")) == key(a.url.rstrip("/")):
                print(f"exists: {r['name']} ({r['url']}) is already in '{cat}'")
                return 3
    match = [c for c in cats if key(c[0]) == key(a.category.strip())]
    if match:
        rows = match[0][1]
    else:
        rows = []
        cats.append((a.category.strip(), rows))
        cats.sort(key=lambda c: key(c[0]))
    row = {"name": a.name.strip(), "url": a.url, "desc": a.desc.strip(),
           "date": a.date or datetime.date.today().isoformat()}
    rows.append(row)
    rows.sort(key=lambda r: key(r["name"]))
    readme_path().write_text(head + START + render(cats) + END + tail)
    print(f"added to '{a.category.strip()}': | [{row['name']}]({row['url']}) | {row['desc']} | {row['date']} |")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="techs.sh")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="validate the list").set_defaults(fn=cmd_check)
    sub.add_parser("list", help="print category, name, url (tab-separated)").set_defaults(fn=cmd_list)
    add = sub.add_parser("add", help="insert a tech in alphabetical order")
    add.add_argument("--name", required=True)
    add.add_argument("--url", required=True)
    add.add_argument("--category", required=True)
    add.add_argument("--desc", required=True)
    add.add_argument("--date", help="YYYY-MM-DD, default today")
    add.set_defaults(fn=cmd_add)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
