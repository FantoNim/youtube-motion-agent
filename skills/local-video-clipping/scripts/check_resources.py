#!/usr/bin/env python3
"""Read-only local Markdown links/schema resource check; does not fetch URLs."""
import json
from pathlib import Path
import re

root=Path(__file__).resolve().parents[1]
count=0
for path in root.rglob('*.md'):
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
        if '://' in target or target.startswith('#'):
            continue
        destination=(path.parent/target.split('#')[0]).resolve()
        assert destination.is_file(), (path,target)
        count+=1
json.loads((root/'assets'/'manifest.example.json').read_text(encoding='utf-8'))
assert (root.parent/'video-lesson-guide'/'SKILL.md').is_file()
assert (root.parent/'video-lesson-guide'/'references'/'local-analysis.md').is_file()
for name in ('transcribe_local.py','inspect_sample.py'):
    assert (root.parent/'video-lesson-guide'/'scripts'/name).is_file()
print('PASS: %d local Markdown links, JSON example and optional sibling resources present.'%count)
