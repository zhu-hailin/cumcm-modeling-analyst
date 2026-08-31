# 图表与文档输出规范

本规范适用于赛题分析、Python 实现、教程、论文和内部交付。

科学可视化详细规则遵循：

- `python-visualization-policy.md`
- `figure-evidence-contract.md`
- `equation-rendering-policy.md`

Codex 本地目录遵循：

- `local-workspace-policy.md`

---

## 1. 图片生成工具边界

默认禁止使用 AI 图片生成工具生成数学建模中的：

- 统计图；
- 预测图；
- 误差图；
- 热力图；
- 路径图；
- 网络图；
- Pareto 前沿；
- 仿真图；
- 收敛图；
- 模型流程图；
- 其他依赖真实数据、模型结果或确定结构的图。

这些图必须由 Python、Graphviz、Mermaid、NetworkX、GeoPandas 等确定性工具，根据真实数据和实际运行结果生成。

只有用户明确要求风格化宣传图、封面或非科学结果类视觉素材时，才允许使用生成式图片工具。

禁止用生成式图片代替真实统计结果、工程结构、地理路线或整题模型框架。

---

## 2. Codex 输出目录

Codex 单赛题工作区中，正式输出集中到：

```text
04_results/
├─ figures/
│  ├─ q1/
│  ├─ q2/
│  ├─ qN/
│  └─ final/
├─ tables/
│  ├─ q1/
│  ├─ q2/
│  ├─ qN/
│  └─ final/
├─ data/
│  ├─ q1/
│  ├─ q2/
│  ├─ qN/
│  └─ final/
├─ logs/
└─ VISUALIZATION_MANIFEST.md
```

没有对应内容时不必提前创建空目录。

规则：

- 不把结果写进 `03_code/`；
- 不把图、CSV、模型文件散落在项目根目录；
- 临时预览、测试图和转换缓存进入 `99_temp/`；
- 最终成果不能只存在于 `99_temp/`；
- 新 Run 替换旧结果后，旧产物应明确归档或标记过期。

其他环境可使用等价目录，但必须维持相同分层和可追溯性。

---

## 3. Python 科学可视化

图表目标是：

- 论文可用；
- 解释有效；
- 可以复现；
- 能追到真实 Run 和数据。

采用 A/B/C 分级：

- **A 级**：核心结果图，回答“最终得到了什么”；
- **B 级**：诊断/验证图，回答“为什么相信这个结果”；
- **C 级**：探索性图，用于 EDA、筛选和调试。

不规定每问固定图数。删除某图不影响理解、验证或决策时，该图通常不该保留。

正式 A/B 级图先建立 Figure Contract，再写代码。

---

## 4. 中文与图表质量

中文论文候选图默认使用中文：

- 标题；
- 坐标轴；
- 图例；
- 关键注释；
- 分类标签；
- 单位。

国际通用模型和指标缩写可以保留英文。

中文字体不能只硬编码 `SimHei`，应检测当前系统真实可用字体并回退。

进入论文的图必须通过：

- 中文字体和负号检查；
- 坐标轴、单位、图例完整性；
- 遮挡、裁切、重叠和空白图检查；
- 最终 A4 插图尺寸可读性；
- 数据与 `FINAL_RUN_ID` 一致性；
- 逐 panel 证据作用检查。

失败状态包括：

```text
CHINESE_FONT_RENDERING_FAILED
PAPER_FIGURE_READABILITY_FAILED
VISUALIZATION_QA_FAILED
```

---

## 5. 图表格式

正式论文候选图建议同时保存：

```text
PNG + SVG
```

必要时增加 PDF。

要求：

- PNG 默认不少于 300 DPI；
- 关键线图、路径图可使用 450–600 DPI；
- SVG/PDF 尽量保留可编辑文字；
- 使用合理的紧致边界；
- 标题、图例、坐标轴和注释不被裁切；
- 文件真实存在且非 0 字节。

