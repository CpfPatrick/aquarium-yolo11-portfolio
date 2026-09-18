from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".txt", ".py", ".ipynb"}
FORBIDDEN = (
    re.compile(r"\bPENDING\b"),
    re.compile(r"REPLACE_[A-Z0-9_]+"),
    re.compile(r"\[(?:TEST|SEALED|PUBLIC|RELEASE)[A-Z0-9_]*\]"),
    re.compile(r"/content/drive/MyDrive", re.IGNORECASE),
)


def main() -> None:
    failures: list[str] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN:
            if pattern.search(text):
                failures.append(f"{path.relative_to(ROOT)} matches {pattern.pattern}")

    if failures:
        raise SystemExit("Publication blocked:\n" + "\n".join(failures))
    print("Publication placeholder/private-path scan passed")


if __name__ == "__main__":
    main()
