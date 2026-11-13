#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "mistralai",
#     "python-dotenv",
# ]
# ///
import os
import re
import subprocess
import sys
import textwrap
from pathlib import Path
from dotenv import load_dotenv
from mistralai.client import Mistral

# --- Load .env immediately on import ---
# Script lives at <repo>/dev/scripts/review_ticket.py; check repo root and dev/.
_repo_root = Path(__file__).resolve().parents[2]
for env_path in (_repo_root / ".env", _repo_root / "dev" / ".env"):
    load_dotenv(dotenv_path=env_path)
# Fallback to local cwd .env if not found relative to script
load_dotenv()


def run_cmd(cmd: list[str]) -> tuple[int, str]:
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = res.stdout
    if res.stderr:
        out += ("\n" if out else "") + "STDERR:\n" + res.stderr
    return res.returncode, out.strip()


def resolve_ticket_path(arg: str) -> Path:
    filename = arg if arg.endswith(".md") else f"{arg}.md"
    candidate = Path(filename)
    if candidate.exists():
        return candidate

    search_dirs = [
        Path("dev/tickets/codes"),
        Path("dev/tickets/docs"),
        Path("dev/tickets"),
    ]
    for d in search_dirs:
        p = d / filename
        if p.exists():
            return p

    print(f"Error: Could not locate ticket '{arg}' in {search_dirs}")
    sys.exit(1)


def get_git_diff() -> str:
    # 1. Uncommitted changes (staged + unstaged vs HEAD)
    _, diff = run_cmd(["git", "diff", "HEAD"])

    # 2. Include untracked files
    _, untracked_raw = run_cmd(["git", "ls-files", "--others", "--exclude-standard"])
    untracked_files = [f for f in untracked_raw.splitlines() if f.strip()]
    untracked_diff = ""
    for f in untracked_files:
        p = Path(f)
        if p.is_file() and p.stat().st_size < 150_000:
            untracked_diff += f"\n--- /dev/null\n+++ b/{f}\n" + p.read_text(errors="replace")

    full_diff = (diff + untracked_diff).strip()

    # 3. Fallback: if working tree is clean, inspect latest commit
    if not full_diff or full_diff == "(no diff detected)":
        _, full_diff = run_cmd(["git", "diff", "HEAD~1...HEAD"])

    # 4. Fallback: compare with main if still empty
    if not full_diff:
        _, full_diff = run_cmd(["git", "diff", "origin/main...HEAD"])

    return full_diff if full_diff else "(no diff detected)"


