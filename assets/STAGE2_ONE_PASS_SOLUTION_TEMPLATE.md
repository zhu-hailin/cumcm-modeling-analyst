# 第二阶段：一次性完整求解

**阶段状态：`STAGE_2_ONE_PASS`**

> 仅在用户明确选择“一次性完整求解”后使用。连续完成整题，不在问题之间常规暂停，但每问仍要保留模型、代码、真实运行、结果、验证和上下问接口。

---

# Codex 工作区映射

Codex 中先加载 `references/local-workspace-policy.md`，并在单赛题根目录工作：

```text
00_problem/      # 原题、官方附件、官方模板
01_data/         # raw / processed / external
02_analysis/     # problem_analysis、assumptions、symbols、model_plan、逐问教程
03_code/         # common、q1、q2、qN、run_all.py
04_results/      # figures、tables、data、logs
05_paper/        # outline、草稿、终稿
06_submission/   # 内部四包与官方提交候选
07_references/   # 论文、网站和笔记
99_temp/         # 临时文件
```

用户已有合理结构或指定其他路径时，以用户要求为准。不要再创建额外 `modeling_workspace/` 或顶层 `deliverables/`。

---

# 路线与探索依据

- 已确认主路线：
- 备用路线：
- 切换条件：
- 第一阶段关键探索证据：
- 已纳入关键参考文献/数据：
- 外部现实数据缺口及处理：
- 与第一阶段相比的调整：

这些内容同步到 `02_analysis/model_plan.md`。

---

# 整题模型链

| 问题 | 核心任务 | 最终方法 | 输入 | 输出 | 传给哪一问 |
|---|---|---|---|---|---|

说明共享变量、公共假设和问题依赖，并同步：

- 统一假设 → `02_analysis/assumptions.md`
- 统一符号 → `02_analysis/symbols.md`
- 题意与依赖 → `02_analysis/problem_analysis.md`

同时规划一张真实的整题建模框架图，使用 Graphviz、Mermaid、Matplotlib patches 或 NetworkX 等确定性方式，不使用生成式图片代替。

---

# 每个实际问题的完整闭环

问题一、问题二直到问题 n 均按实际题面继续，不固定三问。每问至少完成：

1. 原题要求与输出；
2. 前后问接口；
3. 变量、参数、假设、公式和约束；
4. 必要探索与路线复核；
5. 现实数据缺口检索和来源核验；
6. 图前证据契约；
7. A/B/C 可视化与结果表计划；
8. `03_code/qN/` 中的正式 Python；
9. 真实运行并写入 `04_results/logs/RUN_LEDGER.md`；
10. 明确 `FINAL_RUN_ID`；
11. 从 Final/Validation Run 生成 `04_results/` 中的结果、图表和表格；
12. Visual QA；
13. 模型验证；
14. 生成 `02_analysis/qN_solution.md`；
15. 本问直接答案；
16. 向后一问交接。

任何新证据推翻路线时触发 `ROUTE_REOPEN_REQUIRED`，不得因为一次性模式就硬跑到底。

一次性模式不要求每问常规进入 `QUESTION_PLAN_CONFIRMATION`；但出现关键数据缺口、路线失效、需要用户决定的假设或外部资料冲突时，仍要暂停沟通。

---

# 正式代码与总入口

正式代码：

```text
03_code/
├─ common/
├─ q1/
├─ q2/
├─ qN/
└─ run_all.py
```

要求：

- 各问代码职责清楚；
- 公共逻辑进入 `03_code/common/`；
- `run_all.py` 按问题依赖顺序运行最终流程；
- 不覆盖 `01_data/raw/`；
- 清洗数据写入 `01_data/processed/`；
- 网络补充数据写入 `01_data/external/`；
- 正式输出集中写入 `04_results/`；
- 临时测试和转换文件进入 `99_temp/`；
- 不硬编码本机私人绝对路径。

---

# 模型运行账本

完整遵循 `references/model-run-ledger.md`。

维护：

```text
04_results/logs/
├─ RUN_LEDGER.md
└─ runs/
   ├─ R001.md
   └─ ...
```

每问最终结果都必须绑定：

```text
FINAL_RUN_ID = Rxxx
```

最终数字、排名、预测、路径、参数、图表和表格不得从旧截图、旧 CSV、聊天记录或 `SUPERSEDED` 运行中手抄。

如果新运行替代旧结果，同步更新：

```text
Run Ledger
→ 04_results
→ Visualization Manifest
→ 02_analysis/qN_solution.md
→ 05_paper
→ 最终结论
```

