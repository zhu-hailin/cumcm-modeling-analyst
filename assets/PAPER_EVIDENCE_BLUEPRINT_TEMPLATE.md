# PAPER_EVIDENCE_BLUEPRINT

- 赛题：
- Skill 版本与 commit：
- 当前模式：LIVE_CONTEST / BLIND / OPEN_REFERENCE
- Requirement Traceability：
- Run Ledger：
- 当前阶段：EARLY_SKELETON / FINAL_FREEZE
- 当前状态：PLANNED / READY / BLOCKED

> 读题后即可建立 `EARLY_SKELETON`；每问 Final Run 后增量补充。只有全部关键问题冻结并通过 Ready Gate 后才进入 `FINAL_FREEZE` 并标记 `PAPER_EVIDENCE_BLUEPRINT_READY`。

---

## 原题交付项骨架

| Requirement ID | 问题 | 动作词 | 对象/单位/范围 | 输入/依赖 | 硬约束 | 当前歧义/缺口 | 状态 |
|---|---|---|---|---|---|---|---|

早期阶段只需把原题交付边界建清楚，不要求提前填写 Final Run、论文位置和正式图表。

---

## 问题 Q{k} / Requirement Q{k}-R{n}

```yaml
question_id: Q{k}
requirement_id: Q{k}-R{n}
prompt_action:
required_deliverable:
primary_answer:
strongest_supported_alternative:
additional_data_needed:
evidence_grade: A | B | C
scientific_validity: PASS | QUALIFIED | FAIL
contest_task_completion: PASS | FAIL
primary_run_ids: []
validation_run_ids: []
main_table:
  artifact:
  paper_location:
  role: 直接结果 | 数据口径 | 模型比较 | 约束审计 | NOT_NEEDED
main_figure:
  artifact:
  paper_location:
  role: 结果 | 机制 | 验证 | 决策 | FIGURE_NOT_NEEDED
main_formula_or_rule:
  paper_location:
  code_mapping:
independent_validation:
  artifact:
  method:
uncertainty_or_sensitivity:
limitations:
downstream_interface:
status: PLANNED | READY | BLOCKED | NOT_APPLICABLE
```

说明：A/B/C、Run ID、PASS/FAIL 等用于内部证据管理；正式论文正文不要求机械展示这些状态，而应用具体验证、误差、稳定性和适用条件表达。

---

## 后台成果选编

| Artifact | 类型：PAPER_CORE / PAPER_SUPPORT / RUN_ONLY | 支撑什么 | 正文/附录位置 | Run ID/方法版本 | 备注 |
|---|---|---|---|---|---|

---

## 图表去重

| 信息主题 | 候选图 | 候选表 | 最终保留 | 理由 | 删除后损失 |
|---|---|---|---|---|---|

只有升级为正式证据的图才进入蓝图；普通 `EXPLORATION_FIGURE` 不要求逐张登记。

---

## 跨问接口

| 上游问题 | 下游问题 | 传递对象 | 正式文件/字段 | 上游 Final Run | 下游使用位置 |
|---|---|---|---|---|---|

---

## 总体技术路线图评估

- 结论：REQUIRED / NOT_NEEDED
- 理由：
- 图中必须包含：
- 图中不得包含：
- Python 绘图脚本：
- 正文位置：
- 方法版本：CURRENT / SUPERSEDED

方法结构图允许：

```text
Run ID：N/A（方法结构图）
```

---

## 论文证据预算

| 章节 | 必须可见的直接答案 | PAPER_CORE | PAPER_SUPPORT / 附录接口 | 阅读风险 |
|---|---|---|---|---|

目标是让评委快速找到答案和关键证据，不是给图表设数量配额。

---

## FINAL_FREEZE Ready Gate

- [ ] 每个原题交付项都有 Requirement ID；
- [ ] 每项有直接 `primary_answer` 或合规 `NOT_IDENTIFIABLE`；
- [ ] 每项有真实 Final/Validation Run 或明确不适用原因；
- [ ] 科学有效性与竞赛完成度分别判断；
- [ ] 关键结论有与风险匹配的独立验证；
- [ ] `PAPER_CORE` 已安排进正文；
- [ ] 图/表/公式没有机械配额和明显重复；
- [ ] 总体技术路线图已评估；
- [ ] 前后问接口从正式文件读取；
- [ ] `SUPERSEDED` 结果已排除；
- [ ] 无未解决 `BLOCKED` 项。

通过后：

```text
PAPER_EVIDENCE_BLUEPRINT_READY
```
