#!/usr/bin/env just --justfile
export PATH := join(justfile_directory(), ".env", "bin") + ":" + env_var('PATH')


[group('python')]
lint:
    uv run ty check
    uvx ruff check

[group('python')]
format:
    uvx black ./src

# Run Robyn in Dev mode
[group('python')]
dev: lint format
    uv run robyn ./src/chaos/__init__.py --dev

upgrade:
  uv lock --upgrade