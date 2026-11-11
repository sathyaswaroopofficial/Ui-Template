# Ui-Template

A reusable, production-style project template so every new application starts with the same
structure, tooling and conventions. Built with [Copier](https://copier.readthedocs.io), so
projects can also **pull in template improvements later**.

## What you get

| Part | Included |
|---|---|
| **Backend** | FastAPI · SQLAlchemy · Pydantic settings · auto-registered feature modules · one error format · auth hook · JSON logging · pytest |
| **Frontend** (optional) | React 18 · TypeScript · Vite · React Query · React Router · auto-discovered feature routes · design tokens · loading/empty/error states · Vitest · ESLint |
| **ML** (optional) | `ml_core` package (data, features, models, training, evaluation, inference) · YAML configs · baseline comparison · prediction API + UI · model card template |
| **Team tooling** | `CLAUDE.md` conventions · Claude Code slash commands (`/new-module`, `/review-conventions`) · module generator · structure check · GitHub Actions CI · CODEOWNERS · PR template · ADRs · Makefile · docker-compose |

## Create a new project

Prerequisites: Python 3.12+, [uv](https://docs.astral.sh/uv/), Git, and Node.js 20+ if you want the frontend.

```bash
uv tool install copier
copier copy gh:sathyaswaroopofficial/Ui-Template my-new-project
cd my-new-project
git init && git add . && git commit -m "chore: scaffold from Ui-Template"
make setup
```

Copier asks:

- **Project name / slug / description / author**
- **Project type**: `web` (React + FastAPI) or `ml` (adds `ml_core`, training pipeline and prediction API)
- **Include frontend?** yes/no
- **Database**: SQLite (zero setup) or PostgreSQL (via Docker)

## Keep projects in sync with the template

When you improve this template, tag a release (`git tag v1.1.0 && git push --tags`), then in any project:

```bash
copier update
```

Copier merges the template changes into the project and shows conflicts like a Git merge.
Projects remember their answers in `.copier-answers.yml`. Don't delete that file.

## Generated project layout

```
my-new-project/
├── apps/
│   ├── api/                 FastAPI backend
│   │   ├── app/core/        config, db, auth, errors, logging
│   │   ├── app/modules/     one folder per feature (auto-mounted at /api/v1/<name>)
│   │   └── tests/
│   └── web/                 React frontend (optional)
│       └── src/{app,features,shared,styles}
├── ml/                      ml_core package, configs, pipelines, notebooks (ml projects)
├── data/  models/           local data & artifacts, git-ignored (ml projects)
├── docs/adr/                architecture decision records
├── scripts/                 new_module.py, check_structure.py
├── .claude/commands/        shared Claude Code slash commands
├── .github/                 CI, CODEOWNERS, PR template
├── CLAUDE.md                conventions for humans and AI assistants
├── Makefile  docker-compose.yml  pyproject.toml  .env.example
```

## Developing this template

Template files live in `template/`. Files ending in `.jinja` are rendered with the answers;
folder names like `{% if include_frontend %}web{% endif %}` are only created when the condition is true.

Test changes by generating projects locally (uncommitted changes are included):

```bash
copier copy --defaults --vcs-ref HEAD . ../test-web
copier copy --defaults --vcs-ref HEAD -d project_type=ml . ../test-ml
cd ../test-ml && uv sync && uv run pytest && uv run python scripts/check_structure.py
```
