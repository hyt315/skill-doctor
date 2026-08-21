# Changelog

本项目采用 [Conventional Commits](https://www.conventionalcommits.org/) 格式记录变更。

## [1.1.0] - 2026-08-20

首个公开版本对应的功能状态（基于维护者提交历史整理）：

### Added

- `manifest.json` 治理元数据（owner / review_cadence / maturity_tier）
- CK001 口径一致检查，将坑14（多处口径打架）从纯人工升级为自动 + 负向夹具
- 触发评测 `evals/`（概念配置 + 家族用例），使 description 改动可回归

### Changed

- SKILL.md 固化自审 / 互审流程（selftest + trigger_eval 双回归、外部检查器交叉审、治理元数据登记）
