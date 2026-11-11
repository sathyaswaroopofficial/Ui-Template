---
description: Scaffold a new feature module (backend + frontend) the standard way
argument-hint: <module_name>
---

Create a new feature module named `$ARGUMENTS`.

1. Run `uv run python scripts/new_module.py $ARGUMENTS` to generate the skeleton. Do not hand-create the folders.
2. Read the generated files and the example module `apps/api/app/modules/items/` to match its patterns.
3. Ask me what the module should do if it is not clear, then implement it following `CLAUDE.md`:
   models -> repository -> service -> routes -> tests, then the frontend feature.
4. Run `make check` (or the commands inside it) and fix anything that fails before reporting back.
