#!/usr/bin/env python3
"""skill-doctor audit.py 自测：好夹具全绿 + 坏夹具逐规则被抓。

用法: python selftest.py
零依赖。夹具建在系统临时目录，跑完即删。
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

AUDIT = Path(__file__).resolve().parent / "audit.py"
TRIGGER_EVAL = Path(__file__).resolve().parent / "trigger_eval.py"

GOOD_SKILL_MD = """---
name: good-skill
description: 演示合规夹具。当用户要求审查技能时使用，触发词齐全。
---

# Good Skill

先读 [规则](references/rules.md)，跑 `scripts/tool.py`，回归用 `scripts/selftest.py`。
"""

GOOD_RULES = "# Rules\n\n不到 100 行的参考文件。\n"

GOOD_TOOL = '''#!/usr/bin/env python3
"""演示脚本：有 docstring、shebang、退出码语义正确。"""
import sys

if __name__ == "__main__":
    ok = True
    if not ok:
        print("RESULT FAIL")
        sys.exit(1)
    print("RESULT PASS")
'''

# 负向：此夹具技能的负向示例（触发词仅为让 DY002 扫描命中）
GOOD_SELFTEST = '''#!/usr/bin/env python3
# 负向示例占位：正式技能应在此构造该 FAIL 的破坏夹具
print("SELFTEST PASS (1 checks)")
'''

CRASH_SELFTEST = '''#!/usr/bin/env python3
raise RuntimeError("boom")
'''

LYING_SELFTEST = '''#!/usr/bin/env python3
import sys
print("SELFTEST PASS (1 checks)")
sys.exit(1)
'''

BAD_SKILL_MD = """---
name: Claude-WrongName
description: I can help you <fix> documents. 一个纯粹的功能性描述文本。
compatibility: 环境需要大量依赖才能运行于各种复杂系统之中
---

# Bad Skill

