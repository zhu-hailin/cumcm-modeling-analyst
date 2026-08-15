> **⚠️ 禁止直接提交 AI 生成的论文。参赛队员应该详细核查并重写论文。**

<div align="center">

<img src="assets/readme.png" alt="CUMCM Modeling Analyst" width="100%" />

# 🏆 CUMCM Modeling Analyst

### 面向数学建模竞赛的 AI Skill · Codex · Claude Code 工作流

![CUMCM](https://img.shields.io/badge/CUMCM-Mathematical_Modeling-orange?style=flat-square)
![Skill](https://img.shields.io/badge/AI-Skill-blueviolet?style=flat-square)
![Codex](https://img.shields.io/badge/Codex-Ready-black?style=flat-square)
![Claude Code](https://img.shields.io/badge/Claude_Code-Ready-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-Modeling-yellow?style=flat-square)

**深度读题 · 探索性研究 · 证据选模 · Python 实跑 · Evidence-first Figure · Run Ledger · 终稿复审**

> **对话要轻，研究要深。像朋友一样说话，像研究者一样做事。**

</div>

---

## 🌟 这是什么？

`cumcm-modeling-analyst` 是一个面向 **CUMCM 及同类数学建模竞赛** 的赛时协作 Skill，重点适配能够读取附件、编写代码并在本地执行 Python 的 **Codex、Claude Code** 等 Agent。

它不是“看到预测就套 ARIMA、看到评价就套 TOPSIS”的模型词典，也不是一次性输出几千字然后结束。

它更像一个陪队伍一起比赛的 **建模学长 / 指导老师 / 研究搭档**：后台认真读题、做 EDA、比较方案、写代码、跑实验、验证结果；聊天窗口只说真正影响决策的结论、风险和下一步。

```text
赛题 + 附件
    ↓
深度读题 / 数据审计
    ↓
探索性研究 / baseline
    ↓
逐问候选模型 + 证据评分
    ↓
整题路线确认
    ↓
Python 正式求解 + Final Run
    ↓
Evidence-first Figure + 验证
    ↓
原题逐条回查
    ↓
内部四包
    ↓
队员人工重写论文
    ↓
终稿一致性复审
```

---

## ✨ 核心能力

| 能力 | 做什么 |
|---|---|
| 🧠 **深度读题** | 拆动作词、边界、单位、附件、各问依赖，不靠关键词套模型 |
| 🔬 **探索性研究** | 用 Python 做 EDA、baseline、趋势、缺失/异常、可行性和模型前提验证 |
| 📊 **证据选模** | 比较真正有差异的候选方法，并根据探索证据更新推荐 |
| 🧩 **跨问建模** | 检查上一问输出如何真实进入下一问，避免模型拼盘 |
| 🧪 **Python 实跑** | 最终结论必须来自真实运行，而不是聊天记忆或手写数字 |
| 🧾 **Run Ledger** | 为关键运行建立 `Run ID`，明确哪个运行才是最终结果 |
| 📈 **Evidence-first Figure** | 先定义“这张图要证明什么”，再决定画什么 |
| 🔎 **Panel QA** | 正式图逐 panel 检查结论、数据、不确定性、中文、单位和论文尺寸 |
| 📚 **真实文献与数据** | 核验 DOI、链接、全文、参数和数据来源，禁止编造 |
| ✅ **原题回查** | 全题完成后逐条映射原题要求 → 结果 → 代码 / 输出 |
| 🔁 **Consistency Sweep** | 检查数值、单位、术语、图表、摘要、正文和结论是否漂移 |
| 📦 **内部四包** | 题目详解 / 参考论文 / 源码 / 其他，供队伍复核和人工写论文 |
| 🔍 **终稿复审** | 检查错别字、串题、公式、解法、结果、图表和解释错误 |

---

## 🤝 三天比赛里，更像队友而不是流程机器人

底层研究流程仍然严格，但聊天默认只说：

```text
我刚做了什么
→ 最重要的发现
→ 这个发现有什么用
→ 我建议下一步怎么走
```

完整公式、实验、文献、代码解释和图表证据全部沉淀到 Markdown。

**聊天变短，不代表研究缩水。**

---

## 🔬 Stage 1：先看数据，再决定模型

第一阶段允许并鼓励轻量探索：缺失/异常、描述统计、趋势/季节性、相关性、可行域、baseline、聚类倾向和候选模型前提小实验。

每问后台执行：

```text
核心问题
→ 探索证据
→ 2–3 个真实候选方法
→ 100 分推荐指数
→ 首选 / 备用 / 切换条件
```

聊天里只汇报每问推荐方法、理由、风险和整题主路线；完整分析进入 Markdown。

---

## 🚦 每一问完成后：推进，还是继续研究？

只有本问核心流程已经完整闭环后，才允许做扩展研究。

继续前必须回答：

1. **研究什么？**
2. **为什么值得？**
3. **可能改变什么决策？**
4. **什么时候停止？**

合法结局：

```text
MEANINGFUL_FINDING
NO_MEANINGFUL_FINDING
INCONCLUSIVE
```

**没有新发现不是失败。** 宁愿明确说没有，也不为了显得深入去制造模型、规律、图表和创新点。

---

## 🧾 Run Ledger：最终结果来自哪一次运行？

建议维护：

```text
其他/运行与实验/
├── RUN_LEDGER.md
└── runs/
    ├── R001.md
    ├── R002.md
    └── ...
```

关键运行状态：

```text
EXPLORATORY / BASELINE / CANDIDATE / FINAL
VALIDATION / REJECTED / SUPERSEDED
```

每个问题完成前必须明确：

```text
FINAL_RUN_ID = Rxxx
```

最终数字、预测、排名、路径、参数、表格和正式图表优先从 Final Run 或关联 Validation Run 读取。随机算法记录种子策略和重复规则，禁止挑最好看的一次结果。

---

## 📈 Evidence-first Figure：图是证据，不是装饰

正式 A/B 级图在写代码前先建立 Figure Contract：

```text
核心结论
→ Hero Evidence
→ Supporting Evidence
→ 每个 panel 的唯一任务
→ 源数据 / Run ID
→ 不确定性定义
→ 评阅风险
→ 再开始画图
```

A/B/C 分级：

- **A 级**：核心结果图——最终得到了什么？
- **B 级**：诊断 / 验证图——为什么相信？
- **C 级**：EDA / 调试图——服务探索和选模。

不规定每问至少几张图。严禁为了图更漂亮或结果更有利而静默删数据、隐藏失败随机种子、只挑有利场景。

正式 Figure 必须逐 panel 检查数据完整性、不确定性、中文、单位、标签碰撞、A4 尺寸可读性和 `Run ID` 一致性。

---

## 🔗 从代码到论文，形成真正的证据链

```text
原题要求
↕
最终模型 / 参数
↕
FINAL_RUN_ID
↕
Python / 输入数据 / 输出表
↕
VISUALIZATION_MANIFEST.md
↕
论文图表
↕
正文结论
```

如果 Final Run 被新运行替代，关联旧图、旧表和旧结论都应该视为潜在失效。

---

## 🌐 正式比赛与旧题测试：双联网模式

| 模式 | 用途 | 联网规则 |
|---|---|---|
| `LIVE_RESEARCH_MODE` | 正式比赛 | 正常查论文、数据、参数、标准、算法和领域案例 |
| `BLIND_BENCHMARK_MODE` | 历年旧题测试 | 禁止用题号、题名、原文、附件特征定位历史答案 |

旧题盲测仍可去题目标识化地搜索通用理论、原始方法论文、官方数据和库文档。

如果意外命中完整历史答案：

```text
ANSWER_LEAKAGE_DETECTED
```

必须立即停止继续读取，本次测试不再声称完全独立。

---

## ⚙️ Stage 2：两种求解方式

| 模式 | 更适合 | 特点 |
|---|---|---|
| **逐题深度求解** | Codex / Claude Code / 正式比赛 | 一问一问做深，每问形成完整 Final Run 和证据链 |
| **一次性完整求解** | Chat / 前期快速参考 | 连续完成整题，但每问仍保留模型、代码、验证和上下问接口 |

真实运行推翻原路线时允许触发：

```text
ROUTE_REOPEN_REQUIRED
```

---

## ✅ Final Consistency Sweep：防止论文越改越乱

AI 参考论文、组员终稿以及重大结果修改后，会检查：

- 同一个数字出现不同版本 / 精度；
- 单位漂移；
- 模型名、术语、参数名漂移；
- 问题 1 写成问题 2 的解法；
- 图已经重跑，正文还解释旧图；
- 强结论超过真实证据；
- 复制旧段落留下旧模型、旧数字、旧图号。

重大冲突：

```text
CROSS_ARTIFACT_CONSISTENCY_FAILED
```

P0 / P1 修改后必须沿链重新同步：

```text
模型 / 参数 → Python 重跑 → Final Run → 图表 / 表格 → 教程 → 摘要 / 正文 / 结论 → 再审
```

---

## 📚 文献、数据、参数必须真实

禁止编造题名、作者、年份、DOI、URL、下载状态、参数来源和外部数据。

链接状态区分：

```text
PAGE_VERIFIED
DOWNLOAD_VERIFIED
METADATA_ONLY
PAYWALLED
DOWNLOAD_UNVERIFIED
BROKEN_LINK
REJECTED
```

只有真实验证过全文入口才能标记 `DOWNLOAD_VERIFIED`。

---

## 🧮 Markdown / Word / PDF 公式都要正确

教程 Markdown：行内 `$...$`，独立 `$$...$$`；关键公式解释变量、单位、上下标、作用和代码对应。

最终 Word / PDF：禁止出现未经渲染的 LaTeX 源码，Word 优先 OMML / Office 原生数学公式，符号说明表也必须正确渲染。

```text
FORMULA_DOCUMENTATION_FAILED
FORMULA_RENDERING_FAILED
```

---

## 📦 内部四包，不等于官方提交

```text
题目详解.zip
参考论文.zip
源码.zip
其他.zip
```

`题目详解.zip` 串起题意 → 模型 → 公式 → 数据 → Python → Final Run → 输出 → 图表 → 验证。

`参考论文.zip` 包含 AI 针对本次赛题撰写的内部参考论文 `.docx + .pdf`，**禁止直接提交**。

`源码.zip` 保存最终 Python、必要数据、依赖、真实图表、结果表和中间产物。

`其他.zip` 保存 Run Ledger、AI 使用日志、建模决策、路线变化、文献/数据来源、赛时协作和复现材料。

Codex / Claude Code 本地模式以项目根目录真实成果目录为主，ZIP 只是副本；Chat / 云端模式加强下载与压缩包兼容性验收。

---

## 🔎 队员写完论文，再交回来终审

终稿审核重新对齐：

```text
原题 + FINAL_RUN_ID + 最终模型 / 代码
+ 图表 / 表格 + Visualization Manifest + 组员终稿
```

至少执行：

```text
正确性审计 → 跨成果一致性审计 → 语言与格式审计
```

默认输出 `最终论文审核报告.md`。

---

## 🧭 Manifest Router：规则很多，但不会开局全塞进上下文

v10 新增根目录 `manifest.yaml`。开题只加载最核心规则，到了不同阶段再按需读取：

```text
EDA → exploratory-research
绘图 → python-visualization + figure-evidence-contract
公式 → equation-rendering
文献 → source-verification
运行 → model-run-ledger
论文 → reference-paper-writing + consistency-sweep
终稿 → final-paper-audit
官方提交 → official-submission-policy
```

减少 Codex 上下文负担，但**按需加载绝不能成为跳过质量规则的理由**。

---

## ⚡ Quick Start

```bash
git clone https://github.com/zhu-hailin/cumcm-modeling-analyst.git
```

然后直接告诉 Agent：

```text
使用 cumcm-modeling-analyst 分析这道数学建模赛题。
```

正式比赛：

```text
这是实战赛题，按实战研究模式进行。
```

旧题测试：

```text
这是旧题盲测，不允许搜索或读取这道题的历史答案。
```

比赛过程中正常交流即可，例如：

```text
这一问还值得继续研究吗？
这个结果为什么能信？
问题二最终用的是哪一次 Run？
这问够了就继续下一问。
```

---

## 📁 关键结构

```text
.
├── SKILL.md
├── manifest.yaml
├── README.md
├── CHANGELOG.md
├── agents/openai.yaml
├── assets/
│   ├── readme-intro.svg
│   ├── QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md
│   ├── STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md
│   ├── RUN_LEDGER_TEMPLATE.md
│   └── FINAL_PAPER_AUDIT_TEMPLATE.md
└── references/
    ├── competition-collaboration.md
    ├── search-mode-policy.md
    ├── exploratory-research.md
    ├── model-run-ledger.md
    ├── figure-evidence-contract.md
    ├── python-visualization-policy.md
    ├── final-consistency-sweep.md
    ├── source-verification-policy.md
    ├── equation-rendering-policy.md
    ├── reference-paper-writing.md
    ├── final-delivery-packaging.md
    └── final-paper-audit.md
```

---

## 🎯 设计原则

**先读懂题，再选模型。**  
**先看数据，再给方案评分。**  
**模型是分析结果，不是分析起点。**  
**对话要轻，研究要深。**  
**像朋友一样说话，像研究者一样做事。**  
**没有新发现可以，禁止为了研究而制造研究。**  
**每个关键结果都要知道它来自哪一次 Run。**  
**每张正式图都要知道它在证明什么。**  
**论文里的数字、图、表、模型和结论必须能互相追溯。**  
**旧题盲测不能偷看历史答案。**  
**数据、参数、文献和链接必须可核验。**  
**AI 论文禁止直接提交，必须由队员理解、核查并重写。**

---

## 🔍 Search Keywords

CUMCM · 数学建模 · Mathematical Modeling · AI Skill · Agent Skill · Codex · Claude Code · Python Modeling · EDA · Model Selection · Evidence-first Figure · Run Ledger · Experiment Tracking · Visualization QA · Optimization · Prediction · Simulation · Literature Verification · Sensitivity Analysis · Robustness Analysis · Blind Benchmark · Paper Review

---

<div align="center">

### ⭐ 如果这个项目对你有帮助，欢迎 Star

如果你在真实赛题中发现流程会让 AI **误解题意、错误选模、无意义研究、混用旧 Run、画错图、忽略跨问关系、编造来源、漏答原题、泄漏旧题答案或错误审查论文**，Issue / PR 都非常欢迎。

</div>
