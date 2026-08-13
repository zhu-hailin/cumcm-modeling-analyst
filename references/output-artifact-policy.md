# 图表与文档输出规范

本规范适用于赛题分析、第二阶段求解、Python 实现、教程编写、最终论文和内部四包交付。

科学可视化的详细执行规则统一遵循：

- [python-visualization-policy.md](python-visualization-policy.md)
- [equation-rendering-policy.md](equation-rendering-policy.md)

## 1. 图片生成工具使用边界

默认禁止使用 AI 图片生成工具或文生图工具生成数学建模过程中的统计图、预测图、误差图、热力图、路径图、网络图、Pareto 前沿、仿真图、模型流程图或其他结果图。

这些图默认必须由 Python 根据真实数据、真实模型结果或确定结构生成。

只有用户明确提出需要生成式图片、风格化设计或非科学结果类视觉素材时，才允许使用图片生成工具。

禁止用生成式图片替代真实统计结果、实验结果、工程结构、地理路线或模型框架。

## 2. Python 科学可视化

图表目标是“论文可用 + 解释有效 + 可复现”，不是数量越多越好。

统一采用 A/B/C 分级：

- A：核心结果图，回答“最终得到了什么”；
- B：诊断/验证图，回答“为什么相信这个结果”；
- C：探索性图，用于 EDA、模型筛选和调试。

不规定每问固定图数。删除某图不影响理解、验证或决策时，该图通常不应保留。

中文论文中的论文候选图默认使用中文标题、坐标轴、图例、注释和分类标签；国际通用模型缩写和指标可保留英文。单位必须完整。

中文字体不得只硬编码 `SimHei`，应检测系统真实可用字体并回退；出现中文乱码时标记 `CHINESE_FONT_RENDERING_FAILED`。

进入论文的图必须通过：

- `PAPER_FIGURE_READABILITY_FAILED` 检查；
- `VISUALIZATION_QA_FAILED` 检查；
- 数据、代码、问题和结论可追溯检查。

## 3. 图表与表格输出

正式图建议保存 PNG + SVG，必要时增加 PDF；PNG 默认不少于 300 DPI。

推荐目录：

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

普通数值结果表优先：

```text
DataFrame → CSV/XLSX → Word 原生表格
```

不要默认把 DataFrame 截图成 PNG。

只有具有明显二维结构意义的矩阵结果才优先可视化为 heatmap，例如相关矩阵、混淆矩阵、敏感性矩阵、场景矩阵和分配矩阵。

结果表格按：核心结果表 / 模型参数表 / 验证表 / 完整明细表分级；长表进入 `outputs/tables/full/`，不塞进论文正文。

## 4. Visualization Manifest

第二阶段应维护 `VISUALIZATION_MANIFEST.md`，至少记录：图号、文件、问题、等级、数据源、生成代码、图表目的/支撑结论、是否进入论文。

论文生成和终稿复审都应以 Manifest 核对最终图，防止错图、旧图、模型已换但图未换、图中数字与正文不一致。

## 5. 启发式算法

GA、SA、PSO、ACO、Tabu Search 等迭代启发式算法若支撑最终结论，应保存真实迭代历史，并在适合时生成收敛曲线或重复实验稳定性证据。

没有任何收敛、重复实验或稳定性证据却声称“算法稳定”时，标记：

`OPTIMIZATION_CONVERGENCE_EVIDENCE_MISSING`

## 6. 文档格式总规则

AI 自行创建的普通文本型文档统一使用 UTF-8 Markdown，包括教程、README、AI 使用说明、建模决策、路线变更、文献账本、数据来源、链接核验、问题反馈、环境说明、Visualization Manifest 等。

最终参考论文 `.docx + .pdf` 是明确例外。

官方竞赛提交文件也属于例外，其格式由当年官方规则决定，详见 [official-submission-policy.md](official-submission-policy.md)。

## 7. AI-friendly Markdown 标准

Markdown 应便于人和后续 Agent 使用：

- 稳定的标题层级；
- 公式使用规范 LaTeX；
- 代码块标明语言；
- 路径、函数、参数和字段使用反引号；
- 表格不过度复杂；
- 长流程优先列表或 Mermaid；
- 假设、风险、待核验项分节；
- 核心模型不能依赖图片才能理解；
- 文档路径、命令和输出与真实交付一致。

## 8. 最终检查

进入内部最终交付前检查：

- 用户未要求时是否未用 AI 图片生成工具代替科学图表；
- Stage 1 是否仍只保留影响选模的必要探索图；
- Stage 2 是否形成合理可视化计划；
- 中文图表和字体回退是否正常；
- 正式图是否通过 Visual QA 与论文尺寸可读性检查；
- 普通结果表是否使用原生表格链路而非全部截图；
- 启发式算法是否有必要的收敛/稳定性证据；
- `VISUALIZATION_MANIFEST.md` 是否可追溯到真实数据和代码；
- 最终论文图是否全部来自最终 Python 输出；
- Markdown、DOCX/PDF 公式规则是否通过。
