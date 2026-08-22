#!/usr/bin/env python3
"""skill-doctor 静态检查器：对单个技能目录做五类静态审查。

用法:
  python audit.py <被审技能目录>          # 报告落 <目录>/audit-report.txt
  python audit.py <被审技能目录> --stdout  # 只打印不落盘

规则与级别以 references/静态规则清单.md 为唯一事实源（改动规则前先读其出处节）。
零依赖，仅 Python 标准库。退出码：有 ERROR 为 1，否则 0。

检查类别：
  A 结构合规 FM/SK    B 引用一致 LK    C 静默失效 SF
  D 安全卫生 SEC      E 脚本工程 EN
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

TRIGGER_WORDS = ("当用户", "使用时", "何时", "触发", "用于", "适用于", "use when",
                 "use for", "invoke when", "when the user", "trigger")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RESERVED_NAME_RE = re.compile(r"(?i)\b(anthropic|claude)\b")
XML_TAG_RE = re.compile(r"[<>]")
FIRST_PERSON_RE = re.compile(r"(?i)\b(i can|i will|i help|i am|i'm|my skill|i do)\b|我能|我会|我帮助|我可以")
SECRET_PATTERNS = (
    (re.compile(r"sk-[a-zA-Z0-9]{20,}"), "OpenAI 风格 key"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key"),
    (re.compile(r"Bearer\s+[a-zA-Z0-9_.\-]{50,}"), "硬编码 bearer token"),
    (re.compile(r"(?i)(api_key|token|secret|password)\s*=\s*[\"'][^\"']{12,}[\"']"), "凭据变量带实值"),
)
DANGEROUS_CALL_PATTERNS = (
    (re.compile(r"\beval\s*\("), "eval 动态执行"),
    (re.compile(r"\bos\.system\s*\("), "os.system 命令执行"),
    (re.compile(r"subprocess\.(?:run|Popen|call)\s*\([^)]*shell\s*=\s*True"), "subprocess shell=True"),
    (re.compile(r"curl\s+[^|\n]*\|\s*(?:ba)?sh\b"), "curl|bash 管道执行"),
    (re.compile(r"base64\s*(?:-d|--decode)\s+[^|\n]*\|\s*(?:ba)?sh\b"), "base64 解码管道执行"),
)
INTERACTIVE_INPUT_RE = re.compile(r"(?<![.\w])input\s*\(")
SCAN_EXT = {".md", ".py", ".sh", ".js", ".ts", ".json", ".yaml", ".yml", ".txt", ".toml", ".cfg", ".ini"}
SKIP_DIRS = {".git", ".private", "node_modules", "__pycache__", ".venv", "venv",
             "projects", "articles",  # 内容产物目录，非技能本体
             "工作区", "workspace"}  # 显式嵌套技能工作区：里面的 SKILL.md 是有意为之，不算误识别
BROAD_EXCEPT_RE = re.compile(r"except\s*(Exception|BaseException)?\s*$")
BARE_EXCEPT_RE = re.compile(
    r"except[^:\n]*:\s*\n\s*(pass|continue)\b[^\n]*")
NEG_HINT_RE = re.compile(r"(负向|破坏|抽掉|篡改|破图|should[_ ]?fail|expect.{0,12}fail|negative|corrupt|tamper)", re.IGNORECASE)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
INLINE_PATH_RE = re.compile(r"`([^`\n]+)`")
PATH_EXT_RE = re.compile(r"\.(md|py|txt|json|sh|js|ts|yaml|yml)$", re.IGNORECASE)
ABS_PATH_RE = re.compile(r"[A-Za-z]:[/\\]+Users[/\\]|/home/[a-z]")
CALIBER_RE = re.compile(
    r"(上限|不超过|最多|禁止超过|超过|至少|最少)\s*(\d+)\s*(行|个|字符|token|分钟|秒|次|项|张)")
CALIBER_CEIL_WORDS = {"上限", "不超过", "最多", "禁止超过", "超过"}
ALLOW_MARK = "skill-doctor: allow"  # 行尾豁免标记，lint 惯例（同 eslint-disable）


class Findings:
    def __init__(self) -> None:
        self.items: list[tuple[str, str, str]] = []  # level, code, msg

    def add(self, level: str, code: str, msg: str) -> None:
        self.items.append((level, code, msg))

    @property
    def errors(self) -> list[tuple[str, str, str]]:
        return [i for i in self.items if i[0] == "FAIL"]

    def counts(self) -> tuple[int, int, int, int]:
        ok = sum(1 for i in self.items if i[0] == "OK")
        warns = sum(1 for i in self.items if i[0] == "WARN")
        infos = sum(1 for i in self.items if i[0] == "INFO")
        fails = len(self.errors)
        return ok, warns, infos, fails


def extract_frontmatter(text: str) -> str | None:
    stripped = text.lstrip("\ufeff")
    if not stripped.startswith("---"):
        return None
    end = stripped.find("\n---", 3)
    if end == -1:
        return None
    return stripped[4:end] if stripped[3] == "\n" else stripped[3:end]


def parse_field(fm_text: str, key: str) -> str:
    """取顶层标量或多行块（> | 缩进）值，够用即可，不实现完整 YAML。"""
    lines = fm_text.splitlines()
    i = 0
    while i < len(lines):
        m = re.match(rf"^{key}:\s*(.*)$", lines[i])
        if m:
            rest = m.group(1).strip()
            if rest in ("|", ">", "|+", ">", "|-", ">-", ">+"):
                block = []
                i += 1
                while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                    if lines[i].strip():
                        block.append(lines[i].strip())
                    i += 1
                return " ".join(block)
            return rest.strip("\"'")
        i += 1
    return ""


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def estimate_tokens(text: str) -> int:
    """粗估 token 数：CJK 字符按 1 token，其余按 4 字符 1 token（零依赖近似）。"""
    cjk = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
    return cjk + (len(text) - cjk) // 4


def block_allowed(text: str, code: str) -> bool:
    """文件级豁免：`skill-doctor: allow-block CODE1 CODE2`（不带码=豁免整文件）。

    供文件级启发式（SF002/SEC002）的正则字面量类确证误报使用，见静态规则清单.md 豁免节。
    """
    for m in re.finditer(r"skill-doctor:\s*allow-block([^\n]*)", text):
        codes = re.findall(r"[A-Z]+\d+", m.group(1))
        if not codes or code in codes:
            return True
    return False


def skill_files(root: Path) -> list[Path]:
    out = []
    for path in root.rglob("*"):
        if path.is_file() and not any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            out.append(path)
    return out


def check_structure(root: Path, findings: Findings) -> str:
    """返回 SKILL.md 正文（供后续检查用）。"""
    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        findings.add("FAIL", "FM001", "SKILL.md 不存在")
        return ""
    findings.add("OK", "FM001", "SKILL.md 存在")

    nested = [p for p in root.rglob("SKILL.md")
              if p != skill_md and not any(part in SKIP_DIRS for part in p.relative_to(root).parts)]
    if nested:
        findings.add("FAIL", "FM001",
                     f"嵌套 SKILL.md 会被宿主误识别为主入口：{[str(p.relative_to(root)) for p in nested]}")
    else:
        findings.add("OK", "SK004", "全树唯一 SKILL.md")

    text = read_text(skill_md)
    fm = extract_frontmatter(text)
    if fm is None:
        findings.add("FAIL", "FM002", "缺少 YAML frontmatter（--- 包裹）")
        return text
    findings.add("OK", "FM002", "frontmatter 存在")

    name = parse_field(fm, "name")
    if not name:
        findings.add("FAIL", "FM003", "缺少 name 字段")
    else:
        problems = []
        if not NAME_RE.match(name):
            problems.append("格式不符 ^[a-z0-9]+(-[a-z0-9]+)*$")
        if len(name) > 64:
            problems.append("超 64 字符")
        if name != root.name:
            problems.append(f"与目录名 {root.name!r} 不一致")
        if problems:
            findings.add("FAIL", "FM003", f"name: {name!r}（{'；'.join(problems)}）")
        else:
            findings.add("OK", "FM003", "name 合规且与目录名一致")

    desc = parse_field(fm, "description")
    if not desc:
        findings.add("FAIL", "FM004", "缺少 description 字段")
    else:
        if len(desc) > 1024:
            findings.add("FAIL", "FM004", f"description {len(desc)} 字符，超 1024 上限")
        else:
            findings.add("OK", "FM004", f"description 存在（{len(desc)} 字符）")
        lowered = desc.lower()
        if any(w.lower() in lowered for w in TRIGGER_WORDS):
            findings.add("OK", "SK001", "description 含触发条件信息")
        else:
            findings.add("WARN", "SK001", "description 疑似只有功能描述、无何时触发信息（欠触发风险）")

    # FM005 可选字段合法性（agentskills.io 规范）
    fm_issues = []
    compat = parse_field(fm, "compatibility")
    if compat and len(compat) > 500:
        fm_issues.append(f"compatibility {len(compat)} 字符超 500 上限")
    tools = parse_field(fm, "allowed-tools")
    if tools and ("," in tools or not tools.strip()):
        fm_issues.append("allowed-tools 应空格分隔、不含逗号")
    findings.add("WARN" if fm_issues else "OK", "FM005",
                 f"可选字段校验：{'；'.join(fm_issues)}" if fm_issues else "可选字段（compatibility/allowed-tools）合法")

    # FM006 name 保留字（Anthropic 官方）
    if name and RESERVED_NAME_RE.search(name):
        findings.add("FAIL", "FM006", f"name 含保留字 anthropic/claude（平台会拒收）：{name!r}")
    else:
        findings.add("OK", "FM006", "name 无保留字 anthropic/claude")

    # FM007 name/description XML 尖括号（防系统提示注入）
    xml_violations = []
    if name and XML_TAG_RE.search(name):
        xml_violations.append("name")
    if desc and XML_TAG_RE.search(desc):
        xml_violations.append("description")
    if xml_violations:
        findings.add("FAIL", "FM007", f"{'、'.join(xml_violations)} 含 XML 尖括号（注入系统提示风险）")
    else:
        findings.add("OK", "FM007", "name/description 无 XML 尖括号")

    # FM008 description 第三人称（Anthropic best practices）
    if desc and FIRST_PERSON_RE.search(desc):
        findings.add("WARN", "FM008", "description 疑似第一人称（应第三人称：Processes X, Use when...）")
    else:
        findings.add("OK", "FM008", "description 未现第一人称表述")

    body_lines = text.count("\n")
    if body_lines > 500:
        findings.add("WARN", "SK002", f"SKILL.md {body_lines} 行，超 500 行建议拆 references/")
    else:
        findings.add("OK", "SK002", f"SKILL.md {body_lines} 行")

    est_tokens = estimate_tokens(text)
    if est_tokens > 5000:
        findings.add("WARN", "SK005", f"SKILL.md 估算 {est_tokens} tokens，超 5000 建议拆 references/")
    else:
        findings.add("OK", "SK005", f"SKILL.md 估算 {est_tokens} tokens")
    return text


def referenced_targets(text: str, kind: str) -> list[str]:
    """kind=link 提取 markdown 链接；kind=inline 提取行内代码中的文件路径。

    行内代码常含整条命令（含空格/参数），须先按空白分词：
    丢弃选项（-开头）、键值对（含=）、SKIP_DIRS 开头的运行期产物路径（如 .private/xxx.json）。
    """
    if kind == "link":
        tokens = [m.group(1) for m in LINK_RE.finditer(text)]
    else:
        tokens = []
        for m in INLINE_PATH_RE.finditer(text):
            tokens += m.group(1).split()
    out = []
    for token in tokens:
        if kind == "inline":
            if "/" not in token and "\\" not in token:
                continue
            if token.startswith("-") or "=" in token:
                continue
            token = token.replace("\\", "/")
            token = re.sub(r"^[<{(\[]+|[>})\].,;'\"]+$", "", token)
            if "<" in token or ">" in token or "*" in token or token.startswith("http"):
                continue  # 尖括号/花括号占位符（<本技能> 之类）是模板，不是真实路径
            if token.split("/")[0] in SKIP_DIRS:
                continue
        else:
            if token.startswith(("http://", "https://", "#", "mailto:", "computer://")):
                continue
        if PATH_EXT_RE.search(token.split("/")[-1]):
            out.append(token)
    return out


def check_references(root: Path, skill_text: str, findings: Findings) -> None:
    for kind, code in (("link", "LK001"), ("inline", "LK002")):
        missing = []
        for target in referenced_targets(skill_text, kind):
            resolved = (root / target).resolve()
            if not resolved.is_file():
                missing.append(target)
        if missing:
            findings.add("FAIL", code,
                         f"SKILL.md 引用但不存在：{sorted(set(missing))}（Agent 会幻觉其内容）")
        else:
            findings.add("OK", code, "SKILL.md 引用的文件全部在盘")

    scripts_dir = root / "scripts"
    doc_text = skill_text + "".join(
        read_text(p) for p in (root / "references").glob("*.md")) if (root / "references").is_dir() else skill_text
    if scripts_dir.is_dir():
        doc_text += "".join(read_text(p) for p in scripts_dir.glob("*.py"))  # 脚本互调也算提及
    if scripts_dir.is_dir():
        orphans = [p.name for p in scripts_dir.iterdir()
                   if p.is_file() and p.name not in doc_text]
        if orphans:
            findings.add("WARN", "LK003", f"scripts/ 存在但文档未提及（死代码或漏写用法）：{orphans}")
        else:
            findings.add("OK", "LK003", "scripts/ 文件均被文档提及")

    # SK003 引用一层深：SKILL.md 引用的 .md 不得再引用其他 .md
    nested_ref = []
    checked_refs: set[str] = set()
    for target in referenced_targets(skill_text, "link") + referenced_targets(skill_text, "inline"):
        target_path = (root / target).resolve()
        if target_path.suffix == ".md" and target not in checked_refs and target_path.is_file():
            checked_refs.add(target)
            inner = read_text(target_path)
            deeper = [t for t in referenced_targets(inner, "link") if t.endswith(".md")]
            if deeper:
                nested_ref.append(f"{target} -> {deeper}")
            if inner.count("\n") > 100 and not re.search(r"(?m)^#{1,2}\s*(目录|Contents|TOC)", inner[:3000]):
                findings.add("WARN", "SK003", f"{target} 超 100 行且头部无目录")
    if nested_ref:
        findings.add("WARN", "SK003", f"参考文件嵌套引用（应一层深，SKILL.md 直达）：{nested_ref}")
    elif not any(i[1] == "SK003" for i in findings.items):
        findings.add("OK", "SK003", "引用层次一层深")

    # LK004 references/ 孤儿文件：从未被 SKILL.md / 其他 references / scripts 提及
    refs_dir = root / "references"
    if refs_dir.is_dir():
        corpus = skill_text + "".join(read_text(p) for p in refs_dir.rglob("*.md"))
        if scripts_dir.is_dir():
            corpus += "".join(read_text(p) for p in scripts_dir.rglob("*.py"))
        orphans = [str(p.relative_to(root)).replace("\\", "/")
                   for p in refs_dir.rglob("*.md")
                   if p.name not in corpus and str(p.relative_to(root)).replace("\\", "/") not in corpus]
        if orphans:
            findings.add("WARN", "LK004", f"references/ 孤儿文件（无任何引用，Agent 永不加载）：{sorted(orphans)}")
        else:
            findings.add("OK", "LK004", "references/ 文件均被 SKILL.md/脚本提及")

    # LK005 references 弱引用：有链接但无明确读取时机（坑 27）。
    # 规范规定 references 按需加载（loaded only when required），SKILL.md 的引导措辞
    # 决定执行 AI 会不会真的去读；"详见/可参考"类弱措辞没有读取时机，模型不会自觉补读。
    if refs_dir.is_dir():
        strong_guidance = re.compile(
            r"必读|先读|先查|再读|完整阅读|完整读|另读|通读|读取时机|读取动作|何时读|逐条|对照|照抄|"
            r"读[^。\n]{0,24}(节|定义|方法|清单|流程|全文)|读[：:]|(时|后|前)[，,：:]\s*读|"
            r"按\s*`?references/|"
            r"When\s+\w|If you need|\bMUST\b|follow its instructions",
            re.I,
        )
        # 结构化信号：SKILL.md 有专门的参考文件章节（Reference Files/参考文档/按需加载参考），
        # 且文件在其中被列出（官方 webapp-testing 模式：文件 + 触发条件/用途清单）
        section = re.search(r"(?ms)^##\s+(Reference Files|参考文档[^\n]*|按需加载参考[^\n]*).*?(?=^##\s|\Z)", skill_text)
        listed_in_section = set(re.findall(r"references/[\w\-]+\.md", section.group(0))) if section else set()
        weak_only = []
        for p in sorted(refs_dir.glob("*.md")):
            if f"references/{p.name}" in listed_in_section:
                continue
            mention_lines = [ln for ln in skill_text.splitlines() if p.name in ln]
            if not mention_lines:
                continue  # 完全未提及由 LK004 管
            if not any(strong_guidance.search(ln) for ln in mention_lines):
                weak_only.append(p.name)
        if weak_only:
            findings.add("WARN", "LK005",
                         f"references 仅弱引用（如'详见/可参考'），无明确读取时机——AI 可能不读（坑 27）：{weak_only}")
        elif refs_dir.glob("*.md"):
            findings.add("OK", "LK005", "references 均有明确读取时机（强引导措辞）")


def check_silent_failures(files: list[Path], root: Path, findings: Findings) -> None:
    broad, narrow, skipping, bad_rc = [], [], [], []
    dangerous, interactive = [], []
    for path in files:
        if path.suffix != ".py":
            continue
        text = read_text(path)
        rel = str(path.relative_to(root))
        for m in BARE_EXCEPT_RE.finditer(text):
            if ALLOW_MARK in m.group(0):
                continue
            loc = f"{rel}:{text[:m.start()].count(chr(10)) + 1}"
            clause = m.group(0).split(":")[0]
            if BROAD_EXCEPT_RE.fullmatch(clause.strip()):
                broad.append(loc)  # 裸/宽捕获直接吞 = 门放行
            else:
                narrow.append(loc)  # 窄类型捕获 + 回退，人工确认回退是否合理
        if (re.search(r"(skipped|跳过|忽略)", text) and "warn" not in text.lower()
                and not block_allowed(text, "SF002")):
            skipping.append(rel)
        if "RESULT FAIL" in text and not re.search(r"sys\.exit|SystemExit", text):
            bad_rc.append(rel)
        # SF005 危险动态执行（正则字面量类确证误报用 allow-block 豁免）
        if not block_allowed(text, "SF005"):
            for pattern, desc in DANGEROUS_CALL_PATTERNS:
                m = pattern.search(text)
                if m:
                    line_no = text[:m.start()].count("\n") + 1
                    dangerous.append(f"{rel}:{line_no}（{desc}）")
                    break
        # SF006 交互提示扫描（agent 非交互 shell 会挂死）
        if not block_allowed(text, "SF006"):
            m = INTERACTIVE_INPUT_RE.search(text)
            if m:
                line_no = text[:m.start()].count("\n") + 1
                interactive.append(f"{rel}:{line_no}")
    findings.add("FAIL" if broad else "OK", "SF001a",
                 f"裸/宽 except 后 pass/continue（吞掉一切异常=门放行）：{broad}" if broad else "无宽捕获吞异常")
    findings.add("WARN" if narrow else "OK", "SF001b",
                 f"窄类型 except 后 pass/continue（人工确认回退合理性）：{narrow}" if narrow else "无窄捕获吞异常")
    findings.add("WARN" if skipping else "OK", "SF002",
                 f"含跳过逻辑但全文无 WARN 字样（静默跳过风险）：{skipping}" if skipping else "跳过逻辑有告警或无跳过逻辑")
    findings.add("WARN" if bad_rc else "OK", "SF003",
                 f"输出 RESULT FAIL 但无 sys.exit/SystemExit（退出码骗人风险）：{bad_rc}" if bad_rc else "FAIL 路径退出码语义正常")
    findings.add("WARN" if dangerous else "OK", "SF005",
                 f"危险动态执行（eval/os.system/curl|bash 等，须人工确认用途）：{dangerous}" if dangerous else "无危险动态执行")
    findings.add("WARN" if interactive else "OK", "SF006",
                 f"含交互提示 input 调用（agent 非交互 shell 会挂死）：{interactive}" if interactive else "无交互提示 input 调用")


FIXTURE_DIR_TOKENS = {"tests", "test", "fixtures", "examples", "evals"}


def is_fixture_path(rel: str) -> bool:
    """测试夹具/示例上下文：里面的假密钥是故意写的违规样本，不是真泄露。"""
    return bool(FIXTURE_DIR_TOKENS.intersection(Path(rel).parts))


def check_security(files: list[Path], root: Path, findings: Findings) -> None:
    secrets, fixture_secrets, abs_paths = [], [], []
    for path in files:
        if path.suffix not in SCAN_EXT:
            continue
        text = read_text(path)
        rel = str(path.relative_to(root))
        for line_no, line in enumerate(text.splitlines(), 1):
            if ALLOW_MARK in line:
                continue
            for pattern, desc in SECRET_PATTERNS:
                m = pattern.search(line)
                if m:
                    item = f"{rel}:{line_no}（{desc}）"
                    (fixture_secrets if is_fixture_path(rel) else secrets).append(item)
        if not block_allowed(text, "SEC002"):
            for m in ABS_PATH_RE.finditer(text):
                line_no = text[:m.start()].count("\n") + 1
                if ALLOW_MARK not in text.splitlines()[line_no - 1]:
                    abs_paths.append(f"{rel}:{line_no}")
    findings.add("FAIL" if secrets else "OK", "SEC001",
                 f"疑似硬编码密钥：{secrets}" if secrets else "未发现硬编码密钥")
    findings.add("WARN" if fixture_secrets else "OK", "SEC001",
                 f"测试夹具/示例中的假密钥（人工确认为故意违规样本即可放行）：{fixture_secrets}"
                 if fixture_secrets else "夹具上下文无密钥样式命中")
    findings.add("WARN" if abs_paths else "OK", "SEC002",
                 f"绝对个人路径（交付泄露风险，示例上下文可豁免）：{abs_paths}" if abs_paths else "未发现绝对个人路径")


def check_engineering(files: list[Path], root: Path, skill_text: str, findings: Findings) -> None:
    no_shebang, no_doc = [], []
    py_files = [p for p in files if p.suffix == ".py"]
    for path in py_files:
        rel = str(path.relative_to(root))
        text = read_text(path)
        if not text.startswith("#!"):
            no_shebang.append(rel)
        if len(text.splitlines()) > 50 and not re.search(r'"""', text):
            no_doc.append(rel)
    findings.add("WARN" if no_shebang else "OK", "EN001",
                 f"缺 shebang 行：{no_shebang}" if no_shebang else "脚本均有 shebang")
    findings.add("WARN" if no_doc else "OK", "EN002",
                 f">50 行脚本缺模块 docstring（用法无处可查）：{no_doc}" if no_doc else "大脚本均有 docstring")

    # EN005 bash 脚本缺 set -euo pipefail（管道中间失败被静默吞掉）
    no_pipefail = []
    for path in files:
        if path.suffix == ".sh":
            sh_text = read_text(path)
            if "set -euo pipefail" not in sh_text and "set -eu" not in sh_text:
                no_pipefail.append(str(path.relative_to(root)))
    findings.add("WARN" if no_pipefail else "OK", "EN005",
                 f"bash 脚本缺 set -euo pipefail（管道失败静默风险）：{no_pipefail}" if no_pipefail else "bash 脚本均有 set -euo pipefail")

    bom_files = []
    for path in files:
        try:
            head = path.open("rb").read(2)
        except OSError:
            continue  # skill-doctor: allow（扫描器自身边界容错，非校验门）
        if head in (b"\xff\xfe", b"\xfe\xff"):
            bom_files.append(str(path.relative_to(root)))
    findings.add("WARN" if bom_files else "OK", "EN003",
                 f"UTF-16 BOM 文件（脚本回读会失败）：{bom_files}" if bom_files else "无 UTF-16 文件")

    scripts_dir = root / "scripts"
    if py_files and scripts_dir.is_dir():
        declared = "零依赖" in skill_text or "标准库" in skill_text or (scripts_dir / "requirements.txt").is_file()
        findings.add("INFO" if not declared else "OK", "EN004",
                     "scripts/ 无 requirements.txt 且 SKILL.md 未声明零依赖/标准库" if not declared
                     else "依赖情况已声明")
    else:
        findings.add("OK", "EN004", "无脚本目录，跳过依赖登记检查")


