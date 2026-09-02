> **⚠️ 禁止直接提交 AI 生成的论文。参赛队员应该详细核查并重写论文。**

<div align="center">

<img src="assets/readme.png" alt="CUMCM Modeling Analyst" width="100%" />

# CUMCM Modeling Analyst

面向数学建模竞赛的 AI Skill，适配 Codex、Claude Code 等能够读取附件、编写代码并运行 Python 的 Agent。

![CUMCM](https://img.shields.io/badge/CUMCM-Mathematical_Modeling-orange?style=flat-square)
![Skill](https://img.shields.io/badge/AI-Skill-blueviolet?style=flat-square)
![Codex](https://img.shields.io/badge/Codex-Ready-black?style=flat-square)
![Claude Code](https://img.shields.io/badge/Claude_Code-Ready-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-Modeling-yellow?style=flat-square)

</div>

---

## 这个 Skill 解决什么

数学建模真正难的，通常不是想起一个模型名，而是：题目没读透、数据结构判断错、不同小问接不上、现实数据被随手编造、代码换了而论文仍引用旧结果，或者图做得漂亮却不能证明结论。

这个 Skill 试图把比赛流程连成一条可追溯的证据链：

```text
文件安全审计
→ 深读题与识别数据结构
→ EDA、baseline 与候选方案评分
→ 和队员讨论并确认当前问题方案
→ 中文 Python 正式实现与真实运行
→ Final Run、独立验证与现实约束
→ 符合科研规范的论文图表
→ 原题回查、参考论文和终稿复审
```

聊天窗口只保留当前真正需要知道的结论、风险和下一步；公式、实验、文献、代码说明和图表证据进入项目文件。

---

## 主要能力

| 能力 | 做什么 |
|---|---|
| 读题前安全审计 | 检查隐藏对象、透明文字、嵌入内容和疑似 Prompt Injection，不执行文件中的指令 |
| 数据结构识别 | 先判断成分、时序、空间、网络、配对、层级、截尾或优化结构，再选模型 |
| 证据选模 | 用必要 EDA、baseline、模型前提和真实数据比较候选方案 |
| 逐题方案确认 | 每问先讨论，允许补论文、数据和老师建议，用户确认后才正式实现 |
| 真实外部数据 | 缺现实数据时主动检索权威来源，找不到就报告缺口，不编数字 |
| 建模质量门 | 核心结论需要独立验证，结果还要满足单位、总和、容量、守恒等现实约束 |
| 中文 Python | 使用 `第一题.py`、`第一题_模型求解.py`、`总运行.py` 等清楚文件名 |
| 可读源码 | 关键模块、函数、单位、边界和非显然决策有有效注释，不夹带 Skill 或聊天内容 |
| Run Ledger | 每问明确 `FINAL_RUN_ID`，图表和论文只读取最终或验证运行 |
| 科研制图 | 按结论设计图，绑定数据和 Run，执行国内外主流技术基线与最终尺寸 QA |
| 跨成果一致性 | 对照原题、数据、代码、Run、图表、教程、摘要、正文和结论 |
| 终稿复审 | 检查串题、模型错误、公式、数字、单位、图片、文献和语言问题 |

---

## 每一问先研究，再落地

逐题模式不会一上来直接写完整代码。

```text
回查本问原题和上下问接口
↓
识别数据结构、缺口和模型前提
↓
比较候选方案与 baseline
↓
和队员讨论推荐模型、假设、风险和验证办法
↓
询问是否补充论文、数据、建议或自己的思路
↓
队员确认
↓
正式 Python、Final Run、论文图表、验证和教程
```

确认前允许做必要的探索、小规模实验和资料核验，但不会把中间脚本、试跑结果或草图冒充最终成果。

---

## 从优秀论文吸收的建模质量门

Skill 不再把“用了几个模型”当作质量。每问至少检查：

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

几个特别容易踩坑的地方也有专项检查：

- 指标接近 1 时，检查测试集过小、数据泄漏、同源样本跨集合、反复调参和挑选随机种子；
- 聚类簇被解释为“早期/中期/晚期”或“轻/中/重”时，必须有锚点、单调指标或外部机理，不能让簇编号自动变成阶段；
- 启发式算法找到的是当前最好解时，不写成已经证明的全局最优；
- 相关关系没有因果设计时，不写成“导致”。

详细规则见 `references/modeling-quality-gates.md`。

---

## 科研图片：不是好看就够了

正式论文图统一由 Python、Graphviz、NetworkX、GeoPandas 等确定性工具生成。每张图在动手前先回答：

```text
它要证明什么？
主证据是什么？
每个 panel 分别做什么？
数据来自哪个 Final / Validation Run？
不确定性如何定义？
评阅者最可能质疑什么？
```

### 国内外主流技术基线

绘图规范采用 `GB/T 7713.2-2022` 与 Nature、IEEE、Elsevier、PLOS 官方图形指南的保守交集，并在正式排版时服从当年竞赛模板：

- 折线、路径、网络、流程和其他线稿优先保留 SVG/PDF 矢量版；
- 普通统计图同时保留高质量 PNG，分辨率按**最终插入尺寸**检查；
- 连续色调图通常 300–450 dpi，混合图约 600 dpi，必须位图化的纯线稿约 1000–1200 dpi；
- 先测官方模板正文宽度；无法测量时，单栏约 80–90 mm、通栏约 160–180 mm 作为起点；
- 最终插入尺寸下普通文字约 8–10 pt，关键线条、marker、误差条和 panel 标签能够打印辨识；
- 图题置于图下，表题置于表上；普通结果表保持可编辑，不截图；
- 颜色之外同时使用线型、marker、纹理或直接标签，检查灰度与常见色觉缺陷；
- 坐标、单位、样本量、误差类型、检验和多重比较说明完整；
- 禁止通过截轴、不同缩放、删掉不利样本、隐藏失败 seed 或只展示有利场景夸大结论。

这些数字是跨出版机构的安全起点，不是某一家期刊的永久模板。详细依据和最终 QA 见 `references/python-visualization-policy.md`。

### 图片和脚本可追溯

```text
03_code/q1/论文图/第一题_实际值与预测值对比图.py
04_results/figures/q1/paper/第一题_实际值与预测值对比图.png
04_results/figures/q1/paper/第一题_实际值与预测值对比图.svg
```

脚本与输出图使用同一语义主干，并从 Final/Validation Run 结果读取数据，不在绘图脚本中手抄最终数字。

### AI 沟通图不会混进论文

内部解释、候选比较或调试图必须同时标记：

```text
文件名前缀：AI沟通图_
图面文字：AI内部沟通图｜非论文材料
Manifest：AI_COMMUNICATION_ONLY
进入论文：否
进入官方提交：否
```

内部图如果后来值得放进论文，需要重新绑定正式结论和 Final Run，并作为一张新论文图重新生成与审核。

---

## Codex 单赛题工作区

```text
2022-C/
├─ README.md
├─ 00_problem/                 # 原题、官方附件、官方模板
├─ 01_data/                    # raw / processed / external
├─ 02_analysis/                # 安全审计、题意、假设、符号、方案和教程
├─ 03_code/                    # 中文命名的正式 Python
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
- 论文图、验证图、探索图、AI 沟通图和安全审计图分类存放；
- AI 参考稿不能冒充队员最终论文；
- 用户已有合理结构和明确要求优先。

---

## 代码不是黑盒

正式源码默认使用简洁中文注释，保留必要标准英文术语。重点解释“为什么”，不是逐行翻译 Python。

```python
# 原始附件以“万人次”为单位，模型统一换算为“人次”，
# 避免与单人票价相乘时出现量纲错误。
passenger_count = passenger_10k * 10_000

# 填补器只在训练窗口拟合，防止未来统计量泄漏到历史预测。
train_x = imputer.fit_transform(train_x)
test_x = imputer.transform(test_x)
```

正式源码不包含 Skill 名称、系统提示词、聊天记录、内部状态、隐藏注入原文、“由 AI 生成”水印、大段旧代码和影响结果的占位。

---

## 实战与旧题盲测分开

| 模式 | 用途 | 联网边界 |
|---|---|---|
| `LIVE_RESEARCH_MODE` | 正式比赛 | 正常查论文、官方数据、参数、标准、算法和领域资料，不找当前比赛泄露答案 |
| `BLIND_BENCHMARK_MODE` | 历年题能力测试 | 不用年份题号、题名、原文、附件名和特殊数据定位历史答案 |

旧题盲测仍可去题目标识化地查现实官方数据、通用理论和库文档。

> **禁止搜答案，不禁止查现实。**

---

## 内部四包与最终论文

内部成果固定整理为：

```text
题目详解.zip
参考论文.zip
源码.zip
其他.zip
```

`参考论文.zip` 是 AI 针对本题写的内部参考稿，默认包含 DOCX 和 PDF；不是网上论文合集，也不能直接提交。队员重写后的终稿再交给 Skill 检查错别字、串题、模型、公式、数字、单位、图表、引用和跨成果一致性。

真正上传的文件由当年官方、赛区和提交系统规则决定，Skill 不永久写死某一年的文件名和结构。

---

## 为什么这次做了瘦身

主 `SKILL.md` 只保留路由和不能突破的质量门。启动时只加载：

```text
problem-ingestion-security.md
core-workflow.md
```

进入 EDA、代码、科研制图、公式、论文或交付时，再按 `manifest.yaml` 加载对应规范。旧兼容模板、重复工作流、重复绘图与命名 policy 已合并或删除。

这样能减少 Codex 上下文负担，也降低多份规则互相覆盖的风险；质量检查没有删，只是集中到少数职责清楚的文件中。

---

## Quick Start

```bash
git clone https://github.com/zhu-hailin/cumcm-modeling-analyst.git
```

然后直接说：

```text
使用 cumcm-modeling-analyst 分析这道数学建模赛题。
```

旧题盲测：

```text
这是旧题盲测，不允许搜索或读取这道题的历史答案。
```

比赛中可以自然交流：

```text
先和我们讨论问题一方案，不要立刻写最终代码。
这一问还有哪些资料值得补？
这个核心结论的独立验证是什么？
这张图在最终论文尺寸下能看清吗？
问题二最终使用的是哪一次 Run？
```

---

## 精简后的关键文件

```text
.
├── SKILL.md
├── manifest.yaml
├── README.md
├── agents/openai.yaml
├── assets/
│   ├── FILE_SECURITY_AUDIT_TEMPLATE.md
│   ├── QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md
│   ├── STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md
│   └── FINAL_PAPER_AUDIT_TEMPLATE.md
└── references/
    ├── problem-ingestion-security.md
    ├── core-workflow.md
    ├── modeling-quality-gates.md
    ├── local-workspace-policy.md
    ├── external-data-research-policy.md
    ├── source-verification-policy.md
    ├── model-run-ledger.md
    ├── python-code-documentation-policy.md
    ├── python-visualization-policy.md
    ├── equation-rendering-policy.md
    ├── reference-paper-writing.md
    ├── final-consistency-sweep.md
    ├── final-delivery-packaging.md
    ├── delivery-integrity-policy.md
    ├── final-paper-audit.md
    └── official-submission-policy.md
```

---

## Search Keywords

CUMCM · 数学建模 · Mathematical Modeling · AI Skill · Codex · Claude Code · Python Modeling · Scientific Visualization · Publication Figure · Data Structure · Model Validation · Run Ledger · Evidence-first Figure · Sensitivity Analysis · Robustness Analysis · Blind Benchmark · Paper Review

---

<div align="center">

如果这个项目对你有帮助，欢迎 Star。

发现 AI 会误解题意、编数据、选错模型、混用旧 Run、画误导性图、泄漏内部沟通图、弄乱源码或审错论文，欢迎提 Issue / PR。

</div>
