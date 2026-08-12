# 最终交付与 ZIP 打包规范

## 目标

第二阶段完成整题建模、Python 实现、运行验证、专业图表、逐问教程与最终参考论文后，进入 `FINAL_DELIVERY`。

最终固定交付仍为：

```text
题目详解.zip
参考论文.zip
源码.zip
其他.zip
```

但在创建 ZIP 前，必须先识别当前运行环境，并完整执行：

- [delivery-integrity-policy.md](delivery-integrity-policy.md)
- [output-artifact-policy.md](output-artifact-policy.md)
- [reference-paper-writing.md](reference-paper-writing.md)
- [equation-rendering-policy.md](equation-rendering-policy.md)
- [source-verification-policy.md](source-verification-policy.md)

核心区别：

- **Codex / Claude Code / 本地 Agent**：项目根目录中的真实成果目录是主成果，ZIP 是打包副本；
- **Chat / 云端附件交付**：用户主要依赖下载文件，ZIP 必须额外通过跨平台解压与文件可用性预检。

---

## 0. 环境感知交付

### LOCAL_WORKSPACE_DELIVERY

如果 AI 在本地项目根目录内工作，应优先保持完整未压缩成果，例如：

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

如果用户已经指定输出目录，则使用用户指定目录。

本地模式下：

- 未压缩目录不得因为打包而删除；
- 中文文件名可以保留，不强制全部改 ASCII；
- ZIP 仍必须做结构测试和真实解压预检；
- 即使 ZIP 出现问题，本地真实成果也必须完整保留；
- 最终回复应告诉用户成果所在根目录/输出目录。

### CHAT_ARTIFACT_DELIVERY

如果成果通过 Chat / 云端附件下载交付：

- 四个 ZIP 必须实际生成；
- ZIP 内文件名编码与跨平台兼容性必须真实验证；
- 如果当前打包工具不能稳定处理中文 entry，可回退到 ASCII-safe 内部路径，并用 `README.md` / `MANIFEST.md` 写中文说明；
- 平台支持时，参考论文 `.docx/.pdf` 应同时提供独立下载作为 ZIP 故障兜底。

详细规则见 [delivery-integrity-policy.md](delivery-integrity-policy.md)。

---

## 1. 题目详解.zip

用途：结合最终源码真正教会队员。

推荐源目录结构：

```text
题目详解/
├── 00_赛题总览.md
├── 问题1/问题1_完整教程.md
├── 问题2/问题2_完整教程.md
├── 问题3/问题3_完整教程.md
└── ...按实际题面继续
```

该目录中 AI 创建的文本只使用 UTF-8 `.md`。

每问教程至少包含：题意转建模任务、输入输出、变量单位、模型选择理由、公式推导、数据处理、算法步骤、前后问衔接、源码路径、关键函数、运行命令、实际输出、关键图表解释、验证方法、常见错误、调参位置和论文表达。

公式必须完整遵循 [equation-rendering-policy.md](equation-rendering-policy.md)，教程必须与最终源码、参数、文件名和输出一致。

---

## 2. 参考论文.zip

### 关键定义

这里的“参考论文”指 **AI 针对本次赛题认真撰写的最终数学建模成果论文**，不是外部参考文献原文合集。

不得因为外部论文无法下载而让该目录或 ZIP 为空。

默认源目录：

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

推荐源目录：

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

---

## 4. 其他.zip

推荐源目录：

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
├── 赛时协作/
└── 其他必要文件/
```

AI 自行创建的文本型文件统一为 UTF-8 Markdown。

外部参考文献链接在这里记录真实状态：`PAGE_VERIFIED`、`DOWNLOAD_VERIFIED`、`METADATA_ONLY`、`PAYWALLED`、`DOWNLOAD_UNVERIFIED`、`BROKEN_LINK`、`REJECTED`。

---

## 5. 打包完整性预检

不能只运行压缩命令后就宣布完成。

每个 ZIP 至少执行两轮：

### 第一轮：结构测试

例如：

```bash
unzip -t 参考论文.zip
```

或使用 ZIP 库完成 CRC / entry 检查。

### 第二轮：真实解压

必须把 ZIP 解压到新的临时目录，并从解压后的副本检查：

- 文件数量；
- 文件名是否正常；
- 文件大小；
- 关键文件是否存在；
- 是否有 0 字节文件；
- Markdown / Python / 文本是否可读取；
- DOCX 是否为有效 Office 文档；
- PDF 是否有效且页数大于 0；
- 关键图表和表格是否存在。

推荐使用 `MANIFEST.md` 记录相对路径、大小与 SHA-256，在打包前后对账。

任何异常标记：

```text
DELIVERY_INTEGRITY_FAILED
```

修复前不得进入 `FINAL_DELIVERY`。

---

## 最终打包前检查

必须确认：

- 当前交付环境已识别为 `LOCAL_WORKSPACE_DELIVERY` 或 `CHAT_ARTIFACT_DELIVERY`；
- 本地模式下四个未压缩成果目录仍真实存在；
- 四个 ZIP 实际存在且名称正确；
- 四个 ZIP 均完成结构测试；
- 四个 ZIP 均实际解压到临时目录验证过；
- 解压后关键文件名、数量、大小正常；
- 不存在“运行时有文件，但解压后像空包”的情况；
- 每个实际子问题都有 `.md` 教程；
- Markdown 教程公式与说明通过；
- 教程与源码一致；
- Python 代码可运行或已诚实记录限制；
- 图表来自真实 Python 结果；
- `参考论文.zip` 不为空；
- 参考论文同时有 `.docx` 和 `.pdf`；
- DOCX/PDF 本身均能打开且非空；
- Word 与 PDF 内容一致；
- 论文中的数值、图表和表格与源码实际结果一致；
- Word/PDF 中公式均正确渲染；
- 不存在 `FORMULA_DOCUMENTATION_FAILED`；
- 不存在 `FORMULA_RENDERING_FAILED`；
- 不存在 `DELIVERY_INTEGRITY_FAILED`；
- 所有正式参考文献真实；
- 标记“可下载”的链接已达到 `DOWNLOAD_VERIFIED`；
- 除最终参考论文外，AI 自行创建的文本型文档均为 `.md`；
- 未在用户未要求时调用 AI 图片生成工具；
- 无缓存、虚拟环境、临时文件和无关重复文件。

全部通过后才能标记 `FINAL_DELIVERY`。
