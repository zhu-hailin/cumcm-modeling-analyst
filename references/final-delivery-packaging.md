# INTERNAL_DELIVERY：内部四包与 ZIP 打包规范

## 目标

第二阶段完成整题建模、Python 实现、运行验证、科学可视化、逐问教程与 AI 参考论文后，先进入队伍内部成果交付：

```text
INTERNAL_DELIVERY
```

内部固定四包：

```text
题目详解.zip
参考论文.zip
源码.zip
其他.zip
```

这些文件用于队伍内部学习、审核、复现、人工重写论文、结果保存和终稿复审，**不等同于官方比赛提交格式**。

正式比赛需要上传官方文件时，必须在内部成果完成并经人工终审后，再执行 [official-submission-policy.md](official-submission-policy.md)。

按需遵循：`delivery-integrity-policy.md`、`output-artifact-policy.md`、`python-visualization-policy.md`、`figure-evidence-contract.md`、`model-run-ledger.md`、`reference-paper-writing.md`、`equation-rendering-policy.md`、`source-verification-policy.md`、`final-consistency-sweep.md`。

---

## 0. 环境感知交付

### LOCAL_WORKSPACE_DELIVERY

Codex / Claude Code / 本地 Agent 工作时，项目根目录中的真实成果目录是主成果，ZIP 是打包副本。

推荐：

```text
<project-root>/deliverables/
├── 题目详解/
├── 参考论文/
├── 源码/
├── 其他/
├── 题目详解.zip
├── 参考论文.zip
├── 源码.zip
└── 其他.zip
```

用户指定输出目录时以用户目录为准。

### CHAT_ARTIFACT_DELIVERY

Chat / 云端附件交付时，ZIP 和独立下载文件必须通过跨平台预检。中文 ZIP entry 无法稳定验证时才回退 ASCII-safe 路径，并用 `README.md / MANIFEST.md` 保留中文映射。

---

## 1. 题目详解.zip

推荐源目录：

```text
题目详解/
├── 00_赛题总览.md
├── 问题1/问题1_完整教程.md
├── 问题2/问题2_完整教程.md
└── ...
```

每问教程至少包含：题意、输入输出、变量单位、选模理由、公式与解释、数据处理、算法、前后问衔接、源码路径、Final Run、运行命令、实际输出、图表/表格解释、验证、常见错误和论文表达。

教程中的最终数字和图表必须能追到对应 `FINAL_RUN_ID`。

公式遵循 [equation-rendering-policy.md](equation-rendering-policy.md)。

---

## 2. 参考论文.zip

默认：

```text
参考论文/
├── 数学建模参考论文.docx
└── 数学建模参考论文.pdf
```

用户提供官方模板时按模板生成。

论文必须基于最终锁定路线、Final/Validation Run、最终图表/表格和已核验参考文献，且公式真正渲染。

论文中的图必须来自最终 `VISUALIZATION_MANIFEST.md` 对应的 Python 产物，并满足：

```text
论文图号 ↔ Visualization Manifest ↔ Run ID ↔ Python 文件 ↔ 数据 ↔ 最终结果
```

禁止手绘类似结果、使用 Stage 1 旧图或使用已经被换掉模型/Run 的旧图。

参考论文生成后必须通过 [final-consistency-sweep.md](final-consistency-sweep.md)。

---

## 3. 源码.zip

推荐：

```text
源码/
├── README.md
├── requirements.txt
├── 公共/
│   └── utils/
│       ├── visualization.py
│       └── table_export.py
└── 赛题A/
    ├── 问题1/
    │   ├── src/
    │   ├── data/
    │   └── outputs/
    │       ├── figures/
    │       │   ├── paper/
    │       │   ├── validation/
    │       │   └── exploration/
    │       ├── tables/
    │       │   ├── paper/
    │       │   └── full/
    │       └── intermediate/
    └── ...
```

必须包含最终 Python、依赖、必要数据、真实图表、真实表格、必要中间结果和 `VISUALIZATION_MANIFEST.md`。

普通 DataFrame 优先保存 CSV/XLSX；不要把所有表截图为 PNG。

`VISUALIZATION_MANIFEST.md` 中正式图应绑定对应 Run ID。

---

## 4. 其他.zip

推荐：

```text
其他/
├── AI使用说明/
│   └── AI_USAGE_LOG.md
├── 运行与实验/
│   ├── RUN_LEDGER.md
│   └── runs/
│       ├── R001.md
│       └── ...仅重要运行
├── 建模决策/
├── 文献与来源/
├── 环境与复现/
├── 赛时协作/
└── 其他必要文件/
```

