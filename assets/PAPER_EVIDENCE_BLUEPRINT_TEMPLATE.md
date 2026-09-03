# PAPER_EVIDENCE_BLUEPRINT

- 赛题：
- Skill 版本与 commit：
- 模型/推理档位：
- 当前模式：LIVE_CONTEST / BLIND / OPEN_REFERENCE
- 生成日期：
- Requirement Traceability：
- Run Ledger：
- 当前状态：PLANNED / READY / BLOCKED

---

## 总体技术路线图评估

- 结论：REQUIRED / NOT_NEEDED
- 依据：多问依赖 / 三步以上方法链 / 多层数据变换 / 训练—验证—迁移 / 多环节优化 / 其他
- 图中必须包含：
- 图中不得包含：
- Python 绘图脚本：
- Manifest 记录：
- 正文位置：
- 方法版本状态：CURRENT / SUPERSEDED

---

## 原题交付项覆盖矩阵

| Requirement ID | 问题 | 原题动作词 | 交付对象/单位/范围 | 主答案 | 证据等级 | 科学有效性 | 竞赛完成度 | 正文位置 | 状态 |
|---|---|---|---|---|---|---|---|---|---|

---

## 问题 Q{k}

```yaml
question_id: Q{k}
requirement_id: Q{k}-R1
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

### 本问正文优先顺序

```text
主答案
→ 关键数字/规则
→ 证据等级
→ 方法摘要
→ 验证
→ 限制
```

### 后台成果选编

| Artifact | 类型：PAPER_CORE / PAPER_SUPPORT / RUN_ONLY | 支撑什么 | 正文/附录位置 | Run ID | 备注 |
|---|---|---|---|---|---|

### 图表去重

| 信息主题 | 候选图 | 候选表 | 保留哪一种 | 理由 | 删除后损失 |
|---|---|---|---|---|---|

### 跨问接口

| 下游问题 | 传递对象 | 正式文件/字段 | 上游 Final Run | 下游使用位置 |
|---|---|---|---|---|

---

## 论文版面证据预算

| 章节/页面 | 主答案 | PAPER_CORE 图/表 | PAPER_SUPPORT | 附录接口 | 阅读风险 |
|---|---|---|---|---|---|

检查：

- [ ] 主结果没有只留在 CSV/JSON/日志；
- [ ] 没有把所有后台结果塞入正文；
- [ ] 长名单和大矩阵采用正文摘要 + 附录完整可编辑表；
- [ ] 普通结果图没有无必要独占整页；
- [ ] 互补独立图同排时字号仍可读；
- [ ] 摘要、路线图、每问首段、主图表和结论能形成快速阅读链。

---

## Ready Gate

- [ ] 每个原题交付项有主答案或合规 `NOT_IDENTIFIABLE`；
- [ ] 每项有正文位置、证据等级和 Run；
- [ ] 科学有效性与竞赛完成度分别通过或明确限定；
- [ ] A 级结论有独立验证；
- [ ] PAPER_CORE 已安排进正文；
- [ ] 总体技术路线图已评估；
- [ ] 图/表/公式没有机械配额或明显重复；
- [ ] 前后问接口可追溯；
- [ ] 无未解决 BLOCKED 项。

通过后：

```text
PAPER_EVIDENCE_BLUEPRINT_READY
```
