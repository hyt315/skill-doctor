# Changelog

本项目采用 [Conventional Commits](https://www.conventionalcommits.org/) 格式记录变更。

## [1.2.3] - 2026-08-23

### Added

- 坑库新增 4 条实战坑（源自 md2wechat 减法改造全链演练）：33 状态机无产物阶段收尾是暗环节、34 校验计数口径与写作者直觉不一致、35 回退路径输入格式只活在脚本里、36 硬指令词通胀条数越多越失效（含 IFScale 基准实证与 Anthropic skill-creator 官方口径）。
- 审查方法论、静态规则清单同步微调（各 1 行）。

### Fixed

- 补推 1.2.2 条目对应的 audit.py / selftest.py 完整代码（LK005 结构化判定与强引导正则、EN006 md 资源字节级污染检查及配套负向夹具），此前本地已改但未推送。

## [1.2.2] - 2026-08-22

### Added

- LK005 强引导正则增强（源自 md2wechat 实审）：补"另读/通读"、行首"读："、"按 `references/x` 结构写"三类真实强引导模式。
- LK005 结构化判定新增中文别名「按需加载参考」章节标题。
- 坑库回写坑 28「CK001 数字对撞的两类误报」（引文数字、跨对象数字），含被审技能侧的 allow 豁免处置。

## [1.2.1] - 2026-08-22

### Fixed

- LK005 检测器两处修正：① 强引导正则补"先查"；② 新增结构化判定——SKILL.md 含「Reference Files/参考文档」专门章节且文件在其中被列出（官方 webapp-testing 模式：文件+触发条件清单）即视为合格引导。修复将合格技能（如 windows-cleanup-optimize 的"参考文档（按需加载）"章节）误报为弱引用的漏报。
- 修复 listed 集合与文件名比对错位（完整路径 vs 裸文件名）导致结构化判定永不生效的 bug。

## [1.2.0] - 2026-08-22

### Added

- **LK005 弱引用检测**：SKILL.md 对 references/ 文件的引导若只有"详见/可参考"类弱措辞、无明确读取时机，给 WARN——Agent Skills 规范规定 references 按需加载，措辞决定执行 AI 会不会真的去读（坑 27）。依据：agentskills.io 规范 + 官方 skill-creator（"linked with guidance on when to read them"、"explain why in lieu of heavy-handed MUSTs"）+ 官方 pdf 技能条件触发句式。
- SKILL.md 新增「Reference Files」章节：按审查节点列出三个参考文件的读取时机与理由（机对机场景，条件触发式）。
- 坑库回写坑 27「弱引用措辞导致 references 不被读」，目录新增"九、引导与发现类"。
- selftest 新增 LK005 正反夹具（弱引用必须 WARN；强引导不报），并修正坑 14 断言锚点与新好夹具措辞的联动。

### Changed

- 步骤 4 的方法论引用升级为条件触发式（"做负向抽查前，先读……构造方法在里面"）。
- 审查纪律加两条：报告引用规则/坑注明出处文件；未读对应文件不得标记步骤完成。

## [1.1.0] - 2026-08-20

首个公开版本对应的功能状态（基于维护者提交历史整理）：

### Added

- `manifest.json` 治理元数据（owner / review_cadence / maturity_tier）
- CK001 口径一致检查，将坑14（多处口径打架）从纯人工升级为自动 + 负向夹具
- 触发评测 `evals/`（概念配置 + 家族用例），使 description 改动可回归

### Changed

- SKILL.md 固化自审 / 互审流程（selftest + trigger_eval 双回归、外部检查器交叉审、治理元数据登记）
