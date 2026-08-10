> **⚠️ 禁止直接提交 AI 生成的论文。参赛队员应该详细核查并重写论文。**

<div align="center">

# 🏆 CUMCM Modeling Analyst

### 面向数学建模竞赛的 AI Skill · Codex · Claude Code 工作流

**深度读题 · 探索性研究 · 证据选模 · 双模式求解 · Python 实跑 · 文献核验 · 四包交付 · 终稿复审**

![CUMCM](https://img.shields.io/badge/CUMCM-Mathematical_Modeling-orange?style=flat-square)
![Skill](https://img.shields.io/badge/AI-Skill-blueviolet?style=flat-square)
![Codex](https://img.shields.io/badge/Codex-Ready-black?style=flat-square)
![Claude Code](https://img.shields.io/badge/Claude_Code-Ready-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-Modeling-yellow?style=flat-square)

> **不是“看到关键词就套模型”，而是先读懂题、看清数据，再用证据决定模型。**

</div>

---

## 🌟 这是什么？

`cumcm-modeling-analyst` 是一个面向 **全国大学生数学建模竞赛（CUMCM）及同类 Mathematical Modeling Competition** 的 AI Skill，重点适配 **Codex、Claude Code** 等可读取文件、编写代码并在本地执行 Python 的 Agent。

它不是一个“模型推荐词典”，而是一套完整的建模工作流：

```text
拿到赛题
   ↓
深度读题 + 附件审计
   ↓
探索性研究 / EDA / baseline
   ↓
逐问拆解 + 候选模型评分
   ↓
整题路线设计
   ↓
选择解题模式
   ↓
Python 正式求解 + 实际运行验证
   ↓
各问结果衔接 + 原题逐条回查
   ↓
教程 / 参考论文 / 源码 / 其他资料
   ↓
组员手搓最终论文
   ↓
AI 赛前终稿复审
```

核心目标只有一个：**让题意、数据、模型、公式、代码、结果和论文表达真正对应起来。**

---

## ✨ 核心能力

| 能力 | 作用 |
|---|---|
| 🧠 深度读题 | 识别题面事实、动作词、约束、单位、边界和各问依赖 |
| 🔬 探索性研究 | 正式选模前用 Python 做 EDA、baseline、趋势、可行性和模型前提检查 |
| 🧩 逐问拆题 | 每问明确输入、输出、变量、约束、前后问接口 |
| 📊 方案评分 | 对真正有差异的候选方法使用统一 100 分制比较 |
| 🔗 跨问关联 | 检查问题 1 的结果如何真实进入问题 2、问题 3，而不是模型拼盘 |
| 🧪 Python 实跑 | Codex/本地环境直接实现并执行最终代码，保存真实结果 |
| 📈 专业图表 | 建模图表默认由 Python 根据真实数据和模型结果生成 |
| 📚 文献核验 | 核验题名、作者、DOI、URL、全文访问与下载状态，禁止伪造 |
| ✅ 原题回查 | 全部求解后重新读题，逐条确认每个要求都被回答 |
| 📦 四包交付 | 输出题目详解、参考论文、源码、其他资料四个 ZIP |
| 🔎 终稿复审 | 组员手搓论文后再次审查错别字、思路、解法、公式、结果和串题错误 |

---

## 🔬 为什么加入“探索性研究”？

数学建模里，很多模型不能只看题目关键词决定。

例如题目要求预测，不代表一定应该使用 ARIMA、XGBoost 或 LSTM。真正选模之前，应该先看：

- 数据量是否足够；
- 是否存在趋势、周期、季节性和结构突变；
- 是否有严重缺失和异常值；
- 类别是否失衡；
- 聚类数据是否真的存在可分结构；
- 优化问题的规模、约束和可行域如何；
- 简单 baseline 是否已经表现很好；
- 候选模型的关键假设是否成立。

因此 Stage 1 允许 Codex 使用轻量 Python 做探索，但探索只服务于 **理解题目和选择路线**，不把探索性结果冒充最终结论。

```text
题意判断
→ 数据探索
→ 候选模型
→ 小规模验证
→ 更新评分
→ 决定正式路线
```

---

## 🧭 第一阶段：深读题 + 探索 + 路线决策

每个实际子问题按固定节奏处理：

```text
一句话判断
→ 核心思路
→ 关键探索证据
→ 候选方案
→ 100 分评分
→ 首选 / 备用 / 切换条件
```

整题路线通常给出 **2–3 条真正有意义的方案**，不为了数量硬凑第三条。

评分考虑：题意匹配、数据匹配、可验证性、可解释性、实现难度、创新性、论文表达潜力和风险。

---

## ⚙️ 第二阶段：两种解题模式

路线明确后，如果用户尚未指定，AI 必须让用户选择执行模式。

| 模式 | 推荐场景 | 特点 |
|---|---|---|
| **A. 逐题深度求解** | Codex、Claude Code、本地正式比赛 | 每一问都是完整研究循环，做深后再进入下一问 |
| **B. 一次性完整求解** | Chat、队伍前期快速参考 | 沿整题路线连续完成全部问题 |

### A. 逐题深度求解

推荐用于 Codex。

```text
问题 k 原题回查
→ 上下关联探索
→ 本问探索性研究
→ 最终模型与公式
→ Python 实现
→ 实际运行结果
→ 验证
→ 代码解析
→ 本问资料 / 文献
→ 本问最终答案
→ 向下一问交接
```

如果实际运行结果推翻原路线，允许触发：

```text
ROUTE_REOPEN_REQUIRED
```

重新比较方法，而不是因为“已经锁定”就硬做下去。

### B. 一次性完整求解

适合快速获取整题参考，但质量底线不降低：仍要求各问模型、Python、真实结果、验证和上下问接口完整。

---

## ✅ 原题逐条回查

全部问题完成后，AI 必须重新读取原题并建立 Requirement Traceability：

| 原题要求 | 对应问题 | 最终结果 | 对应代码 / 输出 | 是否完整回答 |
|---|---|---|---|---|

重点防止：

- 做了很多模型，却漏答原题；
- 漏掉某个子要求；
- 单位或边界条件没处理；
- 问题之间结果没有真正传递；
- 最终结论超过模型能够支持的范围。

---

## 📚 文献、数据和参数必须真实

Skill 明确禁止：

- 编造题名、作者、年份、DOI；
- 猜测或拼接 URL；
- 把搜索结果页当正式来源；
- 没读全文却声称读过全文；
- 页面能打开就声称全文可下载；
- 给外部参数编一个“文献常用范围”。

文献访问状态严格区分：

```text
PAGE_VERIFIED
DOWNLOAD_VERIFIED
METADATA_ONLY
PAYWALLED
DOWNLOAD_UNVERIFIED
BROKEN_LINK
REJECTED
```

只有经过实际核验的全文下载入口才能标记为 `DOWNLOAD_VERIFIED`。重要来源无法可靠获取时必须反馈用户，不能用假链接补洞。

---

## 📈 图表规则

建模中的预测图、误差图、敏感性图、热力图、路径图、网络图、Pareto 图、仿真图等默认全部由 **Python** 根据真实数据和模型结果生成。

目标：**论文可用、专业、清晰，但不过度设计。**

用户没有明确提出图片生成需求时，不主动使用 AI 图片生成工具。

---

## 📦 最终四包交付

```text
题目详解.zip
参考论文.zip
源码.zip
其他.zip
```

### 题目详解.zip

按实际子问题生成 Markdown 教程，并把：

```text
题意 → 模型 → 公式 → 数据 → Python 文件 / 函数 → 运行 → 输出 → 验证
```

完整串起来。

### 参考论文.zip

这里的“参考论文”是 **AI 针对本次赛题撰写的完整数学建模成果论文**，不是网上下载的外部论文合集。

默认生成：

```text
数学建模参考论文.docx
数学建模参考论文.pdf
```

### 源码.zip

包含最终 Python、必要数据、依赖、真实图表、表格和中间结果，并按赛题 / 问题编号组织。

### 其他.zip

保存 AI 使用说明、建模决策、路线变化、文献账本、数据来源、链接核验、环境与复现等材料。

---

# 🔎 新增：组员手搓论文后的赛前终稿复审

AI 的参考论文和四包交付完成后，队伍通常还会自己重新组织最终参赛论文。

**组员手搓终稿完成后，可以再次把论文交给 Skill。**

此时进入：

```text
FINAL_PAPER_AUDIT
```

AI 不把它当普通“润色文章”，而是重新对照：

```text
原题
+ 组员最终论文
+ 最终建模路线
+ Python 源码
+ 实际结果
+ 图表 / 表格
+ 可用文献与数据记录
```

至少执行三轮审核：

```text
第一轮：正确性审计
        ↓
第二轮：一致性审计
        ↓
第三轮：语言与格式审计
```

### 会重点检查什么？

不仅是错别字，还包括：

- ❌ 问题一误写成问题二的解法；
- ❌ 某问用了另一问的参数、结果或图表；
- ❌ 模型名称对，但公式写成另一个模型；
- ❌ 思路存在逻辑跳跃或前后矛盾；
- ❌ 对模型结果解释错误；
- ❌ 把相关性写成因果；
- ❌ 公式、下标、不等号、求和范围写错；
- ❌ 参数、单位、百分比、小数点或正负号抄错；
- ❌ 正文数字与 Python 实际结果不一致；
- ❌ 图表与正文结论不一致；
- ❌ 摘要、正文、结论使用了不同结果；
- ❌ 原题某个子要求被漏掉；
- ❌ 错别字、病句、术语、编号、图号、表号错误；
- ❌ 参考文献引用位置或元数据写错；
- 以及其他可能导致论文失分的真实问题。

问题分为：

| 等级 | 含义 |
|---|---|
| 🔴 **P0** | 致命问题：答非所问、模型/核心结果错误，不建议直接提交 |
| 🟠 **P1** | 重大问题：思路、解释、公式、跨问逻辑等明显错误 |
| 🟡 **P2** | 一般问题：单位、图表引用、严谨性、表达歧义等 |
| ⚪ **P3** | 文字与格式：错别字、病句、标点、编号等 |

默认输出：

```text
最终论文审核报告.md
```

AI 默认只指出问题和修改建议，**不会直接把队伍手搓论文整篇改成 AI 风格**。只有用户明确要求时才生成修订版。

修订后还可以再次提交，进行二审并输出：

```text
已解决 / 未解决 / 新增问题
```

---

## ⚡ Quick Start

```bash
git clone https://github.com/zhu-hailin/cumcm-modeling-analyst.git
```

核心入口：

```text
SKILL.md
```

推荐首次使用：

```text
使用 cumcm-modeling-analyst 分析这道数学建模赛题。
先完整读取题目和附件，完成探索性研究、逐问方案比较和整题路线推荐。
路线明确后让我选择逐题深度求解或一次性完整求解。
```

Codex / Claude Code 正式比赛深挖：

```text
第一阶段完成后选择逐题深度求解。
每问都要完成上下关联探索、Python 实现、实际结果验证、代码解析和本问资料整理。
```

组员最终论文写完后：

```text
进入最终论文复审。请重新对照原题、最终模型、源码和实际结果，检查这份终稿的所有错误。
```

---

## 📁 关键文件

```text
.
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── STAGE1_STRATEGY_BRIEF_TEMPLATE.md
│   ├── QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md
│   ├── STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md
│   └── FINAL_PAPER_AUDIT_TEMPLATE.md
└── references/
    ├── exploratory-research.md
    ├── solve-modes.md
    ├── source-verification-policy.md
    ├── reference-paper-writing.md
    ├── final-delivery-packaging.md
    └── final-paper-audit.md
```

---

## 🎯 设计原则

**先深读题，再选模型。**  
**先探索数据，再给方案评分。**  
**模型是分析结果，不是分析起点。**  
**各问必须形成真实的问题链。**  
**真实运行结果可以推翻原路线。**  
**最终必须重新回查原题。**  
**数据、参数、文献和链接必须可核验。**  
**组员最终论文也必须重新接受一次正确性审计。**

---

## 🔍 Search Keywords

CUMCM · 数学建模 · 数学建模国赛 · Mathematical Modeling · Mathematical Modeling Competition · AI Skill · Agent Skill · Codex · Claude Code · Python Modeling · Exploratory Data Analysis · EDA · Model Selection · Optimization · Prediction · Time Series · Simulation · Operations Research · Literature Verification · Sensitivity Analysis · Robustness Analysis · Paper Review

---

<div align="center">

### ⭐ 如果这个项目对你有帮助，欢迎 Star

如果你在真实赛题中发现流程会让 AI **误解题意、错误选模、忽略跨问关系、编造来源、漏答原题或错误审查论文**，Issue / PR 都非常欢迎。

</div>