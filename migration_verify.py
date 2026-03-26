from __future__ import annotations

import filecmp
import os
import py_compile
import sys
from pathlib import Path


SOURCE = Path(r"C:\Users\Administrator\Desktop\Agent仓库\mspbots-Briefing")
TARGET = Path(r"C:\Users\Administrator\Desktop\Agent仓库\test")

ROOT_FILES = [
    ".env",
    ".gitignore",
    "AGENTS.md",
    "SOUL.md",
    "TOOLS.md",
    "USER.md",
]

ROOT_DIRS = [
    "skills",
    "templates",
]

UNWANTED_TARGET_FILES = [
    "BOOTSTRAP.md",
    "HEARTBEAT.md",
    "IDENTITY.md",
]

IGNORE_PARTS = {
    ".git",
    "__pycache__",
    "memory",
}

IGNORE_RELATIVE = {
    Path("migration_verify.py"),
}


def iter_source_files(base: Path) -> list[Path]:
    results: list[Path] = []
    for root, dirs, files in os.walk(base):
        root_path = Path(root)
        dirs[:] = [d for d in dirs if d not in IGNORE_PARTS]
        for filename in files:
            path = root_path / filename
            rel = path.relative_to(base)
            if any(part in IGNORE_PARTS for part in rel.parts):
                continue
            if rel.suffix == ".pyc":
                continue
            if rel in IGNORE_RELATIVE:
                continue
            if rel.parts and rel.parts[0] == "docs":
                continue
            results.append(rel)
    return sorted(results)


def compare_file(rel: Path, failures: list[str]) -> None:
    source_file = SOURCE / rel
    target_file = TARGET / rel
    if not target_file.exists():
        failures.append(f"Missing file: {rel}")
        return
    if not filecmp.cmp(source_file, target_file, shallow=False):
        failures.append(f"Content mismatch: {rel}")


def check_required_paths(failures: list[str]) -> None:
    for rel in ROOT_FILES:
        if not (SOURCE / rel).exists():
            failures.append(f"Source missing expected file: {rel}")
        elif not (TARGET / rel).exists():
            failures.append(f"Target missing required file: {rel}")

    for rel in ROOT_DIRS:
        if not (SOURCE / rel).is_dir():
            failures.append(f"Source missing expected directory: {rel}")
        elif not (TARGET / rel).is_dir():
            failures.append(f"Target missing required directory: {rel}")

    for rel in UNWANTED_TARGET_FILES:
        if (TARGET / rel).exists():
            failures.append(f"Unexpected bootstrap artifact present: {rel}")


def check_content_parity(failures: list[str]) -> None:
    for rel in iter_source_files(SOURCE):
        compare_file(rel, failures)


def check_python_compilation(failures: list[str]) -> None:
    for root, dirs, files in os.walk(TARGET):
        dirs[:] = [d for d in dirs if d not in IGNORE_PARTS]
        for filename in files:
            if not filename.endswith(".py"):
                continue
            path = Path(root) / filename
            rel = path.relative_to(TARGET)
            if rel.parts and rel.parts[0] == "docs":
                continue
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                failures.append(f"Python compile failure: {rel}: {exc.msg}")


def main() -> int:
    failures: list[str] = []

    if not SOURCE.exists():
        print(f"Source workspace not found: {SOURCE}")
        return 2

    if not TARGET.exists():
        print(f"Target workspace not found: {TARGET}")
        return 2

    check_required_paths(failures)
    check_content_parity(failures)
    check_python_compilation(failures)

    if failures:
        print("Migration verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Migration verification passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
