#!/usr/bin/env python3
"""skill-doctor 触发评测：验证 SKILL.md description 的触发边界没有退化。

用法: python trigger_eval.py [--skill-root <目录>] [--cases <cases.json>]
默认 skill-root 为本技能根目录，cases 为 evals/trigger_cases.json。
零依赖。评测两层：
  1. description 覆盖检查——每个 positive 概念组须有词出现在 description，缺了说明
     description 改丢了关键词（触发面退化，agent 会无视该技能）
  2. 用例行为评测——按概念权重打分预测 trigger/no_trigger，与期望比对，
     按家族统计 pass rate（家族全错=该类请求整体路由失败，比总数更早暴露问题）
退出码：覆盖缺口或任一用例 FAIL 为 1，否则 0。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def extract_description(skill_root: Path) -> str:
    text = (skill_root / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^description:\s*(.+?)(?=\n\w|\n---)", text, re.MULTILINE | re.DOTALL)
    if not m:
        raise SystemExit("SKILL.md 无 description 字段")
    return " ".join(m.group(1).split())


def score_case(text: str, concepts: dict, desc: str) -> tuple[int, int, list[str]]:
    """返回 (positive分, negative分, 命中概念名)。positive 只计 description 也覆盖的概念。"""
    pos, neg, hits = 0, 0, []
    for name, c in concepts.items():
        case_hit = any(t.lower() in text.lower() for t in c["terms"])
        if not case_hit:
            continue
        if c["kind"] == "positive":
            if any(t.lower() in desc.lower() for t in c["terms"]):
                pos += c["weight"]
                hits.append(f"{name}(+{c['weight']})")
        else:
            neg += c["weight"]
            hits.append(f"{name}(-{c['weight']})")
    return pos, neg, hits


def main() -> int:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-root", default=str(here.parent))
    parser.add_argument("--cases", default=str(here.parent / "evals" / "trigger_cases.json"))
    args = parser.parse_args()

    cfg = json.loads(Path(args.cases).read_text(encoding="utf-8"))
    concepts, cases, threshold = cfg["concepts"], cfg["cases"], cfg["threshold"]
    desc = extract_description(Path(args.skill_root))

    failed = 0

    coverage_gaps = [
        f"{name}（词组 {c['terms'][0]}… 无一在 description）"
        for name, c in concepts.items()
        if c["kind"] == "positive" and not any(t.lower() in desc.lower() for t in c["terms"])
    ]
    if coverage_gaps:
        failed += 1
        print("FAIL description 覆盖缺口（触发面退化）:")
        for gap in coverage_gaps:
            print(f"  - {gap}")
    else:
        print("OK   description 覆盖全部 positive 概念组")

    family_stats: dict[str, list[int]] = {}
    for case in cases:
        pos, neg, hits = score_case(case["text"], concepts, desc)
        predicted = "trigger" if (pos >= threshold and pos > neg) else "no_trigger"
        ok = predicted == case["expect"]
        stat = family_stats.setdefault(case["family"], [0, 0])
        stat[0] += ok
        stat[1] += 1
        if not ok:
            failed += 1
        mark = "OK  " if ok else "FAIL"
        print(f"{mark} [{case['family']}] expect={case['expect']} predicted={predicted} "
              f"pos={pos} neg={neg} hits={','.join(hits) or '-'} | {case['text']}")

    print("\n家族汇总:")
    for family, (ok_n, total) in sorted(family_stats.items()):
        rate = ok_n / total
        mark = "OK  " if rate == 1.0 else "FAIL"
        print(f"  {mark} {family}: {ok_n}/{total}")
        if rate < 1.0:
            failed += 0  # 用例级已计，家族行只做展示聚合

    total_ok = sum(s[0] for s in family_stats.values())
    total = sum(s[1] for s in family_stats.values())
    print(f"\nRESULT {'PASS' if failed == 0 else 'FAIL'}（{total_ok}/{total} 用例，"
          f"{'无' if not coverage_gaps else len(coverage_gaps)} 覆盖缺口）")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
