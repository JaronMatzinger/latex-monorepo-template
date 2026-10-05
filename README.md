# Monolith LaTeX Template

A reproducible Dev Container setup for LaTeX reports and research monoliths.

## Directory Structure
- `.devcontainer/`: Container toolchain (native Apple Silicon TeX Live)
- `.vscode/`: Workspace settings configuring LaTeX Workshop (`settings.json`)
- `compile.sh`: Host runner script invoking the container toolchain
- `report/document/`: LaTeX source files (`acronyms.tex`, `main.tex`, `references.bib`, `title_page.tex`)

## Usage

### 1. Start Environment
Open the repository in VS Code and ensure the Dev Container is running:
- `Cmd + Shift + P` -> `Dev Containers: Reopen in Container` (or run it via OrbStack).

### 2. Compile Document

**Host terminal:**
```bash
./compile.sh
```
