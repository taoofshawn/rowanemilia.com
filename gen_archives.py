#!/usr/bin/env python3
"""Generate per-month archive pages for Hugo based on actual posts."""
import os
import json
import glob
import re
from datetime import datetime

ARCHIVES_DIR = "content/archives"

def get_months_with_posts():
    """Get set of year/month tuples that have posts."""
    months = set()
    posts_dir = "content/posts"
    for root, dirs, files in os.walk(posts_dir):
        for f in files:
            if f.endswith('.md'):
                # Parse date from path: content/posts/YYYY/MM/filename.md
                parts = root.split(os.sep)
                if len(parts) >= 3:
                    year = parts[-2]
                    month = parts[-1]
                    if year.isdigit() and len(year) == 4 and month.isdigit():
                        months.add((int(year), int(month)))
    return sorted(months, reverse=True)

def generate_archive_files(months):
    """Create _index.md files for each month."""
    # First, identify all years
    years = sorted(set(m[0] for m in months), reverse=True)
    
    # Remove old archive files (except top-level _index.md)
    for root, dirs, files in os.walk(ARCHIVES_DIR):
        for f in files:
            if f == '_index.md' and root == ARCHIVES_DIR:
                continue
            os.remove(os.path.join(root, f))
        for d in dirs:
            full = os.path.join(root, d)
            # Remove empty dirs
            if not os.listdir(full):
                os.rmdir(full)
    
    # Create year/month directory structure
    for year in years:
        year_dir = os.path.join(ARCHIVES_DIR, str(year))
        os.makedirs(year_dir, exist_ok=True)
        
        # Create year _index.md
        # (optional - just lists months in that year)
        with open(os.path.join(year_dir, '_index.md'), 'w') as f:
            f.write(f'''---
title: "{year}"
year: {year}
---

Posts from {year}

''')
        
        for year_m, month in months:
            if year_m != year:
                continue
            month_dir = os.path.join(year_dir, f"{month:02d}")
            os.makedirs(month_dir, exist_ok=True)
            
            # Get first and last post dates for the month to determine the title
            month_name = datetime(year, month, 1).strftime("%B %Y")
            
            with open(os.path.join(month_dir, '_index.md'), 'w') as f:
                f.write(f'''---
title: "{month_name}"
year: {year}
month: "{month:02d}"
layout: archive
---

''')
            print(f"  Created: {year}/{month:02d} - {month_name}")

def main():
    months = get_months_with_posts()
    print(f"Found {len(months)} months with posts")
    for y, m in months:
        print(f"  {y}/{m:02d}")
    
    print("\nGenerating archive files...")
    generate_archive_files(months)
    print("Done!")

if __name__ == '__main__':
    main()
