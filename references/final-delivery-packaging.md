# 最终交付与 ZIP 打包规范

## 目标

第二阶段完成整题建模、Python 实现、运行验证、专业图表、逐问教程与最终参考论文后，进入 `FINAL_DELIVERY`。

最终固定交付：

```text
题目详解.zip
参考论文.zip
源码.zip
其他.zip
```

环境具备文件创建与压缩能力时必须实际生成 ZIP，不得只给目录示意。问题数量和目录数量按实际题面调整。

同时遵循：

- [output-artifact-policy.md](output-artifact-policy.md)
- [reference-paper-writing.md](reference-paper-writing.md)
- [equation-rendering-policy.md](equation-rendering-policy.md)
- [source-verification-policy.md](source-verification-policy.md)

---

## 1. 题目详解.zip

用途：结合最终源码真正教会队员。

推荐结构：

```text
题目详解/
├── 00_赛题总览.md
├── 问题1/问题1_完整教程.md
├── 问题2/问题2_完整教程.md
├── 问题3/问题3_完整教程.md
└── ...按实际题面继续
```

该 ZIP 中 AI 创建的文本只使用 UTF-8 `.md`。

每问教程至少包含：题意转建模任务、输入输出、变量单位、模型选择理由、公式推导、数据处理、算法步骤、前后问衔接、源码路径、关键函数、运行命令、实际输出、关键图表解释、验证方法、常见错误、调参位置和论文表达。

教程必须与最终源码、参数、文件名和输出一致。

---

## 2. 参考论文.zip

### 关键定义

这里的“参考论文”指 **AI 针对本次赛题认真撰写的最终数学建模成果论文**，不是外部参考文献原文合集。

不得因为外部论文无法下载而让该 ZIP 为空。

默认结构：

```text
参考论文/
├── 数学建模参考论文.docx
└── 数学建模参考论文.pdf
```

若用户提供官方论文模板、Word 模板或排版规范，应按模板生成更贴合赛题的文件名，例如：

```text
A题_参考论文.docx
A题_参考论文.pdf
```

### 论文内容要求

论文必须基于：

- 最终锁定路线；
- 实际 Python 运行结果；
- Python 生成的最终图表；
- 已核验参考文献和数据来源。

至少覆盖：标题、摘要、关键词、问题重述、问题分析、模型假设、符号说明、数据预处理、总体路线、各实际子问题模型与求解、结果与图表解释、模型检验、误差/敏感性/鲁棒性分析、模型优缺点、结论、参考文献和必要附录。

不得用教程复制件、第二阶段草稿或空壳模板冒充论文。

### 公式渲染要求

Word/PDF 公式必须完整执行 [equation-rendering-policy.md](equation-rendering-policy.md)。

硬性要求：

- Markdown/LaTeX 可以作为公式源，但 `.docx/.pdf` 中不能残留未经渲染的 LaTeX 源码；
- Word 优先使用 OMML / Office 原生数学公式；
- 符号说明表第一列的变量也必须按数学公式正确渲染；
- 独立公式、行内公式、表格公式、附录公式都要检查；
- DOCX 生成后必须做公式源码残留扫描和 OMML/结构检查；
- Word 与 PDF 都必须进行公式视觉验收；
- PDF 不得只是把公式错误的 Word 原样导出；
- 任何 `FORMULA_RENDERING_FAILED` 都必须先修复。

### 论文与参考文献的区别

- `参考论文.zip`：放 AI 本次撰写的成果论文 `.docx + .pdf`；
- 外部参考文献：用于论文引用和模型证据，不要求把其原文文件放入 `参考论文.zip`。

外部文献的元数据、链接、核验状态和问题反馈进入 `其他.zip/文献与来源/`。

---

## 3. 源码.zip

推荐结构：

```text
源码/
├── README.md
├── requirements.txt
├── 公共/
│   ├── src/
│   ├── data/
│   └── utils/
└── 赛题A/
    ├── 问题1/
    │   ├── src/
    │   ├── data/
    │   └── outputs/
    │       ├── figures/
    │       ├── tables/
    │       └── intermediate/
    ├── 问题2/
    └── ...
```

赛题编号与问题数量必须按实际题面调整。

必须包含最终 Python 代码、依赖、必要数据/处理后数据、关键图表、关键表格、必要中间结果和根目录 `README.md`。

当前环境允许执行 Python 时，必须实际运行关键入口并修复明显错误。随机算法固定或记录随机种子。

图表默认全部由 Python 生成，且遵循专业、简洁、论文可用、不堆叠无用信息的要求。

---

## 4. 其他.zip

推荐结构：

```text
其他/
├── AI使用说明/AI_USAGE_LOG.md
├── 建模决策/
│   ├── MODELING_DECISION_STATE.md
│   └── 路线变更记录.md
├── 文献与来源/
│   ├── LITERATURE_LEDGER.md
│   ├── 数据来源清单.md
│   ├── 参考文献链接核验.md
│   └── 文献问题反馈.md
├── 环境与复现/运行环境说明.md
└── 其他必要文件/
```

AI 自行创建的文本型文件统一为 UTF-8 Markdown。

外部参考文献链接在这里记录真实状态：`PAGE_VERIFIED`、`DOWNLOAD_VERIFIED`、`METADATA_ONLY`、`PAYWALLED`、`DOWNLOAD_UNVERIFIED`、`BROKEN_LINK`、`REJECTED`。

若重要文献链接打不开、无法下载、需要权限、DOI 不匹配或只能看到摘要，必须在 `文献问题反馈.md` 中记录，并在最终回复中向用户反馈。

---

## 最终打包前检查

必须确认：

- 四个 ZIP 实际存在且名称正确；
- 每个实际子问题都有 `.md` 教程；
- 教程与源码一致；
- Python 代码可运行或已诚实记录限制；
- 图表来自真实 Python 结果；
- `参考论文.zip` 不为空；
- AI 已认真撰写完整参考论文；
- 参考论文同时有 `.docx` 和 `.pdf`；
- Word 与 PDF 内容一致；
- 论文中的数值、图表和表格与源码实际结果一致；
- Word/PDF 中公式均已正确渲染，无明显 LaTeX 源码残留；
- 符号说明表数学变量正确渲染；
- DOCX 公式结构检查通过；
- Word 与 PDF 公式视觉检查通过；
- 不存在 `FORMULA_RENDERING_FAILED`；
- 所有正式参考文献真实；
- 所有论文链接实际核验可打开；
- 标记“可下载”的链接已达到 `DOWNLOAD_VERIFIED`；
- 文献链接问题已向用户反馈并记录；
- 未因无法下载外部论文而拒绝生成 AI 自写参考论文；
- 除最终参考论文外，AI 自行创建的文本型文档均为 `.md`；
- 未在用户未要求时调用 AI 图片生成工具；
- 无缓存、虚拟环境、临时文件和无关重复文件。

全部通过后才能标记 `FINAL_DELIVERY`。
