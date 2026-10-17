#!/usr/bin/env python3
"""Safely install Unified Motion Director for local Codex user/project.
Dry-run by default. Never overwrites an existing skill or agent without --force.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ['motion-aesthetic-juror.toml', 'motion-holistic-juror.toml']


def plan(project: Path | None, user: bool, with_agents: bool = True):
    if user:
        dest_skills = Path.home()/'.agents'/'skills'/'unified-motion-director'
        agents_dir = Path.home()/'.codex'/'agents'
    else:
        assert project is not None
        dest_skills = project/'.agents'/'skills'/'unified-motion-director'
        agents_dir = project/'.codex'/'agents'
    targets = [(ROOT, dest_skills)]
    if with_agents:
        targets.extend((ROOT/'codex-agents'/name, agents_dir/name) for name in AGENTS)
    return targets


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--project', type=Path, help='Codex repo root')
    group.add_argument('--user', action='store_true', help='Install personal skill and agents')
    p.add_argument('--apply', action='store_true', help='Apply proposed copies (default: show plan)')
    p.add_argument('--force', action='store_true', help='Allow overwriting existing destination')
    p.add_argument('--no-agents', action='store_true', help='Install only skill, not agent TOMLs')
    args=p.parse_args(argv)
    project=args.project.expanduser().resolve() if args.project else None
    if project and not project.is_dir():
        p.error(f'Project path not found: {project}')
    targets=plan(project,args.user,not args.no_agents)
    for source,target in targets:
        if not source.exists(): p.error(f'Missing source file: {source}')
        if target.exists() and source.resolve() != target.resolve() and not args.force and args.apply:
            p.error(f'Already exists: {target}. Re-run with --force to overwrite intentionally')
        prefix = 'SKIP (already installed)' if source.resolve() == target.resolve() else ('INSTALL' if args.apply else 'PLAN')
        print(f'{prefix}: {source} -> {target}' + (' (exists)' if target.exists() else ''))
    if not args.apply: return 0
    for source,target in targets:
        if source.resolve() == target.resolve(): continue
        target.parent.mkdir(parents=True,exist_ok=True)
        if source.is_dir():
            if target.exists(): shutil.rmtree(target)
            shutil.copytree(source,target,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.DS_Store','external'))
        else:
            shutil.copy2(source,target)
    print('Installed Codex skill and agent configuration. Restart Codex or refresh skills if not discovered.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
