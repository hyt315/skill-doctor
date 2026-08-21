# 🩺 Skill Doctor

<div align="center">

**Audit any AI Agent skill to catch silent failures, inconsistencies, and broken workflows.**

**给任意 AI Agent 技能做全身体检，揪出“流程走不通、口径矛盾、静默失效”三类病。**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/release/hyt315/skill-doctor?sort=semver)](CHANGELOG.md)
[![GitHub Stars](https://img.shields.io/github/stars/hyt315/skill-doctor?style=social)](https://github.com/hyt315/skill-doctor/stargazers)

**English · [简体中文](./README.md)**

</div>

---

### 📖 What is this?

**Skill Doctor** is an AI Agent Skill that performs a full health check on **SKILL.md-style skills** (Claude Code / Codex / DSH, etc.). It uses a **four-piece toolkit** to catch three dangerous classes of problems:

- 🔗 **Broken workflows** — documented files / commands that don't exist or won't run
- 🌀 **Inconsistent wording** — docs, scripts, and references disagree
- 🤫 **Silent failures** — gates that should block but don't (the most dangerous)

The four-piece toolkit:

1. **Static alignment** — docs / scripts / references promises line up
2. **Dynamic execution** — actually runs the audited skill's selftest
3. **Negative cases** — constructs fixtures that must FAIL to prove gates work
4. **Pitfall library** — cross-checks against historical mistakes

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🔍 **Five static checks** | Structure / Reference integrity / Wording / Security hygiene / Script engineering |
| 🧪 **Negative regression** | `selftest.py`: good fixtures green + bad fixtures caught per rule |
| 🤖 **Trigger regression** | `trigger_eval.py` covers description trigger families |
| 📝 **Graded fixes** | Each issue gets a minimal fix path, rooted at the deepest cause |
| 🐍 **Zero dependencies** | Python standard library only |
| 🌐 **Bilingual** | SKILL.md and references are bilingual |

### 🚀 Quick Start

> ✨ **One-liner install into your AI agent**: paste this to your AI assistant and it will install itself:
>
> ```text
> Please install the skill-doctor Skill: clone https://github.com/hyt315/skill-doctor into your skills directory (Claude Code: ~/.claude/skills/skill-doctor/; Codex: ~/.codex/skills/skill-doctor/; Cursor: ~/.cursor/skills/skill-doctor/), and verify that SKILL.md, references/, and scripts/ are all present. Whenever a skill needs to be reviewed or audited, follow the SKILL.md workflow and run the audit script with static + dynamic checks.
> ```

This is an AI Agent Skill — clone it into your assistant's skills directory.

| Platform | Install |
|----------|---------|
| **Claude Code** | `git clone https://github.com/hyt315/skill-doctor.git ~/.claude/skills/skill-doctor` |
| **Codex** | `git clone https://github.com/hyt315/skill-doctor.git ~/.codex/skills/skill-doctor` |
| **Cursor** | `git clone https://github.com/hyt315/skill-doctor.git ~/.cursor/skills/skill-doctor` |

```bash
# Static audit (report -> <skill-dir>/audit-report.txt)
python <skill-doctor>/scripts/audit.py <skill-dir>

# Also run the audited skill's selftest dynamically
python <skill-doctor>/scripts/audit.py <skill-dir> --dynamic

# Regression tests (run after changing this skill)
python <skill-doctor>/scripts/selftest.py
```

### 📥 Download

| Method | Command / Link |
|--------|----------------|
| **HTTPS** | `git clone https://github.com/hyt315/skill-doctor.git` |
| **SSH** | `git clone git@github.com:hyt315/skill-doctor.git` |
| **GitHub CLI** | `gh repo clone hyt315/skill-doctor` |
| **ZIP** | [Download ZIP](https://github.com/hyt315/skill-doctor/archive/refs/heads/main.zip) |
| **Tar** | [Download Tar](https://github.com/hyt315/skill-doctor/archive/refs/heads/main.tar.gz) |
| **Single file (SKILL.md)** | `curl -O https://raw.githubusercontent.com/hyt315/skill-doctor/main/SKILL.md` |

### 📁 File Structure

```
skill-doctor/
├── SKILL.md                    # Core skill definition
├── manifest.json               # Governance metadata (owner/cadence/tier)
├── LICENSE                     # MIT License
├── .gitignore
├── README.md                   # This repo, Chinese version
├── README.en.md                # English version (this file)
├── CHANGELOG.md
├── agents/
│   └── openai.yaml             # Codex/OpenAI skill metadata
├── scripts/
│   ├── audit.py                # Static auditor (five categories)
│   ├── selftest.py             # Regression tests (good/bad fixtures)
│   └── trigger_eval.py         # Trigger-boundary regression
├── evals/
│   └── trigger_cases.json      # Trigger family cases
├── references/
│   ├── 静态规则清单.md         # Rule & severity single source of truth
│   ├── 审查方法论.md            # Four-piece audit approach
│   └── 坑库.md                  # Historical pitfalls
└── .github/
    ├── pull_request_template.md
    ├── workflows/ci.yml        # Self-audit + regression CI
    └── ISSUE_TEMPLATE/         # Bug / Docs-improvement templates
```

### 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

### 📄 License

[MIT](LICENSE). See [CHANGELOG.md](CHANGELOG.md) for version history.

---

> 🌏 **中文版: [README.md](./README.md)**
