"""Local structural checks only; these are NOT a real Codex visual review."""
import json
import os
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import review_gate

class CodexPackagingTest(unittest.TestCase):
    def test_codex_agents_are_real_toml(self):
        for role in review_gate.REVIEWERS.values():
            doc=tomllib.loads((ROOT/'codex-agents'/f'{role}.toml').read_text())
            self.assertEqual(doc['name'],role)
            self.assertGreater(len(doc['developer_instructions']),300)
            self.assertIn('JSON',doc['developer_instructions'])

    def test_codex_cli_command_attaches_full_images(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            contact=root/'contact.jpg';contact.touch()
            frames=[root/f'{i:02}.png' for i in range(20)]
            for x in frames:x.touch()
            cmd,attached=review_gate.codex_command('/usr/bin/codex',{'contact_sheet':str(contact)},frames,root/'out.json')
            self.assertIn('read-only',cmd)
            self.assertEqual(cmd.count('--image'),9)
            self.assertEqual(len(attached),9)
            self.assertEqual(attached[0],contact)
            self.assertEqual(attached[-1],frames[-1])
            self.assertEqual(cmd[-1],'-')

    def test_installer_project_and_user_simulation(self):
        with tempfile.TemporaryDirectory() as td:
            project=Path(td)/'repo'; project.mkdir()
            cmd=[sys.executable,str(ROOT/'scripts'/'install_codex.py'),'--project',str(project),'--apply']
            proc=subprocess.run(cmd,capture_output=True,text=True)
            self.assertEqual(proc.returncode,0,proc.stderr)
            self.assertTrue((project/'.agents/skills/unified-motion-director/SKILL.md').is_file())
            self.assertTrue((project/'.codex/agents/motion-aesthetic-juror.toml').is_file())
            self.assertTrue((project/'.codex/agents/motion-holistic-juror.toml').is_file())
            again=subprocess.run(cmd,capture_output=True,text=True)
            self.assertNotEqual(again.returncode,0)
            self.assertIn('--force',again.stderr)
            force=subprocess.run(cmd+['--force'],capture_output=True,text=True)
            self.assertEqual(force.returncode,0,force.stderr)

    def test_frontmatter_name(self):
        raw=(ROOT/'SKILL.md').read_text()
        self.assertTrue(raw.startswith('---\nname: unified-motion-director\n'))
        self.assertIn('description:',raw.split('---',2)[1])

if __name__=='__main__':unittest.main()
