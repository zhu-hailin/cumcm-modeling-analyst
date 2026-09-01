# INTERNAL_DELIVERY：内部四包与打包规范

## 目标

全部问题完成、结果通过验证、正式 Python 通过注释与源码纯净度检查、参考论文生成并完成一致性检查后，进入：

```text
INTERNAL_DELIVERY
```

固定生成四个内部成果包：

```text
题目详解.zip
参考论文.zip
源码.zip
其他.zip
```

它们用于队伍学习、复核、复现、人工重写论文和终稿审核，**不等于官方比赛提交文件**。

正式比赛需要上传文件时，必须在队员人工重写论文并完成终稿审核后，再执行 `OFFICIAL_SUBMISSION_EXPORT`。

---

# 1. Codex 本地保存位置

Codex 工作区遵循：

[local-workspace-policy.md](local-workspace-policy.md)

默认根目录例如：

```text
2022-C/
```

未指定其他位置时，四个内部包保存到：

```text
2022-C/06_submission/internal_delivery/
├─ 题目详解.zip
├─ 参考论文.zip
├─ 源码.zip
├─ 其他.zip
└─ MANIFEST.md
```

打包源文件仍保留在 `00_problem/` 至 `07_references/` 的正式目录中。ZIP 是筛选后的副本，不得打包后删除原文件。

用户指定其他路径时，以用户要求为准。

Chat / 云端模式不要求模拟完整本地目录，只需实际交付并验证四个 ZIP 和必要独立文件。

---

# 2. `题目详解.zip`

推荐内容：

```text
题目详解/
├─ 00_赛题总览.md
├─ 问题1/
│  └─ 问题1_完整教程.md
├─ 问题2/
│  └─ 问题2_完整教程.md
└─ 问题N/
   └─ 问题N_完整教程.md
```

每问教程至少串起：

```text
题意
→ 输入输出
→ 数据与来源
→ 模型选择理由
→ 变量、公式和假设
→ 对应正式代码与关键注释
→ FINAL_RUN_ID
→ 实际结果
→ 图表与表格
→ 验证
→ 向下一问传递什么
```

Codex 可从以下位置整理：

- `02_analysis/`：题意、假设、符号、方案；
- `03_code/qN/`：正式代码、docstring 和关键注释；
- `04_results/`：真实结果、图表、表格和日志；
- `07_references/`：本问使用的资料和来源。

教程公式必须符合 `equation-rendering-policy.md`。最终数字必须来自对应问题的 Final Run。教程中的代码解释必须与最终源码及其注释一致。

---

# 3. `参考论文.zip`

默认包含：

```text
参考论文/
├─ 数学建模参考论文.docx
└─ 数学建模参考论文.pdf
```

Codex 本地源文件通常来自 `05_paper/`。

AI 第一次生成的成果是内部参考稿，不得把未经队员人工重写的版本冒充正式参赛终稿。可在 `05_paper/` 中使用：

```text
draft.docx
```

或清楚的“参考论文”命名。

论文必须：

- 基于各问最终模型和 `FINAL_RUN_ID`；
- 使用最终 Python 结果；
- 图表来自最终 `VISUALIZATION_MANIFEST.md`；
- 表格与 `04_results/tables/` 一致；
- 公式在 Word/PDF 中真正渲染；
- 引用真实可核验；
- 通过 `final-consistency-sweep.md`。

禁止使用旧 Run、旧图、旧表或未运行实验补齐论文。

---

# 4. `源码.zip`

推荐内容从工作区正式代码和复现所需材料中筛选：

```text
源码/
├─ README.md
├─ requirements.txt
├─ run_all.py
├─ common/
├─ q1/
├─ q2/
├─ qN/
├─ data/
│  ├─ processed/
│  └─ external/
├─ results/
│  ├─ figures/
│  ├─ tables/
│  └─ data/
└─ VISUALIZATION_MANIFEST.md
```

主要来源：

