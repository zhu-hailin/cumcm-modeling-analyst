# AI 参考论文撰写与参考文献核验规范

## 1. 先区分三个概念

### 参考论文

指 **AI 基于最终锁定建模路线、Final/Validation Run、最终图表/表格和已核验参考文献，认真撰写的完整数学建模参考论文**。

它进入内部 `参考论文.zip`，供队员理解、核查和人工重写，不是官方提交成品。

### 参考文献

指论文中用于支撑背景、方法、参数、数据、模型定义和验证方式的真实外部资料。

### 官方提交论文

队员人工理解、核查并重写后的正式论文，经终稿复审后，再按当年官方规则进入 `OFFICIAL_SUBMISSION_EXPORT`。AI 参考论文不得直接提交。

---

## 2. 参考论文.zip 的目标

默认：

```text
参考论文/
├── 数学建模参考论文.docx
└── 数学建模参考论文.pdf
```

用户提供官方论文模板、格式文件或排版要求时，应优先基于模板生成 Word 与 PDF。

环境可以创建 DOCX/PDF 时必须实际生成，不得只输出结构或空占位文件。

---

## 3. 写作前必须冻结结果来源

开始正式写参考论文前，先确认每个实际问题都有：

```text
FINAL_RUN_ID = Rxxx
```

并完成必要的 Validation Run。

论文的关键数字、排名、预测、路径、参数、图表、结果表和验证结论必须从 Final/Validation Run 及其真实输出读取。

禁止从：

- 聊天记录；
- 旧截图；
- 早期 CSV；
- 已标记 `SUPERSEDED` 的运行；
- Stage 1 探索结果；

手工拼出“最终结果”。

如果写作过程中发现结果版本仍未冻结，应先回到模型运行和 Run Ledger，不能一边换结果一边继续排版论文。

---

## 4. 参考论文必须认真编写

论文必须按正式数学建模论文重新组织，而不是复制教程或第二阶段报告。

至少根据实际题面包含：标题、摘要、关键词、问题重述、问题分析、模型假设、符号说明、数据说明与预处理、总体建模路线、各实际子问题模型与求解、关键结果与图表解释、模型检验、误差/敏感性/鲁棒性分析、模型优缺点、最终结论、参考文献和必要附录。

必须做到：

- 模型链统一；
- 公式、变量、数据和结果互相对应；
- 每个关键结论有真实计算或验证依据；
- 图表来自 Final/Validation Run 对应的最终 Python 运行；
- 普通数值表来自最终结果数据并优先使用原生表格；
- 参考文献真实；
- 不虚构数值、实验、图表、参数来源或引用。

---

## 5. 论文必须与源码、Run Ledger 和结果一致

论文中的模型、参数、数值、表格、敏感性/鲁棒性结论必须能追溯到：

```text
问题
↔ FINAL_RUN_ID / Validation Run
↔ 代码入口 + 输入数据 + 参数
↔ 输出结果
↔ 论文表述
```

不得出现：

- 论文写模型 A，Final Run 跑模型 B；
- 论文写旧参数，Final Run 使用新参数；
- 正文数字来自旧运行；
- 摘要、正文和结论混用不同 Run；
- 为了论文完整补造没有运行过的实验。

新运行若替代旧结果，应先在 Run Ledger 中将旧运行标记 `SUPERSEDED`，再同步更新图表、表格、教程和论文。

---

## 6. 论文图表必须经过 Figure Contract + Visualization Manifest

完整执行：

- [python-visualization-policy.md](python-visualization-policy.md)
- [figure-evidence-contract.md](figure-evidence-contract.md)

论文中的每一张 A/B 级结果图、验证图都必须形成可追溯链：

```text
论文图号
↔ VISUALIZATION_MANIFEST.md
↔ Run ID
↔ Python 输出文件
↔ 生成代码
↔ 输入/中间数据
↔ 最终模型与结果
```

正式复合图还应能说明：核心结论、Hero evidence、Supporting evidence、每个 panel 的唯一任务和不确定性定义。

禁止：

- 手动画一张“看起来像结果”的图；
- 使用 Stage 1 的旧探索图替代最终结果图；
- 使用 `SUPERSEDED` Run 的旧图；
- 路线已从模型 A 换成 B，却继续使用 A 的旧图；
- 图中数字、排名、路径、预测值与 Final Run 不一致；
- 图号与文件映射错误；
- 为图更好看而静默删数据、删失败种子或选择性展示；
- 图表只为装饰，不能说明它支撑什么结论。

中文论文候选图默认使用中文标题、坐标轴、图例和必要注释，单位完整，并通过中文字体、论文尺寸可读性与逐 panel Visual QA。

