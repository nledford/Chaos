#!/usr/bin/env just --justfile
export PATH := join(justfile_directory(), ".env", "bin") + ":" + env_var('PATH')


# Run Robyn in Dev mode
[group('python')]
dev:
    uv run robyn ./src/chaos/__init__.py --dev

upgrade:
  uv lock --upgrade