def check_caliber_consistency(files: list[Path], root: Path, findings: Findings) -> None:
    """坑 14 口径打架：同一量词与方向（上限/下限）的阈值在多个 md 文件数值不一。"""
    seen: dict[tuple[str, str, int], str] = {}  # (方向, 量词, 数值) -> 首次出现位置
    conflicts = []
    for path in files:
        if path.suffix != ".md":
            continue
        rel = str(path.relative_to(root))
        for line_no, line in enumerate(read_text(path).splitlines(), 1):
            if ALLOW_MARK in line:
                continue
            for m in CALIBER_RE.finditer(line):
                word, num, unit = m.group(1), int(m.group(2)), m.group(3)
                direction = "上限" if word in CALIBER_CEIL_WORDS else "下限"
                key = (direction, unit, num)
                where = f"{rel}:{line_no}（{word} {num} {unit}）"
                if key in seen:
                    continue  # 同值同口径，一致
                sibling = [k for k in seen if k[0] == direction and k[1] == unit and k[2] != num]
                if sibling:
                    conflicts.append(f"{where} 与 {seen[sibling[0]]} 数值打架")
                    continue
                seen[key] = where
    findings.add("WARN" if conflicts else "OK", "CK001",
                 f"阈值口径打架（同一约束散落多处且数值不一，改一处忘其余）：{conflicts}"
                 if conflicts else "md 文件间阈值口径一致")


