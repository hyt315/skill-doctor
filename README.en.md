<p align="center">
  <img src="assets/banner.svg" alt="Skill Doctor - AI Agent Skill Auditor & Iterative Evolution Engine" width="100%" />
</p>

# 🩺 Skill Doctor / skill-doctor

<div align="center">

**Industrial-grade AI Agent skill auditor & iterative evolution engine: 5 architectural engines, 50+ static rules, 4-phase closed-loop pipeline, SEI index, multi-file scaffolding, and actionable fix hints.**

**给 AI Agent 技能做全维度深度体检与自进化：五大形态专属引擎、50+ 项工业级规则、四阶段闭环工程流水线、SEI 进化度量化评估、多文件脚手架一键注入与自愈修复指引。**

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

**`skill-doctor`** is an industrial-grade meta-skill and CLI auditing engine designed for AI Agent skills. Featuring **5 Architectural Auditing Engines**, **50+ Comprehensive Static Rules**, **Dynamic Selftest Execution**, **Negative Destructive Sampling**, and **40+ Real-World Pitfalls**, it outputs actionable reports with `--json`, `--markdown`, and **Auto-Fix Guidance** to eliminate the gap between "it seems to run" and "production-grade reliability".

---

## ✨ Key Features

| Core Module | Capabilities & Scope | Quality Gates & Delivered Value |
|---|---|---|
| 🤖 **5 Archetype Auditing Engines** | Tailored checks for Pure Prompt, Tool-Augmented CLI, MCP Protocol Server, Multi-Stage Pipeline, and Hybrid skills | Eliminates one-size-fits-all dogma; never forces dummy scripts onto cognitive prompt skills |
| 🌐 **4D Multi-Source Benchmark Matrix** | Generates targeted queries for Peer Agent Skills on GitHub, Top OSS Repos, Official Specs/RFCs, and Killer Pitfalls; supports executable AST probes and Tier-3 offline fallback | Benchmarks against state-of-the-art skills and ensures robust execution even in offline environments |
| 🔍 **50+ Comprehensive Static Rules** | Covers FM structure, LK/AS links & assets, SF silent failures, SEC security, EN/PL cross-platform, CK/TC prompt health | Traceable rule IDs intercepting CRLF, Token URLs, consecutive hyphens, broad exceptions, and dead links |
| 🧬 **Skill Evolution Engine (`evolve.py`)** | Adaptive SEI index (0-100), 4-Phase Closed-Loop Pipeline, automated evolution plans (`--plan`), and tailored scaffolding (`--scaffold-test` / `--scaffold-prompt` / `--scaffold-all`) | Upgrades skills into robust multi-file architectures with genuine test suites |
| 🏃 **Dynamic Execution Verification** | Executes target skill's actual `selftest.py` or `evals/` test suite to verify exit code semantics and genuine test passes | Eliminates false confidence from pure text inspections |
| 🎯 **Negative Destructive Sampling** | Injects invalid/corrupted test samples to verify that guardrails truly block bad inputs | Eliminates dangerous "guards that exist in name only" |
| 🧠 **50+ Real-World Pitfalls** | Curated catalog of anti-patterns collected across hundreds of skill audits (Symptom → Cause → Fix → Prevention) | Consolidates best practices to prevent repeated errors |
| 📄 **Multi-Format Export & Auto-Fix** | Supports ANSI console summary, `--json` machine-readable output, and `--markdown` GitHub tables | Ready for CI pipelines with actionable code fix snippets |
| 🛡️ **Zero-Dependency Read-Only** | Pure Python 3.10+ standard library with 100% read-only analysis | Runs anywhere with zero external dependencies and zero side effects |

### 🧬 Skill Evolution Index Dashboard (SEI Radar Preview)

Quantify skill maturity and generate actionable roadmaps plus full scaffolding with a single command:

