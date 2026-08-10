# 两阶段赛题工作流

## 开题前：先确定联网研究模式

在第一次外部联网检索之前，如果用户尚未明确说明，必须先询问一次：

> 这是 **A. 实战赛题**，还是 **B. 旧题盲测**？

- **实战赛题**：进入 `LIVE_RESEARCH_MODE`，保留正常联网研究能力，可搜索论文、数据、参数、官方资料、相似案例、算法与代码文档，但不得以寻找当前比赛现成完整答案为目的。
- **旧题盲测**：进入 `BLIND_BENCHMARK_MODE`，禁止使用年份、题号、题名、题面原句、附件特征等可定位旧题的信息去搜索历史优秀论文、现成解答或源码；仍允许去题目标识化地搜索通用理论、原始模型文献、官方数据和方法资料。

盲测中一旦意外命中该旧题的历史完整答案，必须立即停止继续读取并标记 `ANSWER_LEAKAGE_DETECTED`；该次严格盲测不能再宣称完全独立。完整规则见 [search-mode-policy.md](search-mode-policy.md)。

搜索模式与后面的“逐题深度求解 / 一次性完整求解”是两个独立选择。

---

## 总体流程

```text
确定联网研究模式
↓
深读题目与附件
↓
第一阶段探索性研究
↓
逐问核心思路与候选方案
↓
基于证据评分并形成整题路线
↓
用户确认路线 + 选择解题模式
↓
A. 逐题深度求解  或  B. 一次性完整求解
↓
原题逐条回查
↓
最终参考论文
↓
四包交付
```

同时遵循：

- [search-mode-policy.md](search-mode-policy.md)
- [exploratory-research.md](exploratory-research.md)
- [solve-modes.md](solve-modes.md)
- [source-verification-policy.md](source-verification-policy.md)
- [output-artifact-policy.md](output-artifact-policy.md)
- [reference-paper-writing.md](reference-paper-writing.md)
- [final-delivery-packaging.md](final-delivery-packaging.md)

---

# 第一阶段：深读题与路线决策

第一阶段先完整理解题面、附件和问题依赖，再做与模型选择有关的探索性研究。

允许使用 Python 做：数据结构检查、缺失/异常、描述统计、必要可视化、趋势/季节性、相关性、baseline、可行域/计算规模、小规模模型前提验证等。

第一阶段不要求生成最终正式代码和最终结果；探索只服务于“理解题目”和“选择路线”。

联网检索必须始终服从已选择的 `LIVE_RESEARCH_MODE` 或 `BLIND_BENCHMARK_MODE`，不得在盲测中为了补证据绕过防泄漏规则。

## 用户看到的输出顺序

每个问题保持：

```text
# 问题一
一句话判断
核心思路
关键探索证据
候选方案
推荐/备用/切换条件
---
# 问题二
...
```

避免深层数字标题和长篇流水账。

所有问题完成后：

```text
各问推荐总览
→ 整题路线
→ 关键文献/数据证据
→ 证据缺口
→ 用户确认路线并选择解题模式
```

候选路线以真正有意义为准，通常 2–3 条，不机械凑数。

状态：`WAITING_FOR_CONFIRMATION`。

---

# 第二阶段前：强制模式选择

如果用户尚未提前指定，AI 必须让用户选择：

### A. 逐题深度求解

推荐用于 Codex、本地执行和正式比赛深挖。

```text
问题1 → 问题2 → ... → 问题n → 全局总结 → 最终参考论文
```

每问都完成模型、Python、实际运行、验证、代码解析、资料/文献和上下问交接。

### B. 一次性完整求解

适合 Chat 模式或队伍前期快速拿到整题参考。

```text
问题1 → 问题2 → ... → 问题n → 全局验证 → 总结 → 最终参考论文
```

不在问题之间暂停，但质量底线与逐题模式相同。

用户没有选择时，AI 不得自行猜测。

---

# 模式 A：逐题深度求解

使用 [../assets/QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md](../assets/QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md)。

进入每个问题前必须重新检查：

- 原题本问要求；
- 公共约束；
- 前面问题的真实结果；
- 上一问传入什么；
- 本问向下一问输出什么；
- 当前新证据是否改变后续模型；
- 是否需要回头修订前面的接口、参数或假设。

每问完整闭环：

`要求回查 → 上下关联探索 → 问题级探索 → 最终模型 → Python → 实际结果 → 验证 → 代码解析 → 本问资料/文献 → 本问答案 → 下一问交接`

默认每问完成后暂停并询问是否继续；若用户明确要求自动连续执行，则可以不停，但必须保留问题级闭环和交接记录。

核心路线被新证据或实测结果推翻时，输出 `ROUTE_REOPEN_REQUIRED`。

---

# 模式 B：一次性完整求解

使用 [../assets/STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md](../assets/STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md)。

按问题依赖连续完成整题，仍必须保留每问模型、Python、真实结果、验证和问题间接口。

该模式更强调速度和整题视角，但不允许降低真实性、代码完整性或文献核验标准。

---

# 原题逐条回查

无论选择 A 或 B，全部问题完成后必须重新读取原题并建立：

| 原题要求 | 对应问题 | 最终答案/结果 | 对应代码/输出 | 是否完整回答 | 备注 |
|---|---|---|---|---|---|

检查是否漏掉：动作词、子要求、边界、单位、指定输出格式和问题间真实传递。

没有完成 Requirement Traceability，不得进入最终论文和 `FINAL_DELIVERY`。

如果当前为 `BLIND_BENCHMARK_MODE`，到这里仍不得自动搜索历史答案。只有全部独立求解结果固定，并且用户明确同意后，才能进入 `POST_SOLUTION_COMPARISON` 搜索历史优秀论文或已有解法进行对照。任何对照后产生的改进必须标记 `POST_HOC_IMPROVEMENT`，不得冒充盲测原始能力。

---

# 最终参考论文与四包交付

完成全部问题、原题回查和全局一致性检查后，才撰写 AI 自己的最终参考论文 `.docx + .pdf`。

随后交付：

```text
题目详解.zip
参考论文.zip
源码.zip
其他.zip
```

参考论文与外部参考文献严格区分；建模图表默认 Python 生成；普通文本交付统一 Markdown。
