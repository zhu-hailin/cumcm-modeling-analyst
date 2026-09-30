# PAPER_EVIDENCE_BLUEPRINT

- 赛题：
- Skill 版本与 commit：
- 当前模式：LIVE_CONTEST / BLIND / OPEN_REFERENCE
- Requirement Traceability：
- Run Ledger：
- 当前阶段：EARLY_SKELETON / FINAL_FREEZE
- 当前状态：PLANNED / READY / BLOCKED

> 需要跨问管理或准备论文证据时沿用已有需求骨架增量填写。字段是引用接口，尚无成果的部分留空；早期提纲仅使用 `PAPER_OUTLINE_TEMPLATE.md`。冻结条件统一按[证据架构](../references/paper-evidence-architecture.md)第 8 节，`PAPER_EVIDENCE_BLUEPRINT_READY` 不限制开始工作稿。

---

## 原题交付项骨架

| Requirement ID | 问题 | 动作词 | 对象/单位/范围 | required_location 及依据 | 输入/依赖 | 硬约束 | 当前歧义/缺口 | 状态 |
|---|---|---|---|---|---|---|---|---|

早期阶段只需把原题交付边界建清楚，不要求提前填写 Final Run、论文位置和正式图表。

---

## 问题 Q{k} / Requirement Q{k}-R{n}

```yaml
question_id: Q{k}
requirement_id: Q{k}-R{n}
prompt_action:
required_deliverable:
required_location: BODY | SUPPORT | EITHER
location_basis:
decision_refs: []
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
  explanation_below:
main_figure:
  artifact:
  paper_location:
  role: 结果 | 机制 | 验证 | 决策 | FIGURE_NOT_NEEDED
  python_entry:
  supports_claim:
  explanation_below:
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

`decision_refs` 引用本问模型说明中的关键建模决策，不重复抄写。`required_location` 依据题面/适用要求填写，删段移表前回查；未规定位置时仍保证主答案和关键论证在正文可见。

---

## 后台成果选编

| Artifact | 类型：PAPER_CORE / PAPER_SUPPORT / RUN_ONLY | 支撑什么 | 正文/附录位置 | Run ID/方法版本 | 备注 |
|---|---|---|---|---|---|

论文位置分类按[证据架构](../references/paper-evidence-architecture.md)第 3 节；正式入选及同步按[交付规范](../references/final-delivery-packaging.md)。

---

## 图表去重

| 信息主题 | 候选图 | 候选表 | 最终保留 | 理由 | 删除后损失 |
|---|---|---|---|---|---|

有实际重复信息时才填写去重表。图表生成、来源与下方说明按[绘图规范](../references/python-visualization-policy.md)，探索图不逐张登记。

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

使用[证据架构](../references/paper-evidence-architecture.md)第 8 节的唯一检查清单，本模板不维护副本。运行引用按[运行账本](../references/model-run-ledger.md)；各问完成状态按[核心流程](../references/core-workflow.md)。