def find_regression_entry(root: Path) -> tuple[str, str, list[Path]]:
    """按优先级找回归入口：selftest 命名 > tests/ 目录 > Makefile test 目标。

    只认 selftest 一种命名会误伤用 pytest/tests/ 布局的技能（坑库坑 25）。
    返回 (kind, 描述, 负向特征扫描文件列表)；找不到返回 ("none", "", [])。
    """
    candidates = [root / "scripts" / "selftest.py", root / "selftest.py"]
    scripts_dir = root / "scripts"
    if scripts_dir.is_dir():
        candidates += sorted(scripts_dir.glob("selftest*.py"))
    candidates += sorted(root.glob("test_*.py"))
    for candidate in candidates:
        if candidate.is_file():
            return "selftest", str(candidate.relative_to(root)), [candidate]

    for dir_name in ("tests", "test"):
        tests_dir = root / dir_name
        if tests_dir.is_dir():
            test_files = sorted(p for p in tests_dir.rglob("*.py")
                                if p.name != "__init__.py" and "__pycache__" not in p.parts)
            if test_files:
                return "tests", f"{dir_name}/（{len(test_files)} 个测试文件）", test_files

    makefile = root / "Makefile"
    if makefile.is_file() and re.search(r"^test\s*:", read_text(makefile), re.MULTILINE):
        return "make", "Makefile test 目标", [makefile]
    return "none", "", []


