# 论文证据架构与选编规范

## 目标

论文证据架构不是最后突然填写的一张大表，而是把“原题要求 → 当前答案 → 真实运行 → 图表/公式 → 验证 → 论文位置”逐步连接起来。

> **读题后可以建骨架，逐问完成后持续补充，全部 Final/Validation Run 冻结后再正式封版。**

只有封版状态：

```text
PAPER_EVIDENCE_BLUEPRINT_READY
```

表示整题证据已就绪、可以冻结；它不是开始组织完整工作稿的门槛。读题后即可建立论文主线，逐问写入已验证材料，未完成部分明确标记。

---

## 1. 两个阶段

### 1.1 EARLY_SKELETON

单问小题或局部验证可把需求、答案、验证和未完成项留在本问交接中，不强制独立蓝图文件。需要跨问管理或准备论文时再汇入一份权威蓝图，不让两处继续重复维护。

读题后建立轻量 Requirement / Evidence 骨架，至少记录：

- Requirement ID；
- 原题动作词、对象、范围、单位；
- 需要交付的答案形式；
- `required_location: BODY | SUPPORT | EITHER` 及其题面/适用要求依据；
- 当前输入与跨问依赖；
- 已知硬约束；
- 当前歧义 / 数据缺口；
- 预计可能需要的模型或证据角色（尚未定稿时允许空缺）。

每问完成 Final Run 后立即补：主答案、Run、验证、结果表/图、关键决策引用和下游接口。论文图表在比赛过程中随当前问使用 Python 生成，通过 `python-visualization-policy.md` 使用 nature-skills，不等整题冻结后再补画。

### 1.2 FINAL_FREEZE

全部关键问题完成后：

1. 回查正常人类可见原题；
2. 确认每个交付项都有直接答案或合规 `NOT_IDENTIFIABLE`；
3. 排除 `SUPERSEDED` 结果；
4. 补齐 Final/Validation Run、图表、公式、验证、限制与论文位置；
5. 分成 `PAPER_CORE / PAPER_SUPPORT / RUN_ONLY`；
6. 评估总体技术路线图；
7. 执行 final-consistency-sweep.md 的 EVIDENCE_FREEZE 范围，检查已有证据及计划正文位置，不要求尚未写出的论文；
8. 才标记 `PAPER_EVIDENCE_BLUEPRINT_READY`。

蓝图不是新的计算阶段，不允许手算核心数字或从聊天抄结果。

---

## 2. 每个交付项的正式蓝图

```yaml
question_id: Q1
requirement_id: Q1-R1
prompt_action: 分析/预测/分类/评价/优化/解释/给出方案
required_deliverable: 原题要求对象、单位和范围
required_location: BODY | SUPPORT | EITHER
location_basis: 题面位置或适用交付要求；未指定时说明依据
decision_refs: [Q1-D01]
primary_answer: 一句话主答案或 NOT_IDENTIFIABLE
strongest_supported_alternative: 仅 NOT_IDENTIFIABLE 时填写
additional_data_needed: 仅 NOT_IDENTIFIABLE 时填写
evidence_grade: A | B | C
scientific_validity: PASS | QUALIFIED | FAIL
contest_task_completion: PASS | FAIL
primary_run_ids: [Rxxx]
validation_run_ids: [Ryyy]
main_table:
  artifact: 04_results/tables/...
  paper_location: 4.2
  role: 直接结果 | 数据口径 | 模型比较 | 约束审计
  explanation_below: 展示什么、反映什么、支持什么判断及必要边界
main_figure:
  artifact: 04_results/figures/...
  paper_location: 4.2
  role: 结果 | 机制 | 验证 | 决策 | FIGURE_NOT_NEEDED
  python_entry: 03_code/...
  supports_claim: 回答的问题与支撑的判断
  explanation_below: 展示什么、反映什么、支持什么判断及必要边界
main_formula_or_rule:
  paper_location: 4.1
  code_mapping: 03_code/...
independent_validation:
  artifact: 04_results/...
  method: 当前题实际采用的验证
uncertainty_or_sensitivity: 区间、误差、稳定性、翻转率或条件性说明
limitations: 结论成立范围与不能声称的内容
downstream_interface: 向后问传递的正式文件/字段/参数/模型
status: PLANNED | READY | BLOCKED | NOT_APPLICABLE
```

要求：

1. `primary_answer` 直接回答原题；
2. 核心数字只从登记的 Final/Validation 成果读取；
3. `paper_location` 最终可定位，不写“正文某处”；
4. A 级核心结论有主证据和能检验主要失效方式的独立验证，具体口径以 modeling-quality-gates.md 为准；
5. `NOT_IDENTIFIABLE` 同时给最强替代结论与补充数据需求；
6. `CONTEST_TASK_COMPLETION = FAIL` 不能靠谨慎措辞掩盖。
7. `required_location` 依据原题/适用要求确定，正文位置未定时允许计划位置；最终位置不得违反原题。需求未指定位置时，直接答案和关键论证仍优先在正文可见。
8. `decision_refs` 引用本问模型说明中的关键建模决策，不复制整段内容或另建重复台账。局部任务无对应选择时可为空，不制造比较。

