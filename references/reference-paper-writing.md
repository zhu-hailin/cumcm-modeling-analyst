# AI 参考论文撰写与参考文献核验规范

## 1. 先区分三个概念

### AI 参考论文

AI 根据最终锁定路线、Final/Validation Run、真实图表与表格、已核验文献认真撰写的完整数学建模参考稿。

它供队员理解、核查和人工重写，不能直接当作正式参赛论文提交。

### 参考文献

论文中支撑背景、方法、参数、数据、模型定义和验证方式的真实外部资料。

### 官方提交论文

队员人工理解、核查并重写后的正式论文。它需要通过终稿复审，再按当年官方规则进入 `OFFICIAL_SUBMISSION_EXPORT`。

---

## 2. Codex 中的论文目录

Codex 单赛题工作区遵循 `local-workspace-policy.md`。

默认：

```text
05_paper/
├─ outline.md
├─ draft.docx
├─ final.docx
└─ final.pdf
```

`outline.md` 保存论文结构、图表位置、公式清单和待补内容。

AI 第一次生成的论文属于内部参考稿，应保存为 `draft.docx` 或使用清楚的“参考论文”命名。未经队员人工重写、核查和确认，不得直接命名为 `final.docx` 或 `final.pdf`。

如果需要同时保存 AI 参考稿的 PDF，可使用：

```text
05_paper/reference_paper.docx
05_paper/reference_paper.pdf
```

用户已有自己的命名、版本管理或协作方式时，以用户要求为准，不能覆盖队员正在编辑的文件。

---

## 3. 写作前冻结结果来源

开始正式写参考论文前，确认每个实际问题都有：

```text
FINAL_RUN_ID = Rxxx
```

并完成必要的 Validation Run。

Codex 默认从以下位置读取：

```text
01_data/processed/                    # 最终建模数据
01_data/external/                     # 已核验外部数据
02_analysis/                          # 题意、假设、符号、模型方案与逐问教程
03_code/qN/                           # 最终代码
04_results/data/qN/                   # 最终数值与跨问结果
04_results/tables/qN/                 # 最终表格
04_results/figures/qN/                # 最终图表
04_results/logs/RUN_LEDGER.md         # 运行账本
04_results/VISUALIZATION_MANIFEST.md  # 图表来源清单
07_references/                        # 文献、网页与来源笔记
```

论文中的关键数字、排名、预测、路径、参数、表格、图表和验证结论必须从 Final/Validation Run 的真实输出读取。

禁止从聊天记录、旧截图、早期 CSV、Stage 1 探索结果或 `SUPERSEDED` Run 拼出“最终结果”。

写作过程中若结果仍未冻结，应先回到模型和 Run Ledger，不要一边换结果一边继续排版。

---

## 4. 参考论文要重新组织

参考论文不能只是把教程和阶段报告拼接起来。至少根据实际题面包含：

- 标题；
- 摘要与关键词；
- 问题重述；
- 问题分析；
- 模型假设；
- 符号说明；
- 数据说明与预处理；
- 总体建模路线；
- 各问题模型与求解；
- 关键结果及图表解释；
- 模型检验；
- 误差、敏感性或鲁棒性分析；
- 模型优缺点；
- 最终结论；
- 参考文献；
- 必要附录。

必须做到：

- 模型链统一；
- 公式、变量、数据、代码和结果互相对应；
- 关键结论有真实计算或验证依据；
- 图表来自 Final/Validation Run；
- 普通数值表来自最终结果数据，并优先使用 Word 原生表格；
- 文献与外部数据真实；
- 不虚构结果、实验、参数来源或引用。

---

## 5. 与工作区保持一致

论文必须形成：

```text
原题要求
↔ 02_analysis 中的最终模型与符号
↔ 03_code 中的正式实现
↔ FINAL_RUN_ID
↔ 04_results 中的数值、表格和图表
↔ 05_paper 中的论文表述
```

不得出现：

- 论文写模型 A，Final Run 实际跑模型 B；
- 论文使用旧参数，代码使用新参数；
- 摘要、正文和结论混用不同 Run；
- 图表属于旧模型或旧数据；
- 为了论文结构完整而补造没有运行过的实验。

新 Run 替代旧结果时，先把旧 Run 标记为 `SUPERSEDED`，再同步更新 `04_results/`、逐问教程和论文。

---

## 6. 图表必须来自最终证据链

完整执行：

- `python-visualization-policy.md`
- `figure-evidence-contract.md`

论文中的每张 A/B 级图都要能追到：

```text
论文图号
↔ 04_results/VISUALIZATION_MANIFEST.md
↔ Run ID
↔ 04_results/figures 中的文件
↔ 03_code 中的生成代码
↔ 01_data / 04_results/data 中的数据
↔ 最终模型与结论
```

复合图还应说明：

- 核心结论；
- Hero evidence；
- Supporting evidence；
- 每个 panel 的唯一任务；
- 不确定性定义。

