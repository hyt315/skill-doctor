<div align="center">

# 🩺 Skill Doctor

**Health checks for AI Agent skills: 35 static rules + dynamic selftest runs + negative-case probes, catching the silent "gate exists on paper, passes in practice" failures.**

**English · [简体中文](./README.md)**

[![License: MIT](https://img.shields.io/github/license/hyt315/skill-doctor)](LICENSE)
[![Release](https://img.shields.io/github/v/release/hyt315/skill-doctor?sort=semver)](https://github.com/hyt315/skill-doctor/releases)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-1f6feb)](SKILL.md)
[![Tests](https://github.com/hyt315/skill-doctor/actions/workflows/ci.yml/badge.svg)](https://github.com/hyt315/skill-doctor/actions)
[![Stars](https://img.shields.io/github/stars/hyt315/skill-doctor?style=social)](https://github.com/hyt315/skill-doctor/stargazers)

</div>

---

## 📖 What is this?

Your skill runs, the demo looks great — but is it actually reliable? **Skill Doctor** is a meta-skill that audits AI Agent skills: **35 numbered static rules** (frontmatter compliance, reference links, caliber consistency, security hygiene, exit-code semantics…), **dynamic runs** of the audited skill's own selftest, and **negative-case probes** (samples that must be caught have to actually be caught). It quantifies the gap between "looks like it works" and "provably works". Every check has an ID (FM/SK/LK/CK/SF/SEC/EN/DY) and the report is written to disk for traceability.

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🔍 **35 static rules** | Frontmatter, reserved names, orphan references, conflicting thresholds, broad exception swallowing, hardcoded secrets, personal-path leaks — all numbered and traceable |
| 🏃 **Dynamic runs** | Not just reading docs — actually runs the audited skill's selftest and verifies exit-code semantics match the printed conclusion |
| 🎯 **Negative probes** | The most dangerous failure is a gate that exists on paper but passes everything: build breaking samples and verify gates actually block |
| 🧠 **26-entry pitfall library** | Real-world failure patterns (symptom → root cause → fix → prevention → check method), continuously written back |
| 📄 **Report on disk** | `audit-report.txt` written into the audited skill directory, item-by-item OK/WARN/FAIL |
| 🛡️ **Zero-dep read-only** | Python standard library only; audit is read-only, `--dynamic` off by default to avoid side effects |

---

## 🚀 Quick Start

> ✨ **One-liner install into your AI agent**: paste this to your AI assistant and it will install itself:
>
> ```text
> Please install the skill-doctor Skill: clone https://github.com/hyt315/skill-doctor into your skills directory (Claude Code: ~/.claude/skills/skill-doctor/; Codex: ~/.codex/skills/skill-doctor/; Cursor: ~/.cursor/skills/skill-doctor/), and verify that SKILL.md, references/, and scripts/ are all present. Whenever a skill needs to be reviewed or audited, follow the SKILL.md workflow and run the audit script with static + dynamic checks.
> ```

| Platform | Install |
|----------|---------|
| **Claude Code** | `git clone https://github.com/hyt315/skill-doctor.git ~/.claude/skills/skill-doctor` |
| **Codex** | `git clone https://github.com/hyt315/skill-doctor.git ~/.codex/skills/skill-doctor` |
| **Cursor** | `git clone https://github.com/hyt315/skill-doctor.git ~/.cursor/skills/skill-doctor` |

---

## 💬 When to trigger

Say any of these to your AI agent:

- "Review this skill" / "give this skill a health check" / "audit it before release"
- "Does this skill have hidden pitfalls?" / "why does my skill work only sometimes?"
- "Run a quality gate before publishing this skill"

## ⚙️ Prerequisites

- **Python 3.10+** (standard library only, zero third-party deps)
- Path to the skill directory you want audited
- No admin rights needed; the audit is read-only and never modifies the audited skill

## 📦 Deliverables

```text
audit-report.txt      — written into the audited skill directory: per-item OK/WARN/INFO/FAIL + RESULT verdict
Dynamic run verdict   — did the selftest really pass, are exit codes honest (--dynamic)
Negative probe result — do the critical gates actually block breaking samples (guided by the methodology)
```

---

## 📚 Example: a real audit report

```text
Skill static audit report: network-slow-diagnosis
Results:
OK   [FM001] SKILL.md exists
OK   [SK004] single SKILL.md in tree
OK   [LK004] all references/ files linked from SKILL.md/scripts
OK   [SEC001] no hardcoded secrets
WARN [EN005] bash script missing set -euo pipefail
INFO [DY003] non-selftest entry (tests), run its regression manually
35 items: 33 passed, 2 WARN, 2 INFO, 0 FAIL
RESULT PASS
```

Every line maps to a rule definition and fix guidance in `references/静态规则清单.md`.

---

## 📥 Download / Install

```bash
# HTTPS
git clone https://github.com/hyt315/skill-doctor.git

# SSH
git clone git@github.com:hyt315/skill-doctor.git

# GitHub CLI
gh repo clone hyt315/skill-doctor

# ZIP
# https://github.com/hyt315/skill-doctor/archive/refs/heads/main.zip

# Single file (SKILL.md only)
curl -O https://raw.githubusercontent.com/hyt315/skill-doctor/main/SKILL.md
```

---

## 📁 File Structure

```
skill-doctor/
├── SKILL.md                     # entry point (audit workflow + methodology routing)
├── manifest.json
├── references/
│   ├── 静态规则清单.md           # authoritative definitions of the 35 rules (Chinese)
│   ├── 审查方法论.md             # full methodology: static → dynamic → negative (Chinese)
│   └── 坑库.md                   # 26 real-world pitfalls, continuously updated (Chinese)
├── scripts/
│   ├── audit.py                  # audit entry (--stdout / --dynamic)
│   ├── selftest.py               # this skill's regression (good fixtures green + bad caught)
│   └── trigger_eval.py           # description trigger-boundary regression
├── evals/                        # trigger evaluation cases
├── LICENSE
├── README.md  /  README.en.md  # bilingual docs (this file is English)
└── .github/                     # Issue/PR templates + CI
```

---

## ▶️ Quick Usage

```bash
# Static audit, report written to <audited-skill-dir>/audit-report.txt
python scripts/audit.py <skill-dir>

# Also run the audited skill's dynamic selftest (off by default, avoids side effects)
python scripts/audit.py <skill-dir> --dynamic

# Required regressions after changing this skill
python scripts/selftest.py
python scripts/trigger_eval.py
```

---

## 🤝 Contributing / Feedback

- Report bugs / suggestions: use the repo's Issue templates
- Contribute: see [CONTRIBUTING.md](CONTRIBUTING.md); run `selftest.py` and `trigger_eval.py` before any PR
- Submit a new pitfall: follow the pitfall format (symptom → root cause → fix → prevention → check) into `references/坑库.md`
- Security: see [SECURITY.md](SECURITY.md) (private vulnerability reporting, not public issues)

---

## 📜 License

[MIT](LICENSE) © 2026 hyt315

> 🌏 **中文版: [README.md](./README.md)**