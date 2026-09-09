#!/usr/bin/env python3
"""Focused evolution-engine regressions; no repository selftest invocation."""
import json
import os
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.evolve import SkillEvolutionAnalyzer


class TestEvolution(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "demo-skill"
        self.root.mkdir()
        self.skill_md = self.root / "SKILL.md"
        self.skill_md.write_text(
            "---\nname: demo-skill\ndescription: Use when checking examples.\n---\n",
            encoding="utf-8",
        )
        self.task = self.root / ".doctor" / "research-task.json"

    def cli(self, *args, target=None):
        return subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts" / "evolve.py"),
             str(target or self.root), *args],
            capture_output=True, text=True, encoding="utf-8", timeout=20,
        )

    def snapshot(self):
        return {
            p.relative_to(self.root).as_posix():
                (p.read_bytes(), p.stat().st_mtime_ns) if p.is_file() else None
            for p in self.root.rglob("*")
        }

    def seed_task(self, status="COMPLETED"):
        analyzer = SkillEvolutionAnalyzer(self.root)
        domain, queries = analyzer.generate_research_queries()
        data = {
            "domain": domain,
            "target_skill": "demo-skill",
            "status": status,
            "queries": queries,
            "executed_queries": [queries[0]["query"]],
            "visited_sources": [{"url": "https://example.com/spec", "read": True}],
            "fringe_findings": ["Retain this finding"],
            "reviewer": "human",
            "generation_mode": "Online research",
        }
        self.task.parent.mkdir(exist_ok=True)
        self.task.write_text(json.dumps(data), encoding="utf-8")
        return data

    def test_research_preview_is_read_only_with_or_without_task(self):
        for existing in (False, True):
            with self.subTest(existing=existing):
                if existing:
                    self.seed_task()
                before = self.snapshot()
                result = self.cli("--research-plan")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(self.snapshot(), before)
                self.assertIn("--write-task", result.stdout)

    def test_explicit_task_write_preserves_same_domain_progress(self):
        result = self.cli("--research-plan", "--write-task")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(self.task.read_text())["status"],
                         "AWAITING_SEARCH_AND_PITFALLS")
        existing = self.seed_task()
        result = self.cli("--research-plan", "--write-task")
        self.assertEqual(result.returncode, 0, result.stderr)
        saved = json.loads(self.task.read_text())
        for key, value in existing.items():
            self.assertEqual(saved[key], value, key)
        self.assertEqual(saved["target_artifact"], "references/demo-skill-pitfalls.md")

    def test_changed_domain_starts_new_task(self):
        self.seed_task()
        text = self.skill_md.read_text().replace("checking examples", "deploying databases")
        self.skill_md.write_text(text, encoding="utf-8")
        result = self.cli("--research-plan", "--write-task")
        self.assertEqual(result.returncode, 0, result.stderr)
        saved = json.loads(self.task.read_text())
        self.assertEqual(saved["status"], "AWAITING_SEARCH_AND_PITFALLS")
        self.assertEqual(saved["visited_sources"], [])

    def test_offline_preserves_metadata_completed_status_and_existing_artifact(self):
        for status in ("COMPLETED", "AWAITING_SEARCH_AND_PITFALLS"):
            with self.subTest(status=status):
                existing = self.seed_task(status)
                artifact = self.root / "references" / "demo-skill-pitfalls.md"
                artifact.parent.mkdir(exist_ok=True)
                artifact.write_text("Human research", encoding="utf-8")
                result = self.cli("--offline-fallback")
                self.assertEqual(result.returncode, 0, result.stderr)
                saved = json.loads(self.task.read_text())
                for key in ("executed_queries", "visited_sources", "fringe_findings", "reviewer"):
                    self.assertEqual(saved[key], existing[key])
                self.assertEqual(saved["status"], "COMPLETED" if status == "COMPLETED"
                                 else "OFFLINE_HEURISTIC_FALLBACK")
                if status == "COMPLETED":
                    self.assertEqual(saved["generation_mode"], "Online research")
                self.assertEqual(artifact.read_text(), "Human research")
        result = self.cli("--offline-fallback", "--force")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Tier-3", artifact.read_text())

    def test_invalid_task_is_not_overwritten_or_partially_scaffolded(self):
        self.task.parent.mkdir()
        for content in ("{broken", "[]"):
            for args in (("--research-plan", "--write-task"), ("--offline-fallback",)):
                with self.subTest(content=content, args=args):
                    self.task.write_text(content, encoding="utf-8")
                    before = self.snapshot()
                    result = self.cli(*args)
                    self.assertEqual(result.returncode, 1)
                    self.assertNotIn("Traceback", result.stderr)
                    self.assertEqual(self.snapshot(), before)

    def test_conflicting_actions_and_standalone_write_task_fail_before_writes(self):
        for args in (("--research-plan", "--offline-fallback"),
                     ("--scaffold-test", "--scaffold-prompt"),
                     ("--analyze", "--plan"), ("--report-file", "report.md", "--plan"),
                     ("--write-task",)):
            with self.subTest(args=args):
                before = self.snapshot()
                result = self.cli(*args)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(self.snapshot(), before)

    def test_invalid_targets_fail_cleanly(self):
        empty = Path(self.temp.name) / "empty"
        empty.mkdir()
        for target in (empty, self.skill_md, empty / "missing"):
            with self.subTest(target=target):
                result = self.cli("--scaffold-test", target=target)
                self.assertEqual(result.returncode, 1)
                self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(list(empty.iterdir()), [])

    def test_unsafe_metadata_names_cannot_escape_or_generate_invalid_scaffolds(self):
        for name in ("../escape", "/tmp/escape", "..\\escape", 'bad"name'):
            self.skill_md.write_text(
                f"---\nname: {name}\ndescription: Use when checking examples.\n---\n",
                encoding="utf-8",
            )
            for args in (("--offline-fallback",), ("--research-plan", "--write-task"),
                         ("--scaffold-prompt",)):
                with self.subTest(name=name, args=args):
                    before = self.snapshot()
                    result = self.cli(*args)
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.root.parent / "escape-pitfalls.md").exists())

    @unittest.skipIf(os.name == "nt", "Symlinks may require administrator privileges")
    def test_research_outputs_reject_symlink_escape(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        for name in ("references", ".doctor"):
            with self.subTest(name=name):
                link = self.root / name
                link.symlink_to(outside, target_is_directory=True)
                try:
                    result = self.cli("--offline-fallback")
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertEqual(list(outside.iterdir()), [])
                finally:
                    link.unlink()

    def run_generated_selftest(self):
        return subprocess.run(
            [sys.executable, "-B", str(self.root / "scripts" / "selftest.py")],
            capture_output=True, text=True, encoding="utf-8", timeout=20,
        )

    def test_generated_suite_accepts_valid_metadata_references_and_path_exemptions(self):
        self.skill_md.write_text(
            '---\nname: "demo-skill"\ndescription: Use when checking examples.\n---\n'
            "[Fact](references/fact.card.md)\n[Nested](references/nested/other.card.md)\n"
            "Example /home/alice/demo <!-- skill-doctor: allow SEC002 -->\n",
            encoding="utf-8",
        )
        refs = self.root / "references"
        (refs / "nested").mkdir(parents=True)
        (refs / "fact.card.md").write_text("# Facts\n", encoding="utf-8")
        (refs / "nested" / "other.card.md").write_text("# More\n", encoding="utf-8")
        (self.root / "manifest.json").write_text(
            json.dumps({"name": "demo-skill", "version": "1.2.3-rc.1+build.7"}),
            encoding="utf-8",
        )
        SkillEvolutionAnalyzer(self.root).scaffold_test()
        result = self.run_generated_selftest()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with self.skill_md.open("a", encoding="utf-8") as stream:
            stream.write("Unapproved /home/alice/private\n")
        result = self.run_generated_selftest()
        self.assertEqual(result.returncode, 1)
        self.assertIn("personal path found", result.stderr)

    def test_generated_powershell_probe_quotes_apostrophes_in_paths(self):
        SkillEvolutionAnalyzer(self.root).scaffold_test()
        source = self.root / "scripts" / "user's-probe.ps1"
        source.write_text("Write-Output 'example'\n", encoding="utf-8")
        runner = runpy.run_path(str(self.root / "scripts" / "selftest.py"))
        with patch("shutil.which", return_value="pwsh"), patch("subprocess.run") as run:
            run.return_value.returncode = 0
            self.assertTrue(runner["check_ps1_syntax"](source))
        command = run.call_args.args[0][-1]
        self.assertIn(str(source).replace("'", "''"), command)

    def test_generated_selftest_parses_nested_python_without_executing_it(self):
        SkillEvolutionAnalyzer(self.root).scaffold_test()
        nested = self.root / "scripts" / "nested"
        nested.mkdir()
        source = nested / "probe.py"
        source.write_text("raise RuntimeError('must not execute')\n", encoding="utf-8")
        result = self.run_generated_selftest()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        source.write_text("def broken(:\n", encoding="utf-8")
        result = self.run_generated_selftest()
        self.assertEqual(result.returncode, 1)
        self.assertIn("Python syntax check failed", result.stderr)
        self.assertIn("probe.py", result.stderr)


if __name__ == "__main__":
    unittest.main()
