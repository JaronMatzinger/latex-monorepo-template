FROM mcr.microsoft.com/devcontainers/base:debian

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    texlive-full \
    latexmk \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