正式图默认放在 `04_results/figures/qN/`，整题最终候选放 `04_results/figures/final/`。

---

## 6. 结果表格

普通数值结果优先：

```text
Python DataFrame
→ CSV / XLSX
→ Word 原生表格
```

正式结果表放到：

```text
04_results/tables/qN/
```

整题汇总表放：

```text
04_results/tables/final/
```

不要默认把 DataFrame 截图为 PNG。

只有具有真实二维结构的数据才优先使用 heatmap，例如：

- 相关矩阵；
- 混淆矩阵；
- 敏感性矩阵；
- 场景矩阵；
- 分配矩阵。

长明细表保存在结果目录，不塞进论文正文。

---

## 7. 数值与跨问传递结果

最终数值、参数、路径、预测序列、模型对象和跨问接口文件放到：

```text
04_results/data/qN/
```

整题最终汇总放到：

```text
04_results/data/final/
```

每个重要文件应能追到：

- 输入数据；
- `03_code/qN/` 中的生成代码；
- `FINAL_RUN_ID`；
- 使用它的后续问题或论文位置。

---

## 8. Visualization Manifest

Codex 默认维护：

```text
04_results/VISUALIZATION_MANIFEST.md
```

至少记录：

| 图号 | 文件 | 问题 | Run ID | 等级 | 数据源 | 生成代码 | 图表目的/支撑结论 | 是否进入论文 |
|---|---|---|---|---|---|---|---|---|

论文生成和终稿复审都应据此核对最终图，防止：

- 错图；
- 旧图；
- 模型已换但图未换；
- 图中数字与正文不一致；
- 图无法追到真实运行。

---

## 9. 启发式算法

GA、SA、PSO、ACO、Tabu Search 等迭代算法若支撑最终结论，应保存真实迭代历史，并在适合时生成收敛曲线或重复实验稳定性证据。

没有收敛、重复实验或稳定性证据却声称“算法稳定”时，标记：

```text
OPTIMIZATION_CONVERGENCE_EVIDENCE_MISSING
```

运行日志和重复实验记录放在 `04_results/logs/`。

---

## 10. 文档格式

AI 创建的普通文本型文档统一使用 UTF-8 Markdown，例如：

- `README.md`；
- `02_analysis/*.md`；
- 数据来源说明；
- 文献账本；
- Run Ledger；
- Visualization Manifest；
- 审核报告；
- 提交检查表。

最终参考论文 `.docx + .pdf` 是明确例外。

官方提交文件也属于例外，其格式由当年官方规则决定。

---

## 11. AI-friendly Markdown

Markdown 应方便队员和后续 Agent 接手：

- 标题层级稳定；
- 公式使用规范 LaTeX；
- 代码块注明语言；
- 路径、函数、参数和字段使用反引号；
- 表格不过度复杂；
- 假设、风险和待核验项分开；
- 核心模型不能只靠图片才能理解；
- 文档中的路径、命令和输出必须与真实工作区一致。

---

## 12. 最终检查

进入内部交付前检查：

- [ ] 用户未要求时，没有用生成式图片代替科学图表；
- [ ] Stage 1 只保留影响选模的必要探索图；
- [ ] 正式图来自 Python 或确定性工具；
- [ ] Codex 输出集中在 `04_results/`；
- [ ] 正式图通过 Figure Contract 和逐 panel QA；
- [ ] 中文、单位、字体和最终尺寸正常；
- [ ] 普通结果表没有全部截图；
- [ ] 启发式算法有必要的收敛/稳定性证据；
- [ ] `VISUALIZATION_MANIFEST.md` 能追到 Run、代码和数据；
- [ ] 最终论文图全部来自最终运行；
- [ ] Markdown、DOCX 和 PDF 公式规则通过；
- [ ] 根目录、`03_code/` 和 `99_temp/` 没有散落唯一正式成果。
