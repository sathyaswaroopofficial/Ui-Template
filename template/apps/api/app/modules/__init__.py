"""Feature modules. Each sub-package is auto-registered: never edit a central routes file.

Contract for a module package app/modules/<name>/:
  routes.py      must define `router: APIRouter`; optional `PUBLIC = True` skips auth
  service.py     business logic
  schemas.py     Pydantic request/response models
  repository.py  persistence (optional, with models.py)

Routes are mounted at /api/v1/<name> (underscores become dashes).
"""

import importlib
import pkgutil

from fastapi import Depends, FastAPI

from app.core.auth import require_auth


def register_modules(app: FastAPI) -> None:
    for info in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
        if not info.ispkg:
            continue
        routes = importlib.import_module(f"{__name__}.{info.name}.routes")
        dependencies = [] if getattr(routes, "PUBLIC", False) else [Depends(require_auth)]
        app.include_router(
            routes.router,
            prefix=f"/api/v1/{info.name.replace('_', '-')}",
            tags=[info.name],
            dependencies=dependencies,
        )
