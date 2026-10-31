---
applyTo: "docs/**/*.md"
---
# Documentation instructions

- Follow `COLLABORATION_PROTOCOL.md` for document authority, decision status, provenance, and update rules.
- Preserve the distinction between Confirmed, Provisional, Unresolved, and Superseded decisions.
- Do not promote AI recommendations, references, prototypes, or experiment outputs into accepted decisions without explicit human approval.
- Keep one authoritative home for each fact. Link to it rather than copying long explanations into status, handoff, and index files.
- Record source, creator, attribution, and usage rights for visual references when known; mark unknown details as unknown.
- Separate visual qualities being studied from protected characters, exact compositions, logos, or an artist's distinctive expression.
- Validate relative Markdown links with `python3 tools/validate_docs.py`.
- Update PROJECT_STATUS.md only when stage, verified progress, or canonical priorities change; update HANDOFF.md when the next action or active work changes.