若某图存在 `VISUALIZATION_QA_FAILED`、`PAPER_FIGURE_READABILITY_FAILED` 或 `CHINESE_FONT_RENDERING_FAILED`，不得进入论文。

### 模型总览图

论文原则上应有一张真实的整题建模框架图，展示问题之间的串行、并行和汇合关系。

优先使用 Graphviz、Mermaid、Matplotlib patches、NetworkX 等确定性方式生成，禁止生成式 AI 图片代替。

---

## 7. 论文结果表格

普通结果表不应由 DataFrame 截图替代。

优先：

```text
Python DataFrame
→ CSV/XLSX
→ Word 原生表格
```

正文只保留核心结果表、关键参数表、验证表；完整长表留在 `outputs/tables/full/`。

真正具有二维结构意义的矩阵才适合作为 heatmap。

论文表格中的数值必须能追溯到 Final/Validation Run 输出表。

---

## 8. 写作前后都执行最终一致性扫描

正式写作前先执行 [final-consistency-sweep.md](final-consistency-sweep.md)，至少保证：

```text
原题
↔ Requirement Traceability
↔ Final Run
↔ 结果表
↔ Visualization Manifest
↔ 题目详解
```

论文 DOCX/PDF 完成后再次执行：

```text
Final Run
↔ 摘要
↔ 正文
↔ 图表/表格
↔ 结论
```

重点检查：

- 同一指标不同数值/精度；
- 单位漂移；
- 模型名、变量名、问题编号漂移；
- Claim 与真实数据冲突；
- 图已更新但正文仍解释旧版本；
- “始终最好”“稳定”“显著”“全局最优”等强结论是否真的有证据。

存在未解决重大冲突：

```text
CROSS_ARTIFACT_CONSISTENCY_FAILED
```

不得进入内部交付。

---

## 9. Word / PDF 公式必须真正渲染

完整遵循 [equation-rendering-policy.md](equation-rendering-policy.md)。

Markdown 可以使用 LaTeX 数学源，但 DOCX/PDF 中禁止保留未经渲染的 LaTeX 字符串。

Word 优先使用 OMML / Office 原生公式；符号说明表中的数学变量同样需要正确渲染。

发现未渲染公式：

```text
FORMULA_RENDERING_FAILED
```

修复前不得进入内部最终交付。

---

## 10. 最终论文参考文献链接

最终 AI 参考论文中若给出参考文献链接，必须达到 `DOWNLOAD_VERIFIED`。

要求页面/文件可实际打开，元数据匹配，来源可靠，全文下载入口真实稳定，下载内容与目标文献一致。

仅 `PAGE_VERIFIED`、`METADATA_ONLY`、`PAYWALLED`、`DOWNLOAD_UNVERIFIED` 的链接不得冒充可下载链接。

如果重要文献无法取得可靠全文：优先寻找官方/作者/机构仓储或合法开放版本；仍失败则反馈用户并记录证据缺口，绝不伪造。

---

## 11. 严禁伪造链接与元数据

禁止猜 URL、编 DOI、把搜索结果页当正式来源、把无法打开的链接写入论文、声称未验证的链接“可下载”。

参考文献状态统一遵循 [source-verification-policy.md](source-verification-policy.md)。

---

## 12. 最终论文质量检查

生成内部参考论文前至少确认：

- 覆盖所有实际子问题；
- 使用最终锁定路线；
- 每问存在 `FINAL_RUN_ID`；
- 数值来自 Final/Validation Run；
- `RUN_LEDGER.md` 与论文结果没有版本冲突；
- 每张论文图都在 `VISUALIZATION_MANIFEST.md` 中且绑定正确 Run ID；
- 没有旧模型/旧结果/`SUPERSEDED` 图；
- 图表通过 Figure Contract、数据完整性门和逐 panel QA；
- 图表中文、单位、字体和论文尺寸可读性正常；
- 图表确实支撑正文对应主张；
- 普通结果表使用真实原生数据表而非无必要截图；
- 公式和符号一致且 DOCX/PDF 正确渲染；
- 没有编造模型效果、实验或结果；
- 没有编造题名、作者、DOI、URL；
- 带链接参考文献达到 `DOWNLOAD_VERIFIED`；
- Word 与 PDF 内容、公式、图表、编号一致；
- 不存在 `CROSS_ARTIFACT_CONSISTENCY_FAILED`；
- 用户提供模板时按模板排版。

通过后才能进入 `INTERNAL_DELIVERY`。

AI 参考论文只属于内部成果；正式比赛提交仍需队员人工重写、终稿复审并执行 [official-submission-policy.md](official-submission-policy.md)。
