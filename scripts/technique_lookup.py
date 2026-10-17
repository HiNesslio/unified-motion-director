#!/usr/bin/env python3
"""Search locally installed Claude Motion Playbook for relevant techniques.

No third-party source text is packaged in this skill. Install the playbook repo
using source_manager.py --install (with consent) or clone it manually.
"""
import argparse
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "external" / "claude-motion-playbook" / "docs" / "techniques.md"
SYNONYMS = {
    "storyboard": "camera transition continuity",
    "分鏡": "camera transition continuity",
    "鏡頭": "camera zoom camera move",
    "轉場": "transition handoff morph",
    "字體": "typography kinetic masked",
    "動態字": "typography kinetic type",
    "介面": "UI cursor interaction",
    "巴士": "UI camera data map",
    "數據": "data counter chart graph",
    "音樂": "audio beat sound",
    "審查": "render QA popscan",
}


def parse_techniques(markdown):
    section = ""
    rows = []
    for line in markdown.splitlines():
        heading = re.match(r"^##\s+(\d+)\.\s+(.+)", line)
        if heading:
            section = heading.group(2).strip()
        if line.startswith("|") or " | " in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                name, implementation = parts[0].strip(), parts[1].strip()
                if name and len(name) < 170 and name.lower() not in ("technique", "---", "") and not name.startswith("-"):
                    if len(implementation) > 35:
                        rows.append((section, re.sub(r"\*+", "", name), implementation))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--query", required=True, help="Technique goal, e.g. 'shared element UI morphing'")
    ap.add_argument("--limit", type=int, default=6)
    ap.add_argument("--source", type=Path, default=DEFAULT)
    args = ap.parse_args()
    if not args.source.is_file():
        print("Playbook techniques.md not found locally.", file=sys.stderr)
        print(f"Expected: {args.source}", file=sys.stderr)
        print("To retrieve with user consent: python3 scripts/source_manager.py --install", file=sys.stderr)
        print("Read online: https://github.com/PHY041/claude-motion-playbook/blob/main/docs/techniques.md", file=sys.stderr)
        return 2
    q = args.query.lower()
    expanded = q + " " + " ".join(v for k, v in SYNONYMS.items() if k in q)
    tokens = {t for t in re.split(r"[^\w-]+", expanded.lower()) if len(t) >= 2}
    results = []
    for group, name, hint in parse_techniques(args.source.read_text(encoding="utf-8")):
        title = (name + " " + group).lower()
        body = (name + " " + group + " " + hint).lower()
        rank = sum(5 for t in tokens if t in title) + sum(1 for t in tokens if t in body)
        if rank:
            results.append((rank, group, name, hint))
    results.sort(reverse=True)
    if not results:
        print("No matching technique rows found. Try broader English terms (camera, morph, audio, UI).")
        return 0
    print("Source: PHY041/claude-motion-playbook (CC BY 4.0), docs/techniques.md")
    print("https://github.com/PHY041/claude-motion-playbook/blob/main/docs/techniques.md\n")
    for _, group, name, hint in results[:max(1,args.limit)]:
        # Implementation hint is from local upstream: don't falsely attribute to this skill.
        cleaned = re.sub(r"\[[^\]]+\]\([^)]+\)", "[linked example]", hint)
        print(f"[{group}] {name}\n  {cleaned[:500]}{'…' if len(cleaned)>500 else ''}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
