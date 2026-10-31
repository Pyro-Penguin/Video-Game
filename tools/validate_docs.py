#!/usr/bin/env python3
"""Validate the repository's lightweight project-governance documents."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "COLLABORATION_PROTOCOL.md",
    "PROJECT_INDEX.md",
    "PROJECT_STATUS.md",
    "HANDOFF.md",
    "docs/DECISION_LOG.md",
    "docs/OPEN_QUESTIONS.md",
)
ALLOWED_STATUSES = {"Confirmed", "Provisional", "Unresolved", "Superseded"}
DECISION_ROW = re.compile(r"^\|\s*(D-\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|")
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
DECISION_ID = re.compile(r"\bD-\d+\b")


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"required file missing: {relative}")

    decision_path = root / "docs/DECISION_LOG.md"
    if decision_path.is_file():
        text = decision_path.read_text(encoding="utf-8")
        ids: set[str] = set()
        superseded_rows: list[tuple[str, str]] = []

        for line_number, line in enumerate(text.splitlines(), 1):
            if not line.lstrip().startswith("| D-"):
                continue
            match = DECISION_ROW.match(line)
            if not match:
                errors.append(f"decision log line {line_number}: malformed decision row")
                continue

            decision_id, _topic, status = (part.strip() for part in match.groups())
            if decision_id in ids:
                errors.append(f"decision log line {line_number}: duplicate ID {decision_id}")
            ids.add(decision_id)

            if status not in ALLOWED_STATUSES:
                errors.append(
                    f"decision log line {line_number}: invalid status {status!r}"
                )

            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if status == "Superseded":
                superseded_rows.append((decision_id, cells[-1] if cells else ""))

        if re.search(r"\bConfirmed direction\b", text, re.IGNORECASE):
            errors.append("decision log contains legacy status 'Confirmed direction'")

        for decision_id, supersession_cell in superseded_rows:
            targets = set(DECISION_ID.findall(supersession_cell))
            if not targets:
                errors.append(
                    f"superseded decision {decision_id} has no replacement decision ID"
                )
            for target in targets:
                if target not in ids:
                    errors.append(
                        f"superseded decision {decision_id} references missing {target}"
                    )

    handoff_path = root / "HANDOFF.md"
    if handoff_path.is_file():
        handoff = handoff_path.read_text(encoding="utf-8")
        required_headings = (
            "## Mandatory Startup",
            "## Current Work State",
            "## Highest-Priority Next Work",
            "## Do Not Assume",
        )
        for heading in required_headings:
            if heading not in handoff:
                errors.append(f"HANDOFF.md missing required section: {heading}")

    # Validate relative Markdown links throughout tracked documentation.
    for markdown_path in root.rglob("*.md"):
        if any(part in {".git", ".venv", "__pycache__"} for part in markdown_path.parts):
            continue
        try:
            content = markdown_path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"cannot read {markdown_path.relative_to(root)}: {exc}")
            continue

        for destination in MARKDOWN_LINK.findall(content):
            destination = destination.strip()
            if not destination or destination.startswith(("http://", "https://", "mailto:", "#")):
                continue
            destination = destination.split("#", 1)[0].split("?", 1)[0]
            if not destination:
                continue
            # Markdown link destinations are URI paths; decode before filesystem lookup.
            destination = unquote(destination)
            target = (markdown_path.parent / destination).resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                errors.append(
                    f"{markdown_path.relative_to(root)}: link escapes repository: {destination}"
                )
                continue
            if not target.exists():
                errors.append(
                    f"{markdown_path.relative_to(root)}: broken link: {destination}"
                )

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Documentation validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Documentation validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
