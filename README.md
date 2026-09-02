# 🩺 技能审查师 / Skill Doctor

<div align="center">

**给 AI Agent 技能做深度体检：37 项静态规则 + 动态实跑 + 负向抽查，专抓「门名义存在实际放行」的静默失效。**

**AI Agent skill auditor & linter with 37 static rules, dynamic execution, negative sample verification, and zero silent failures.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/hyt315/skill-doctor?sort=semver)](CHANGELOG.md)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-1f6feb)](SKILL.md)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Pure%20Python)-brightgreen)](SKILL.md)
[![GitHub Stars](https://img.shields.io/github/stars/hyt315/skill-doctor?style=social)](https://github.com/hyt315/skill-doctor/stargazers)

[English](./README.en.md) | [中文](./README.md)

</div>

---

## 📖 这是什么？

技能写完了、能跑、Demo 很漂亮——但它真的可靠吗？
- 是否在代码里用了宽捕获 `except Exception:` 悄悄吞掉了关键报错？
- 是否在 `references/` 里留下了 AI 永远不会读取的孤儿文件？
- 是否在 Markdown 示例里不小心硬编码了本地开发机绝对路径甚至 API 密钥？
- 自测脚本是不是“看似存在、实则永远返回 0 假装通过”？

**`skill-doctor`** 是一个专为 AI Agent 技能打造的质量审查元技能与终端审计工具。它通过 **37 项严密静态规则**（涵盖 Frontmatter 合规、引用链路、口径一致、退出码语义、安全卫生）、**动态实跑自测** 与 **负向破坏用例抽查**，将「看起来能跑」和「真正工业级可靠」之间的差距量化出来，逐项编号输出审计报告。

---

## ✨ 核心特性

| 核心模块 | 覆盖功能 | 带来价值 |
|---|---|---|
| 🔍 **37 项全维度静态规则** | Frontmatter、命名保留字、引用孤儿、口径打架、宽捕获吞异常、密钥扫描、绝对路径排查 | 覆盖 FM/SK/LK/CK/SF/SEC/EN/DY 八大维度，逐项编号可追溯 |
| 🏃 **动态实跑验证** | 实际拉起并运行被审技能的自测脚本（`selftest.py`），核验真实退出码语义 | 杜绝仅靠文本判断产生的虚假安全感 |
| 🎯 **负向破坏用例抽查** | 针对安全与质量门禁构造破坏样本，验证拦截门是否真的会拦截 | 专抓「门名义存在、实际放行」的最危险静默失效 |
| 🧠 **27 条真实通病坑库** | 从数百次真实技能审查中沉淀的典型坑库（现象 → 根因 → 修复 → 预防） | 持续沉淀最佳实践，避免重蹈覆辙 |
| 📄 **可追溯审计报告** | 自动生成标准化报告，逐项列明 OK / WARN / INFO / FAIL 与修改指引 | 方便 CI 自动化集成与团队代码审查 |
| 🛡️ **纯 Python 零依赖只读** | 仅使用 Python 标准库，审查过程对目标代码纯只读，零副作用 | 随处可运行，无需安装繁琐环境 |

---

## 📊 技能体检全流程架构

```
[输入: 待审查的 AI 技能目录]
                       │
      [Phase 1: Frontmatter 与结构解析] ──> 校验 name / description / 单层 SKILL.md
                       │
      [Phase 2: 37 项全维度静态规则扫描] ─> 引用完整性 / 异常捕获 / 密钥与路径安全
                       │
      [Phase 3: 动态回归实跑 (--dynamic)] > 实际执行被审技能 selftest，核验退出码
                       │
      [Phase 4: 负向破坏样本抽查] ────────> 验证质量门是否能真实阻断非法输入
                       │
      [Phase 5: 报告落盘与修复建议] ──────> 输出 audit-report.txt，逐项指导修复
```

---

## 🚀 快速开始

这是一个标准的 AI Agent Skill —— 既可装进 AI 助手使用，也可在终端直接当作 CLI 工具运行。

### 方式 A：把一句话发给任意 Agent（最推荐、最通用）

把下面这句话直接复制发送给你的 AI 助手，它会自动完成安装：

> 请安装 skill-doctor 技能：克隆 `https://github.com/hyt315/skill-doctor` 到你的 skills 目录（如 `~/.claude/skills/skill-doctor` 或 `~/.agents/skills/skill-doctor`），并确认安装成功。以后我要「审查/体检技能、上线前质量把关」时，按 SKILL.md 流程执行静态与动态审计。

### 方式 B：GitHub CLI 2.90+（一行命令）

```bash
gh skill install hyt315/skill-doctor skill-doctor --agent claude-code --scope user
```

### 方式 C：多平台手动安装

| 平台 | 安装命令 |
|---|---|
| **Claude Code** | `git clone https://github.com/hyt315/skill-doctor.git ~/.claude/skills/skill-doctor` |
| **Codex** | `git clone https://github.com/hyt315/skill-doctor.git ~/.codex/skills/skill-doctor` |
| **Cursor** | `git clone https://github.com/hyt315/skill-doctor.git ~/.cursor/skills/skill-doctor` |
| **通用 Agents 目录** | `git clone https://github.com/hyt315/skill-doctor.git ~/.agents/skills/skill-doctor` |

### 方式 D：本地终端直接当 CLI 运行

```powershell
# 对任意本地技能目录执行静态审查
python scripts/audit.py path/to/your-skill

# 包含动态自测实跑
python scripts/audit.py path/to/your-skill --dynamic

# 运行 skill-doctor 自身的回归测试
python scripts/selftest.py
```

---

## 🔒 安全与只读原则

- **严格纯只读**：审查过程只读分析目标技能代码，绝不擅自改动或重写被审项目的任何文件；
- **零网络调用**：所有规则匹配与语法树分析均在本地离线完成，绝不向外上传代码；
- **沙箱化自测**：动态实跑默认仅在传入 `--dynamic` 时显式触发，防止产生未预期的副作用。

---

## 📥 下载与获取

| 方式 | 命令 / 链接 |
|---|---|
| **HTTPS** | `git clone https://github.com/hyt315/skill-doctor.git` |
| **SSH** | `git clone git@github.com:hyt315/skill-doctor.git` |
| **GitHub CLI** | `gh repo clone hyt315/skill-doctor` |
| **ZIP 压缩包** | [下载 ZIP](https://github.com/hyt315/skill-doctor/archive/refs/heads/main.zip) |
| **Tar 归档** | [下载 Tar](https://github.com/hyt315/skill-doctor/archive/refs/heads/main.tar.gz) |
| **单文件 (SKILL.md)** | `curl -O https://raw.githubusercontent.com/hyt315/skill-doctor/main/SKILL.md` |

---

## 📁 文件结构

```
skill-doctor/
├── SKILL.md                          # 核心技能定义、37 项审查流程与调度
├── README.md                         # 中文说明文档
├── README.en.md                      # 英文说明文档
├── CHANGELOG.md                      # 版本发布记录
├── LICENSE                           # MIT 开源许可证
├── .gitignore                        # Git 忽略规则
├── CONTRIBUTING.md                   # 社区贡献指南
├── CODE_OF_CONDUCT.md                # 行为准则
├── SECURITY.md                       # 安全策略
├── SUPPORT.md                        # 支持渠道
├── manifest.json                     # 技能元数据清单
├── agents/                           # 多 Agent 平台元数据
├── scripts/
│   ├── audit.py                      # 核心审计脚本（静态 37 项 + 动态实跑）
│   ├── validate_repo.py              # 结构与隐私安全验证器
│   └── selftest.py                   # 自动化回归自测脚本
└── references/                       # 规则清单、通病坑库与案例
```

---

## ❓ 常见问题 (FAQ)

- **Q: 什么是「门名义存在实际放行」？**  
  A: 指测试代码中虽然写了 `try...except` 或 `if` 门禁，但由于异常被静默吞掉或返回值未断言，导致即使出现重大错误测试依然返回 0 绿标通过。
- **Q: 审查工具需要安装第三方 Python 依赖吗？**  
  A: 完全不需要。基于 Python 3.10+ 原生标准库（`ast`、`re`、`pathlib`）开发，纯净零依赖。
- **Q: 报告中的 WARN 和 FAIL 有什么区别？**  
  A: FAIL 代表阻断性的硬缺陷（如硬编码密钥、退出码欺骗、语法损坏）；WARN 代表设计层面的优化建议（如引用层级过深、Token 偏多）。

---

## 🤝 参与贡献

欢迎提交 Issue 与 Pull Request！详见 [CONTRIBUTING.md](CONTRIBUTING.md)。如果这个技能对你有帮助，欢迎在 GitHub 上点个 [Star ⭐](https://github.com/hyt315/skill-doctor/stargazers)！

---

## 📄 开源协议

本项目采用 [MIT 许可证](LICENSE) 开源。

---

> 🌏 **English: [README.en.md](./README.en.md)**