随机算法应记录种子策略、重复次数和代表结果选择规则，不得只挑最好的一次冒充稳定表现。

---

# Python Visualization System

完整遵循：

- `references/python-visualization-policy.md`
- `references/figure-evidence-contract.md`

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

Codex 默认结果目录：

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

每问根据真实需要规划：

- A 级核心结果图；
- B 级诊断/验证图；
- C 级探索图；
- 核心结果表；
- 完整明细表；
- 数值与跨问传递结果。

没有需求的类别写“无”，禁止为凑数量生成图表。

`VISUALIZATION_MANIFEST.md` 至少记录：

| 图号 | 文件 | 问题 | Run ID | 等级 | 数据源 | 生成代码 | 支撑结论 | 进入论文 |
|---|---|---|---|---|---|---|---|---|

普通 DataFrame 优先导出 CSV/XLSX，论文使用原生表格，不默认截图成 PNG。

中文论文候选图默认使用中文标签，并执行字体回退、论文尺寸可读性和逐 panel Visual QA。

GA、SA、PSO、ACO、Tabu Search 等启发式算法若支撑结论，应保存真实迭代历史，并提供适当的收敛或重复实验稳定性证据。

---

# 全局验证

按题目适用情况完成：

- 单位、量纲、边界与约束；
- baseline 比较；
- 误差分析；
- 敏感性分析；
- 鲁棒性/压力场景；
- 替代模型；
- 随机算法重复性；
- 图表是否真实支持正文结论；
- 数据排除是否有明确理由与记录；
- 同类图中的不确定性定义是否一致；
- 各问传递数据与实际文件是否一致。

---

# 教程与代码解析

每个实际问题生成：

```text
02_analysis/q1_solution.md
02_analysis/q2_solution.md
...
```

教程必须与最终源码和 Final Run 一致，包括：

- 题意；
- 选模理由；
- 数据与来源；
- 公式与假设；
- `03_code/qN/` 的代码结构；
- 运行命令；
- `FINAL_RUN_ID`；
- `04_results/` 中的输出；
- 图表解释；
- 验证；
- 常见错误；
- 向下一问传递什么。

公式遵循 `equation-rendering-policy.md`。

---

# 资料与参考文献

实际查阅的资料放到：

```text
07_references/
├─ papers/
├─ websites.md
└─ notes.md
```

按问题记录真正使用的文献、现实数据和参数来源，并执行链接/下载核验。不得编造 DOI、URL、下载状态、数据或文献内容。

---

# 原题逐条回查

全部问题完成后重新读取 `00_problem/problem.pdf` 和官方附件：

| 原题要求 | 对应问题 | 最终答案/结果 | Final Run/代码/输出 | 是否完整回答 | 备注 |
|---|---|---|---|---|---|

没有完成该表，不得进入参考论文和内部交付。

---

# 最终一致性扫描

写参考论文前执行 `final-consistency-sweep.md`，核对：

```text
00_problem
↔ 01_data
↔ 02_analysis
↔ 03_code
↔ 各问 Final Run
↔ 04_results
↔ 各问教程
```

存在重大冲突时标记：

```text
CROSS_ARTIFACT_CONSISTENCY_FAILED
```

修复后再进入论文。

---

# 论文

使用：

```text
05_paper/
├─ outline.md
├─ draft.docx
├─ final.docx
└─ final.pdf
```

AI 首次生成的是内部参考稿，不得直接冒充队员最终参赛论文。`final.docx` 和 `final.pdf` 只在队员人工重写、核查并确认进入终稿阶段后使用。

论文基于 Final/Validation Run、最终 Manifest、真实图表/表格和已核验文献。论文生成或重大修改后再次执行一致性扫描。

---

# INTERNAL_DELIVERY

执行：

- `references/final-delivery-packaging.md`
- `references/delivery-integrity-policy.md`

未指定位置时保存：

```text
06_submission/internal_delivery/
├─ 题目详解.zip
├─ 参考论文.zip
├─ 源码.zip
└─ 其他.zip
```

这些是队伍内部学习、复核、复现和人工写论文使用的成果，不等于官方比赛提交文件。

通过内部交付验收后标记：

```text
INTERNAL_DELIVERY_COMPLETE
```

---

# OFFICIAL_SUBMISSION_EXPORT

正式比赛需要官方导出时，执行 `official-submission-policy.md`。

默认候选目录：

```text
06_submission/
├─ paper.pdf
├─ source_code.zip
└─ checklist.md
```

但必须先核验当年最新官方规则。禁止长期写死某一年的文件名、页数、支撑材料或 AI 使用说明格式。
