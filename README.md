> **重要：AI 生成的参考论文不能直接提交。参赛队员需要理解、核验并自行重写。**

<p align="center">
  <img src="assets/readme-showcase/hero-cumcm-modeling-analyst.svg" alt="CUMCM Modeling Analyst：从题面、数据与模型走到可复核的结论" width="100%" />
</p>

<p align="center">
  <a href="assets/readme-showcase/cumcm-readme-workflow.svg">
    <img src="assets/readme-showcase/cumcm-readme-workflow.svg" alt="CUMCM Modeling Analyst 工作流程图：从阅读题目到生成 AI 内部参考论文" width="100%" />
  </a>
</p>

<div align="center">

# CUMCM Modeling Analyst

面向 CUMCM 及同类数学建模竞赛的 AI 协作 Skill，适配 Codex、Claude Code 等能够读取附件、管理项目、编写代码并实际运行 Python 的 Agent。

![CUMCM](https://img.shields.io/badge/CUMCM-数学建模-147d84?style=flat-square)
![Skill](https://img.shields.io/badge/AI-Skill-5b6b9a?style=flat-square)
![Codex](https://img.shields.io/badge/Codex-Ready-222222?style=flat-square)
![Claude Code](https://img.shields.io/badge/Claude_Code-Ready-6c63a8?style=flat-square)
![Python](https://img.shields.io/badge/Python-实跑-3776ab?style=flat-square)

</div>

---

## 这个 Skill 解决什么

数学建模真正难的，往往不是想起一个模型名，而是：

- 题目或附件没有读透；
- 数据结构判断错，模型从第一步就套偏；
- 不同小问彼此断开，前问结果没有真正服务后问；
- 现实数据缺失时被随手补成“合理值”；
- 代码、图表、教程和论文引用了不同版本的结果；
- 图做得很漂亮，却不能证明正文结论；
- AI 写出一篇完整论文，但队员并没有真正理解。

这个 Skill 把比赛过程组织成一条可追溯的证据链：

```text
附件安全审计
→ 深读题与识别数据结构
→ EDA、baseline 与候选路线
→ 和队员确认当前问题方案
→ Python 正式实现与真实运行
→ Final Run、独立验证与现实约束
→ 论文证据蓝图与科研图表
→ 原题回查、参考论文和终稿复审
```

聊天窗口只保留当前真正需要决定的事情。完整公式、代码、运行记录、图表、文献和验证证据进入项目文件，避免三天比赛做到最后只剩一堆找不到来源的数字。

---

## 快速开始

```bash
git clone https://github.com/zhu-hailin/cumcm-modeling-analyst.git
```

然后在支持 Skill 的 Agent 中说：

```text
使用 cumcm-modeling-analyst 分析这道数学建模赛题。
```

旧题盲测请直接声明：

```text
这是旧题盲测，不允许搜索或读取这道题的历史答案；
可以核验通用理论、软件文档和去题目标识化的现实资料。
```

---

## 主要能力

| 能力 | 它具体做什么 |
|---|---|
| 读题前安全审计 | 检查隐藏对象、透明文字、嵌入内容和疑似 Prompt Injection，不执行文件中的指令 |
| 数据结构识别 | 先判断成分、时序、空间、网络、配对、层级、截尾或优化结构，再选模型 |
| 证据选模 | 用必要 EDA、baseline、模型前提和真实数据比较候选路线，不为凑数量硬塞模型 |
| 逐题方案确认 | 每问先讨论，允许补论文、数据、老师建议和队员思路，确认后才正式实现 |
| 真实外部数据 | 缺现实数据时主动检索权威来源，找不到就报告缺口，不编数字 |
| 建模质量门 | 核心结论需要独立验证，结果还要满足单位、总和、容量、守恒等现实约束 |
| 可读 Python | 文件职责清楚，关键函数、单位、边界、随机机制和非显然决策有有效注释 |
| Run Ledger | 每问明确 `FINAL_RUN_ID`，图表和论文只读取最终或验证运行 |
| 论文证据蓝图 | 在写完整论文前，把每项原题要求映射到主答案、Run、图表、公式和正文位置 |
| 科研制图 | 按结论设计图，绑定数据和 Run，执行最终尺寸、色彩、误差和可读性 QA |
| 盲测溯源 | 冻结独立解题成果，再开放参考资料；后学到的内容统一标记 `POST_HOC` |
| 快速阅读审核 | 模拟评阅者只看摘要、路线图、每问首段、主图表和结论，检查主答案是否真正显眼 |
| 跨成果一致性 | 对照原题、数据、代码、Run、图表、教程、摘要、正文和结论 |
| 终稿复审 | 检查串题、模型错误、公式、数字、单位、图片、文献和语言问题 |

---

## 每一问先研究，再落地

逐题模式不会一上来直接写完整代码。

```text
回查本问原题和上下问接口
↓
识别数据结构、现实数据缺口和模型前提
↓
完成必要 EDA 与 baseline
↓
比较真正存在差异的候选路线
↓
和队员讨论推荐模型、假设、风险和验证办法
↓
询问是否补充论文、数据、建议或自己的思路
↓
队员确认
↓
正式 Python、Final Run、论文图表、验证和教程
```

确认前允许做会影响判断的小规模实验和资料核验，但不会把探索脚本、试跑结果或草图冒充最终成果。正式运行如果推翻原路线，流程会标记 `ROUTE_REOPEN_REQUIRED`，回到讨论，而不是硬把错误方案写完。

详细流程见 [`references/core-workflow.md`](references/core-workflow.md)。

---

## 先自由研究，再让质量门审计

质量门不是自动选模器。

```text
QUALITY_GATES_ARE_AUDITORS_NOT_MODEL_SELECTORS
```

AI 应先自由理解机制、数据结构和可能路线，再建立透明 baseline。只有候选之间确实存在决策差异时才进行比较，通常 1–3 个就够，不机械凑三个模型，也不在证据不足时给出虚假精确的推荐分。

每问正式完成前至少检查：

```text
DATA_STRUCTURE_IDENTIFIED
数据处理可追溯
模型适用条件
合理 baseline
主模型证据 + 独立验证
现实约束与单位
跨问题正式复用
结论强度不超过证据
```

两个高风险情形会触发额外审计：

- 指标异常接近 1 时，检查测试集过小、同源样本泄漏、反复调参、类别不平衡和只挑最好随机种子；
- 聚类簇被解释成早/中/晚或轻/中/重时，必须有外部锚点、单调指标或领域机制，不能让簇编号自动变成阶段。

详细规则见 [`references/modeling-quality-gates.md`](references/modeling-quality-gates.md)。

---

## 论文证据蓝图：先回答原题，再写长论文

Final Run 完成后，不直接跳到完整论文，而是先建立：

```text
Final / Validation Run
→ 原题交付项回查
→ PAPER_EVIDENCE_BLUEPRINT
→ 图表、公式和正文位置规划
→ PAPER_EVIDENCE_BLUEPRINT_READY
→ 完整参考论文
```

每一项原题要求都要落到：

- 一句话主答案；
- 科学有效性与竞赛任务完成度；
- 主 Run 与验证 Run；
- 主图、主表或公式；
- 正文位置；
- 证据等级、不确定性和适用条件；
- 向后问传递的数据、参数、模型或结论。

后台成果分成三类：

| 类型 | 去向 |
|---|---|
| `PAPER_CORE` | 直接回答原题或支撑核心结论，必须进入正文 |
| `PAPER_SUPPORT` | 正文概述，完整验证、敏感性和明细进入附录或内部材料 |
| `RUN_ONLY` | 调试、被否决候选和重复运行，只留在运行账本 |

“模型很严谨”和“原题已经回答完整”是两个不同判断：

```text
SCIENTIFIC_VALIDITY = PASS | QUALIFIED | FAIL
CONTEST_TASK_COMPLETION = PASS | FAIL
```

完整规范见 [`references/paper-evidence-architecture.md`](references/paper-evidence-architecture.md)，模板见 [`assets/PAPER_EVIDENCE_BLUEPRINT_TEMPLATE.md`](assets/PAPER_EVIDENCE_BLUEPRINT_TEMPLATE.md)。

---

## 科研图片：不是好看就够了

正式数据图由 Python、Graphviz、NetworkX、GeoPandas 等确定性工具生成。每张准备进入论文的图都要先回答：

```text
它支撑哪项结论？
主证据是什么？
每个 panel 分别做什么？
数据来自哪个 Final / Validation Run？
不确定性怎样定义？
评阅者最可能质疑什么？
```

常规要求：

- 折线、路径、网络和流程图优先保留 SVG/PDF 矢量版本；
- 位图按最终插入尺寸检查分辨率，不靠后期修改 DPI 数字冒充清晰；
- 图题在图下，表题在表上，普通结果表保持可编辑；
- 颜色之外同时使用线型、marker、纹理或直接标签；
- 坐标、单位、样本量、误差类型和检验口径完整；
- 不截轴夸大差异，不删不利样本，不隐藏失败 seed，不只展示最有利场景；
- 论文图、验证图、探索图、AI 沟通图和安全审计图分开保存；
- 每张论文图能追到中文绘图脚本、源数据和 Final/Validation Run。

AI 沟通图必须同时标记：

```text
文件名前缀：AI沟通图_
图面文字：AI内部沟通图｜非论文材料
Manifest：AI_COMMUNICATION_ONLY
进入论文：否
进入官方提交：否
```

完整规范见 [`references/python-visualization-policy.md`](references/python-visualization-policy.md)。

---

## 旧题盲测不会和事后学习混在一起

旧题测试采用明确状态链：

```text
BLIND_RUN_STARTED
→ BLIND_SOLUTION_FROZEN
→ POST_SOLUTION_COMPARISON
→ POST_HOC_IMPROVEMENT
```

打开优秀论文、历史答案或赛后讲评之前，先冻结独立方案、代码、结果、论文证据与 SHA-256。开放资料后学到的新模型、参数、验证、图表和表达都标记为 `POST_HOC`，不能倒灌成“AI 独立想到的”。

原则仍然是：

> **禁止搜答案，不禁止查现实。**

详细规则见 [`references/blind-benchmark-provenance.md`](references/blind-benchmark-provenance.md)。

为了避免仓库首页本身污染同一道旧题的后续盲测，本 README 当前不直接展示旧题结果图，只展示不含题目答案的项目宣传图。资源边界见 [`assets/readme-showcase/ASSET_MANIFEST.md`](assets/readme-showcase/ASSET_MANIFEST.md)。

---

## Codex 单赛题工作区

```text
2022-C/
├─ README.md
├─ 00_problem/                 # 原题、官方附件和模板
├─ 01_data/                    # raw / processed / external
├─ 02_analysis/                # 安全审计、题意、假设、符号、方案和教程
├─ 03_code/                    # 正式 Python
├─ 04_results/                 # figures / tables / data / logs
├─ 05_paper/                   # 提纲、参考稿和队员终稿
├─ 06_submission/              # 内部四包与官方提交候选
├─ 07_references/              # 论文、网页和资料笔记
└─ 99_temp/                    # 可清理临时文件
```

几个边界不能混：

- 官方原件不被覆盖；
- `raw`、`processed`、`external` 严格分开；
- 正式源码不把输出写回代码目录；
- 临时文件不能成为唯一一份正式成果；
- AI 参考稿不能冒充队员最终论文；
- 用户已有合理工程和明确要求优先。

详细规则见 [`references/local-workspace-policy.md`](references/local-workspace-policy.md)。

---

## 代码不是黑盒

新建中文赛题项目时，默认推荐：

```text
03_code/q1/第一题.py
03_code/q1/第一题_模型求解.py
03_code/q1/第一题_结果验证.py
03_code/总运行.py
```

已有英文仓库、CI、Python 包、Notebook 或跨平台工具链时，优先继承现有稳定命名。中文还是英文不决定科学质量，真正的硬要求是职责清楚、入口稳定、注释准确、能够独立运行。

注释重点解释“为什么”，而不是逐行翻译 Python：

```python
# 原始附件以“万人次”为单位，模型统一换算为“人次”，
# 避免与单人票价相乘时出现量纲错误。
passenger_count = passenger_10k * 10_000

# 填补器只在训练窗口拟合，防止未来统计量泄漏到历史预测。
train_x = imputer.fit_transform(train_x)
test_x = imputer.transform(test_x)
```

正式源码不包含 Skill 名称、系统提示词、聊天记录、内部状态、疑似注入原文、“由 AI 生成”水印、大段旧代码和影响结果的占位。

---

## 终稿先过“快速阅读门”

终稿复审不会先埋头找错别字，而是先模拟评阅者快速阅读：

```text
摘要
+ 总体技术路线图
+ 每一问首段
+ 主图 / 主表标题
+ 结论
```

仅凭这些位置，应该能够回答：

- 每一问最终给出了什么直接答案；
- 使用了什么核心模型；
- 最关键的定量结果或规则是什么；
- 哪些结论最不确定；
- 前一问成果如何传给后一问。

无法快速回答时标记 `PAPER_FAST_READ_GATE_FAILED`，优先调整主答案位置、标题层级和主图表，而不是继续堆免责声明或装饰图。

终稿审核见 [`references/final-paper-audit.md`](references/final-paper-audit.md)。

---

## 内部成果与正式提交

全部问题完成后，可以整理四个内部包：

```text
题目详解.zip
参考论文.zip
源码.zip
其他.zip
```

它们用于队员学习、复核、复现、人工写论文和赛后留档，不等于官方提交格式。

`参考论文.zip` 中是 AI 针对本题认真编写的内部参考稿，默认包含 DOCX 和 PDF；不是网上论文合集，也不能直接提交。队员人工重写后的终稿，再交给 Skill 检查错别字、串题、模型、公式、数字、单位、图表、引用和跨成果一致性。

真正上传哪些文件、怎样命名、是否需要支撑材料或 AI 使用说明，始终服从当年官方、赛区和提交系统要求。

---

## 仓库结构

```text
.
├── SKILL.md
├── manifest.yaml
├── README.md
├── agents/openai.yaml
├── scripts/quick_validate.py
├── tests/test_old_problem_forward_contract.py
├── assets/
│   ├── readme-showcase/
│   ├── PAPER_EVIDENCE_BLUEPRINT_TEMPLATE.md
│   ├── FILE_SECURITY_AUDIT_TEMPLATE.md
│   ├── QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md
│   ├── STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md
│   └── FINAL_PAPER_AUDIT_TEMPLATE.md
└── references/
    ├── problem-ingestion-security.md
    ├── core-workflow.md
    ├── modeling-quality-gates.md
    ├── paper-evidence-architecture.md
    ├── blind-benchmark-provenance.md
    ├── model-run-ledger.md
    ├── python-code-documentation-policy.md
    ├── python-visualization-policy.md
    ├── reference-paper-writing.md
    ├── final-consistency-sweep.md
    ├── final-paper-audit.md
    └── official-submission-policy.md
```

`manifest.yaml` 负责按阶段路由。启动只加载安全审计和核心流程；进入数据分析、代码、科研制图、论文或交付阶段后，再加载真正需要的规范，避免上下文臃肿和多份规则互相覆盖。

---

## 常用交流方式

```text
先和我们讨论问题一方案，不要立刻写最终代码。
这一问还有哪些资料值得补？
这个核心结论的独立验证是什么？
这张图在最终论文尺寸下能看清吗？
问题二最终使用的是哪一次 Run？
只告诉我当前最重要的发现、风险和下一步。
```

---

## 边界

这个项目不承诺自动获奖，也不能替代队员判断。它的目标更朴素：让题意、数据、模型、代码、图表、论文和提交文件尽量说同一件事，并让每个关键结论都能回到可核验的证据。

如果这个项目对你有帮助，欢迎 Star。发现题意误读、虚构数据、数据泄漏、错误选模、旧 Run 混用、误导性图表或论文一致性问题，也欢迎提交 Issue 或 PR，并附上可复现证据。