- `03_code/`；
- `01_data/processed/`；
- 允许分发且复现必需的 `01_data/external/`；
- `04_results/` 中论文与复现需要的最终结果。

注意：

- 默认不要把 `00_problem/` 官方附件和 `01_data/raw/` 全部重复打进源码包，除非复现确实需要且比赛规则允许；
- 外部数据受许可限制时，提供获取说明，不擅自再分发；
- 不把 `99_temp/`、缓存、无用旧模型和过期结果打包；
- `run_all.py` 应能在合理环境下复现整题最终流程；
- 普通结果表使用 CSV/XLSX，不要全部截图成 PNG；
- 正式源码完整执行 [python-code-documentation-policy.md](python-code-documentation-policy.md)。

## 4.1 源码注释与可读性

打包前必须确认：

- 每个非平凡正式模块有简短模块 docstring，说明职责、输入、输出和运行入口；
- 关键数据、清洗、特征、模型、目标函数、约束、验证、绘图和导出函数/类有准确 docstring；
- 单位换算、统计口径、清洗理由、边界、数值稳定、随机种子、重复实验和停止条件有必要注释；
- 目标函数和主要约束能与教程公式对应；
- 注释默认简洁、真实、有信息量，不逐行翻译 Python 语法；
- 注释与当前代码、参数、公式编号、单位、输入输出和路径一致；
- 不存在大段注释掉的旧代码；
- 不存在影响结果的 `TODO`、`FIXME`、`pass` 占位或伪实现。

不得把“注释行很多”当作质量通过。关键是队员能看懂代码为什么这样写、数据从哪里来、结果从哪里输出。

## 4.2 源码纯净度

正式源码和源码 README 不得混入：

- `cumcm-modeling-analyst` 等 Skill 宣传；
- 系统提示词、开发者指令和聊天记录；
- `QUESTION_PLAN_CONFIRMATION`、`WAITING_FOR_CONFIRMATION` 等内部状态；
- 文件安全审计提示词或隐藏注入原文；
- “我刚研究出来了”等对话话术；
- “由 ChatGPT/Codex 生成”等无运行价值的水印注释。

源码可以记录运行参数、随机种子、输入数据版本和必要元数据，但应使用配置、日志或普通工程说明，不把内部 Skill 状态机写入业务代码。

失败状态：

```text
PYTHON_CODE_DOCUMENTATION_FAILED
SOURCE_CODE_CONTAMINATION_DETECTED
```

修复并重新运行必要入口后，才允许生成最终 `源码.zip`。

---

# 5. `其他.zip`

推荐内容：

```text
其他/
├─ AI使用说明/
│  └─ AI_USAGE_LOG.md
├─ 建模分析/
│  ├─ problem_analysis.md
│  ├─ assumptions.md
│  ├─ symbols.md
│  └─ model_plan.md
├─ 运行与实验/
│  ├─ RUN_LEDGER.md
│  └─ 重要运行记录/
├─ 文献与来源/
│  ├─ websites.md
│  ├─ notes.md
│  └─ 文献问题反馈.md
├─ 数据来源与处理/
├─ 一致性检查/
├─ 环境与复现/
└─ 赛时协作记录/
```

主要来源：

- `02_analysis/`；
- `04_results/logs/`；
- `07_references/`；
- AI 使用记录、数据血缘、环境说明和最终审计材料。

`AI_USAGE_LOG.md` 是内部完整记录。正式比赛若要求单独 AI 使用说明，应按当年规则从该日志导出，不能把内部日志直接冒充官方文件。

Skill 状态、聊天协作记录和安全审计说明应留在“其他”材料，不应为了留档方便塞进正式 Python 注释。

---

# 6. 与 `06_submission/` 官方文件的边界

Codex 默认工作区中：

```text
06_submission/
├─ internal_delivery/   # 四个内部包
├─ paper.pdf            # 官方提交候选，按当年规则调整
├─ source_code.zip      # 官方提交候选，按当年规则调整
└─ checklist.md
```

