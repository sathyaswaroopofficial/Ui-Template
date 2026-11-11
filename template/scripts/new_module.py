"""Scaffold a feature module in the standard shape.

Usage: uv run python scripts/new_module.py <module_name>      e.g.  orders, flight_logs
Creates:
  apps/api/app/modules/<name>/{__init__,models,schemas,repository,service,routes}.py
  apps/api/tests/test_<name>.py
  apps/web/src/features/<name>/{routes.tsx,index.ts,types.ts,api/,pages/}   (if apps/web exists)
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def pascal(name: str) -> str:
    return "".join(p.capitalize() for p in name.split("_"))


def camel(name: str) -> str:
    p = pascal(name)
    return p[0].lower() + p[1:]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.lstrip("\n"), encoding="utf-8", newline="\n")
    print(f"  created {path.relative_to(ROOT)}")


def backend(name: str) -> None:
    cls, url = pascal(name), name.replace("_", "-")
    base = ROOT / "apps/api/app/modules" / name
    write(base / "__init__.py", f'"""{cls} module."""\n')
    write(
        base / "models.py",
        f'''
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class {cls}(Base):
    __tablename__ = "{name}"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
''',
    )
    write(
        base / "schemas.py",
        f"""
from pydantic import BaseModel, ConfigDict, Field


class {cls}Create(BaseModel):
    name: str = Field(min_length=1, max_length=120)


class {cls}Read(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
""",
    )
    write(
        base / "repository.py",
        f"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.{name}.models import {cls}


class {cls}Repository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[{cls}]:
        return list(self.db.scalars(select({cls}).order_by({cls}.id)))

    def get(self, obj_id: int) -> {cls} | None:
        return self.db.get({cls}, obj_id)

    def add(self, obj: {cls}) -> {cls}:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
""",
    )
    write(
        base / "service.py",
        f'''
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.errors import NotFoundError
from app.modules.{name}.models import {cls}
from app.modules.{name}.repository import {cls}Repository
from app.modules.{name}.schemas import {cls}Create


class {cls}Service:
    def __init__(self, repo: {cls}Repository):
        self.repo = repo

    def list(self) -> list[{cls}]:
        return self.repo.list()

    def get(self, obj_id: int) -> {cls}:
        obj = self.repo.get(obj_id)
        if obj is None:
            raise NotFoundError(f"{cls} {{obj_id}} not found")
        return obj

    def create(self, data: {cls}Create) -> {cls}:
        return self.repo.add({cls}(name=data.name))


def get_{name}_service(db: Session = Depends(get_db)) -> {cls}Service:
    return {cls}Service({cls}Repository(db))
''',
    )
    write(
        base / "routes.py",
        f"""
from fastapi import APIRouter, Depends, status

from app.modules.{name}.schemas import {cls}Create, {cls}Read
from app.modules.{name}.service import {cls}Service, get_{name}_service

router = APIRouter()


@router.get("", response_model=list[{cls}Read])
def list_{name}(service: {cls}Service = Depends(get_{name}_service)):
    return service.list()


@router.get("/{{obj_id}}", response_model={cls}Read)
def get_{name}(obj_id: int, service: {cls}Service = Depends(get_{name}_service)):
    return service.get(obj_id)


@router.post("", response_model={cls}Read, status_code=status.HTTP_201_CREATED)
def create_{name}(data: {cls}Create, service: {cls}Service = Depends(get_{name}_service)):
    return service.create(data)
""",
    )
    write(
        ROOT / "apps/api/tests" / f"test_{name}.py",
        f"""
def test_create_and_list_{name}(client):
    res = client.post("/api/v1/{url}", json={{"name": "Example"}})
    assert res.status_code == 201
    res = client.get("/api/v1/{url}")
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_get_missing_{name}_returns_404(client):
    assert client.get("/api/v1/{url}/999").status_code == 404
""",
    )


def frontend(name: str) -> None:
    web = ROOT / "apps/web/src/features"
    if not web.parent.parent.exists():
        return
    cls, cml, url = pascal(name), camel(name), name.replace("_", "-")
    label = name.replace("_", " ").capitalize()
    base = web / name
    write(
        base / "types.ts",
        f"""
export interface {cls} {{
  id: number;
  name: string;
}}

export interface {cls}Create {{
  name: string;
}}
""",
    )
    write(
        base / "api" / f"{cml}.api.ts",
        f"""
import {{ api }} from "@/shared/api/apiClient";
import type {{ {cls}, {cls}Create }} from "../types";

const BASE = "/api/v1/{url}";

export const {cml}Api = {{
  list: () => api.get<{cls}[]>(BASE),
  create: (data: {cls}Create) => api.post<{cls}>(BASE, data),
}};
""",
    )
    write(
        base / "api" / f"use{cls}.ts",
        f'''
import {{ useQuery }} from "@tanstack/react-query";
import {{ {cml}Api }} from "./{cml}.api";

export const {cml}Keys = {{ all: ["{name}"] as const }};

export function use{cls}List() {{
  return useQuery({{ queryKey: {cml}Keys.all, queryFn: {cml}Api.list }});
}}
''',
    )
    write(
        base / "pages" / f"{cls}Page.tsx",
        f"""
import {{ EmptyState, ErrorState, LoadingState }} from "@/shared/components/StateViews";
import {{ use{cls}List }} from "../api/use{cls}";

export function {cls}Page() {{
  const list = use{cls}List();

  return (
    <section>
      <h1>{label}</h1>
      <div className="card">
        {{list.isPending ? (
          <LoadingState />
        ) : list.isError ? (
          <ErrorState message={{list.error.message}} onRetry={{() => list.refetch()}} />
        ) : list.data.length === 0 ? (
          <EmptyState title="Nothing here yet." />
        ) : (
          <ul className="list">
            {{list.data.map((row) => (
              <li key={{row.id}} className="list-row">
                {{row.name}}
              </li>
            ))}}
          </ul>
        )}}
      </div>
    </section>
  );
}}
""",
    )
    write(
        base / "routes.tsx",
        f'''
import type {{ FeatureRoute }} from "@/app/types";
import {{ {cls}Page }} from "./pages/{cls}Page";

export const featureRoutes: FeatureRoute[] = [
  {{ path: "{url}", element: <{cls}Page />, nav: {{ label: "{label}", order: 50 }} }},
];
''',
    )
    write(
        base / "index.ts",
        f"""
export {{ {cls}Page }} from "./pages/{cls}Page";
export type {{ {cls} }} from "./types";
""",
    )


def main() -> int:
    if len(sys.argv) != 2 or not re.fullmatch(r"[a-z][a-z0-9_]*", sys.argv[1]):
        print("Usage: python scripts/new_module.py <module_name>  (lowercase, snake_case)")
        return 1
    name = sys.argv[1]
    if (ROOT / "apps/api/app/modules" / name).exists():
        print(f"Module '{name}' already exists.")
        return 1
    print(f"Scaffolding module '{name}'")
    backend(name)
    frontend(name)
    # Format generated Python so it always passes `make lint`.
    py_paths = [f"apps/api/app/modules/{name}", f"apps/api/tests/test_{name}.py"]
    subprocess.run([sys.executable, "-m", "ruff", "format", "-q", *py_paths], cwd=ROOT, check=False)
    print("Done. Next: fill in the fields, then run `make check`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
