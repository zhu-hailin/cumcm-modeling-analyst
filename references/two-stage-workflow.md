# 两阶段赛题工作流

## 开题前：联网研究模式

第一次外部联网前，如果用户未说明，询问一次：实战赛题还是旧题盲测。

- `LIVE_RESEARCH_MODE`：正式比赛正常研究，不主动找现成完整答案。
- `BLIND_BENCHMARK_MODE`：旧题测试防答案泄漏，禁止题号/题名/原文等定位历史解答。

盲测意外命中历史完整答案：`ANSWER_LEAKAGE_DETECTED`。

---

# 赛时协作

完整执行 [competition-collaboration.md](competition-collaboration.md)。

聊天轻、研究深；重要内容沉淀 Markdown；流程作为后台质量约束，不机械播报。

---

## 总体流程

```text
确定联网模式
↓
深读题目与附件
↓
Stage 1 探索性研究
↓
逐问候选与证据评分
↓
整题路线
↓
用户确认 + 选择求解模式
↓
Stage 2：逐题深解 / 一次性完整求解
↓
真实 Python + Visualization System + 验证
↓
原题逐条回查
↓
AI 参考论文
↓
INTERNAL_DELIVERY（内部四包）
↓
队员人工理解、核查并重写论文
↓
FINAL_PAPER_AUDIT
↓
正式比赛：核验当年官方规则
↓
OFFICIAL_SUBMISSION_EXPORT
```

统一遵循：

- [exploratory-research.md](exploratory-research.md)
- [python-visualization-policy.md](python-visualization-policy.md)
- [solve-modes.md](solve-modes.md)
- [source-verification-policy.md](source-verification-policy.md)
- [reference-paper-writing.md](reference-paper-writing.md)
- [final-delivery-packaging.md](final-delivery-packaging.md)
- [official-submission-policy.md](official-submission-policy.md)

---

# Stage 1：深读题与路线决策

完整理解题面、附件和问题依赖，再做会影响模型选择的轻量探索。

可使用 Python 检查数据结构、缺失/异常、趋势、相关性、baseline、可行域和模型前提。

Stage 1 的图主要是 C 级探索图，必须能改变选模、数据判断或风险判断；不提前生产整套论文图。

完整研究写入 Markdown，聊天只简要报告各问推荐、整题路线和最大风险。

---

# Stage 2：正式求解

用户选择：

- 逐题深度求解；
- 一次性完整求解。

两种模式质量底线相同，都必须：

- 真实 Python 实现与运行；
- 各问上下接口；
- 结果验证；
- 根据问题真实需要形成 A/B/C 可视化计划；
- 中文论文候选图默认中文；
- 普通表格采用数据表链路，不无意义截图；
- 更新 `VISUALIZATION_MANIFEST.md`；
- 图表通过 Visual QA；
- 新证据推翻路线时触发 `ROUTE_REOPEN_REQUIRED`。

逐题模式每问完整闭环后再进入“推进 / 有价值扩展研究”阶段闸门。

---

# 原题回查

全部问题完成后重新读取原题并建立 Requirement Traceability。

未覆盖任何动作词、子要求、边界、单位、指定输出或问题间传递，都不得进入参考论文。

---

# AI 参考论文

基于最终模型、真实 Python 结果、`VISUALIZATION_MANIFEST.md` 中最终图表/表格和已核验文献撰写 `.docx + .pdf`。

它属于队伍内部参考成果，禁止直接提交。

---

# INTERNAL_DELIVERY

固定内部四包：

```text
题目详解.zip
参考论文.zip
源码.zip
其他.zip
```

四包用于学习、复核、复现、人工写论文和赛后留档，不等于官方提交。

通过完整性验收后状态：

`INTERNAL_DELIVERY_COMPLETE`

---

# 终稿复审与 OFFICIAL_SUBMISSION_EXPORT

队员手工完成正式论文后，进入 `FINAL_PAPER_AUDIT`，重新对照原题、代码、结果、Manifest、图表和文献审核。

正式比赛通过终稿复审后，再读取当年官方最新规则并执行 `OFFICIAL_SUBMISSION_EXPORT`。

官方文件名、格式、页数、支撑材料和 AI 使用说明格式不得永久写死。
