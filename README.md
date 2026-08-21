# 🩺 技能审查师 / Skill Doctor

<div align="center">

**给任意 AI Agent 技能做全身体检，揪出“流程走不通、口径矛盾、静默失效”三类病。**

**Audit any AI Agent skill to catch silent failures, inconsistencies, and broken workflows.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/release/hyt315/skill-doctor?sort=semver)](CHANGELOG.md)
[![GitHub Stars](https://img.shields.io/github/stars/hyt315/skill-doctor?style=social)](https://github.com/hyt315/skill-doctor/stargazers)

**简体中文 · [English](./README.en.md)**

</div>

---

### 📖 这是什么？

**Skill Doctor（技能审查师）** 是一个 AI Agent Skill，专门给 **SKILL.md 形态的技能**（Claude Code / Codex / DSH 等）做全身体检。它用**四件套**找出三类最危险的病：

- 🔗 **流程走不通**——文档承诺了文件 / 命令，实际不存在或跑不起来
- 🌀 **口径矛盾**——文档、脚本、参考文件三方对不上（同一件事说法打架）
- 🤫 **静默失效**——该拦的没拦，门在名义上存在、实际放行（最危险）

四件套审查法：

1. **静态口径对齐**——文档 / 脚本 / 参考三方承诺对得上（规则见 `references/静态规则清单.md`）
2. **动态实跑**——真跑被审技能的 selftest / 校验脚本，重跑才是当前真相
3. **负向用例**——对关键门构造“该 FAIL 的夹具”，验证它真会拦
4. **坑库对照**——拿历史踩坑逐条对照（`references/坑库.md`）

### ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🔍 **五类静态检查** | 结构合规 / 引用一致 / 口径一致 / 安全卫生 / 脚本工程 |
| 🧪 **负向夹具回归** | `selftest.py` 好夹具全绿 + 坏夹具逐规则被抓 |
| 🤖 **触发边界回归** | `trigger_eval.py` 覆盖 description 触发词家族 |
| 📝 **分级修复路径** | 每项问题附最小修复路径，按最深根因处理 |
| 🐍 **零依赖** | 仅 Python 标准库，无需安装 |
| 🌐 **中英双语** | SKILL.md 与参考文件均中英对照 |

### 🚀 快速开始

> ✨ **一句话装进 AI Agent**：把下面这段话直接发给你的 AI 助手，它会自动完成安装——
>
> ```text
> 请安装 skill-doctor Skill：把 https://github.com/hyt315/skill-doctor 克隆到你的 skills 目录（Claude Code：~/.claude/skills/skill-doctor/；Codex：~/.codex/skills/skill-doctor/；Cursor：~/.cursor/skills/skill-doctor/），并确认 SKILL.md、references/、scripts/ 都在。以后遇到要审查/体检技能时，按 SKILL.md 的流程用审计脚本做静态 + 动态检查。
> ```

这是一个 AI Agent Skill——装到任意 AI 编程助手的 skills 目录即可使用。

#### 安装（选你的平台）

| 平台 | 安装命令 |
|------|----------|
| **Claude Code** | `git clone https://github.com/hyt315/skill-doctor.git ~/.claude/skills/skill-doctor` |
| **Codex** | `git clone https://github.com/hyt315/skill-doctor.git ~/.codex/skills/skill-doctor` |
| **Cursor** | `git clone https://github.com/hyt315/skill-doctor.git ~/.cursor/skills/skill-doctor` |

#### 怎么用

告诉你的 AI 助手“审查这个技能目录”，或直接跑脚本：

```bash
# 静态审查，报告落 <被审技能目录>/audit-report.txt
python <skill-doctor>/scripts/audit.py <被审技能目录>

# 动态实跑被审技能的 selftest（默认不跑，防副作用）
python <skill-doctor>/scripts/audit.py <被审技能目录> --dynamic

# 回归测试（改本技能后必跑）
python <skill-doctor>/scripts/selftest.py

# 触发边界回归
python <skill-doctor>/scripts/trigger_eval.py
```

### 📥 下载 / Download

| 方式 | 命令 / 链接 |
|------|------------|
| **HTTPS** | `git clone https://github.com/hyt315/skill-doctor.git` |
| **SSH** | `git clone git@github.com:hyt315/skill-doctor.git` |
| **GitHub CLI** | `gh repo clone hyt315/skill-doctor` |
| **ZIP 源码** | [下载 ZIP](https://github.com/hyt315/skill-doctor/archive/refs/heads/main.zip) |
| **Tar 源码** | [下载 Tar](https://github.com/hyt315/skill-doctor/archive/refs/heads/main.tar.gz) |
| **单文件（SKILL.md）** | `curl -O https://raw.githubusercontent.com/hyt315/skill-doctor/main/SKILL.md` |

### 📁 文件结构

```
skill-doctor/
├── SKILL.md                    # 技能核心定义
├── manifest.json              # 治理元数据（owner/cadence/tier）
├── LICENSE                     # MIT
├── .gitignore
├── README.md                   # 本文件（中文）
├── README.en.md                # 英文版
├── CHANGELOG.md
├── agents/
│   └── openai.yaml             # Codex/OpenAI 技能元数据
├── scripts/
│   ├── audit.py                # 静态检查器（五类）
│   ├── selftest.py             # 回归测试（好/坏夹具）
│   └── trigger_eval.py         # 触发边界回归
├── evals/
│   └── trigger_cases.json      # 触发家族用例
├── references/
│   ├── 静态规则清单.md          # 规则与级别唯一事实源
│   ├── 审查方法论.md            # 四件套审查方法
│   └── 坑库.md                  # 历史踩坑对照
└── .github/
    ├── pull_request_template.md
    ├── workflows/ci.yml        # 自审 + 回归 CI
    └── ISSUE_TEMPLATE/         # Bug / 文档改进 模板
```

### 🤝 贡献

请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

### 📄 许可

[MIT](LICENSE)。版本变化见 [CHANGELOG.md](CHANGELOG.md)。

---

> 🌏 **English version: [README.en.md](./README.en.md)**
