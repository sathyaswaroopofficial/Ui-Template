# Build from the repository root:  docker build -f apps/api/Dockerfile .
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.4.20 /uv /usr/local/bin/uv
WORKDIR /srv
COPY . .
RUN uv sync --no-dev
ENV PATH="/srv/.venv/bin:$PATH"
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--app-dir", "apps/api", "--host", "0.0.0.0", "--port", "8000"]
