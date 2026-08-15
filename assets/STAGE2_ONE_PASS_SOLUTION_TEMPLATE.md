# 第二阶段：一次性完整求解

**阶段状态：`STAGE_2_ONE_PASS`**

> 仅在用户明确选择“一次性完整求解”后使用。连续完成整题，不在问题之间暂停，但仍保持各问模型、代码、真实运行、结果、验证和上下问接口完整。

# 路线与探索依据

- 已确认主路线：
- 备用路线：
- 切换条件：
- 第一阶段关键探索证据：
- 已纳入关键参考文献/数据：
- 与第一阶段相比的调整：

---

# 整题模型链

| 问题 | 核心任务 | 最终方法 | 输入 | 输出 | 传给哪一问 |
|---|---|---|---|---|---|

说明共享变量、公共假设和问题依赖。

同时规划一张真实的整题建模框架图，优先使用 Graphviz / Mermaid / Matplotlib patches / NetworkX 等确定性方式生成，不使用生成式 AI 图片代替模型流程图。

---

# 每个实际问题的完整闭环

问题一、问题二直到问题 n 均按实际题面继续，不固定三问。每问至少完成：

1. 原题要求与输出；
2. 前后问接口；
3. 变量、参数、假设、公式和约束；
4. 必要探索与路线复核；
5. 图前证据契约；
6. A/B/C 可视化计划与结果表计划；
7. Python 正式实现；
8. 真实运行并写入 Run Ledger；
9. 明确 `FINAL_RUN_ID`；
10. 从 Final/Validation Run 生成最终结果、图表和表格；
11. Visual QA；
12. 模型验证；
13. 本问直接答案；
14. 向后一问交接。

任何新证据推翻路线时触发 `ROUTE_REOPEN_REQUIRED`，不得因为一次性模式就硬跑到底。

---

# 模型运行账本

完整遵循 [../references/model-run-ledger.md](../references/model-run-ledger.md)。

维护：

```text
其他/运行与实验/RUN_LEDGER.md
```

每问最终结果都必须绑定：

```text
FINAL_RUN_ID = Rxxx
```

最终数字、排名、预测、路径、参数、图表和表格不得从旧截图、旧 CSV、聊天记录或 `SUPERSEDED` 运行中手抄。

如果新运行替代旧结果，应同步更新：

`Run Ledger → Visualization Manifest → 教程 → 参考论文 → 最终结论`

随机算法还应记录种子策略、重复次数和代表结果选择规则，不得只挑最好的一次冒充稳定表现。

---

# 全局 Python Visualization System

完整遵循：

- [../references/python-visualization-policy.md](../references/python-visualization-policy.md)
- [../references/figure-evidence-contract.md](../references/figure-evidence-contract.md)

每张正式 A/B 级图在写绘图代码前先明确：

```text
核心结论
Hero evidence
Supporting evidence
每个 panel 的唯一任务
源数据 / Run ID
不确定性定义
评阅风险
```

禁止按“一个表一张图”机械绘图；禁止为了套模板静默删数据或只展示有利结果。

每问根据真实需要规划：

```text
A 级核心结果图
B 级诊断/验证图
C 级探索图
核心结果表
完整明细表
```

没有需求的类别写“无”，禁止为凑数量生成图表。

推荐统一目录：

```text
outputs/
├── figures/
│   ├── paper/
│   ├── validation/
│   └── exploration/
├── tables/
│   ├── paper/
│   └── full/
└── intermediate/
```

维护：

```text
VISUALIZATION_MANIFEST.md
```

至少记录：

| 图号 | 文件 | 问题 | Run ID | 等级 | 数据源 | 生成代码 | 支撑结论 | 进入论文 |
|---|---|---|---|---|---|---|---|---|

普通 DataFrame 优先导出 CSV/XLSX，论文使用原生表格，不默认截图成 PNG。

中文论文候选图默认使用中文标签，并执行字体自动回退、论文尺寸可读性和逐 panel Visual QA。

GA / SA / PSO / ACO / Tabu Search 等启发式算法若支撑结论，应保存真实迭代历史，并提供适当的收敛或重复实验稳定性证据。

---

# 全局验证

按题目适用情况完成：

- 单位、量纲、边界与约束检查；
- baseline 比较；
- 误差分析；
- 敏感性分析；
- 鲁棒性/压力场景；
- 替代模型；
- 随机算法重复性；
- 图表是否真实支持正文结论；
- 数据排除是否有明确理由与记录；
- 同类图中的不确定性定义是否一致。

---

# 教程与代码解析

对每个实际问题生成 `.md` 教程，与最终源码和 Final Run 一致，包括模型思路、公式、数据、代码路径、关键函数、运行、输出、图表解释、验证和常见问题。

公式遵循 `equation-rendering-policy.md`；图表遵循 `python-visualization-policy.md` 与 `figure-evidence-contract.md`。

---

# 资料与参考文献

按问题整理真正使用的文献、数据和参数来源，并执行链接/下载核验。不得编造 DOI、URL、下载状态或文献内容。

---

# 原题逐条回查

全部问题完成后重新读取原题：

| 原题要求 | 对应问题 | 最终答案/结果 | Final Run/代码/输出 | 是否完整回答 | 备注 |
|---|---|---|---|---|---|

没有完成该表，不得进入最终参考论文和内部交付。

---

# 最终一致性扫描

在写参考论文前执行 [../references/final-consistency-sweep.md](../references/final-consistency-sweep.md)，至少核对：

`Final Run ↔ 结果表 ↔ Visualization Manifest ↔ 教程 ↔ 各问最终答案`

存在重大冲突时标记：

`CROSS_ARTIFACT_CONSISTENCY_FAILED`

修复后再进入论文。

---

# 最终参考论文

执行 [../references/reference-paper-writing.md](../references/reference-paper-writing.md)，基于最终路线、Final/Validation Run、最终 Manifest 选出的真实图表/表格和已核验参考文献重新撰写完整成果论文。

默认生成：

```text
数学建模参考论文.docx
数学建模参考论文.pdf
```

论文生成后再次执行最终一致性扫描。

---

# INTERNAL_DELIVERY：内部四包

执行：

- [../references/final-delivery-packaging.md](../references/final-delivery-packaging.md)
- [../references/delivery-integrity-policy.md](../references/delivery-integrity-policy.md)

生成：

1. `题目详解.zip`
2. `参考论文.zip`
3. `源码.zip`
4. `其他.zip`

这些是队伍内部学习、复核、复现和人工写论文使用的完整成果，不等于官方比赛提交文件。

通过内部交付验收后标记：`INTERNAL_DELIVERY_COMPLETE`。

---

# OFFICIAL_SUBMISSION_EXPORT

只有正式比赛需要官方导出时，进一步执行 [../references/official-submission-policy.md](../references/official-submission-policy.md)。

先核验当年最新官方规则，再从已经核验的内部成果中导出实际需要上传的文件。禁止长期写死某一年的论文、支撑材料或 AI 使用说明格式。
