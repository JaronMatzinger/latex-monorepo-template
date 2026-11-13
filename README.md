# Monolith LaTeX Template

A reproducible Dev Container setup for LaTeX reports and research monoliths.

## Directory Structure
- `.devcontainer/`: Container toolchain (native Apple Silicon TeX Live)
- `.vscode/`: Workspace settings configuring LaTeX Workshop (`settings.json`)
- `compile.sh`: Host runner script invoking the container toolchain
- `report/document/`: LaTeX source files (`acronyms.tex`, `main.tex`, `references.bib`, `title_page.tex`)
- `dev/`: Local agent working directory (gitignored in derived projects, see step 3)
  - `dev/tickets/`: Active tickets (`codes/` for engineering, `docs/` for report work)
  - `dev/literature/`: Literature notes and references
  - `dev/templates/`: Ticket template (`TICKET-template.md`)
  - `dev/scripts/`: Helper scripts (`review_ticket.py` verifies a finished ticket)
  - `dev/PROJECT_OVERVIEW.md`: Project architecture notes

## 1. Fork the Project on GitHub
Fork this repository to your own GitHub account.

## 2. Use This Template
Click **"Use this template"** -> **"Create a new repository"** and follow the setup prompts to scaffold your project from this template.

## 3. Add `dev/` to `.gitignore`
In your new project, add `dev/` to `.gitignore` so that tickets, review logs, and local env files stay out of version control:
```gitignore
dev/
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
