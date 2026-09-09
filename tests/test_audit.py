#!/usr/bin/env python3
"""Audit output, read-only defaults and negative execution regressions."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts import audit


class TestAudit(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "sample-skill"
        (self.root / "scripts").mkdir(parents=True)
        self.skill_text = (
            "---\nname: sample-skill\ndescription: 当用户要求技能体检时使用。\n---\n"
            "# Sample\n运行 `scripts/selftest.py`。\n"
        )
        (self.root / "SKILL.md").write_text(self.skill_text, encoding="utf-8")
        self.selftest = self.root / "scripts" / "selftest.py"
        self.selftest.write_text("# negative fixture\nprint('SELFTEST PASS')\n", encoding="utf-8")

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts" / "audit.py"), str(self.root), *args],
            capture_output=True, text=True, encoding="utf-8", timeout=30,
        )

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes()
                for p in self.root.rglob("*") if p.is_file()}

    def test_default_and_report_are_read_only(self):
        before = self.snapshot()
        for args in ((), ("--stdout",), ("--report",), ("--json",)):
            with self.subTest(args=args):
                result = self.run_cli(*args)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(before, self.snapshot())

    def test_json_and_report_file_both_work(self):
        report = Path(self.temp.name) / "reports" / "audit.md"
        result = self.run_cli("--json", "--report-file", str(report))
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["dynamic"], {"requested": False, "status": "NOT_RUN"})
        self.assertIn("NOT_RUN", report.read_text(encoding="utf-8"))
        self.assertFalse((self.root / "audit-report.txt").exists())

    def test_report_uses_actual_dynamic_result(self):
        cases = [
            ("print('SELFTEST PASS')\n", "PASS", 0),
            ("raise RuntimeError('negative fixture')\n", "FAIL", 1),
            ("print('RESULT FAIL')\n", "FAIL", 1),
            ("print('SELFTEST PASS')\nraise SystemExit(1)\n", "FAIL", 1),
        ]
        for source, status, rc in cases:
            with self.subTest(source=source):
                self.selftest.write_text(source, encoding="utf-8")
                result = self.run_cli("--dynamic", "--report")
                self.assertEqual(result.returncode, rc, result.stderr)
                l2 = next(line for line in result.stdout.splitlines() if "**L2 动态执行**" in line)
                self.assertIn(f"| {status} |", l2)
                self.assertNotIn("实跑通过", l2)

    def test_evals_are_not_reported_as_executed(self):
        self.selftest.unlink()
        (self.root / "evals").mkdir()
        (self.root / "evals" / "cases.json").write_text(
            '[{"type": "negative", "should_trigger": false}]', encoding="utf-8")
        result = self.run_cli("--dynamic", "--json")
        self.assertEqual(json.loads(result.stdout)["dynamic"]["status"], "SKIPPED")

    def test_timeout_and_launch_error_are_dynamic_failures(self):
        for exc in (subprocess.TimeoutExpired("selftest", 1), OSError("cannot start")):
            with self.subTest(error=type(exc).__name__):
                findings = audit.Findings()
                with patch.object(audit.subprocess, "run", side_effect=exc):
                    audit.check_dynamic(self.root, findings, True, timeout=1)
                self.assertEqual(findings.dynamic_status, "FAIL")
                self.assertTrue(any(level == "FAIL" and code == "DY003"
                                    for level, code, _ in findings.items))

    def test_static_failure_does_not_change_dynamic_pass(self):
        findings = audit.Findings()
        findings.add("FAIL", "FM003", "bad name")
        audit.check_dynamic(self.root, findings, True)
        report, rc = audit.render_full_markdown_report(self.root, findings, "test", ("CLI", "test"))
        self.assertEqual(rc, 1)
        l2 = next(line for line in report.splitlines() if "**L2 动态执行**" in line)
        self.assertIn("| PASS |", l2)

    def test_report_metrics_match_static_checks_and_escape_cells(self):
        text = self.skill_text + "必须验证。" * 16
        (self.root / "SKILL.md").write_text(text, encoding="utf-8")
        findings = audit.run_static_audit(self.root)
        findings.add("WARN", "DY002", "left|right\nnext")
        report, _ = audit.render_full_markdown_report(self.root, findings, "test", ("CLI", "test"))
        self.assertIn(f"~{audit.estimate_tokens(text)} Tokens", report)
        self.assertIn("| 16 处 |", report)
        self.assertIn("left&#124;right<br>next", report)
        self.assertIn("| NOT_RUN |", report)

    def test_invalid_flags_and_output_errors_are_clear(self):
        for args in (("--timeout", "0"), ("--json", "--report"),
                     ("--report-file", str(self.root))):
            with self.subTest(args=args):
                result = self.run_cli(*args)
                self.assertEqual(result.returncode, 2)
                self.assertTrue(result.stderr)
                self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
