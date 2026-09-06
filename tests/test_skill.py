#!/usr/bin/env python3
"""skill-doctor 单元测试与语法完整性回归套件。"""
import ast
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class TestSkillDoctor(unittest.TestCase):
    """验证 skill-doctor 核心脚本语法与自测完整性。"""

    def test_scripts_ast_syntax(self):
        """负向防线：确保所有 scripts/ 脚本符合 Python AST 规范，无语法解析破坏。"""
        scripts_dir = ROOT / "scripts"
        self.assertTrue(scripts_dir.is_dir(), "scripts 目录应存在")
        py_files = list(scripts_dir.glob("*.py"))
        self.assertGreater(len(py_files), 0, "应有 Python 脚本")
        for py_file in py_files:
            with self.subTest(file=py_file.name):
                code = py_file.read_text(encoding="utf-8", errors="ignore")
                parsed = ast.parse(code)
                self.assertIsNotNone(parsed, f"{py_file.name} AST 解析不可为空")

    def test_selftest_execution(self):
        """验证 selftest 主回归套件执行成功。"""
        from scripts import selftest
        rc = selftest.main()
        self.assertEqual(rc, 0, "selftest 应返回 0")


if __name__ == "__main__":
    unittest.main()
