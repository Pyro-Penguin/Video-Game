import tempfile
import unittest
from pathlib import Path

from validate_docs import validate


class DocumentationValidatorTests(unittest.TestCase):
    def write_fixture(self, root: Path, decision_log: str, handoff: str = "") -> None:
        for relative in (
            "COLLABORATION_PROTOCOL.md",
            "PROJECT_INDEX.md",
            "PROJECT_STATUS.md",
            "docs/OPEN_QUESTIONS.md",
        ):
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# Fixture\n", encoding="utf-8")

        (root / "docs/DECISION_LOG.md").write_text(decision_log, encoding="utf-8")
        (root / "HANDOFF.md").write_text(handoff, encoding="utf-8")

    def test_accepts_valid_minimal_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            log = (
                "| ID | Topic | Status | Date | Decision | Rationale | Dependencies | Supersession |\n"
                "|---|---|---|---|---|---|---|---|\n"
                "| D-001 | Example | Confirmed | 2026-10-30 | Accepted scope | Human | None | None |\n"
            )
            handoff = (
                "## Mandatory Startup\n## Current Work State\n"
                "## Highest-Priority Next Work\n## Do Not Assume\n"
            )
            self.write_fixture(root, log, handoff)
            self.assertEqual(validate(root), [])

    def test_rejects_invalid_status_and_duplicate_id(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            log = (
                "| ID | Topic | Status | Date | Decision | Rationale | Dependencies | Supersession |\n"
                "|---|---|---|---|---|---|---|---|\n"
                "| D-001 | A | Confirmed direction | 2026-10-30 | A | H | None | None |\n"
                "| D-001 | B | Confirmed | 2026-10-30 | B | H | None | None |\n"
            )
            handoff = (
                "## Mandatory Startup\n## Current Work State\n"
                "## Highest-Priority Next Work\n## Do Not Assume\n"
            )
            self.write_fixture(root, log, handoff)
            errors = validate(root)
            self.assertTrue(any("invalid status" in error for error in errors))
            self.assertTrue(any("duplicate ID" in error for error in errors))

    def test_rejects_superseded_decision_without_valid_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            log = (
                "| ID | Topic | Status | Date | Decision | Rationale | Dependencies | Supersession |\n"
                "|---|---|---|---|---|---|---|---|\n"
                "| D-001 | A | Superseded | 2026-10-30 | Old | H | None | D-099 |\n"
            )
            handoff = (
                "## Mandatory Startup\n## Current Work State\n"
                "## Highest-Priority Next Work\n## Do Not Assume\n"
            )
            self.write_fixture(root, log, handoff)
            errors = validate(root)
            self.assertTrue(any("references missing D-099" in error for error in errors))

    def test_rejects_missing_handoff_section_and_broken_link(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            log = (
                "| ID | Topic | Status | Date | Decision | Rationale | Dependencies | Supersession |\n"
                "|---|---|---|---|---|---|---|---|\n"
                "| D-001 | A | Confirmed | 2026-10-30 | A | H | None | None |\n"
            )
            self.write_fixture(root, log, "## Mandatory Startup\n")
            (root / "PROJECT_INDEX.md").write_text("[missing](no-such-file.md)\n", encoding="utf-8")
            errors = validate(root)
            self.assertTrue(any("missing required section" in error for error in errors))
            self.assertTrue(any("broken link" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
