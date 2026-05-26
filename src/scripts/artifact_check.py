#!/usr/bin/env python3
"""
PaperForge Artifact Check
Verifies that a paper_forge_output directory contains all required artifacts.
Usage:
    python artifact_check.py paper_forge_output --markdown --write
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from dataclasses import dataclass


REQUIRED_ARTIFACTS = [
    ("paper_forge_config.json",        "Run configuration"),
    ("research_dossier.md",            "Scene research profile"),
    ("evidence_bank.md",               "Evidence bank (claim sources)"),
    ("claim_register.md",              "Claim register"),
    ("confirmed_motivation.md",        "Confirmed central motivation"),
    ("section_blueprint.md",           "Section blueprint"),
    ("writing_rationale_matrix.md",    "Writing rationale matrix"),
    ("revision_audit.md",              "Revision audit report"),
    ("final_paper/main.tex",           "LaTeX manuscript"),
    ("final_paper/references.bib",     "BibTeX references"),
    ("final_paper/draft.md",           "Markdown draft"),
]

OPTIONAL_ARTIFACTS = [
    ("rewrite_matrix.md",              "Rewrite decision matrix (rewrite workflow)"),
    ("motivation_candidates.md",       "Motivation candidates list"),
    ("final_paper/paper.pdf",          "Compiled PDF"),
    ("final_paper/paper.docx",         "Word export"),
    ("translation_package/",           "Chinese translation package"),
    ("run_log.txt",                    "Run log"),
]


@dataclass
class CheckResult:
    path: str
    description: str
    exists: bool
    required: bool
    note: str = ""


def check_dir(output_dir: Path) -> list[CheckResult]:
    results = []
    for rel, desc in REQUIRED_ARTIFACTS:
        p = output_dir / rel
        results.append(CheckResult(
            path=rel, description=desc,
            exists=p.exists(), required=True,
        ))
    for rel, desc in OPTIONAL_ARTIFACTS:
        p = output_dir / rel
        results.append(CheckResult(
            path=rel, description=desc,
            exists=p.exists(), required=False,
        ))
    return results


def format_markdown(results: list[CheckResult], output_dir: Path) -> str:
    required = [r for r in results if r.required]
    optional = [r for r in results if not r.required]
    passed = sum(1 for r in required if r.exists)
    total = len(required)
    pct = int(passed / total * 100) if total else 0

    lines = [
        "# PaperForge Artifact Check\n",
        f"**Output directory:** `{output_dir}`\n",
        f"**Required artifacts:** {passed}/{total} ({pct}%)\n",
        "",
        "## Required Artifacts\n",
        "| Status | Path | Description |",
        "|--------|------|-------------|",
    ]
    for r in required:
        icon = "✅" if r.exists else "❌"
        lines.append(f"| {icon} | `{r.path}` | {r.description} |")

    lines += [
        "",
        "## Optional Artifacts\n",
        "| Status | Path | Description |",
        "|--------|------|-------------|",
    ]
    for r in optional:
        icon = "✅" if r.exists else "⬜"
        lines.append(f"| {icon} | `{r.path}` | {r.description} |")

    missing = [r for r in required if not r.exists]
    if missing:
        lines += ["", "## Missing Required Artifacts\n"]
        for r in missing:
            lines.append(f"- `{r.path}` — {r.description}")

    overall = "**PASS**" if not missing else "**FAIL**"
    lines += ["", f"## Overall: {overall}\n"]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="PaperForge artifact checker")
    parser.add_argument("output_dir", help="Path to paper_forge_output directory")
    parser.add_argument("--markdown", action="store_true", help="Output as Markdown")
    parser.add_argument("--write", action="store_true", help="Write report to output_dir/artifact_check.md")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    if not output_dir.exists():
        print(f"Error: directory not found: {output_dir}", file=sys.stderr)
        sys.exit(1)

    results = check_dir(output_dir)
    missing_required = [r for r in results if r.required and not r.exists]

    if args.json:
        print(json.dumps([r.__dict__ for r in results], indent=2))
    elif args.markdown:
        report = format_markdown(results, output_dir)
        print(report)
        if args.write:
            report_path = output_dir / "artifact_check.md"
            report_path.write_text(report, encoding="utf-8")
            print(f"\nReport written to: {report_path}")
    else:
        # Plain text
        for r in results:
            icon = "OK" if r.exists else ("MISSING" if r.required else "optional")
            print(f"  [{icon:<8}] {r.path}")

    sys.exit(1 if missing_required else 0)


if __name__ == "__main__":
    main()
