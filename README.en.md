# 🩺 Skill Doctor / skill-doctor

<div align="center">

**Industrial-grade AI Agent skill auditor & linter with 4 architectural engines, 50+ static rules, dynamic execution, negative sampling, and actionable fix hints.**

**给 AI Agent 技能做全维度深度体检：四大形态专属引擎、50+ 项工业级规则、动态实跑、负向抽查与自愈修复指引。**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/hyt315/skill-doctor?sort=semver)](CHANGELOG.md)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-1f6feb)](SKILL.md)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Pure%20Python)-brightgreen)](SKILL.md)
[![GitHub Stars](https://img.shields.io/github/stars/hyt315/skill-doctor?style=social)](https://github.com/hyt315/skill-doctor/stargazers)

[English](./README.en.md) | [中文](./README.md)

</div>

---

## 📖 What is this?

Your AI Agent skill runs and demos look great — but is it truly reliable and production-grade? In real-world agent deployments, developers frequently hit these hidden anti-patterns:
- Broad `except Exception:` blocks that silently swallow errors, creating quality gates that exist in name only;
- Missing on-disk images, videos, or demo scripts referenced in Markdown documentation, resulting in broken links for users and AI;
- Windows CRLF (`\r\n`) line endings in Bash scripts that crash on Linux CI with `command not found: set`;
- Embedded Git Remote Token URLs (`https://token@github.com`) or personal machine path leaks;
- Over-inflation of hard directives (MUST/NEVER > 15 times) in `SKILL.md`, causing prompt degradation and severe IFScale compliance drops.

**`skill-doctor`** is an industrial-grade meta-skill and CLI auditing engine designed for AI Agent skills. Featuring **4 Architectural Auditing Engines**, **50+ Comprehensive Static Rules**, **Dynamic Selftest Execution**, **Negative Destructive Sampling**, and **40+ Real-World Pitfalls**, it outputs actionable reports with `--json`, `--markdown`, and **Auto-Fix Guidance** to eliminate the gap between "it seems to run" and "production-grade reliability".

---

## ✨ Key Features

| Core Module | Capabilities & Scope | Quality Gates & Delivered Value |
|---|---|---|
| 🤖 **4 Archetype Auditing Engines** | Tailored checks for Pure Prompt, Tool-Augmented CLI, MCP Protocol Server, and Multi-Stage Pipeline skills | Replaces one-size-fits-all checks with targeted architectural profiling |
| 🔍 **50+ Comprehensive Static Rules** | Covers FM structure, LK/AS links & assets, SF silent failures, SEC security, EN/PL cross-platform, CK/TC prompt health | Traceable rule IDs intercepting CRLF, Token URLs, broad exceptions, and dead links |
| 🏃 **Dynamic Execution Verification** | Executes target skill's actual `selftest.py` to verify exit code semantics and genuine test passes | Eliminates false confidence from pure text inspections |
| 🎯 **Negative Destructive Sampling** | Injects invalid/corrupted test samples to verify that guardrails truly block bad inputs | Eliminates dangerous "guards that exist in name only" |
| 🧠 **40+ Real-World Pitfalls** | Curated catalog of anti-patterns collected across hundreds of skill audits (Symptom → Cause → Fix → Prevention) | Consolidates best practices to prevent repeated errors |
| 📄 **Multi-Format Export & Auto-Fix** | Supports ANSI console summary, `--json` machine-readable output, and `--markdown` GitHub tables | Ready for CI pipelines with actionable code fix snippets |
| 🛡️ **Zero-Dependency Read-Only** | Pure Python 3.10+ standard library with 100% read-only analysis | Runs anywhere with zero external dependencies and zero side effects |

---

## 📊 Complete Auditing Pipeline Architecture

```
[Input: Target AI Agent Skill directory]
                         │
      [Step 0: 4-Archetype Architectural Profiling]
      Identify: Pure Prompt / CLI Tool / MCP Protocol / Multi-Stage Pipeline
                         │
      [Step 1: 50+ Full-Spectrum Static Rules Scan]
      Intercept broken assets / broad exceptions / Token URLs / CRLF line endings
                         │
      [Step 2: Dynamic Selftest Execution (--dynamic)]
      Execute target selftest, verifying true exit codes and PASS outputs
                         │
      [Step 3: Negative Destructive Sample Verification]
      Inject corrupted inputs to ensure guardrails actively block bad data
                         │
      [Step 4: 40+ Real-World Pitfalls Verification]
      Audit against common traps, state persistence, and command drift
                         │
      [Step 5: Report Generation & Actionable Fix Hints]
      Output audit-report.txt / --json / --markdown with phased repair paths
```

---

## 🚀 Quick Start

This is an AI Agent Skill — use it directly in your AI assistant or run it as a standalone CLI tool.

### Option A: Paste one sentence into any Agent (recommended, most universal)

Send this to your AI assistant and it will detect the platform and clone to the right skills directory:

> Please install the skill-doctor skill: clone `https://github.com/hyt315/skill-doctor` into your skills directory (e.g. `~/.claude/skills/skill-doctor` or `~/.agents/skills/skill-doctor`) and confirm it works. When I ask to audit, review, or inspect a skill, use the 50+ static and dynamic rules to evaluate its quality.

### Option B: GitHub CLI 2.90+ (one command)

```bash
gh skill install hyt315/skill-doctor skill-doctor --agent claude-code --scope user
```

### Option C: Manual per-platform install

| Platform | User-level Path | Project-level Path |
|---|---|---|
| **Claude Code** | `git clone https://github.com/hyt315/skill-doctor.git ~/.claude/skills/skill-doctor` | `.claude/skills/skill-doctor` |
| **Codex** | `git clone https://github.com/hyt315/skill-doctor.git ~/.agents/skills/skill-doctor` | `.agents/skills/skill-doctor` |
| **Cursor** | `git clone https://github.com/hyt315/skill-doctor.git ~/.cursor/skills/skill-doctor` | `.cursor/skills/skill-doctor` |
| **General Agents** | `git clone https://github.com/hyt315/skill-doctor.git ~/.agents/skills/skill-doctor` | `.agents/skills/skill-doctor` |

### Option D: Run directly in terminal as a CLI

```powershell
# Run static audit on any skill (generates audit-report.txt)
python scripts/audit.py path/to/your-skill

# Include dynamic selftest run
python scripts/audit.py path/to/your-skill --dynamic

# Output machine-readable JSON (for CI pipelines)
python scripts/audit.py path/to/your-skill --json

# Output GitHub Markdown table
python scripts/audit.py path/to/your-skill --markdown

# Run skill-doctor's own regression test
python scripts/selftest.py
```

---

## 🔒 Safety & Read-Only Principles

- **Strictly Read-Only**: Analysis reads target skill files without modifying or overwriting any code;
- **Zero Network Calls**: All AST and regex rules run entirely offline with zero data leakage;
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

## 📖 In-Depth Technical References

| Reference Guide | Core Focus | When to Read | Estimated Time |
|---|---|---|---|
| 📋 [**Static Rules Catalog (`静态规则清单.md`)**](references/静态规则清单.md) | 50+ industrial rule definitions, origins, and repair paths | When diagnosing audit warnings and failures | 4 mins |
| 🛡️ [**Pitfalls Database (`坑库.md`)**](references/坑库.md) | 40+ curated anti-patterns (Symptom → Cause → Fix → Prevention) | When auditing complex pipelines & edge cases | 5 mins |
| 🩺 [**Audit Methodology (`审查方法论.md`)**](references/审查方法论.md) | 4 archetypes, negative fixtures, Evals metrics, and healing workflow | When writing selftests or major refactorings | 4 mins |

---

## 📁 File Structure

```
skill-doctor/
├── SKILL.md                          # Core skill definition, 4-archetype dispatch & workflow
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
├── evals/                            # Trigger eval dataset
├── scripts/
│   ├── audit.py                      # Core audit engine (4 archetypes + 50+ rules + CLI export)
│   ├── trigger_eval.py               # Trigger evaluation runner
│   └── selftest.py                   # Automated regression test runner
└── references/                       # Rule catalog, 40+ pitfalls & methodology
    ├── 静态规则清单.md                # 50+ Industrial rules overview
    ├── 坑库.md                        # 40+ Real-world pitfalls
    └── 审查方法论.md                  # 4 Archetypes & negative testing
```

---

---

## 🌐 GitHub Open Source Lifecycle Suite

A complete, production-ready toolchain for open-source maintainers and contributors:

| Stage / Role | Recommended Skill | Core Mission & Capabilities | GitHub Repository |
|---|---|---|---|
| 📦 **Pre-Launch Prep** | [**`github-oss-prep`**](https://github.com/hyt315/github-oss-prep) | Automated repository scaffolding, bilingual READMEs, CI workflows, and compliance checks | [hyt315/github-oss-prep](https://github.com/hyt315/github-oss-prep) |
| 🩺 **Quality Doctor** | [**`skill-doctor`**](https://github.com/hyt315/skill-doctor) | 50+ industrial static rules + dynamic selftest runner for 100% reliable Agent Skills | [hyt315/skill-doctor](https://github.com/hyt315/skill-doctor) |
| ⚙️ **Post-Launch Ops** | [**`github-oss-ops`**](https://github.com/hyt315/github-oss-ops) | Issue triage, AI hallucination defense, PR review, GHSA vulnerability SOP, and multi-channel broadcasting | [hyt315/github-oss-ops](https://github.com/hyt315/github-oss-ops) |
| 🚀 **Contributor Navigator** | [**`github-oss-contribute`**](https://github.com/hyt315/github-oss-contribute) | End-to-end contributor guide: Fork syncing, Rebase conflict resolution, DCO signing, and anti-AI slop gates | [hyt315/github-oss-contribute](https://github.com/hyt315/github-oss-contribute) |

---

## ❓ FAQ

- **Q: What is a "guard that exists in name only"?**  
  A: When a test catches and swallows exceptions, causing broken code to report exit code 0 (pass) despite critical failures.
- **Q: Does this require third-party Python packages?**  
  A: No. It is built entirely on Python 3.10+ standard libraries with zero external dependencies.
- **Q: What is the difference between WARN and FAIL?**  
  A: FAIL indicates blocking flaws (Token URL leaks, CRLF crashing Linux CI, broken assets, fake exit codes); WARN indicates architectural suggestions (high token counts, directive inflation).

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md). If this skill helped you, please give it a [Star ⭐](https://github.com/hyt315/skill-doctor/stargazers)!

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

> 🌏 **中文版: [README.md](./README.md)**