def check_dynamic(root: Path, findings: Findings, enabled: bool) -> None:
    kind, desc, scan_files = find_regression_entry(root)
    if kind == "none":
        findings.add("FAIL", "DY001", "未找到回归入口（selftest/tests/Makefile test 均无，技能不可回归）")
        findings.add("WARN", "DY002", "无回归入口，负向用例无从谈起")
        return
    findings.add("OK", "DY001", f"回归入口存在（{kind}）：{desc}")

    # tests/ 布局文件可能很多，抽样扫描防大库拖慢（前 20 个足以判特征）
    if any(NEG_HINT_RE.search(read_text(p)) for p in scan_files[:20]):
        findings.add("OK", "DY002", f"{kind} 入口含负向用例特征（破坏/抽掉/should-fail 类）")
    else:
        findings.add("WARN", "DY002", f"{kind} 入口未见负向用例特征——门可能名义存在实际放行，人工抽查关键门")

    if kind != "selftest":
        findings.add("INFO", "DY003", f"非 selftest 入口（{kind}），动态实跑请人工执行其回归命令")
        return
    selftest = scan_files[0]
    rel = selftest.relative_to(root)

    if not enabled:
        findings.add("INFO", "DY003", "动态实跑未开启（加 --dynamic 真跑 selftest）")
        return

    started = time.time()
    try:
        result = subprocess.run([sys.executable, str(selftest)], cwd=str(root),
                                capture_output=True, text=True, encoding="utf-8",
                                errors="replace", timeout=600)
    except subprocess.TimeoutExpired:
        findings.add("FAIL", "DY001", "selftest 实跑超时（600s），疑似挂起或过重")
        return
    out = (result.stdout or "") + (result.stderr or "")
    rc = result.returncode
    says_pass = bool(re.search(r"SELFTEST PASS|RESULT PASS|PASS \(\d+ checks?\)", out))
    says_fail = bool(re.search(r"SELFTEST FAIL|RESULT FAIL", out))
    tail = " | ".join(out.strip().splitlines()[-3:])[:300]
    if rc == 0 and says_pass and not says_fail:
        findings.add("OK", "DY003", f"selftest 实跑通过（rc=0，{time.time() - started:.1f}s）")
    elif rc == 0 and says_fail:
        findings.add("FAIL", "DY003", f"rc=0 但报告 FAIL（退出码骗人）：{tail}")
    elif rc != 0 and not says_fail and not says_pass:
        findings.add("FAIL", "DY003", f"rc={rc} 且无 PASS/FAIL 结论（疑似崩溃）：{tail}")
    elif rc != 0 and says_pass:
        findings.add("FAIL", "DY003", f"rc={rc} 但报告 PASS（退出码语义反向）：{tail}")
    else:
        findings.add("FAIL", "DY003", f"selftest 实跑失败（rc={rc}）：{tail}")


