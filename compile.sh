#!/usr/bin/env bash
set -euo pipefail

# Ensure target output directory exists
mkdir -p report/PDF

COMPILE_CMD="latexmk -synctex=1 -interaction=nonstopmode -file-line-error -pdf -outdir=../PDF main.tex"

# Case 1: Running inside the Dev Container or a system with latexmk installed
if command -v latexmk &> /dev/null; then
    echo "Running compilation locally inside container..."
    cd report/document
    $COMPILE_CMD
    exit 0
fi

# Case 2: Running from macOS host via Docker/OrbStack
WORKSPACE_NAME="$(basename "$(pwd)")"
CONTAINER_ID=$(docker ps -q --filter "label=devcontainer.local_folder=$(pwd)")

if [ -z "$CONTAINER_ID" ]; then
    echo "Error: Dev container is not running. Open VS Code or start it in OrbStack first."
    exit 1
fi

echo "Running compilation via Dev Container ($CONTAINER_ID)..."
docker exec -w "/workspaces/${WORKSPACE_NAME}/report/document" "$CONTAINER_ID" \
    bash -c "$COMPILE_CMD"
