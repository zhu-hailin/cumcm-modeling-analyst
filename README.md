> **⚠️ 禁止直接提交 AI 生成的论文。参赛队员应该详细核查并重写论文。**

<div align="center">

<img src="assets/readme-intro.svg" alt="CUMCM Modeling Analyst" width="100%" />

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

## 🌟 它是什么？

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

## ✨ 现在它能做什么？

| 能力 | 做什么 |
|---|---|
| 🧠 **深度读题** | 拆动作词、边界、单位、附件、各问依赖，不靠关键词套模型 |
| 🔬 **探索性研究** | 用 Python 做 EDA、baseline、趋势、缺失/异常、可行性和模型前提验证 |
| 📊 **证据选模** | 每问比较真正有差异的候选方法，并根据实际探索证据更新推荐 |
| 🧩 **跨问建模** | 检查上一问输出如何真实进入下一问，避免模型拼盘 |
| 🧪 **Python 实跑** | 最终结论必须来自真实运行，而不是靠聊天里的记忆或手写数字 |
| 🧾 **Run Ledger** | 为关键运行建立 `Run ID`，明确哪个运行才是本问最终结果 |
| 📈 **Evidence-first Figure** | 先定义“这张图要证明什么”，再决定画什么，而不是一个表画一张图 |
| 🔎 **Figure / Panel QA** | 正式图逐 panel 检查结论、数据、不确定性、中文、单位、碰撞和论文尺寸 |
| 📚 **真实文献与数据** | 核验题名、DOI、链接、全文下载状态、参数和数据来源，禁止编造 |
| ✅ **原题回查** | 全题完成后逐条映射原题要求 → 结果 → 代码/输出 |
| 🔁 **Consistency Sweep** | 检查数值、单位、术语、模型名、图表、摘要、正文和结论是否漂移 |
| 📦 **内部四包** | 题目详解 / 参考论文 / 源码 / 其他，供队伍学习、复核和人工写论文 |
| 🔍 **终稿复审** | 组员手搓论文后重新检查错别字、串题、公式、解法、结果和解释错误 |

---

## 🤝 三天比赛里，不想再和一个“流程机器人”聊天

Skill 的底层流程依然严格，但不会把 SOP 全部甩到聊天窗口。

聊天默认只说：

```text
我刚做了什么
→ 最重要的发现
→ 这个发现有什么用
→ 我建议下一步怎么走
```

例如：

> 我刚把问题二的三个方案都跑完了。现在随机森林虽然平均指标不是最高，但稳定性明显更好，这对后面问题三更有用。完整实验和评分我已经放到 Markdown 里了。
>
> 这一问现在可以直接推进。如果你们还想多研究一轮，我建议只查一个点：不同特征组合会不会改变排名；没变化就马上停，不继续堆实验。

**聊天变短，不代表研究缩水。** 复杂公式、完整实验、文献、代码解释和图表证据全部沉淀到文件里。

---

## 🔬 Stage 1：先看数据，再决定模型

第一阶段禁止直接进入最终生产实现，但允许并鼓励轻量探索：

- 工作表 / 字段 / 样本量 / 时间空间范围；
- 缺失、重复、异常、单位和编码；
- 描述统计、必要可视化；
- 趋势、季节性、自相关、结构突变；
- 相关性 / 共线性；
- 聚类倾向、图结构、可行域、计算规模；
- baseline；
- 候选模型关键前提的小实验。

每问后台执行：

```text
核心问题
→ 探索证据
→ 2–3 个真实候选方法
→ 100 分推荐指数
→ 首选 / 备用 / 切换条件
```

聊天里只汇报：

```text
问题1：推荐什么，为什么
问题2：推荐什么，风险在哪
问题n：如何承接前面结果
整题：主路线是什么
```

完整分析进入 Markdown。

---

## 🚦 每一问完成后：推进，还是继续研究？

只有本问原有核心流程全部完成后，才允许继续扩展研究。

继续研究前必须回答：

1. **研究什么？**
2. **为什么值得？**
3. **可能改变什么决策？**
4. **什么时候停止？**

说不清楚，就不继续。

合法结局包括：

```text
MEANINGFUL_FINDING
NO_MEANINGFUL_FINDING
INCONCLUSIVE
```

没有新发现不是失败。**宁愿明确说没有，也不为了显得深入去制造模型、规律、图表和创新点。**

---

## 🧾 Run Ledger：最终结果到底来自哪一次运行？

三天比赛里最容易出现的问题之一是：模型不断修改，结果不断重跑，最后论文、图表和 CSV 拿了不同版本。

