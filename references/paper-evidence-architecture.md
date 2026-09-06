# 论文证据架构与选编规范

## 目标

论文证据架构不是最后突然填写的一张大表，而是把“原题要求 → 当前答案 → 真实运行 → 图表/公式 → 验证 → 论文位置”逐步连接起来。

> **读题后可以建骨架，逐问完成后持续补充，全部 Final/Validation Run 冻结后再正式封版。**

只有封版状态：

```text
PAPER_EVIDENCE_BLUEPRINT_READY
```

才允许开始完整参考论文。

---

## 1. 两个阶段

### 1.1 EARLY_SKELETON

读题后建立轻量 Requirement / Evidence 骨架，至少记录：

- Requirement ID；
- 原题动作词、对象、范围、单位；
- 需要交付的答案形式；
- 当前输入与跨问依赖；
- 已知硬约束；
- 当前歧义 / 数据缺口；
- 预计可能需要的模型或证据角色（尚未定稿时允许空缺）。

每问完成 Final Run 后立即补：主答案、Run、验证、结果表/图和下游接口。

### 1.2 FINAL_FREEZE

全部关键问题完成后：

1. 回查正常人类可见原题；
2. 确认每个交付项都有直接答案或合规 `NOT_IDENTIFIABLE`；
3. 排除 `SUPERSEDED` 结果；
4. 补齐 Final/Validation Run、图表、公式、验证、限制与论文位置；
5. 分成 `PAPER_CORE / PAPER_SUPPORT / RUN_ONLY`；
6. 评估总体技术路线图；
7. 执行一致性检查；
8. 才标记 `PAPER_EVIDENCE_BLUEPRINT_READY`。

蓝图不是新的计算阶段，不允许手算核心数字或从聊天抄结果。

---

## 2. 每个交付项的正式蓝图

```yaml
question_id: Q1
requirement_id: Q1-R1
prompt_action: 分析/预测/分类/评价/优化/解释/给出方案
required_deliverable: 原题要求对象、单位和范围
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
main_figure:
  artifact: 04_results/figures/...
  paper_location: 4.2
  role: 结果 | 机制 | 验证 | 决策 | FIGURE_NOT_NEEDED
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
4. A 级核心结论原则上有主证据和至少一种不同原理的独立验证；
5. `NOT_IDENTIFIABLE` 同时给最强替代结论与补充数据需求；
6. `CONTEST_TASK_COMPLETION = FAIL` 不能靠谨慎措辞掩盖。

---

## 3. 后台成果分层

### PAPER_CORE

直接回答原题，或支撑最核心结论。必须在正文可见，不能只存在 CSV、JSON、日志或附录。

### PAPER_SUPPORT

稳健性、敏感性、消融、完整参数、长名单和边界。正文概述关键结果，完整内容可进入附录。

### RUN_ONLY

调试、被否决候选、重复运行、无决策价值的中间表和临时图。留在 Run Ledger/工作区，不进入正文。

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
- [ ] 每项有直接 `primary_answer` 或合规 `NOT_IDENTIFIABLE`；
- [ ] 科学有效性与竞赛完成度分别记录；
- [ ] 每项有 Final/Validation Run 或明确不适用原因；
- [ ] 关键结论有与风险匹配的验证；
- [ ] `PAPER_CORE` 已规划进入正文；
- [ ] 图、表、公式没有机械配额和明显重复；
- [ ] 总体路线图已评估；
- [ ] 前后问正式接口明确；
- [ ] `SUPERSEDED` 结果未进入正式证据；
- [ ] 所有 `BLOCKED` 项已解决或明确阻止写作。

全部通过后标记：

```text
PAPER_EVIDENCE_BLUEPRINT_READY
```

权威蓝图默认保存：

```text
02_analysis/PAPER_EVIDENCE_BLUEPRINT.md
```

`05_paper/` 中的论文只引用这份蓝图，不维护第二份独立副本。