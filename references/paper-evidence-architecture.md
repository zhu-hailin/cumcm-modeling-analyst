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

单问小题或局部验证可把需求、答案、验证和未完成项留在本问交接中，不强制独立蓝图文件。需要跨问证据管理或整题封版时再汇入一份权威蓝图，不让两处继续重复维护。

沿用读题时已有需求骨架，只补尚缺的交付对象/范围、位置要求、真实依赖和疑点。早期不填写尚不存在的 Run、图表、论文页码和有效性状态。

当前问成果选入正式证据后，补主答案、有效运行/推导、关键验证及论文用途的引用。图表规则按[绘图规范](python-visualization-policy.md)，正式入选和同步按[交付规范](final-delivery-packaging.md)；临时 EDA、调参和中间文件不逐项登记到蓝图。

### 1.2 FINAL_FREEZE

全部关键问题完成后：

1. 回查正常人类可见原题；
2. 确认每个交付项都有直接答案或合规 `NOT_IDENTIFIABLE`；
3. 排除 `SUPERSEDED` 结果；
4. 补齐 Final/Validation Run、图表、公式、验证、限制与论文位置；
5. 分成 `PAPER_CORE / PAPER_SUPPORT / RUN_ONLY`；
6. 评估总体技术路线图；
7. 执行[一致性扫描](final-consistency-sweep.md)的 EVIDENCE_FREEZE 范围，检查已有证据及计划正文位置，不要求尚未写出的论文；
8. 才标记 `PAPER_EVIDENCE_BLUEPRINT_READY`。

蓝图不是新的计算阶段，不允许手算核心数字或从聊天抄结果。

---

## 2. 每个交付项的正式蓝图

字段使用[蓝图模板](../assets/PAPER_EVIDENCE_BLUEPRINT_TEMPLATE.md)，按现有成果填写适用部分，不把模板空格当作新增任务。运行引用按[运行账本](model-run-ledger.md)，各问完成状态按[核心流程](core-workflow.md)。

要求：

1. `primary_answer` 直接回答原题；
2. 核心数字只从登记的 Final/Validation 成果读取；
3. `paper_location` 最终可定位，不写“正文某处”；
4. 证据等级、科学有效性与竞赛完成度按[建模质量门](modeling-quality-gates.md)，不要在蓝图中重新定义；
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

图表来源、生成、下方说明及 QA 按[绘图规范](python-visualization-policy.md)；这里仅决定证据角色和位置，正式入选按[交付规范](final-delivery-packaging.md)。

---

## 5. 总体学术技术路线图

共享机制、跨问依赖或多环节决策难以用短段落说明时，再考虑路线图；不用步骤数量触发额外任务。

记录：

```text
总体路线图：REQUIRED | NOT_NEEDED
理由：
必须展示：
不得展示：
绘图脚本：
正文位置：
```

来源接口按[绘图规范](python-visualization-policy.md)第 4 节，不为路线图伪造计算 Run。

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

接口只引用正式文件/字段。上游改变后的运行替换按[运行账本](model-run-ledger.md)，正式材料失效与同步按[交付规范](final-delivery-packaging.md)。

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
- [ ] 正式图表符合[绘图规范](python-visualization-policy.md)的生成、来源、说明与 QA 要求；
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

已有蓝图时，`05_paper/` 中的论文引用该权威记录，不维护第二份副本；单章节写作可先引用已核验的逐问成果，不为此新建完整蓝图。