---

## 3. 后台成果分层

### PAPER_CORE

直接回答原题，或支撑最核心结论。必须在正文可见，不能只存在 CSV、JSON、日志或附录。

### PAPER_SUPPORT

稳健性、敏感性、消融、完整参数、长名单和边界。正文概述关键结果，完整内容可进入附录。

### RUN_ONLY

无决策价值的调试、重复运行、中间表和临时图。留在 Run Ledger/工作区，不进入正文。

被否决候选若说明选型理由、揭示边界或支持最终取舍，可进入 `PAPER_CORE` / `PAPER_SUPPORT`。选编看它是否支撑论证，不看它是否是最终获选方案。

不要把全部后台结果塞进论文，也不要因为“严谨”而只写限制、不展示原题主答案。

---

## 4. 图、表和公式怎么选

数量由证据需求决定，不设配额。

优先问：

1. 评委需要精确数值、趋势、分布、结构还是决策规则？
2. 表格还是图更直接？
3. 删除这个证据会损失什么？
4. 是否与已有图/表重复？

一般：

- 精确名单、参数、约束和离散结果优先表；
- 趋势、分布、空间结构、网络、不确定性优先图；
- 大矩阵和长名单用“正文摘要 + 附录完整可编辑表”；
- 普通 DataFrame 不截图冒充论文表；
- 图不能增加理解时使用 `FIGURE_NOT_NEEDED`。

探索图只有在升级为正式证据后才进入蓝图。

绘图执行与样式统一路由至 `python-visualization-policy.md` 指定的 nature-skills；使用 Python 随问生成和核验。这里仅决定证据角色，不维护另一套绘图程序规范。

---

## 5. 总体学术技术路线图

以下情况必须评估是否需要：

- 三个以上相互依赖步骤；
- 多问共享数据、参数、模型或中间结果；
- 多层预处理、训练、验证或迁移；
- 优化包含多个决策环节；
- 不画图会使跨问接口明显难懂。

记录：

```text
总体路线图：REQUIRED | NOT_NEEDED
理由：
必须展示：
不得展示：
绘图脚本：
正文位置：
```

数据图溯源：

```text
源数据 + Final/Validation Run + 绘图脚本
```

方法图溯源：

```text
Requirement ID + 已确认模型/假设
+ 对应代码模块/算法步骤 + 绘图脚本 + 方法版本
```

方法图允许 `Run ID = N/A（方法结构图）`。

---

## 6. 内部状态与正式论文分离

以下内容适合内部管理：

```text
FINAL_RUN_ID
SCIENTIFIC_VALIDITY
CONTEST_TASK_COMPLETION
A/B/C evidence grade
PAPER_CORE / PAPER_SUPPORT / RUN_ONLY
SUPERSEDED
```

正式论文正文**不要求机械展示这些内部标签**。论文应把它们翻译成评委能直接理解的证据：

- 主答案和关键数字；
- 验证方法与误差；
- 稳定性 / 敏感性；
- 现实约束满足情况；
- 适用范围与限制。

内部蓝图负责追溯，正文负责论证。

---

## 7. 跨问接口

维护：

| 上游问题 | 下游问题 | 复用对象 | 正式文件/字段 | Final Run | 下游使用位置 |
|---|---|---|---|---|---|

上游结果改变后沿实际依赖链重跑；不得从论文文字或聊天手抄上游值。

---

## 8. 完成检查

- [ ] 每个原题交付项有 Requirement ID；
- [ ] 已核对 `required_location` 和题面依据，精简未移走正文必答项；
- [ ] 影响结论的选择有可追溯的 `decision_refs`，包含理由、证据和取舍；
- [ ] 每项有直接 `primary_answer` 或合规 `NOT_IDENTIFIABLE`；
- [ ] 科学有效性与竞赛完成度分别记录；
- [ ] 每项有 Final/Validation Run 或明确不适用原因；
- [ ] 关键结论有与风险匹配的验证；
- [ ] `PAPER_CORE` 已规划进入正文；
- [ ] 图、表、公式没有机械配额和明显重复；
- [ ] 需要的论文图表已随问用 Python 生成并按 nature-skills 核验，而非留到终稿补画；
- [ ] 每张图表下方有说明，解释内容、发现和判断，未以标题代替；
- [ ] 总体路线图已评估；
- [ ] 前后问正式接口明确；
- [ ] `SUPERSEDED` 结果未进入正式证据；
- [ ] 所有 `BLOCKED` 项已解决；科学有效性或竞赛完成度 FAIL 的交付项不能被标为 READY，QUALIFIED 必须带适用条件；NOT_IDENTIFIABLE 是否完成原题要求按建模质量门判断；
- [ ] 本次交付范围内的原题要求已覆盖；仅部分问题完成时只交付明确标注的阶段成果，不宣称全题蓝图就绪。

全部通过后标记：

```text
PAPER_EVIDENCE_BLUEPRINT_READY
```

权威蓝图默认保存：

```text
02_analysis/PAPER_EVIDENCE_BLUEPRINT.md
```

`05_paper/` 中的论文只引用这份蓝图，不维护第二份独立副本。