def render_report(root: Path, findings: Findings, env_note: str) -> tuple[str, int]:
    ok, warns, infos, fails = findings.counts()
    total = len(findings.items)
    lines = [f"技能静态审查报告：{root.name}", env_note, "", "检查结果："]
    for level, code, msg in findings.items:
        lines.append(f"{level:<4} [{code}] {msg}")
    lines.append("")
    lines.append(f"共 {total} 项，通过 {ok}，WARN {warns}，INFO {infos}，FAIL {fails}")
    if fails:
        errors = findings.errors
        lines.append("")
        lines.append("问题清单（每项附最小修复路径）：")
        for level, code, msg in errors:
            lines.append(f"  [{code}] {msg}")
            lines.append(f"      修复：{REPAIR_HINTS.get(code, '按静态规则清单.md 该条目修')}；修完重跑 audit.py")
        lines.append("")
        if len(errors) == 1:
            strategy = "单项问题，按最小修复路径处理即可"
        else:
            strategy = f"多项并存（{len(errors)} 项），按规则类别分组处理，全部修复后重跑"
        lines.append(f"修复策略：{strategy}")
        lines.append("RESULT FAIL")
        return "\n".join(lines) + "\n", 1
    lines.append("RESULT PASS")
    return "\n".join(lines) + "\n", 0


