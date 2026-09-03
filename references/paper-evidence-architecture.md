# 论文证据架构与选编规范

## 目标

Final Run 产生很多文件，不代表论文已经完整。论文写作前必须建立 `PAPER_EVIDENCE_BLUEPRINT`，把每个原题交付项映射到正文中的主答案、证据、验证、限制和位置。

核心原则：

> **让真实算出的关键证据，在评委能快速找到的位置被看见。**

本规范位于 Final/Validation Run 与完整参考论文写作之间。蓝图不是新的计算阶段，不允许重新手算或从聊天抄数字。

蓝图未达到：

```text
PAPER_EVIDENCE_BLUEPRINT_READY
```

不得开始完整参考论文。

---

## 1. 前置条件

开始蓝图前确认：

- 各问已有 Final Run，必要验证已有 Validation Run；
- 每问已经分别判断 `SCIENTIFIC_VALIDITY` 与 `CONTEST_TASK_COMPLETION`；
- 原题动作词、对象、单位、范围和指定输出已形成 Requirement Traceability；
- 关键结果、图表和表格能追到真实数据、代码与 Run；
- `SUPERSEDED` 结果已排除；
- 影响结论的安全审计冲突已解决。

条件不足时标记相应问题为 `BLOCKED`，不能靠论文措辞补齐计算缺口。

---

## 2. 每个交付项的最小蓝图

每个原题交付项单独登记，而不是只按“大问题”笼统登记。

```yaml
question_id: Q1
requirement_id: Q1-R1
prompt_action: 分析/预测/分类/评价/优化/解释/给出方案
required_deliverable: 原题要求交付的对象、单位和范围
primary_answer: 一句话主答案或 NOT_IDENTIFIABLE
strongest_supported_alternative: 仅在 NOT_IDENTIFIABLE 时填写
additional_data_needed: 仅在 NOT_IDENTIFIABLE 时填写
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
  method: 留一/时间外推/扰动/置换/小规模精确解/外部核验等
uncertainty_or_sensitivity: 数值区间、翻转率、误差、稳定性或条件性说明
limitations: 结论成立范围与不能声称的内容
downstream_interface: 向后问传递的正式文件、字段、参数或模型
status: PLANNED | READY | BLOCKED | NOT_APPLICABLE
```

要求：

1. `primary_answer` 必须能直接回答原题；
2. `paper_location` 必须可定位，不写“正文某处”；
3. 核心数字只从登记的 Final/Validation 成果读取；
4. A 级结论关联主证据和至少一种独立验证；
5. `NOT_IDENTIFIABLE` 必须同时登记最强替代结论、证据等级和补充数据需求；
6. `CONTEST_TASK_COMPLETION = FAIL` 的问题不得被“科学上谨慎”掩盖。

---

## 3. 后台成果分层

所有可用结果分为：

### `PAPER_CORE`

直接回答原题，或支撑 A 级核心结论。必须在正文中可见，不能只留在 CSV、JSON、日志或附录。

典型内容：

- 一句话主答案与关键数字；
- 最终分类、预测、排名、路径、方案或阈值；
- 关键数据口径/清洗审计表；
- 主要模型结果和必要独立验证；
- 跨问正式接口。

### `PAPER_SUPPORT`

支撑稳健性、敏感性、消融、完整参数、长名单或边界。正文概述关键结果，完整内容进入附录或支撑材料。

### `RUN_ONLY`

调试、被否决候选、重复随机运行、无决策价值的中间表和临时图。只留 Run Ledger 或工作区，不进入正文。

不得把全部后台表塞进论文，也不得因为保守而只写结论、不展示关键过程。

---

## 4. 图、表、公式的选择

图表数量由证据需求决定，不按配额。

选择顺序：

1. 哪种媒介最直接回答原题？
2. 评委需要比较趋势、结构还是精确数值？
3. 同一信息是表格更清楚，还是图更清楚？
4. 删除该图/表后会损失什么证据？
5. 它是否重复另一项证据？

规则：

