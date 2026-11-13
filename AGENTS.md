# Agent Harness: [Project Name]

## 1. Active State & Current Handover
- Active Mode: Coding
- Current Ticket: DEV-02 (`README.md`, `dev/scripts/review_ticket.py`)
- Immediate Next Action: Restructure README into the fork / use-template / gitignore / writing-session / ticket-workflow flow; add `dev/literature` to the review script search paths
- Last Completed: DEV-01 (dev/ layout documented in README.md and AGENTS.md, review script paths fixed, commit 06d4c34)
- Immediate Verification: `uv run dev/scripts/review_ticket.py <ticket-id>` at the end of each ticket
- Ticket Location: `dev/tickets/codes/` (engineering) and `dev/tickets/docs/` (report), created from `dev/templates/TICKET-template.md`
- Project Overview: `dev/PROJECT_OVERVIEW.md`

## 2. Hard Invariants & Guardrails
### Domain & Methodological Invariants
- Core Assumptions: [Locked definitions, mathematical formulations, or baseline sample boundaries]
- Data Schemas: [Strict column schemas, key primary indices, or date parsing standards]
- Prohibited Patterns: [Practices banned due to edge-case bugs or historical leakage]

### Writing & LaTeX Conventions
- Typography: Never use em dashes; use commas, parentheses, or colons.
- Float Placement: Always use `\begin{table}[htbp]` (avoid rigid `[H]` to prevent compilation floats breaking).
- Asset Paths: Use relative paths anchored to document root (`assets/img/...`).
- Data Alignment: All presented tables, formulas, and metric values must strictly match pipeline output artifacts.

### Tooling & Verification Protocols
- Code Suite: `uv run pytest tests/ -v -W error` (All tests green, zero warnings).
- Report Compilation: `latexmk -outdir=PDF -pdf main.tex` (Target output in `PDF/`, exit code 0, 0 undefined refs).
- Ticket Review: `uv run dev/scripts/review_ticket.py <ticket-id-or-path>` from the repo root at the end of every ticket (requires `MISTRAL_API_KEY` in `.env`, see `.env.example`; writes `<ticket>.review.md` next to the ticket and, on `[VERDICT: FAIL]`, a `<ticket>_remediation.md`).
- Definition of Done (DoD):
  1. Automated checks pass cleanly.
  2. Invariants in this file remain intact.
  3. Git commit follows conventional commit syntax (`feat:`, `fix:`, `chore:`, `doc:`).
  4. Section 1 of this file updated prior to ending the turn.
  5. Ticket review executed via `uv run dev/scripts/review_ticket.py <ticket-id>` with `[VERDICT: PASS]` (or the generated remediation ticket completed).

## 3. Dual-Track Roadmap

### Engineering (Code)
- [ ] CODE-01: Data Ingestion & Hygiene Pipeline
- [ ] CODE-02: Feature Engineering & Transformation
- [ ] CODE-03: Model Architecture & Estimation Harness
- [ ] CODE-04: Backtesting & Performance Evaluation

### Documentation (Report)
- [ ] DOC-01: Scaffolding, Title Page & Acronyms
- [ ] DOC-02: Data Description & Exploratory Data Analysis
- [ ] DOC-03: Methodology & Theoretical Grounding
- [ ] DOC-04: Empirical Results & Discussion
- [ ] DOC-05: Conclusion & Limitations
