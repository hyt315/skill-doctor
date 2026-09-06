---
name: skill-doctor
description: 审查与迭代任意 AI Agent 技能目录（SKILL.md/scripts/references），支持「审查体检」与「迭代进化」双模式。通过五大架构形态自适应适配、50+ 项静态规则、动态实跑、负向用例与 50+ 条坑库对照找出流程走不通、口径矛盾、静默失效与安全泄露；结合 SEI 技能进化指数、四维深水区联网检索矩阵、形态专属测试/评测脚手架与演进方案生成，驱动技能持续迭代升维。当用户要求审查/体检/优化某个技能、提出技能改进方案、技能流程跑不通、或技能改动后需要回归验证时使用。
---

# 技能审查与进化引擎（skill-doctor）

专为 AI Agent 技能打造的工业级质量审查师与持续进化引擎。支持 **模式 A：审查体检（Audit Mode）** 与 **模式 B：迭代进化（Evolution Mode）** 双工作流。

## Reference Files

三个核心参考文件承载本技能积累的审查与进化资产。以下时机必须读取对应文件：

- `references/静态规则清单.md` —— 当 audit.py 报出 FAIL/WARN、需要写审查报告时：读对应规则的**定义与修复路径**，报告中引用规则必须注明出处；
- `references/坑库.md` —— 执行**坑库对照**时：逐条对照每条踩坑的“检查方法”，能脚本化的已进 audit.py，其余靠人工判断；
- `references/审查与进化方法论.md` —— 执行**步骤 0 形态判定、步骤 3 动态实跑、步骤 4 负向抽查与模式 B 迭代进化**时：五大形态专属要点、破坏夹具构造、四维深水区挖掘、只读解耦与 SEI 能力模型都在此文件。

## 工作流双模式

### 模式 A：审查体检（Audit Mode）

当用户要求体检、找茬、查 bug 或回归验证时执行：

```
审查进度：
- [ ] 步骤0：判定技能所属架构形态（纯提示词 / CLI工具 / MCP协议端 / 多阶段流水线 / 复合型）
- [ ] 步骤1：盘点技能目录结构（SKILL.md / scripts / references 逐个登记）
- [ ] 步骤2：跑静态检查 scripts/audit.py <技能目录>（覆盖 50+ 项工业级规则）
- [ ] 步骤3：动态实跑（selftest 或技能自述的验证命令，加 --dynamic）
- [ ] 步骤4：负向用例抽查（对关键门构造破坏夹具）
- [ ] 步骤5：坑库对照（逐条对照 references/坑库.md 的检查方法）
- [ ] 步骤6：汇总审查报告，输出 audit-report.txt 并给出分级修复路径
```

- **步骤2 静态检查**：`python <本技能>/scripts/audit.py <被审技能目录>`，覆盖八类规则。行尾注释 `# skill-doctor: allow` 豁免单行；文件级启发式用 `skill-doctor: allow-block 规则码` 豁免整文件。
- **步骤3 动态实跑**：`python <本技能>/scripts/audit.py <被审技能目录> --dynamic`，核验退出码与末行结论一致性。
- **步骤6 报告导出**：支持标准控制台输出、`--json` 机器可读与 `--markdown` 表格。

### 模式 B：迭代进化（Evolution Mode）

当用户要求优化技能、丰富技能、扩展能力、提出改进方案或重构升维时执行：

```
进化进度：
- [ ] 步骤1：运行进化雷达分析 scripts/evolve.py <技能目录> --analyze（自适应识别形态与计算 SEI 得分）
- [ ] 步骤2：提炼深水区检索矩阵 scripts/evolve.py <技能目录> --research-plan（获取 4 维精准检索词）
- [ ] 步骤3：执行深度联网挖掘（必须项）：调用联网检索工具挖掘官方 RFC、顶级开源标杆与杀手坑
- [ ] 步骤4：专业知识资产沉淀与技能丰富：沉淀 references/<domain>-pitfalls.md、完善 Fact Card、设计 Hero Banner
- [ ] 步骤5：形态适配脚手架注入：
      - CLI/HYBRID 型：scripts/evolve.py <技能目录> --scaffold-test（注入 AST 与负向夹具）
      - PROMPT 型：scripts/evolve.py <技能目录> --scaffold-prompt（注入 evals/ 评测集，绝不强塞空脚本）
- [ ] 步骤6：只读与治理解耦（Zero-Mutation 原则，治理对策须用户明确授权后手动执行）
- [ ] 步骤7：全链回归验证与工程卫生清理（确保 selftest / evals 通过并清除临时文件）
```

- **进化指数分析**：`python <本技能>/scripts/evolve.py <目标技能> --analyze` 查看五大形态识别结果与 SEI 五维量化打分；
- **四维深水区检索**：`python <本技能>/scripts/evolve.py <目标技能> --research-plan` 提取领域关键词，生成官方规范、杀手坑、开源标杆与指标基线 4 组精准检索指令；
- **生成演进方案**：`python <本技能>/scripts/evolve.py <目标技能> --plan` 自动输出针对该领域的演进蓝图与联网挖掘指引；
- **注入测试脚手架**：`python <本技能>/scripts/evolve.py <目标技能> --scaffold-test` 自动生成合规 `selftest.py` 与 `tests/` 套件（适用于 CLI/HYBRID）；
- **注入提示词评测套件**：`python <本技能>/scripts/evolve.py <目标技能> --scaffold-prompt` 自动生成 `evals/trigger_cases.json`（适用于纯提示词型 PROMPT）；
- **注入全套多文件脚手架**：`python <本技能>/scripts/evolve.py <目标技能> --scaffold-all` 一键为目标技能生成测试套件与指标基线事实卡。

### 交付成果事实卡

无论模式 A 还是模式 B，最终交付成果均统一汇总为分层事实卡（静态门禁、动态实跑、SEI 成熟度三层指标，详细结构见 `references/审查与进化方法论.md`）。

## 自审与互审

- **改本技能后**：`python scripts/selftest.py`（负向夹具 + evolve.py 回归）+ `python scripts/trigger_eval.py`（触发边界回归），两者全绿才算完；
- **改 description**：必须过 `evals/trigger_cases.json` 全家族用例；
- **治理元数据**：`manifest.json` 与 `CHANGELOG.md`，版本随功能演进递增；
- **环境依赖**：纯 Python 3 标准库实现，100% 零外部依赖。

## 审查与进化纪律

- **形态自适应与防过度优化原则**：量体裁衣，因材施教。严禁教条主义给纯提示词技能强塞无意义的空脚本；优化必须克制有度，以实战为绳墨，严防负增长与指令词盲目膨胀；
- **只读优先原则 (Zero-Mutation)**：体检与演进分析阶段绝对纯只读排查，绝不擅自修改被审代码与环境，不动任何设置；
- **治理与修改须用户明确授权**：所有破坏性修改、代码重写与治理建议独立拆分，严正标明须用户明确授权后手动执行，并提供回滚对策；
- **每条缺陷必附证据**：注明文件行号、命令输出或复现步骤，不写“感觉有问题”；
- **工程卫生铁律**：测试与审计副产物（如 `audit-report.txt`）在发版前必须物理清除，绝不污染代码仓库；
- **发版日志纯粹性**：Release 说明与 Commit Message 仅陈述优化内容与新增特性，不混入审查过程元说明。