`RUN_LEDGER.md` 必须至少列出每个实际问题的 Final Run、必要 Validation Run、关键参数/种子、输入版本和输出目录。

不要求记录每一次 debug；只记录影响选模、最终结果、验证、正式图表或论文结论的真实运行。

`AI_USAGE_LOG.md` 是内部完整日志。正式比赛若当年要求专门 AI 使用说明文件，应在 `OFFICIAL_SUBMISSION_EXPORT` 阶段根据当年规则从内部日志导出，不直接把内部日志等同于官方文件。

---

## 5. Visualization / Table / Run 验收

内部交付前必须检查：

- A/B/C 图按真实需要生成，没有固定凑数；
- A/B 级图有明确 Figure Contract；
- 不存在为了图好看而静默删数据、删类别、删失败种子或只展示有利结果；
- 中文论文候选图默认中文；
- 中文字体自动回退正常；
- 正式图已逐 panel 通过 Visual QA 和论文尺寸检查；
- 启发式算法在需要时有收敛/稳定性证据；
- 每问存在真实 `FINAL_RUN_ID`；
- `VISUALIZATION_MANIFEST.md` 能追溯图 → Run ID → 数据 → 代码 → 问题 → 结论；
- 普通结果表使用 CSV/XLSX/Word 原生表格链路；
- 长明细表没有塞进论文正文；
- 模型总览图来自确定性绘图而不是生成式 AI 图片。

---

## 6. 跨成果一致性验收

打包前执行 [final-consistency-sweep.md](final-consistency-sweep.md)，至少核对：

```text
原题
↔ Requirement Traceability
↔ 各问 Final Run
↔ 最终结果表
↔ Visualization Manifest
↔ 题目详解
↔ AI 参考论文
```

重点检查：数值版本、舍入、单位、术语、模型名、问题编号、图表版本、Claim vs Data。

存在未解决重大冲突时：

```text
CROSS_ARTIFACT_CONSISTENCY_FAILED
```

不得继续把内部成果标记完成。

---

## 7. ZIP 完整性预检

每个 ZIP 不能只“成功压缩”。至少执行：

1. 源目录与关键文件检查；
2. ZIP CRC/结构测试；
3. 实际解压到新临时目录；
4. 从解压副本检查文件名、数量、大小、0 字节、DOCX/PDF 可打开性、图表/表格存在性；
5. 推荐 `MANIFEST.md + SHA-256` 打包前后对账。

任何异常：

```text
DELIVERY_INTEGRITY_FAILED
```

---

## 8. 内部最终验收

必须确认：

- 当前交付环境已识别；
- 本地模式下四个未压缩成果目录仍存在；
- 四个 ZIP 实际存在并完成真实解压预检；
- 每个实际问题有完整 Markdown 教程；
- 不存在 `FORMULA_DOCUMENTATION_FAILED`；
- 最终 Python 可运行或已诚实记录限制；
- 每问有 Final Run ID；
- `RUN_LEDGER.md` 已完成；
- 图表与表格来自 Final/Validation Run；
- `VISUALIZATION_MANIFEST.md` 已绑定 Run ID；
- 不存在 `CHINESE_FONT_RENDERING_FAILED`；
- 不存在 `PAPER_FIGURE_READABILITY_FAILED`；
- 不存在 `VISUALIZATION_QA_FAILED`；
- 需要收敛证据的启发式算法不存在 `OPTIMIZATION_CONVERGENCE_EVIDENCE_MISSING`；
- 参考论文 `.docx + .pdf` 均存在、非空、可打开；
- 不存在 `FORMULA_RENDERING_FAILED`；
- 文献、数据和参数真实；
- 不存在 `CROSS_ARTIFACT_CONSISTENCY_FAILED`；
- 不存在 `DELIVERY_INTEGRITY_FAILED`。

全部通过后标记：

```text
INTERNAL_DELIVERY_COMPLETE
```

不要把这一状态描述成“官方提交已经准备完成”。

---

## 9. 下一步：队员终稿与官方导出

推荐顺序：

```text
INTERNAL_DELIVERY_COMPLETE
↓
队员人工理解、核查、重写正式论文
↓
FINAL_PAPER_AUDIT
↓
修订 / 二审
↓
最终一致性扫描
↓
核验当年官方最新规则
↓
OFFICIAL_SUBMISSION_EXPORT
```