v10 开始建议维护：

```text
其他/运行与实验/
├── RUN_LEDGER.md
└── runs/
    ├── R001.md
    ├── R002.md
    └── ...
```

关键运行分为：

```text
EXPLORATORY
BASELINE
CANDIDATE
FINAL
VALIDATION
REJECTED
SUPERSEDED
```

每个问题完成前必须明确：

```text
FINAL_RUN_ID = Rxxx
```

最终数字、预测、排名、路径、参数、表格和正式图表优先从该 Final Run 或关联 Validation Run 读取。

随机算法需要记录种子策略、重复次数和代表结果选择规则，禁止只挑最漂亮的一次结果。

---

## 📈 Evidence-first Figure：图是证据，不是装饰

正式 A/B 级图在写代码前先建立 Figure Contract：

```text
核心结论
→ 图的角色
→ Hero Evidence
→ Supporting Evidence
→ 每个 panel 的唯一任务
→ 源数据 / Run ID
→ 不确定性定义
→ 评阅风险
→ 再开始画图
```

### A / B / C 分级

- **A 级**：核心结果图——最终得到了什么？
- **B 级**：诊断 / 验证图——为什么相信？
- **C 级**：EDA / 调试图——只服务探索和选模。

不规定每问至少几张图。删除一张图不影响理解、验证和决策时，它大概率只是装饰。

### 数据完整性门

严禁为了让图更漂亮或结果更有利而静默：

- 删除不喜欢的数据；
- 只挑表现好的年份；
- 删除失败随机种子；
- 隐藏异常场景；
- 只展示有利模型。

合理排除必须记录前后数量、规则、理由和对结论的影响。

### Panel-by-panel QA

正式 Figure 不只看整图“好不好看”，还要逐 panel 检查：

- 这个 panel 是否有唯一证据作用；
- 数据是否完整；
- 不确定性是否正确；
- 中文、单位、图例是否完整；
- 标签是否碰撞 / 裁切；
- A4 论文尺寸下是否仍可读；
- 是否属于正确 `Run ID`。

中文论文候选图默认中文，普通 DataFrame 优先 `CSV/XLSX → Word 原生表格`，不默认截图。

---

## 🔗 从代码到论文，形成真正的证据链

现在正式结果希望能够追到：

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

Visualization Manifest 记录：

```text
图号 / 文件 / 问题 / 等级 / Run ID
数据源 / 生成代码 / 支撑结论 / 是否进入论文
```

如果某个 Final Run 被新运行替代，关联的旧图、旧表和旧结论就应该被视为潜在失效，而不是继续混用。

---

## 🌐 正式比赛与旧题测试：双联网模式

| 模式 | 用途 | 联网规则 |
|---|---|---|
| `LIVE_RESEARCH_MODE` | 正式比赛 | 正常查论文、数据、参数、标准、算法和领域案例 |
| `BLIND_BENCHMARK_MODE` | 历年旧题测试 | 禁止用题号、题名、原文、附件特征定位历史答案 |

旧题盲测仍可以去题目标识化地搜索通用理论、原始方法论文、官方数据和库文档。

如果意外命中完整历史答案：

```text
ANSWER_LEAKAGE_DETECTED
```

必须立即停止继续读取，本次测试不再声称完全独立。

独立求解结束后，经用户同意可进入 `POST_SOLUTION_COMPARISON`，再与历史优秀论文比较。

---

## ⚙️ Stage 2：两种求解方式

| 模式 | 更适合 | 特点 |
|---|---|---|
| **逐题深度求解** | Codex / Claude Code / 正式比赛 | 一问一问做深，每问形成完整 Final Run 和证据链 |
| **一次性完整求解** | Chat / 前期快速参考 | 连续完成整题，但每问仍保留模型、代码、验证和上下问接口 |

真实运行推翻原路线时允许：

```text
ROUTE_REOPEN_REQUIRED
```

重新比较方案，而不是因为“前面已经选了”就硬做。

---

## ✅ Final Consistency Sweep：防止论文越改越乱

在 AI 参考论文、组员终稿、重大结果修改后，重新做跨成果一致性扫描。

重点检查：

- 同一个数字在摘要 / 正文 / 表格中出现不同版本；
- 同一指标精度前后不一致；
- 同一个量一会儿 `km` 一会儿 `m`；
- 模型名 / 参数名 / 符号漂移；
- 问题 1 写成问题 2 的解法；
- 图已经重跑，正文还解释旧图；
- “始终最好 / 稳定 / 显著 / 全局最优”等强结论超过证据；
- 复制旧段落后留下旧模型、旧数字、旧图号。

