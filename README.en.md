# 🩺 Skill Doctor / skill-doctor

<div align="center">

**AI Agent skill auditor & linter with 37 static rules, dynamic execution, negative sample verification, and zero silent failures.**

**给 AI Agent 技能做深度体检：37 项静态规则 + 动态实跑 + 负向抽查，专抓「门名义存在实际放行」的静默失效。**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/hyt315/skill-doctor?sort=semver)](CHANGELOG.md)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-1f6feb)](SKILL.md)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Pure%20Python)-brightgreen)](SKILL.md)
[![GitHub Stars](https://img.shields.io/github/stars/hyt315/skill-doctor?style=social)](https://github.com/hyt315/skill-doctor/stargazers)

[English](./README.en.md) | [中文](./README.md)

</div>

---

## 📖 What is this?

Your AI Agent skill runs and demos look great — but is it truly robust and production-ready?
- Does it hide silent errors with broad `except Exception:` clauses?
- Are there orphan references in `references/` that the LLM never reads?
- Did local personal machine paths or API tokens accidentally leak into docs?
- Does its test script exit with code 0 even when internal logic fails?

**`skill-doctor`** is a specialized meta-skill and CLI auditing tool for AI Agent skills. Through **37 comprehensive static rules** (frontmatter, references, exit code semantics, security), **dynamic test execution**, and **negative destructive sampling**, it accurately benchmarks skill quality and produces itemized, actionable audit reports.

---

## ✨ Key Features

| Core Module | Capabilities | Value Delivered |
|---|---|---|
| 🔍 **37 Comprehensive Rules** | Frontmatter, naming, reference integrity, exception hygiene, secret detection, path leaks | Covers FM/SK/LK/CK/SF/SEC/EN/DY with traceable rule IDs |
| 🏃 **Dynamic Execution** | Executes the target skill's actual `selftest.py` to verify true exit codes | Eliminates false confidence from pure text checks |
| 🎯 **Negative Sample Checks** | Injects invalid/destructive test samples to verify that guardrails truly block failures | Eliminates dangerous "guards that exist in name only" |
| 🧠 **27 Real-World Pitfalls** | Curated catalog of anti-patterns collected across hundreds of audits | Prevents repeating known LLM workflow traps |
| 📄 **Actionable Reports** | Standardized audit reports (`audit-report.txt`) with OK / WARN / INFO / FAIL statuses | Ready for CI pipelines and code reviews |
| 🛡️ **Zero-Dependency Read-Only** | Pure Python standard library with 100% read-only analysis | Safe to run anywhere with zero side effects |

---

## 📊 Complete Audit Pipeline Architecture

```
[Input: Target AI Agent Skill directory]
                         │
      [Phase 1: Frontmatter & Structure Parsing] ──> Verify name, description, SKILL.md
                         │
      [Phase 2: 37 Full-Spectrum Static Rules] ────> Links, exception hygiene, secrets
                         │
      [Phase 3: Dynamic Selftest (--dynamic)] ─────> Execute target selftest, verify rc
                         │
      [Phase 4: Negative Destructive Checks] ──────> Verify guardrails block bad input
                         │
      [Phase 5: Actionable Report & Guidance] ─────> Output audit-report.txt
```

---

## 🚀 Quick Start

This is an AI Agent Skill — use it directly in your AI assistant or run it as a standalone CLI tool.

### Option A: Paste one sentence into any Agent (recommended, most universal)

Send this to your AI assistant and it will detect the platform and clone to the right skills directory:

> Please install the skill-doctor skill: clone `https://github.com/hyt315/skill-doctor` into your skills directory (e.g. `~/.claude/skills/skill-doctor` or `~/.agents/skills/skill-doctor`) and confirm it works. When I ask to audit, review, or inspect a skill, use the 37 static and dynamic rules to evaluate its quality.

### Option B: GitHub CLI 2.90+ (one command)

```bash
gh skill install hyt315/skill-doctor skill-doctor --agent claude-code --scope user
```

### Option C: Manual per-platform install

| Platform | Command |
|---|---|
| **Claude Code** | `git clone https://github.com/hyt315/skill-doctor.git ~/.claude/skills/skill-doctor` |
| **Codex** | `git clone https://github.com/hyt315/skill-doctor.git ~/.codex/skills/skill-doctor` |
| **Cursor** | `git clone https://github.com/hyt315/skill-doctor.git ~/.cursor/skills/skill-doctor` |
| **General Agents** | `git clone https://github.com/hyt315/skill-doctor.git ~/.agents/skills/skill-doctor` |

### Option D: Run directly in terminal as a CLI

```powershell
# Run static audit on any skill
python scripts/audit.py path/to/your-skill

# Include dynamic selftest run
python scripts/audit.py path/to/your-skill --dynamic

# Run skill-doctor's own regression test
python scripts/selftest.py
```

---

## 🔒 Safety & Read-Only Principles

- **Strictly Read-Only**: Analysis reads target skill files without modifying or overwriting any code;
- **Zero Network Calls**: All AST and regex rules run entirely offline;
- **Sandboxed Execution**: Dynamic tests only run when `--dynamic` is explicitly supplied.

---

## 📥 Download

| Method | Command / Link |
|---|---|
| **HTTPS** | `git clone https://github.com/hyt315/skill-doctor.git` |
| **SSH** | `git clone git@github.com:hyt315/skill-doctor.git` |
| **GitHub CLI** | `gh repo clone hyt315/skill-doctor` |
| **ZIP** | [Download ZIP](https://github.com/hyt315/skill-doctor/archive/refs/heads/main.zip) |
| **Tarball** | [Download Tar](https://github.com/hyt315/skill-doctor/archive/refs/heads/main.tar.gz) |
| **Single file (SKILL.md)** | `curl -O https://raw.githubusercontent.com/hyt315/skill-doctor/main/SKILL.md` |

---

## 📁 File Structure

```
skill-doctor/
├── SKILL.md                          # Core skill definition and 37-rule workflow
├── README.md                         # Chinese documentation
├── README.en.md                      # English documentation
├── CHANGELOG.md                      # Version history
├── LICENSE                           # MIT License
├── .gitignore                        # Git ignore rules
├── CONTRIBUTING.md                   # Contribution guide
├── CODE_OF_CONDUCT.md                # Code of conduct
├── SECURITY.md                       # Security policy
├── SUPPORT.md                        # Support channels
├── manifest.json                     # Skill manifest
├── agents/                           # Multi-agent metadata
├── scripts/
│   ├── audit.py                      # Main audit engine (37 rules + dynamic run)
│   ├── validate_repo.py              # Validator
│   └── selftest.py                   # Automated regression test runner
└── references/                       # Rule catalog & pitfall references
```

---

## ❓ FAQ

- **Q: What is a "guard that exists in name only"?**  
  A: When a test uses `try...except` but catches and swallows exceptions, causing broken code to report exit code 0 (pass).
- **Q: Does this require third-party Python packages?**  
  A: No. It is built entirely on Python 3.10+ standard libraries (`ast`, `re`, `pathlib`).
- **Q: What is the difference between WARN and FAIL?**  
  A: FAIL indicates blocking flaws (hardcoded secrets, fake exit codes); WARN indicates architectural recommendations (high token counts, deep nesting).

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md). If this skill helped you, please give it a [Star ⭐](https://github.com/hyt315/skill-doctor/stargazers)!

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

> 🌏 **中文版: [README.md](./README.md)**
