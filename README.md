# Monolith LaTeX Template

A reproducible Dev Container setup for LaTeX reports and research monoliths.

## Prerequisites
- Install [uv](https://docs.astral.sh/uv/) (for example `brew install uv` on macOS, or `curl -LsSf https://astral.sh/uv/install.sh | sh`).
- From the repository root, run `uv sync` to create `.venv` with the dev dependencies (pytest). Helper scripts such as `dev/scripts/review_ticket.py` declare their own dependencies inline and are executed via `uv run`.

## Directory Structure
- `.devcontainer/`: Container toolchain (native Apple Silicon TeX Live)
- `.vscode/`: Workspace settings configuring LaTeX Workshop (`settings.json`)
- `compile.sh`: Host runner script invoking the container toolchain
- `pyproject.toml` / `uv.lock`: uv project definition and lockfile (dev dependencies such as pytest, see Prerequisites)
- `report/document/`: LaTeX source files (`acronyms.tex`, `main.tex`, `references.bib`, `title_page.tex`)
- `dev/`: Local agent working directory (gitignored in derived projects, see step 3)
  - `dev/tickets/`: Active tickets (`codes/` for engineering, `docs/` for report work)
  - `dev/literature/`: Literature notes and references
  - `dev/templates/`: Ticket template (`TICKET-template.md`)
  - `dev/scripts/`: Helper scripts (`review_ticket.py` verifies a finished ticket)
  - `dev/config/`: Tool configuration (`review_ticket.toml` holds the review model, limits, and prompts used by `review_ticket.py`)
  - `dev/PROJECT_OVERVIEW.md`: Project architecture notes

## 1. Fork the Project on GitHub
Fork this repository to your own GitHub account.

## 2. Use This Template
Click **"Use this template"** -> **"Create a new repository"** and follow the setup prompts to scaffold your project from this template.

## 3. Uncomment `dev/` and `AGENTS.md` in `.gitignore`
In your new project, uncomment the two lines at the bottom of `.gitignore` so that tickets, review logs, local env files, and the agent harness file stay out of version control:
```gitignore
dev/
AGENTS.md
```

## 4. Writing Session

### a. Start Environment
Open the repository in VS Code and ensure the Dev Container is running:
- `Cmd + Shift + P` -> `Dev Containers: Reopen in Container` (or run it via OrbStack).

### b. Compile Document

**Host terminal:**
```bash
./compile.sh
```

## 5. Ticket Workflow
- Create a ticket from `dev/templates/TICKET-template.md` in `dev/tickets/codes/` or `dev/tickets/docs/`.
- At the end of each ticket, run from the repo root:
  ```bash
  uv run dev/scripts/review_ticket.py <ticket-id>
  ```
  This requires `MISTRAL_API_KEY` in `.env` (see `.env.example`) and writes the review to `<ticket>.review.md` next to the ticket.
- The review model (primary and fallback), request settings, and prompts live in `dev/config/review_ticket.toml`; point `REVIEW_TICKET_CONFIG` at another file to override.
