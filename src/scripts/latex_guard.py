#!/usr/bin/env python3
"""
PaperForge LaTeX Guard
Checks a main.tex file for common structural and encoding issues.
Usage:
    python latex_guard.py paper_forge_output/final_paper/main.tex --markdown
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class LatexCheck:
    name: str
    passed: bool
    detail: str = ""


def check_latex(tex_path: Path) -> list[LatexCheck]:
    checks = []
    text = tex_path.read_text(encoding="utf-8", errors="replace")

    def add(name: str, condition: bool, detail: str = ""):
        checks.append(LatexCheck(name=name, passed=condition, detail=detail))

    add("File readable", True)
    add("Has \\documentclass", r"\documentclass" in text)
    add("Has \\begin{document}", r"\begin{document}" in text)
    add("Has \\end{document}", r"\end{document}" in text)
    add("Has \\title", r"\title" in text)
    add("Has \\maketitle", r"\maketitle" in text)
    add("Has \\section", r"\section" in text)
    add("Has bibliography", r"\bibliography" in text or r"\begin{thebibliography}" in text)

    # Check for unescaped special chars in body
    body_match = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", text, re.DOTALL)
    if body_match:
        body = body_match.group(1)
        has_bare_amp = bool(re.search(r"(?<!\\)&", body))
        has_bare_pct = bool(re.search(r"(?<!\\)%[^%]", body))
        add("No bare & in body", not has_bare_amp,
            "Found unescaped & — use \\& in tables or text")
        add("No stray % in body", not has_bare_pct,
            "Found % not used as comment — use \\% if literal")
    else:
        add("Body extractable", False, "Could not locate document body")

    # Check for mismatched braces (simple heuristic)
    open_b = text.count("{")
    close_b = text.count("}")
    add("Balanced braces", open_b == close_b,
        f"Open: {open_b}, Close: {close_b}" if open_b != close_b else "")

    # usepackage for inputenc
    add("Has inputenc", "inputenc" in text,
        "Recommend \\usepackage[utf8]{inputenc} for Unicode support")

    return checks


def format_markdown(checks: list[LatexCheck], tex_path: Path) -> str:
    passed = sum(1 for c in checks if c.passed)
    total = len(checks)
    lines = [
        "# PaperForge LaTeX Guard\n",
        f"**File:** `{tex_path}`\n",
        f"**Checks passed:** {passed}/{total}\n",
        "",
        "| Status | Check | Detail |",
        "|--------|-------|--------|",
    ]
    for c in checks:
        icon = "✅" if c.passed else "❌"
        lines.append(f"| {icon} | {c.name} | {c.detail} |")
    failed = [c for c in checks if not c.passed]
    if failed:
        lines += ["", "## Issues to Fix\n"]
        for c in failed:
            detail = f": {c.detail}" if c.detail else ""
            lines.append(f"- **{c.name}**{detail}")
    overall = "**PASS**" if not failed else "**FAIL**"
    lines += ["", f"## Overall: {overall}\n"]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="PaperForge LaTeX Guard")
    parser.add_argument("tex_file", help="Path to main.tex")
    parser.add_argument("--markdown", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    tex_path = Path(args.tex_file)
    if not tex_path.exists():
        print(f"Error: file not found: {tex_path}", file=sys.stderr)
        sys.exit(1)

    checks = check_latex(tex_path)
    failed = [c for c in checks if not c.passed]

    if args.markdown:
        report = format_markdown(checks, tex_path)
        print(report)
        if args.write:
            out = tex_path.parent / "latex_guard.md"
            out.write_text(report, encoding="utf-8")
            print(f"\nReport written to: {out}")
    else:
        for c in checks:
            icon = "OK" if c.passed else "FAIL"
            print(f"  [{icon}] {c.name}" + (f" — {c.detail}" if c.detail else ""))

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