禁止：

- 手画一张“类似结果”的图；
- 用 Stage 1 旧探索图代替最终结果图；
- 使用 `SUPERSEDED` Run 的图；
- 模型已更换但图没更换；
- 图中数字、排名、路径或预测值与 Final Run 不一致；
- 为了更好看静默删除数据、失败种子或不利场景；
- 把没有证据作用的装饰图塞进正文。

中文论文候选图默认使用中文标题、坐标轴、图例、必要注释和完整单位，并通过中文字体、最终尺寸和逐 panel QA。

### 整题模型框架图

论文原则上应有一张真实的整题建模框架图，展示各问之间的串行、并行和汇合关系。

优先使用 Graphviz、Mermaid、Matplotlib patches 或 NetworkX 等确定性方式。禁止用生成式图片代替模型流程图。

---

## 7. 论文表格

普通结果表优先：

```text
04_results/tables/qN/*.csv|xlsx
→ Word 原生表格
```

正文只保留真正需要的：

- 核心结果表；
- 关键参数表；
- 验证表。

完整明细继续保存在 `04_results/tables/`，不要把几百行结果塞入正文，也不要默认把 DataFrame 截图成 PNG。

真正具有二维结构意义的矩阵才适合作为 heatmap。

论文表格中的数字必须能追到 Final/Validation Run 输出。

---

## 8. 写作前后执行一致性扫描

正式写作前执行 `final-consistency-sweep.md`，至少保证：

```text
00_problem
↔ Requirement Traceability
↔ 各问 Final Run
↔ 04_results
↔ 02_analysis/qN_solution.md
```

论文 DOCX/PDF 完成后再次检查：

```text
Final Run
↔ 摘要
↔ 正文
↔ 图表与表格
↔ 结论
```

重点检查：

- 同一指标出现不同数值或精度；
- 单位漂移；
- 模型名、变量名和问题编号漂移；
- Claim 与真实数据冲突；
- 图已更新但正文还在解释旧图；
- “始终最好”“稳定”“显著”“全局最优”等强结论是否真的有证据。

存在未解决重大冲突时：

```text
CROSS_ARTIFACT_CONSISTENCY_FAILED
```

不得进入内部交付。

---

## 9. Word 与 PDF 公式

完整遵循 `equation-rendering-policy.md`。

Markdown 可以使用 LaTeX 数学源，但 DOCX/PDF 中不能残留未经渲染的 LaTeX 字符串。

Word 优先使用 OMML / Office 原生公式；符号说明表中的数学变量也需要正确渲染。

失败状态：

```text
FORMULA_RENDERING_FAILED
```

修复前不得进入内部交付。

---

## 10. 参考文献与现实数据

发生外部检索时同时执行：

- `source-verification-policy.md`
- `external-data-research-policy.md`

中国现实场景不能只因为国际论文更容易找到，就让外国文献替代国内统计、政策、标准、行业参数和实体运营数据。

方法论可以使用高质量国际原始文献；中国现实背景与数据应优先寻找官方和本土资料。

论文中的参考文献链接必须真实核验。需要声称“可下载”时必须达到：

```text
DOWNLOAD_VERIFIED
```

仅 `PAGE_VERIFIED`、`METADATA_ONLY`、`PAYWALLED` 或 `DOWNLOAD_UNVERIFIED` 的链接，不得冒充可下载链接。

重要文献无法取得可靠全文时，继续寻找出版社、作者仓储、机构仓储或合法开放版本；仍失败则明确反馈并记录证据缺口，绝不拼接假链接。

实际下载和查阅的论文、标准与报告可保存到 `07_references/papers/`；网页来源和用途分别记录到 `07_references/websites.md` 与 `07_references/notes.md`。

---

## 11. 进入内部交付前检查

至少确认：

- [ ] 覆盖所有实际问题；
- [ ] 使用最终锁定路线；
- [ ] 每问存在 `FINAL_RUN_ID`；
- [ ] 数值来自 Final/Validation Run；
- [ ] Run Ledger 与论文没有版本冲突；
- [ ] 每张论文图都在 Manifest 中，并绑定正确 Run ID；
- [ ] 没有旧模型、旧结果或 `SUPERSEDED` 图；
- [ ] 图表通过 Figure Contract、数据完整性门和逐 panel QA；
- [ ] 图表中文、单位、字体和最终尺寸正常；
- [ ] 普通结果表来自真实数据，而非无必要截图；
- [ ] 公式和符号一致，并在 DOCX/PDF 中正确渲染；
- [ ] 没有编造模型效果、实验、现实数据、文献或链接；
- [ ] Word 与 PDF 的内容、公式、图表和编号一致；
- [ ] 不存在 `CROSS_ARTIFACT_CONSISTENCY_FAILED`；
- [ ] 用户提供模板时已按模板排版；
- [ ] AI 参考稿没有冒充队员最终论文。

通过后才能进入 `INTERNAL_DELIVERY`。
