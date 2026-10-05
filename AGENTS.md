# Agent Harness: [Project Name]

## 1. Active State & Current Handover
- Active Mode: [Coding | Writing]
- Current Ticket: [TICKET-ID] (`path/to/target/file`)
- Immediate Next Action: [Precise task to start immediately, e.g. Implement module or draft section]
- Last Completed: [Previous ticket ID, brief summary of verified deliverables]
- Immediate Verification: [CLI command to run after making changes, e.g. pytest or latexmk]

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
- Definition of Done (DoD):
  1. Automated checks pass cleanly.
  2. Invariants in this file remain intact.
  3. Git commit follows conventional commit syntax (`feat:`, `fix:`, `chore:`, `doc:`).
  4. Section 1 of this file updated prior to ending the turn.

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