def load_repository_invariants() -> str:
    invariants = []

    # 1. Core Econometric Mandate & Validation Hierarchy
    overview_file = Path("dev/PROJECT_OVERVIEW.md")
    if overview_file.exists():
        invariants.append("### Project Architecture (from PROJECT_OVERVIEW.md):\n" + overview_file.read_text().strip())

    # 2. Operating Contract & Technical Invariants
    agents_file = Path("AGENTS.md")
    if agents_file.exists():
        invariants.append("### Master Invariants (from AGENTS.md):\n" + agents_file.read_text().strip())
    
    return "\n\n".join(invariants)


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run dev/scripts/review_ticket.py <ticket_id_or_path>")
        sys.exit(1)

    ticket_path = resolve_ticket_path(sys.argv[1])
    is_doc = "docs" in ticket_path.parts or "DOC" in ticket_path.stem.upper()

    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        zshrc = Path.home() / ".zshrc"
        if zshrc.exists():
            match = re.search(r'export\s+MISTRAL_API_KEY=["\']?([^"\'\n]+)["\']?', zshrc.read_text())
            if match:
                api_key = match.group(1).strip()
    if not api_key:
        print("Error: MISTRAL_API_KEY environment variable is not set.")
        sys.exit(1)

    print(f"Reviewing ticket: {ticket_path} (Type: {'DOCS' if is_doc else 'WPS'})")

    ticket_content = ticket_path.read_text()
    git_diff = get_git_diff()
    invariants_context = load_repository_invariants()

    diff_char_limit = 50_000
    if len(git_diff) > diff_char_limit:
        diff_payload = git_diff[:diff_char_limit] + "\n\n[WARNING: DIFF TRUNCATED DUE TO SIZE LIMIT]"
    else:
        diff_payload = git_diff

    verification_section = ""
    if is_doc:
        print("Validating document build via ./compile.sh clean...")
        compile_script = Path("./compile.sh")
        if compile_script.exists():
            code, compile_output = run_cmd(["./compile.sh", "clean"])
            verification_section = (
                f"\n### Build Verification (`./compile.sh clean`)\n"
                f"Exit Code: {code}\n"
                f"```plaintext\n{compile_output[-4000:]}\n```\n"
            )
        role_description = "an expert quantitative econometrician, technical editor, and thesis supervisor"
        review_criteria = textwrap.dedent("""
        1. Rigorously check LaTeX syntax, equation labels, and List of Equations registration (`\\myequations`).
        2. Ensure strict adherence to style invariants: ZERO em dashes anywhere (use commas, parentheses, colons).
        3. Verify all mathematical formulations match the theoretical specifications in the ticket.
        4. Check that compilation reported 0 errors and 0 undefined citations.
        5. Verdict:
           - If PASS: Output "[VERDICT: PASS]" followed by concise bullet points.
           - If FAIL: Output "[VERDICT: FAIL]", explain precisely what failed, and provide the remediation ticket wrapped strictly between `NEXT_TICKET` and `END_NEXT_TICKET` tokens.
        """).strip()
    else:
        print("Running pytest test suite...")
        code, test_output = run_cmd(["uv", "run", "pytest", "-v", "-W", "error"])
        
        # If passed, only send the tail summary; if failed, send the tracebacks
        lines = test_output.splitlines()
        if code == 0:
            compact_test_output = "\n".join(lines[-25:])
        else:
            compact_test_output = "\n".join(lines[-150:])

        verification_section = (
            f"\n### Test Suite Output (`pytest`)\n"
            f"Exit Code: {code}\n"
            f"```plaintext\n{compact_test_output}\n```\n"
        )
        role_description = "a senior quantitative software engineer and econometric QA lead"
        review_criteria = textwrap.dedent("""
        1. Verify that all implementation requirements and mathematical equations in the ticket are fulfilled.
        2. Scrutinize test rigor: confirm tests assert non-trivial edge cases, numerical tolerances, and invariants.
        3. Verify that test exit code is 0 with zero warnings.
        4. Verdict:
           - If PASS: Output "[VERDICT: PASS]" followed by concise bullet points.
           - If FAIL: Output "[VERDICT: FAIL]", detail specifically what failed, and provide the remediation ticket wrapped strictly between `NEXT_TICKET` and `END_NEXT_TICKET` tokens.
        """).strip()

    prompt = textwrap.dedent(f"""
    You are {role_description} evaluating an implementation artifact.

    {invariants_context}

    ### Target Ticket ({ticket_path})
    {ticket_content}

    ### Verification Execution
    {verification_section}

    ### Git Diff
    ```diff
    {diff_payload}
    ```

    ### Review Criteria:
    {review_criteria}
    """).strip()

    model_name = "zai-glm-5-3"
    print(f"Submitting context for automated review using {model_name}...")
    client = Mistral(api_key=api_key, timeout_ms=300_000)

    try:
        response = client.chat.complete(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
    except Exception as e:
        print(f"Request failed with {e}. Falling back to 'codestral-latest'...")
        response = client.chat.complete(
            model="codestral-latest",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )

    review_text = response.choices[0].message.content
    # Some models (e.g. zai-glm-5-3) return ``content`` as a list of content
    # blocks instead of a plain string (ThinkChunk / TextChunk, or plain
    # str/dict items); keep only the text blocks and join into one string.
    if isinstance(review_text, list):
        parts = []
        for block in review_text:
            if isinstance(block, str):
                parts.append(block)
                continue
            btype = block.get("type") if isinstance(block, dict) else getattr(
                block, "type", None
            )
            if btype not in (None, "text"):
                continue  # skip thinking / non-text blocks
            text = (
                block.get("text")
                if isinstance(block, dict)
                else getattr(block, "text", None)
            )
            if isinstance(text, str) and text:
                parts.append(text)
        review_text = "\n".join(parts)
    if not isinstance(review_text, str):
        review_text = str(review_text)
    print("\n" + "=" * 60)
    print(review_text)
    print("=" * 60 + "\n")

    review_log_path = ticket_path.with_suffix(".review.md")
    review_log_path.write_text(review_text)
    print(f"Review saved to: {review_log_path}")

    if "[VERDICT: FAIL]" in review_text:
        match = re.search(r"NEXT_TICKET\s*([\s\S]*?)\s*END_NEXT_TICKET", review_text)
        remedy_path = ticket_path.parent / f"{ticket_path.stem}_remediation.md"
        if match:
            remedy_content = match.group(1).strip()
            # Clean possible markdown block wrappers inside the match
            if remedy_content.startswith("```"):
                remedy_content = re.sub(r"^```[a-zA-Z]*\n", "", remedy_content)
                remedy_content = re.sub(r"\n```$", "", remedy_content)
            remedy_path.write_text(remedy_content)
            print(f"Remediation ticket automatically generated: {remedy_path}")
        else:
            print("Failed verdict detected, but NEXT_TICKET delimiter block was missing or malformed.")


if __name__ == "__main__":
    main()
