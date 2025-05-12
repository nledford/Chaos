FROM python:3.12-slim-bookworm
LABEL authors="nledford"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN uv sync --locked

#ENTRYPOINT ["top", "-b"]
EXPOSE 8080
CMD ["uv", "run", "chaos"]