引用不存在的文件：[missing](references/missing.md)，跑 `scripts/ghost.py`。
本机路径示例 C:\\Users\\someone\\secret。
"""

# 夹具内容运行时拼接生成：源码里不出现完整违规字面量，避免本文件被 audit 误报
BAD_LEAK = "\n".join([
    "import os",
    'key = "' + "sk-" + "a" * 28 + '"',
    "try:",
    "    import optional",
    "except ImportError:",
    "    pass",
    "try:",
    "    load_config()",
    "except Exception:",
    "    pass",
    'print("skipped figure")',
    'print("RESULT FAIL")',
])

# 危险动态执行样例拼接（ev+al 拆开写，规避 audit 扫本文件时误报 SF005）
DANGER_SCRIPT = "\n".join([
    "import os",
    "os.s" + "ystem('ls -la')",
    "x = ev" + "al('1 + 1')",
])

# 交互提示样例拼接（in+put 拆开写，规避 audit 扫本文件时误报 SF006）
ASK_SCRIPT = "name = in" + "put('What is your name? ')\n"

# SEC002 编码形态负向夹具：双反斜杠/正斜杠形态的 Windows 个人路径
# 拼接生成（chr(92)=反斜杠），源码不出现完整违规字面量，同 BAD_LEAK 惯例
LEAK_FORMS = "\n".join([
    "A = 'C:" + chr(92) * 2 + "Users" + chr(92) * 2 + "someone" + chr(92) * 2 + "a.ini'",
    "B = 'C:" + "/" + "Users/someone/b.txt'",
])

BAD_NESTED = "---\nname: nested\n---\n嵌套入口。\n"

UTF16_NOTE = "这个文件是 UTF-16 编码，会坑回读。"

# FM005 负向：compatibility 超 500 字符 + allowed-tools 含逗号（拼接超长串）
BAD_FM_COMPAT = "环境要求" + "X" * 520


def run_audit(target: Path, *extra: str) -> tuple[int, str]:
    result = subprocess.run([sys.executable, str(AUDIT), str(target), "--stdout", *extra],
                            capture_output=True, text=True, encoding="utf-8", errors="replace")
    return result.returncode, result.stdout


def build_good(tmp: Path) -> Path:
    good = tmp / "good-skill"
    (good / "references").mkdir(parents=True)
    (good / "scripts").mkdir()
    (good / "SKILL.md").write_text(GOOD_SKILL_MD, encoding="utf-8")
    (good / "references" / "rules.md").write_text(GOOD_RULES, encoding="utf-8")
    (good / "scripts" / "tool.py").write_text(GOOD_TOOL, encoding="utf-8")
    (good / "scripts" / "selftest.py").write_text(GOOD_SELFTEST, encoding="utf-8")
    return good


def build_bad(tmp: Path) -> Path:
    root = tmp / "bad-skill"
    (root / "references").mkdir(parents=True)
    (root / "scripts").mkdir()
    (root / "nested").mkdir()
    (root / "SKILL.md").write_text(BAD_SKILL_MD, encoding="utf-8")
    (root / "nested" / "SKILL.md").write_text(BAD_NESTED, encoding="utf-8")
    (root / "scripts" / "leaky.py").write_text(BAD_LEAK, encoding="utf-8")
    (root / "scripts" / "danger.py").write_text(DANGER_SCRIPT, encoding="utf-8")
    (root / "scripts" / "ask.py").write_text(ASK_SCRIPT, encoding="utf-8")
    (root / "scripts" / "run.sh").write_text("#!/bin/bash\nls -la\n", encoding="utf-8")
    (root / "references" / "orphan.md").write_text("# 孤儿参考文件，无人引用\n", encoding="utf-8")
    (root / "notes.txt").write_bytes(("\ufeff" + UTF16_NOTE).encode("utf-16"))
    return root


def build_bad_fm(tmp: Path) -> Path:
    """FM005 负向：compatibility 超 500 + allowed-tools 含逗号（其余合规）。"""
    root = tmp / "bad-fm"
    (root / "scripts").mkdir(parents=True)
    (root / "SKILL.md").write_text(
        "---\nname: bad-fm\ndescription: 当用户需要合规检查时使用。\n"
        f"compatibility: {BAD_FM_COMPAT}\n"
        "allowed-tools: Bash(git:*), Bash(jq:*)\n---\n正文\n",
        encoding="utf-8")
    (root / "scripts" / "selftest.py").write_text(GOOD_SELFTEST, encoding="utf-8")
    return root


def build_bad_token(tmp: Path) -> Path:
    """SK005 负向：SKILL.md 正文超 5000 token（CJK 按 1 字符 1 token 粗估）。"""
    root = tmp / "bad-token"
    (root / "scripts").mkdir(parents=True)
    body = "这是一个很长的说明文字。" * 500  # ~5500 汉字 > 5000 token 阈值
    (root / "SKILL.md").write_text(
        "---\nname: bad-token\ndescription: 当用户需要演示 token 超限时使用。\n---\n" + body,
        encoding="utf-8")
    (root / "scripts" / "selftest.py").write_text(GOOD_SELFTEST, encoding="utf-8")
    return root


def clone_good(tmp: Path, name: str, selftest_src: str) -> Path:
    root = tmp / name
    (root / "references").mkdir(parents=True)
    (root / "scripts").mkdir()
    (root / "SKILL.md").write_text(GOOD_SKILL_MD.replace("name: good-skill", f"name: {name}"), encoding="utf-8")
    (root / "references" / "rules.md").write_text(GOOD_RULES, encoding="utf-8")
    (root / "scripts" / "tool.py").write_text(GOOD_TOOL, encoding="utf-8")
    (root / "scripts" / "selftest.py").write_text(selftest_src, encoding="utf-8")
    return root


def main() -> int:
    checks = 0
    with tempfile.TemporaryDirectory() as tmp_name:
        tmp = Path(tmp_name)

        good = build_good(tmp)
        rc, out = run_audit(good)
        if rc != 0 or "RESULT PASS" not in out:
            raise RuntimeError(f"好夹具应全绿：\n{out}")
        checks += 1

        rc, out = run_audit(good, "--dynamic")
        if rc != 0 or "RESULT PASS" not in out:
            raise RuntimeError(f"好夹具动态实跑应通过：\n{out}")
        if "selftest 实跑通过" not in out:
            raise RuntimeError(f"DY003 应报实跑通过：\n{out}")
        checks += 1

        # 动态层负向：无 selftest → DY001 FAIL
        bare = tmp / "bare-skill"
        (bare / "scripts").mkdir(parents=True)
        (bare / "SKILL.md").write_text(
            "---\nname: bare-skill\ndescription: 无自测夹具。当用户要求演示时使用。\n---\n正文\n",
            encoding="utf-8")
        rc, out = run_audit(bare)
        if rc != 1 or "DY001" not in out or not any(l.startswith("FAIL") and "[DY001]" in l for l in out.splitlines()):
            raise RuntimeError(f"无 selftest 应 DY001 FAIL：\n{out}")
        checks += 1

        # 坑 25 回归：tests/ 布局（无 selftest.py）应识别为回归入口，DY001 不再误判 FAIL
        pytest_layout = tmp / "pytest-skill"
        (pytest_layout / "tests").mkdir(parents=True)
        (pytest_layout / "SKILL.md").write_text(
            "---\nname: pytest-skill\ndescription: pytest 布局夹具。当用户要求演示时使用。\n---\n正文\n",
            encoding="utf-8")
        (pytest_layout / "tests" / "verify_core.py").write_text(
            "# 负向用例：篡改输入应被拦\ndef test_tamper():\n    assert True\n",
            encoding="utf-8")
        rc, out = run_audit(pytest_layout)
        if rc != 0 or "FAIL [DY001]" in out or "回归入口存在（tests）" not in out:
            raise RuntimeError(f"tests/ 布局应识别为回归入口（坑 25）：\n{out}")
        if not any(l.startswith("OK") and "[DY002]" in l for l in out.splitlines()):
            raise RuntimeError(f"tests/ 含负向特征字样应 DY002 OK：\n{out}")
        checks += 1

        # 坑 26 回归：tests/ 夹具里的假密钥应 SEC001 WARN 而非 FAIL
        # 夹具只含密钥违规（BAD_LEAK 会带进裸 except 干扰 SF001a，故单独拼）
        fixture_leak = clone_good(tmp, "fixture-leak-skill", GOOD_SELFTEST)
        (fixture_leak / "tests").mkdir()
        (fixture_leak / "tests" / "test_secret_gate.py").write_text(
            "# 负向用例：此假密钥应降级 WARN\ndef test_gate():\n    return True\n"
            + 'key = "' + "sk-" + "b" * 28 + '"\n',
            encoding="utf-8")
        rc, out = run_audit(fixture_leak)
        if rc != 0 or any(l.startswith("FAIL") and "[SEC001]" in l for l in out.splitlines()) \
                or not any(l.startswith("WARN") and "[SEC001]" in l for l in out.splitlines()):
            raise RuntimeError(f"tests/ 假密钥应降级 WARN（坑 26）：\n{out}")
        checks += 1

        # 动态层负向：selftest 崩溃 → DY003 FAIL（疑似崩溃）
        crash = clone_good(tmp, "crash-skill", CRASH_SELFTEST)
        rc, out = run_audit(crash, "--dynamic")
        if rc != 1 or "疑似崩溃" not in out:
            raise RuntimeError(f"崩溃 selftest 应被抓：\n{out}")
        checks += 1

        # 动态层负向：报 PASS 但退出码 1 → DY003 FAIL（语义反向）
        lying = clone_good(tmp, "lying-skill", LYING_SELFTEST)
        rc, out = run_audit(lying, "--dynamic")
        if rc != 1 or "退出码语义反向" not in out:
            raise RuntimeError(f"说谎 selftest 应被抓：\n{out}")
        checks += 1

        # 豁免机制负向：allow-block 只豁免指定规则，不得殃及他项
        exempt = clone_good(tmp, "exempt-skill", GOOD_SELFTEST)
        (exempt / "notes.md").write_text(
            "skill-doctor: allow-block SEC002\n本机路径示例 /home/someone/x.py。\n",
            encoding="utf-8")
        rc, out = run_audit(exempt)
        if rc != 0 or "WARN [SEC002]" in out:
            raise RuntimeError(f"allow-block SEC002 应豁免该文件：\n{out}")
        checks += 1

        # SEC002 编码形态负向：单反斜杠之外，转义双反斜杠与正斜杠形态必须同样被拦
        # （WARN 不阻断，rc 仍为 0，凭输出里的 WARN 行与行号断言）
        forms = clone_good(tmp, "leak-forms", GOOD_SELFTEST)
        (forms / "scripts" / "paths.py").write_text(LEAK_FORMS + "\n", encoding="utf-8")
        rc, out = run_audit(forms)
        if rc != 0 or "WARN [SEC002]" not in out \
                or "paths.py:1" not in out or "paths.py:2" not in out:
            raise RuntimeError(f"双反斜杠/正斜杠个人路径应触发 SEC002 WARN（两形态各一行）：\n{out}")
        checks += 1

        # 坑 27 回归：弱引用（无读取时机）必须 WARN [LK005]，强引导措辞不报
        weakref = tmp / "weakref-skill"
        (weakref / "references").mkdir(parents=True)
        (weakref / "references" / "rules.md").write_text("# rules\n", encoding="utf-8")
        (weakref / "SKILL.md").write_text(
            "---\nname: weakref\ndescription: 当用户需要演示弱引用检测时使用。\n---\n详见 references/rules.md\n",
            encoding="utf-8")
        rc, out = run_audit(weakref)
        if "WARN [LK005]" not in out or "rules.md" not in out:
            raise RuntimeError(f"弱引用应 WARN [LK005]（坑 27）：\n{out}")
        strongref = tmp / "strongref-skill"
        (strongref / "references").mkdir(parents=True)
        (strongref / "references" / "rules.md").write_text("# rules\n", encoding="utf-8")
        (strongref / "SKILL.md").write_text(
            "---\nname: strongref\ndescription: 当用户需要演示强引导时使用。\n---\n"
            "做分流前先读 references/rules.md：规则定义在里面\n",
            encoding="utf-8")
        rc, out = run_audit(strongref)
        if "WARN [LK005]" in out:
            raise RuntimeError(f"强引导不应报 LK005：\n{out}")
        checks += 2

        # 坑 29 回归：md 资源被注入 NUL 字节必须 FAIL [EN006]。
        # 注入点须在 ASCII 边界（文件头）——打在多字节汉字中间会整体变成解码失败，
        # 走不到"控制字符"分支，测不到目标路径
        nul_skill = clone_good(tmp, "nul-skill", GOOD_SELFTEST)
        rules_md = nul_skill / "references" / "rules.md"
        rules_md.write_bytes(b"\x00" + rules_md.read_bytes())
        rc, out = run_audit(nul_skill)
        if rc != 1 or not any(l.startswith("FAIL") and "[EN006]" in l for l in out.splitlines()):
            raise RuntimeError(f"NUL 字节污染应 FAIL [EN006]（坑 29）：\n{out}")
        checks += 1

        # 坑 27 补充回归：「先读取资源」类祈使标题下列出 references 应视为结构化强引用，
        # 不报 LK005（2026-08-22 源自 douyin 技能误报：正文措辞是中性的"读取"，但章节本身就是读取时机）
        sectionref = tmp / "sectionref-skill"
        (sectionref / "references").mkdir(parents=True)
        (sectionref / "references" / "rules.md").write_text("# rules\n", encoding="utf-8")
        (sectionref / "SKILL.md").write_text(
            "---\nname: sectionref\ndescription: 当用户需要演示结构化引用章节时使用。\n---\n"
            "## 先读取资源\n\n1. 读取 references/rules.md，获得规则。\n",
            encoding="utf-8")
        rc, out = run_audit(sectionref)
        if "WARN [LK005]" in out:
            raise RuntimeError(f"先读类标题下的结构化引用不应报 LK005：\n{out}")
        checks += 1

        bad = build_bad(tmp)
        rc, out = run_audit(bad)
        if rc != 1 or "RESULT FAIL" not in out:
            raise RuntimeError(f"坏夹具应 FAIL（rc=1）：\n{out}")
        checks += 1
        # 级别口径与 references/静态规则清单.md 严格对齐：改级别须两边同步
        expected_fail = ["FM001", "FM003", "FM006", "FM007", "LK001", "LK002", "SF001a", "SEC001"]
        expected_warn = ["SK001", "SF001b", "SF002", "SF003", "FM008", "LK004",
                         "SF005", "SF006", "EN005", "SEC002", "EN003"]
        got_fail = {line.split("[")[1].split("]")[0] for line in out.splitlines()
                    if line.startswith("FAIL")}
        got_warn = {line.split("[")[1].split("]")[0] for line in out.splitlines()
                    if line.startswith("WARN")}
        missed_fail = [c for c in expected_fail if c not in got_fail]
        missed_warn = [c for c in expected_warn if c not in got_warn]
        if missed_fail or missed_warn:
            raise RuntimeError(f"违规未按预期级别抓到：FAIL 缺 {missed_fail}，WARN 缺 {missed_warn}\n{out}")
        checks += 1

        # FM005 负向：compatibility 超 500 + allowed-tools 含逗号 → WARN（不阻断）
        bad_fm = build_bad_fm(tmp)
        rc, out = run_audit(bad_fm)
        if "WARN [FM005]" not in out or "RESULT PASS" not in out:
            raise RuntimeError(f"可选字段违规应 WARN [FM005] 且 PASS：\n{out}")
        checks += 1

        # SK005 负向：正文超 5000 token → WARN（不阻断）
        bad_token = build_bad_token(tmp)
        rc, out = run_audit(bad_token)
        if "WARN [SK005]" not in out or "RESULT PASS" not in out:
            raise RuntimeError(f"token 超限应 WARN [SK005] 且 PASS：\n{out}")
        checks += 1

        result = subprocess.run([sys.executable, str(AUDIT), str(bad)],
                                capture_output=True, text=True, encoding="utf-8", errors="replace")
        if result.returncode != 1 or not (bad / "audit-report.txt").is_file():
            raise RuntimeError(f"默认模式应 FAIL 且落盘报告：rc={result.returncode}")
        checks += 1

        # 坑 14 回归：SKILL.md 与 references 阈值口径打架 → CK001 WARN
        caliber = clone_good(tmp, "caliber-skill", GOOD_SELFTEST)
        (caliber / "references" / "limits.md").write_text(
            "# 限额\n\n引用文件最多 3 个，超了要合并。\n", encoding="utf-8")
        caliber_text = (caliber / "SKILL.md").read_text(encoding="utf-8")
        (caliber / "SKILL.md").write_text(
            caliber_text.replace("先读 [规则]",
                                 "引用文件上限 5 个。先读 [规则]"),
            encoding="utf-8")
        rc, out = run_audit(caliber)
        if rc != 0 or not any(l.startswith("WARN") and "[CK001]" in l for l in out.splitlines()):
            raise RuntimeError(f"阈值口径打架应触发 CK001 WARN（坑 14）：\n{out}")
        checks += 1

        # 触发评测回归：description 覆盖与全部用例必须全绿
        te = subprocess.run([sys.executable, str(TRIGGER_EVAL)],
                            capture_output=True, text=True, encoding="utf-8", errors="replace")
        if te.returncode != 0 or "RESULT PASS" not in te.stdout:
            raise RuntimeError(f"触发评测应全绿：\n{te.stdout}\n{te.stderr}")
        checks += 1

    print(f"SELFTEST PASS ({checks} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