- 精确名单、参数、约束和数值优先表格；
- 趋势、分布、结构、空间关系和不确定性优先图；
- 同一信息若表格更清楚，图标记 `FIGURE_NOT_NEEDED`；
- 不能把普通 DataFrame 截图冒充论文表；
- 大矩阵和长名单采用“正文摘要 + 附录完整可编辑表”；
- 主结果不得只存在后台文件；
- 不能为了页数压缩掉原题直接答案和关键证据。

---

## 5. 总体学术技术路线图评估

以下任一情况出现时，必须评估总体路线图：

- 方法链含三个以上相互依赖步骤；
- 多个问题共享数据、参数、模型或中间结果；
- 数据经历多层变换、训练、验证和迁移；
- 优化包含多个决策环节；
- 不画图会让跨问接口难以理解。

记录：

```text
总体路线图：REQUIRED | NOT_NEEDED
理由：
图中必须包含：
图中不得包含：
对应绘图脚本：
正文位置：
```

需要时只保留：输入数据、关键预处理、每问核心模型/计算、Final/Validation 分支、正式跨问接口和最终输出。

禁止 KPI 卡片、状态徽章、PASS/FAIL 大标签、巨型页眉、宣传副标题、圆角卡片墙、App/网页 UI、发光、阴影、渐变背景和大段内部审计状态。

若旧流程图因海报化被淘汰，必须判断是否需要学术风格重画，不能直接删除“总体路线”这一证据角色。

### 两类溯源契约

数据结果图：

```text
源数据 + Final/Validation Run + 绘图脚本
```

方法/流程图：

```text
Requirement ID + 已确认模型计划/假设
+ 对应代码模块或算法步骤 + 绘图脚本 + 版本状态
```

方法图允许 `Run ID = N/A（方法结构图）`，但最终模型或接口改变后必须失效并重新生成。

---

## 6. 版面与信息层级

为正文和附录做证据预算，而不是图表数量预算。

每问首段优先：

```text
主答案 → 关键数字/规则 → 证据等级 → 方法摘要 → 验证 → 限制
```

页面级检查：

- 单张普通结果图接近独占一页时是否科学必要；
- 两张互补且字号仍可读的独立图是否适合同排；
- 图是否紧裁剪，图题是否紧随，是否有大面积空白；
- 连续两页是否只有免责声明或稀疏图件，却没有主结果接力；
- 长名单、大矩阵和完整参数是否进入附录；
- 摘要、总体路线、每问首段、主图表和结论是否形成快速阅读链。

默认独立图片；只有多个 panel 共同回答同一科学问题、共享坐标或明确比较逻辑时才合并。

---

## 7. 跨问接口

维护：

| 上游问题 | 下游问题 | 复用对象 | 正式文件/字段 | Final Run | 下游正文位置 |
|---|---|---|---|---|---|

上游结果更新后，蓝图、下游代码、结果、图表和论文必须同步检查。不得从论文文字或聊天手抄上游值。

---

## 8. 蓝图完成检查

- [ ] 每个原题交付项都有 Requirement ID；
- [ ] 每项都有直接 `primary_answer` 或合规 `NOT_IDENTIFIABLE`；
- [ ] 科学有效性和竞赛完成度分别记录；
- [ ] 每项有证据等级、正文位置和 Final/Validation Run；
- [ ] A 级结论有独立验证；
- [ ] `PAPER_CORE` 不只存在后台文件；
- [ ] 图/表/公式没有机械配额和明显重复；
- [ ] 总体学术路线图已经评估；
- [ ] 方法图与数据图使用正确溯源契约；
- [ ] 前后问正式接口明确；
- [ ] 版面预算能让主答案优先可见；
- [ ] 所有 `BLOCKED` 项已解决或明确阻止写作。

全部通过后标记：

```text
PAPER_EVIDENCE_BLUEPRINT_READY
```

蓝图文件建议保存到：

```text
02_analysis/PAPER_EVIDENCE_BLUEPRINT.md
```
