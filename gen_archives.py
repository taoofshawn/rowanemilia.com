#!/usr/bin/env python3
"""Generate per-month archive pages for Hugo based on actual posts."""
import os
from datetime import datetime

ARCHIVES_DIR: str = "content/archives"


def get_months_with_posts() -> list[tuple[int, int]]:
    """Get sorted list of (year, month) tuples that have posts."""
    months: set[tuple[int, int]] = set()
    posts_dir: str = "content/posts"
    for root, _dirs, files in os.walk(posts_dir):
        for f in files:
            if not f.endswith('.md'):
                continue
            # Parse date from path: content/posts/YYYY/MM/filename.md
            parts: list[str] = os.path.normpath(root).split(os.sep)
            if len(parts) >= 2:
                year_str: str = parts[-2]
                month_str: str = parts[-1]
                if year_str.isdigit() and len(year_str) == 4 and month_str.isdigit():
                    months.add((int(year_str), int(month_str)))
    return sorted(months, reverse=True)


def _remove_old_archives() -> None:
    """Remove all generated archive files except the top-level _index.md."""
    for root, dirs, files in os.walk(ARCHIVES_DIR):
        for f in files:
            full = os.path.join(root, f)
            if f == '_index.md' and os.path.samefile(root, ARCHIVES_DIR):
                continue
            os.remove(full)
        for d in dirs:
            full = os.path.join(root, d)
            if not os.listdir(full):
                os.rmdir(full)


def _write_year_index(year: int) -> None:
    """Write the _index.md for a year-level archive page."""
    year_dir: str = os.path.join(ARCHIVES_DIR, str(year))
    os.makedirs(year_dir, exist_ok=True)
    with open(os.path.join(year_dir, '_index.md'), 'w') as f:
        _ = f.write(f"""---
title: "{year}"
year: {year}
---

Posts from {year}

""")


def _write_month_index(year: int, month: int) -> None:
    """Write the _index.md for a month-level archive page."""
    month_dir: str = os.path.join(ARCHIVES_DIR, str(year), f"{month:02d}")
    os.makedirs(month_dir, exist_ok=True)
    month_name: str = datetime(year, month, 1).strftime("%B %Y")
    with open(os.path.join(month_dir, '_index.md'), 'w') as f:
        _ = f.write(f"""---
title: "{month_name}"
year: {year}
month: "{month:02d}"
layout: archive
---

""")
    print(f"  Created: {year}/{month:02d} - {month_name}")


def generate_archive_files(months: list[tuple[int, int]]) -> None:
    """Create _index.md files for each month and year."""
    years: list[int] = sorted(set(m[0] for m in months), reverse=True)

    _remove_old_archives()

    for year in years:
        _write_year_index(year)
        for year_m, month in months:
            if year_m == year:
                _write_month_index(year, month)


def main() -> None:
    months: list[tuple[int, int]] = get_months_with_posts()
    print(f"Found {len(months)} months with posts")
    for y, m in months:
        print(f"  {y}/{m:02d}")

    print("\nGenerating archive files...")
    generate_archive_files(months)
    print("Done!")


if __name__ == '__main__':
    main()