`paper.pdf`、`source_code.zip` 只是用户给出的默认示例。正式提交前必须重新核验当年官网、赛区和提交系统要求。如果官方规则不同，就按最新规则改名、增删或调整目录。

禁止把 `参考论文.zip` 中的 AI 参考稿直接复制为官方 `paper.pdf`。

若官方允许或要求提交源码，官方源码候选同样必须通过运行、注释质量、源码纯净度、匿名性和当年提交范围检查。

---

# 7. 图表、表格、代码与 Run 验收

打包前检查：

- 每问存在明确 `FINAL_RUN_ID`；
- 正式 Python 已实际运行；
- 正式 Python 注释和 docstring 与实现一致；
- 正式源码不存在 Skill/聊天污染；
- 正式图有 Figure Contract；
- `VISUALIZATION_MANIFEST.md` 能追到 Run ID、代码和数据；
- 图表来自 `04_results/figures/` 的最终版本；
- 表格来自 `04_results/tables/`；
- 数值结果来自 `04_results/data/`；
- 运行日志和 Run Ledger 位于 `04_results/logs/`；
- 没有为了图好看静默删数据、删类别、删失败种子或隐藏不利场景；
- 中文、单位、字体、裁切和论文尺寸可读性通过；
- 迭代启发式算法在需要时有真实收敛和重复性证据。

---

# 8. 跨成果一致性验收

打包前执行 `final-consistency-sweep.md`，至少核对：

```text
原题与附件
↔ 02_analysis
↔ 01_data
↔ 03_code（实现 + 注释）
↔ 各问 FINAL_RUN_ID
↔ 04_results
↔ 题目详解
↔ 05_paper
↔ 四个内部包
```

重点检查：

- 数值版本和舍入；
- 单位、符号、模型名和问题编号；
- 代码注释、docstring 与当前实现是否一致；
- 图表版本；
- 摘要、正文和结论；
- Claim vs Data；
- 被替代 Run 的残留内容。

存在重大未解决冲突时：

```text
CROSS_ARTIFACT_CONSISTENCY_FAILED
```

不得继续标记内部交付完成。

---

# 9. ZIP 完整性预检

每个 ZIP 至少执行：

1. 打包源目录和关键文件检查；
2. ZIP CRC / entry 结构检查；
3. 实际解压到 `99_temp/zip_check/` 或其他临时目录；
4. 从解压副本检查文件名、数量、大小、0 字节、DOCX/PDF、代码、数据、图表和表格；
5. 从解压副本抽查正式 Python 的注释、docstring 和源码纯净度；
6. 推荐使用 `MANIFEST.md + SHA-256` 做打包前后对账；
7. 验收通过后再清理临时解压目录。

异常状态：

```text
DELIVERY_INTEGRITY_FAILED
```

---

# 10. 内部最终验收

必须确认：

- [ ] Codex 单赛题工作区结构清楚，或已按用户指定结构映射；
- [ ] 原题、原始数据、清洗数据、外部数据分层正确；
- [ ] 每问正式代码在 `03_code/qN/`；
- [ ] 正式代码具有真实有效的模块说明、docstring 和关键注释；
- [ ] 注释与模型、公式、单位、参数、路径和返回值一致；
- [ ] 源码无 Skill/聊天/提示词污染，无影响结果的占位实现；
- [ ] 每问最终结果能追到 `FINAL_RUN_ID`；
- [ ] 图、表、数据和日志集中在 `04_results/`；
- [ ] 参考论文 DOCX/PDF 存在、非空、可打开；
- [ ] Markdown 与 Word/PDF 公式均通过；
- [ ] 四个 ZIP 实际生成并真实解压验证；
- [ ] 重大跨成果冲突已解决；
- [ ] 官方提交候选与内部四包没有混淆；
- [ ] 用户原文件没有被擅自覆盖、删除或改名。

全部通过后标记：

```text
INTERNAL_DELIVERY_COMPLETE
```

不要把这一状态描述成“官方提交已经准备完成”。
