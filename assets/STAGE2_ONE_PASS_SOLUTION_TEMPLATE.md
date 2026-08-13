# 第二阶段：一次性完整求解

**阶段状态：`STAGE_2_ONE_PASS`**

> 仅在用户明确选择“一次性完整求解”后使用。连续完成整题，不在问题之间暂停，但仍保持各问模型、代码、结果、验证和上下问接口完整。

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

# 问题一

依次完成：

- 原题要求与输出；
- 变量、参数与假设；
- 模型、公式、目标函数/核心关系、约束；
- 本问可视化计划（A/B/C 图 + 核心表/明细表）；
- Python 实现；
- 实际运行结果、图表和表格；
- Visual QA；
- 验证；
- 向后续问题传递的结果。

---

# 问题二

使用同样结构，并明确实际使用了哪些前置问题结果。

---

# 后续问题

按实际题面继续，不固定三问。

---

# 全局 Python Visualization System

完整遵循 [../references/python-visualization-policy.md](../references/python-visualization-policy.md)。

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

并维护：

```text
VISUALIZATION_MANIFEST.md
```

至少记录图号、文件、问题、等级、数据源、生成代码、图表目的和是否进入论文。

普通 DataFrame 优先导出 CSV/XLSX，论文使用原生表格，不默认截图成 PNG。

中文论文候选图默认使用中文标签，并执行字体自动回退、论文尺寸可读性和 Visual QA。

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
- 图表是否真实支持正文结论。

如果正式运行结果推翻第一阶段路线，应触发 `ROUTE_REOPEN_REQUIRED`。

---

# 教程与代码解析

对每个实际问题生成 `.md` 教程，与最终源码一致，包括模型思路、公式、数据、代码路径、关键函数、运行、输出、图表解释、验证和常见问题。

公式遵循 `equation-rendering-policy.md`；图表遵循 `python-visualization-policy.md`。

---

# 资料与参考文献

按问题整理真正使用的文献、数据和参数来源，并执行链接/下载核验。不得编造 DOI、URL、下载状态或文献内容。

---

# 原题逐条回查

全部问题完成后重新读取原题：

| 原题要求 | 对应问题 | 最终答案/结果 | 对应代码/输出 | 是否完整回答 | 备注 |
|---|---|---|---|---|---|

没有完成该表，不得进入最终参考论文和内部交付。

---

# 最终参考论文

执行 [../references/reference-paper-writing.md](../references/reference-paper-writing.md)，基于最终路线、实际 Python 结果、最终 Manifest 选出的真实图表/表格和已核验参考文献重新撰写完整成果论文。

默认生成：

```text
数学建模参考论文.docx
数学建模参考论文.pdf
```

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

通过内部交付验收后标记：

`INTERNAL_DELIVERY_COMPLETE`

---

# OFFICIAL_SUBMISSION_EXPORT

只有正式比赛需要官方导出时，进一步执行：

[../references/official-submission-policy.md](../references/official-submission-policy.md)

先核验当年最新官方规则，再从已经核验的内部成果中导出实际需要上传的文件。禁止长期写死某一年的论文、支撑材料或 AI 使用说明格式。
