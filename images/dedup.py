#!/usr/bin/env python3
"""Deduplicate images in product folders - keep 1 per colour variant, remove extra angle dupes."""
import os, glob, re

BASE = os.path.dirname(os.path.abspath(__file__))

for product in sorted(os.listdir(BASE)):
    pdir = os.path.join(BASE, product)
    if not os.path.isdir(pdir) or product.startswith('.'):
        continue
    files = sorted(f for f in os.listdir(pdir) if f.endswith('.webp'))
    if not files:
        continue

    # Group files by their base name (remove trailing _N)
    groups = {}
    for f in files:
        base = re.sub(r'_(\d+)\.webp$', '', f)
        suffix = re.search(r'_(\d+)\.webp$', f)
        idx = int(suffix.group(1)) if suffix else 0
        groups.setdefault(base, []).append((idx, f))

    removed = 0
    kept = 0
    for base, variants in groups.items():
        variants.sort()
        # Dedup: keep only the first (lowest index) frame
        for idx, fname in variants[1:]:
            os.remove(os.path.join(pdir, fname))
            removed += 1
        kept += 1

    remaining = len([f for f in os.listdir(pdir) if f.endswith('.webp')])
    print(f"{product}: {kept} unique images kept, {removed} duplicates removed, {remaining} total remaining")

print("\nDone!")
