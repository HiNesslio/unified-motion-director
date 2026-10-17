#!/usr/bin/env python3
"""Inspect/optionally download upstream references; NEVER execute upstream code."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EXTERNAL = ROOT / "external"
MANIFEST = ROOT / "config" / "sources.json"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--status", action="store_true", help="Check which source repos are installed")
    group.add_argument("--plan", action="store_true", help="Print what --install would clone; no network")
    group.add_argument("--install", action="store_true", help="Explicitly clone missing repos (network required)")
    args = parser.parse_args()
    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))["repositories"]
    for repo in entries:
        path = EXTERNAL / repo["id"]
        if args.status:
            if (path / ".git").exists():
                p = subprocess.run(["git", "-C", str(path), "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
                print(f"[installed] {repo['id']} {p.stdout.strip() if p.returncode == 0 else '(unknown commit)'}")
            elif path.exists():
                print(f"[review] {repo['id']}: path exists but is not a git repository")
            else:
                print(f"[missing] {repo['id']}")
        elif args.plan:
            print(f"{'SKIP exists' if path.exists() else 'CLONE'} {repo['url']} -> {path}")
            print(f"  role: {repo['role']} | third-party license: {repo['license']}")
        elif args.install:
            if path.exists():
                print(f"SKIP {path} already exists; no overwrites", flush=True)
                continue
            EXTERNAL.mkdir(exist_ok=True)
            print(f"Cloning {repo['url']} into {path} (source only, no execution)", flush=True)
            try:
                subprocess.run(["git", "clone", "--depth", "1", repo["url"], str(path)], check=True)
            except (OSError, subprocess.CalledProcessError) as e:
                print(f"ERROR: clone failed for {repo['id']}: {e}", file=sys.stderr)
                return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
