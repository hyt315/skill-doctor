<div align="center">

# 🩺 技能审查师 / Skill Doctor

**给 AI Agent 技能做体检：35 项静态规则 + 动态实跑 + 负向抽查，专抓「门名义存在实际放行」的静默失效。**

**简体中文 · [English](./README.en.md)**

[![License: MIT](https://img.shields.io/github/license/hyt315/skill-doctor)](LICENSE)
[![Release](https://img.shields.io/github/v/release/hyt315/skill-doctor?sort=semver)](https://github.com/hyt315/skill-doctor/releases)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-1f6feb)](SKILL.md)
[![Tests](https://github.com/hyt315/skill-doctor/actions/workflows/ci.yml/badge.svg)](https://github.com/hyt315/skill-doctor/actions)
[![Stars](https://img.shields.io/github/stars/hyt315/skill-doctor?style=social)](https://github.com/hyt315/skill-doctor/stargazers)

</div>

---

## 📖 这是什么？

技能写完了、能跑、demo 很漂亮——但它真的可靠吗？**Skill Doctor** 是一个审计 AI Agent 技能的元技能：用 **35 项静态规则**（frontmatter 合规、引用链接、口径一致、安全卫生、退出码语义…）+ **动态实跑**被审技能的自测 + **负向用例抽查**（该 FAIL 的样本必须被抓），把「看起来能用」和「确实可靠」之间的差距量出来。每条检查都有编号（FM/SK/LK/CK/SF/SEC/EN/DY），报告落盘可追溯。

### ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🔍 **35 项静态规则** | frontmatter、命名保留字、引用孤儿、阈值口径打架、宽捕获吞异常、硬编码密钥、个人路径泄露……逐项编号可追溯 |
| 🏃 **动态实跑** | 不只看文档——实际运行被审技能的 selftest，验证退出码语义与文本结论一致 |
| 🎯 **负向抽查** | 「门名义存在实际放行」是最危险的失效：构造该被抓的破坏样本，验证门真的会拦 |
| 🧠 **26 条坑库** | 从真实审查中沉淀的通病库（现象→根因→修复→预防→检查方法），持续回写 |
| 📄 **报告落盘** | `audit-report.txt` 写入被审技能目录，逐项 OK/WARN/FAIL 可追溯 |
| 🛡️ **零依赖只读** | 仅 Python 标准库；审查过程只读被审技能，`--dynamic` 默认不跑防副作用 |

---

## 🚀 快速开始

> ✨ **一句话装进 AI Agent**：把下面这段话直接发给你的 AI 助手，它会自动完成安装——
>
> ```text
> 请安装 skill-doctor Skill：把 https://github.com/hyt315/skill-doctor 克隆到你的 skills 目录（Claude Code：~/.claude/skills/skill-doctor/；Codex：~/.codex/skills/skill-doctor/；Cursor：~/.cursor/skills/skill-doctor/），并确认 SKILL.md、references/、scripts/ 都在。以后遇到要审查/体检技能时，按 SKILL.md 的流程用审计脚本做静态 + 动态检查。
> ```

| 平台 | 安装命令 |
|------|----------|
| **Claude Code** | `git clone https://github.com/hyt315/skill-doctor.git ~/.claude/skills/skill-doctor` |
| **Codex** | `git clone https://github.com/hyt315/skill-doctor.git ~/.codex/skills/skill-doctor` |
| **Cursor** | `git clone https://github.com/hyt315/skill-doctor.git ~/.cursor/skills/skill-doctor` |

---

## 💬 触发方式

对 AI 说以下任意一类话，即会触发本技能：

- 「审查这个技能」「给这个技能做体检」「审一遍再上线」
- 「看看这个技能有没有坑」「为什么我的技能有时灵时不灵」
- 「技能发布前做一次质量门禁」

## ⚙️ 前置条件

- **Python 3.10+**（仅标准库，零第三方依赖）
- 被审技能的目录路径
- 无需管理员权限；审查过程只读，不改被审技能任何文件

## 📦 输出交付物

```text
audit-report.txt      —— 落盘到被审技能目录，逐项 OK/WARN/INFO/FAIL + RESULT 结论
动态实跑结论          —— selftest 是否真跑通、退出码语义是否诚实（--dynamic）
负向抽查结论          —— 关键门的破坏样本是否真被拦截（人工配合方法论执行）
```

---

## 📚 示例：一份真实的审查报告

```text
技能静态审查报告：network-slow-diagnosis
检查结果：
OK   [FM001] SKILL.md 存在
OK   [SK004] 全树唯一 SKILL.md
OK   [LK004] references/ 文件均被 SKILL.md/脚本提及
OK   [SEC001] 未发现硬编码密钥
WARN [EN005] bash 脚本缺 set -euo pipefail
INFO [DY003] 非 selftest 入口（tests），动态实跑请人工执行其回归命令
共 35 项，通过 33，WARN 2，INFO 2，FAIL 0
RESULT PASS
```

每一行都能在 `references/静态规则清单.md` 里找到规则定义与修复建议。

---

## 📥 下载 / 安装

```bash
# HTTPS
git clone https://github.com/hyt315/skill-doctor.git

# SSH
git clone git@github.com:hyt315/skill-doctor.git

# GitHub CLI
gh repo clone hyt315/skill-doctor

# ZIP
# https://github.com/hyt315/skill-doctor/archive/refs/heads/main.zip

# 单文件（仅 SKILL.md）
curl -O https://raw.githubusercontent.com/hyt315/skill-doctor/main/SKILL.md
```

---

## 📁 文件结构

```
skill-doctor/
├── SKILL.md                     # 技能入口（审查流程 + 方法论路由）
├── manifest.json
├── references/
│   ├── 静态规则清单.md           # 35 项规则的权威定义
│   ├── 审查方法论.md             # 静态→动态→负向的完整审查流程
│   └── 坑库.md                   # 26 条真实踩坑沉淀（持续回写）
├── scripts/
│   ├── audit.py                  # 审计入口（--stdout / --dynamic）
│   ├── selftest.py               # 本技能回归（好夹具绿 + 坏夹具被抓）
│   └── trigger_eval.py           # description 触发边界回归
├── evals/                        # 触发评测用例
├── LICENSE
├── README.md  /  README.en.md  # 双语说明（本文件为中文）
└── .github/                     # Issue/PR 模板 + CI
```

---

## ▶️ 快速使用

```bash
# 静态审查，报告落 <被审技能目录>/audit-report.txt
python scripts/audit.py <被审技能目录>

# 加跑被审技能的动态自测（默认不跑，防副作用）
python scripts/audit.py <被审技能目录> --dynamic

# 改动本技能后必跑的回归
python scripts/selftest.py
python scripts/trigger_eval.py
```

---

## 🤝 贡献 / 反馈

- 报 Bug / 提建议：用仓库的 Issue 模板
- 贡献：见 [CONTRIBUTING.md](CONTRIBUTING.md)，改动前必跑 `selftest.py` 与 `trigger_eval.py`
- 提交新坑：按坑库格式（现象→根因→修复→预防→检查方法）回写 `references/坑库.md`
- 漏洞报告：见 [SECURITY.md](SECURITY.md)（私有漏洞报告，勿走公开 Issue）

---

## 📜 License

[MIT](LICENSE) © 2026 hyt315

> 🌏 **English version: [README.en.md](./README.en.md)**