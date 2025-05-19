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

[group('python')]
upgrade:
    @uv-bump
    uv lock --upgrade

[group('docker')]
docker-build: lint format
    uv lock
    docker build -t nledford/chaos .

[group('docker')]
docker-run: docker-build
    docker run --rm -it -p '8080:8080' --name chaos nledford/chaos:latest
