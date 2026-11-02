#!/usr/bin/env python3
"""Resolve merge conflicts by retaining the current branch's content."""

import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


CONFLICT_START = re.compile(r"^<{7}(?:\s|$)")
CONFLICT_SEPARATOR = re.compile(r"^={7}(?:\s|$)")
CONFLICT_END = re.compile(r"^>{7}(?:\s|$)")


def find_conflict_files() -> List[Path]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=U"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [Path(path) for path in result.stdout.splitlines() if path]


def resolve_conflicts_in_file(file_path: Path) -> Tuple[bool, str]:
    try:
        lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as error:
        return False, f"Failed to read file: {error}"

    resolved_lines = []
    in_conflict = False
    in_current_section = False
    conflict_count = 0

    for line in lines:
        if CONFLICT_START.match(line):
            in_conflict = True
            in_current_section = True
            conflict_count += 1
        elif CONFLICT_SEPARATOR.match(line) and in_conflict:
            in_current_section = False
        elif CONFLICT_END.match(line) and in_conflict:
            in_conflict = False
            in_current_section = False
        elif not in_conflict or in_current_section:
            resolved_lines.append(line)

    if in_conflict:
        return False, "Unterminated conflict block"
    if conflict_count == 0:
        return True, "No conflicts found"

    try:
        file_path.write_text("\n".join(resolved_lines) + "\n", encoding="utf-8")
    except OSError as error:
        return False, f"Failed to write file: {error}"

    return True, f"Resolved {conflict_count} conflict(s)"


def main() -> int:
    conflict_files = find_conflict_files()
    if not conflict_files:
        print("No files with unresolved conflicts found.")
        return 0

    failed_files = []
    for file_path in conflict_files:
        success, message = resolve_conflicts_in_file(file_path)
        print(f"{file_path}: {message}")
        if success:
            subprocess.run(["git", "add", str(file_path)], check=True)
        else:
            failed_files.append(file_path)

    if failed_files:
        print(f"Failed to resolve {len(failed_files)} file(s).")
        return 1

    print(f"Resolved {len(conflict_files)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
