# 两阶段赛题工作流

## 开题前：先确定联网研究模式

在第一次外部联网检索之前，如果用户尚未明确说明，先自然询问一次：

> 这是 **A. 实战赛题**，还是 **B. 旧题盲测**？

- **实战赛题**：进入 `LIVE_RESEARCH_MODE`，保留正常联网研究能力，可搜索论文、数据、参数、官方资料、相似案例、算法与代码文档，但不得以寻找当前比赛现成完整答案为目的。
- **旧题盲测**：进入 `BLIND_BENCHMARK_MODE`，禁止使用年份、题号、题名、题面原句、附件特征等可定位旧题的信息去搜索历史优秀论文、现成解答或源码；仍允许去题目标识化地搜索通用理论、原始模型文献、官方数据和方法资料。

盲测中一旦意外命中该旧题的历史完整答案，必须立即停止继续读取并标记 `ANSWER_LEAKAGE_DETECTED`。

---

# 赛时协作原则

完整执行 [competition-collaboration.md](competition-collaboration.md)。

底层研究流程保持严谨，但聊天窗口默认简洁、口语化、像队友交流。

重要内容优先写入 Markdown，聊天只说：

- 我刚做了什么；
- 最重要的真实发现；
- 这个发现有什么用；
- 我建议下一步怎么走。

不要把状态机、检查表和完整研究报告机械展示给用户。

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
每个完整阶段结束后：推进 / 有价值的扩展研究
↓
原题逐条回查
↓
最终参考论文
↓
四包交付
```

同时遵循：

- [competition-collaboration.md](competition-collaboration.md)
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

允许使用 Python 做数据结构检查、缺失/异常、描述统计、必要可视化、趋势/季节性、相关性、baseline、可行域/计算规模、小规模模型前提验证等。

第一阶段不要求生成最终正式代码和最终结果；探索只服务于理解题目和选择路线。

联网检索必须始终服从已选择的 `LIVE_RESEARCH_MODE` 或 `BLIND_BENCHMARK_MODE`。

## 完整研究与聊天分离

第一阶段完整研究应写入 Markdown，例如：

```text
其他/赛时协作/第一阶段_完整研究.md
```

其中保存：

- 各问真正目标；
- 探索证据；
- 候选模型；
- 评分；
- 首选/备用/切换条件；
- 整题路线；
- 文献、数据、参数与证据缺口。

聊天窗口默认只简要告诉队员：

```text
问题1推荐 XXX；问题2推荐 XXX；……
整题我更倾向路线 A，最大风险是 XXX。
完整研究已经整理进 Markdown。
```

根据真实结果自然表达，不机械照抄。

候选路线以真正有意义为准，通常 2–3 条，不机械凑数。

状态可内部记为 `WAITING_FOR_CONFIRMATION`，但默认不需要把状态名显示给用户。

---

# 第二阶段前：模式选择

如果用户尚未提前指定，AI 用简短口语让用户选择：

### A. 逐题深度求解

推荐用于 Codex、本地执行和正式比赛深挖。

### B. 一次性完整求解

适合 Chat 模式或队伍前期快速拿到整题参考。

用户没有选择时不要自行猜测；已经明确时不要重复追问。

---

# 模式 A：逐题深度求解

使用 [../assets/QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md](../assets/QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md)。

进入每个问题前必须重新检查原题本问要求、公共约束、前面真实结果、上下问接口和新证据对路线的影响。

每问完整闭环：

`要求回查 → 上下关联探索 → 问题级探索 → 最终模型 → Python → 实际结果 → 验证 → 代码解析 → 本问资料/文献 → 本问答案 → 下一问交接`

核心路线被新证据或实测结果推翻时，输出 `ROUTE_REOPEN_REQUIRED`。

## 问题完成后的阶段闸门

核心闭环完成之后，再决定：

- 直接推进；
- 或做一轮真正有价值的扩展研究。

扩展研究必须明确：

1. 研究什么；
2. 为什么值得；
3. 可能改变什么决策；
4. 什么时候停。

没有明确价值就不要继续。

扩展研究允许：

- `MEANINGFUL_FINDING`
- `NO_MEANINGFUL_FINDING`
- `INCONCLUSIVE`

宁愿没有研究发现，也禁止制造垃圾结果。

完成后用几句自然口语告诉队员结果、意义和建议，不把全部实验贴进聊天。

---

# 模式 B：一次性完整求解

使用 [../assets/STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md](../assets/STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md)。

按问题依赖连续完成整题，仍必须保留每问模型、Python、真实结果、验证和问题间接口。

该模式不需要频繁停下来，但遇到真正会改变路线、重大风险、异常结果时，应主动和队员交流。

---

# 原题逐条回查

无论选择 A 或 B，全部问题完成后必须重新读取原题并建立：

| 原题要求 | 对应问题 | 最终答案/结果 | 对应代码/输出 | 是否完整回答 | 备注 |
|---|---|---|---|---|---|

检查动作词、子要求、边界、单位、指定输出格式和问题间真实传递。

没有完成 Requirement Traceability，不得进入最终论文和 `FINAL_DELIVERY`。

如果当前为 `BLIND_BENCHMARK_MODE`，到这里仍不得自动搜索历史答案。只有独立求解结果固定且用户明确同意后，才能进入 `POST_SOLUTION_COMPARISON`。

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
