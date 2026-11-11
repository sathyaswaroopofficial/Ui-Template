# 2. Modular monorepo with auto-registered feature modules

Date: project start · Status: Accepted

## Context

Several developers (and AI sessions) build features in parallel. Shared entry files (route tables,
routers, menus) cause merge conflicts and drift.

## Decision

- One repository for backend, frontend and ML code.
- Code is grouped by feature: `apps/api/app/modules/<m>` and `apps/web/src/features/<m>`.
- Backend modules and frontend routes are discovered automatically; nobody edits a central list.
- Shared foundations (`core/`, `shared/`) are protected by CODEOWNERS.

## Consequences

Parallel work rarely conflicts. Modules must respect their public interfaces, enforced by lint
rules and `scripts/check_structure.py`.