重大冲突：

```text
CROSS_ARTIFACT_CONSISTENCY_FAILED
```

P0 / P1 修改后执行 Ripple Check：

```text
模型 / 参数
→ Python 重跑
→ Final Run
→ 图表 / 表格
→ 教程
→ 摘要 / 正文 / 结论
→ 再审
```

不能只在 Word 里改一个数字就当修好了。

---

## 📚 文献、数据和参数必须真实

明确禁止：

- 编造题名、作者、年份、DOI；
- 猜测或拼接 URL；
- 没读全文却说读过全文；
- 页面能打开就说全文可下载；
- 给参数编一个“文献常用范围”；
- 把假设、推断和外部事实混在一起。

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

教程 Markdown：

- 行内公式：`$...$`
- 独立公式：`$$...$$`
- 每个关键公式解释变量、单位、上下标、作用和代码对应。

最终 Word / PDF：

- 禁止出现未经渲染的 `x_{icst}`、`\\sum`、`\\frac` 等源码；
- Word 优先 OMML / Office 原生数学公式；
- 符号说明表也必须正确渲染。

失败状态：

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

### `题目详解.zip`

每问教程把：

```text
题意 → 模型 → 公式 → 数据 → Python → Final Run → 输出 → 图表 → 验证
```

完整串起来。

### `参考论文.zip`

AI 针对本次赛题写出的内部参考论文：

```text
数学建模参考论文.docx
数学建模参考论文.pdf
```

**禁止直接提交。** 队员必须理解、核查并人工重写。

### `源码.zip`

最终 Python、必要数据、依赖、真实图表、结果表和中间产物。

### `其他.zip`

包括：

- `RUN_LEDGER.md` 与重要运行记录；
- AI 使用日志；
- 建模决策和路线变化；
- 文献 / 数据来源；
- 赛时协作记录；
- 环境与复现材料。

Codex / Claude Code 本地模式以项目根目录真实成果目录为主，ZIP 只是副本；Chat / 云端模式则加强下载与压缩包兼容性验收。

---

## 🔎 队员写完论文，再交回来终审

终稿审核重新对齐：

```text
原题
+ FINAL_RUN_ID
+ 最终模型 / 代码
+ 图表 / 表格
+ Visualization Manifest
+ 组员终稿
```

至少执行：

```text
正确性审计
→ 跨成果一致性审计
→ 语言与格式审计
```

重点检查但不限于：串题、解法写错、公式参数错误、结果不一致、旧图、解释错误、相关写成因果、漏答、错别字、图号表号和引用问题。

默认输出：

```text
最终论文审核报告.md
```

---

## 🧭 Manifest Router：规则很多，但不会开局全塞进上下文

v10 新增根目录：

```text
manifest.yaml
```

开题只加载最核心的赛时协作、搜索模式和两阶段工作流。

到了不同阶段，再按需读取：

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

这样可以减少 Codex 上下文负担，但**按需加载绝不能成为跳过质量规则的理由**。

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

比赛过程中不需要背提示词，正常交流即可：

```text
这一问还值得继续研究吗？
```

```text
这个结果为什么能信？
```

```text
问题二现在最终用的是哪一次 Run？
```

```text
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
├── agents/
│   └── openai.yaml
├── assets/
│   ├── STAGE1_STRATEGY_BRIEF_TEMPLATE.md
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
**真实结果可以推翻原路线。**  
**旧题盲测不能偷看历史答案。**  
**数据、参数、文献和链接必须可核验。**  
**AI 论文禁止直接提交，必须由队员理解、核查并重写。**

---

## 🔍 Search Keywords

CUMCM · 数学建模 · 数学建模国赛 · Mathematical Modeling · Mathematical Modeling Competition · AI Skill · Agent Skill · Codex · Claude Code · Python Modeling · EDA · Model Selection · Evidence-first Figure · Run Ledger · Experiment Tracking · Visualization QA · Optimization · Prediction · Time Series · Simulation · Operations Research · Literature Verification · Sensitivity Analysis · Robustness Analysis · Blind Benchmark · Paper Review

---

<div align="center">

### ⭐ 如果这个项目对你有帮助，欢迎 Star

如果你在真实赛题中发现流程会让 AI **误解题意、错误选模、无意义研究、混用旧 Run、画错图、忽略跨问关系、编造来源、漏答原题、泄漏旧题答案或错误审查论文**，Issue / PR 都非常欢迎。

</div>
