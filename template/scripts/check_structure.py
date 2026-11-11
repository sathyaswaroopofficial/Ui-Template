"""Fail CI when the project drifts from the agreed structure.

Run: uv run python scripts/check_structure.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API_MODULES = ROOT / "apps/api/app/modules"
API_TESTS = ROOT / "apps/api/tests"
WEB_FEATURES = ROOT / "apps/web/src/features"

REQUIRED_BACKEND_FILES = ["routes.py", "service.py", "schemas.py"]
REQUIRED_FRONTEND_FILES = ["routes.tsx", "index.ts"]
CROSS_MODULE_IMPORT = re.compile(r"from app\.modules\.(\w+)\.(repository|models)")


def main() -> int:
    errors: list[str] = []

    for module in sorted(
        p for p in API_MODULES.iterdir() if p.is_dir() and p.name != "__pycache__"
    ):
        for f in REQUIRED_BACKEND_FILES:
            if not (module / f).exists():
                errors.append(f"backend module '{module.name}' is missing {f}")
        if not any(API_TESTS.glob(f"test_{module.name}*.py")):
            errors.append(f"backend module '{module.name}' has no tests (test_{module.name}.py)")
        for py in module.rglob("*.py"):
            for match in CROSS_MODULE_IMPORT.finditer(py.read_text(encoding="utf-8")):
                if match.group(1) != module.name:
                    errors.append(
                        f"{py.relative_to(ROOT)} imports another module's {match.group(2)} "
                        f"('{match.group(1)}'); use its service instead"
                    )

    if WEB_FEATURES.exists():
        for feature in sorted(p for p in WEB_FEATURES.iterdir() if p.is_dir()):
            for f in REQUIRED_FRONTEND_FILES:
                if not (feature / f).exists():
                    errors.append(f"frontend feature '{feature.name}' is missing {f}")

    if errors:
        print("Structure check failed:\n  - " + "\n  - ".join(errors))
        return 1
    print("Structure check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