```text
======================================================================
       skill-doctor 技能进化度评估看板 (Skill Evolution Index)
======================================================================
目标技能: my-agent-skill
综合进化指数 (SEI): 85 / 100
----------------------------------------------------------------------
评估维度                             | 当前得分       | 满分基线      
----------------------------------------------------------------------
Architecture (Multi-File Completeness)| 20         | 20
Tooling (Deterministic Tool Scripts)  | 20         | 20
FactCard (Fact Cards & Metric Baselines)| 20       | 20
Safety (Read-First & Explicit Consent)| 15         | 20
Verification (Negative Fixtures & AST)| 10         | 20
----------------------------------------------------------------------
```

---

## 📊 Complete Auditing & Evolution Pipeline Architecture

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
      [Step 4: 50+ Real-World Pitfalls Verification]
      Audit against common traps, state persistence, and command drift
                         │
      [Step 5: Report Generation & Actionable Fix Hints]
      Output audit-report.txt / --json / --markdown with phased repair paths
                         │
      [Step 6: SEI Skill Evolution & Scaffolding (evolve.py)]
      Compute 5D maturity index, output Evolution Plan Markdown & scaffold files
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

# --- 🚀 Skill Evolution Engine ---
# 1. Profile skill archetype and compute Skill Evolution Index (SEI 0-100)
python scripts/evolve.py path/to/your-skill --analyze

# 2. Extract domain keywords and generate 4D multi-source research queries (Peer Skills / OSS / RFC / Pitfalls)
python scripts/evolve.py path/to/your-skill --research-plan

# If in an offline or search-restricted environment, activate Tier-3 offline fallback scaffolding:
python scripts/evolve.py path/to/your-skill --offline-fallback

# 3. Automatically generate customized evolution roadmap Markdown
python scripts/evolve.py path/to/your-skill --plan -o evolution-plan.md

# 4. For CLI / script skills: scaffold standard test suite (tests/ + scripts/selftest.py with AST check and DY002 fixtures)
python scripts/evolve.py path/to/your-skill --scaffold-test

# 5. For pure prompt skills: scaffold evaluation suite (evals/trigger_cases.json with negative boundary cases)
python scripts/evolve.py path/to/your-skill --scaffold-prompt

# 6. Scaffold complete multi-file architecture (tests/ + references/fact-card.md baseline)
python scripts/evolve.py path/to/your-skill --scaffold-all

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
| 🛡️ [**Pitfalls Database (`坑库.md`)**](references/坑库.md) | 50+ curated anti-patterns (Symptom → Cause → Fix → Prevention) | When auditing complex pipelines & edge cases | 5 mins |
| 🩺 [**Audit & Evolution Methodology (`审查与进化方法论.md`)**](references/审查与进化方法论.md) | 5 archetypes, negative fixtures, healing workflow, 4-phase closed-loop pipeline & SEI metric | When writing selftests, deep audit & evolving skills | 5 mins |

---

## 📁 File Structure

```
skill-doctor/
├── SKILL.md                          # Core skill definition, 4-phase closed-loop pipeline (Audit ➔ Research ➔ Refactor ➔ Verify)
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
├── assets/                           # Visual assets
│   └── banner.svg                    # Vector SVG Hero Banner
├── evals/                            # Trigger eval dataset
├── tests/                            # Unit tests & AST syntax validation
│   └── test_skill.py                 # Standard unit test entry (asserting AST syntax integrity)
├── scripts/
│   ├── audit.py                      # Core audit engine (5 archetypes + 40+ rules + CLI export)
│   ├── evolve.py                     # Skill evolution engine (SEI radar + roadmap + scaffold)
│   ├── trigger_eval.py               # Trigger evaluation runner
│   └── selftest.py                   # Automated regression test runner (32 checks)
└── references/                       # Rule catalog, 50+ pitfalls & methodology
    ├── 静态规则清单.md                # 50+ Industrial rules overview
    ├── 坑库.md                        # 50+ Real-world pitfalls (incl. pitfalls 44-52)
    └── 审查与进化方法论.md            # 5 Archetypes, 4-phase closed-loop pipeline & SEI metric
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