REPAIR_HINTS = {
    "FM001": "删除或改名嵌套 SKILL.md（如 README.md），保唯一入口",
    "FM002": "补 YAML frontmatter（--- 包裹 name/description）",
    "FM003": "改 name 为小写连字符、≤64 字符、与目录名一致",
    "FM004": "补 description 或压到 1024 字符内",
    "FM006": "去掉 name 中的 anthropic/claude 保留字（如 claude-helper → helper）",
    "FM007": "去掉 name/description 中的 XML 尖括号（防系统提示注入）",
    "LK001": "补齐缺失文件或修正引用路径",
    "LK002": "补齐缺失脚本或从文档删掉该命令",
    "LK005": "给该 reference 的链接补上读取时机（如'做 X 前先读 Y：Z 在里面'），并说明为什么值得读（坑 27）",
    "SEC001": "密钥移到环境变量/.private（并入 .gitignore），清洗历史",
    "DY001": "补 selftest.py（好夹具全绿+坏夹具被抓），参考审查方法论.md 负向用例节",
    "DY003": "修 selftest 本身或其夹具，退出码与结论文本对齐",
    "CK001": "统一各文件阈值数值，或抽公共常量/单一来源文件，其余处指针引用",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="skill-doctor 静态+动态检查器")
    parser.add_argument("target", help="被审技能目录")
    parser.add_argument("--stdout", action="store_true", help="只打印不落盘")
    parser.add_argument("--dynamic", action="store_true",
                        help="动态实跑被审技能 selftest（有副作用风险，确认安全后显式开启）")
    args = parser.parse_args()

    root = Path(args.target).resolve()
    if not root.is_dir():
        print(f"ERROR: 目录不存在 {root}")
        return 2

    findings = Findings()
    skill_text = check_structure(root, findings)
    files = skill_files(root)
    check_references(root, skill_text, findings)
    check_caliber_consistency(files, root, findings)
    check_silent_failures(files, root, findings)
    check_security(files, root, findings)
    check_engineering(files, root, skill_text, findings)
    check_dynamic(root, findings, args.dynamic)

    mode = "静态+动态（selftest 已实跑）" if args.dynamic else "静态层（动态实跑与负向用例见审查方法论.md）"
    env_note = f"环境：{sys.version.split()[0]} / {mode}"
    report, rc = render_report(root, findings, env_note)
    print(report, end="")
    if not args.stdout:
        (root / "audit-report.txt").write_text(report, encoding="utf-8")
        print(f"\n报告已写入 {root / 'audit-report.txt'}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
