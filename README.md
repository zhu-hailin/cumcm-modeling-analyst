> **⚠️ 禁止直接提交 AI 生成的论文。参赛队员应该详细核查并重写论文。**

<div align="center">

<img src="assets/readme.png" alt="CUMCM Modeling Analyst" width="100%" />

# CUMCM Modeling Analyst

面向数学建模竞赛的 AI Skill，适配 Codex、Claude Code 等能够读取附件、编写代码并在本地运行 Python 的 Agent。

![CUMCM](https://img.shields.io/badge/CUMCM-Mathematical_Modeling-orange?style=flat-square)
![Skill](https://img.shields.io/badge/AI-Skill-blueviolet?style=flat-square)
![Codex](https://img.shields.io/badge/Codex-Ready-black?style=flat-square)
![Claude Code](https://img.shields.io/badge/Claude_Code-Ready-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-Modeling-yellow?style=flat-square)

</div>

---

## 这个 Skill 做什么

数学建模比赛最麻烦的地方通常不是“不会写一个模型名字”，而是题目没读透、附件没看清、不同小问之间接不上，或者代码已经改了，论文和图表还停在旧版本。

这个 Skill 主要处理这些问题。

它会先读题和附件，再做必要的数据探索。模型不是看到关键词就直接套，而是结合题意、数据特征和小规模实验来选。路线确认后再进入正式求解，代码实际运行，关键结果留下 Run 记录，图表和论文也能追到对应的数据和代码。

比赛过程中，聊天窗口尽量只说真正需要队员知道的东西。完整公式、实验、评分、文献和代码说明写进 Markdown，不把所有研究过程一股脑塞进对话里。

```text
赛题 + 原始附件
    ↓
深度读题 / 数据审计
    ↓
探索性研究 / baseline
    ↓
逐问候选方法 + 证据评分
    ↓
整题路线确认
    ↓
Python 正式求解 + Final Run
    ↓
结果验证 + Evidence-first Figure
    ↓
原题逐条回查
    ↓
内部四包
    ↓
队员人工重写论文
    ↓
终稿复审
```

---

## 主要能力

| 能力 | 作用 |
|---|---|
| 深度读题 | 拆动作词、边界、单位、附件和各问依赖，不靠关键词套模型 |
| 探索性研究 | 用 Python 做 EDA、baseline、趋势、异常、可行性和模型前提检查 |
| 证据选模 | 比较真正有差异的方法，并根据探索结果更新推荐 |
| 跨问建模 | 明确上一问的哪些结果会进入下一问，避免各问各做各的 |
| Python 实跑 | 最终数字来自真实运行，不从聊天记忆或旧截图里抄 |
| Run Ledger | 记录关键运行，明确每一问最终采用哪一次 Run |
| Evidence-first Figure | 先确定图要说明什么，再决定画什么 |
| 图表 QA | 检查数据完整性、中文、单位、标签、尺寸和 Run 版本 |
| 文献与数据核验 | 核验 DOI、链接、全文、参数和数据来源 |
| 原题回查 | 做完后重新逐条核对题目有没有真的回答完整 |
| Consistency Sweep | 查数字、单位、模型名、图表、摘要、正文和结论有没有串版本 |
| 终稿复审 | 检查错别字、公式、思路、解释、串题、结果和图表错误 |

---

## 比赛时怎么交流

AI 可以做很多后台工作，但不需要每次都把几十段分析贴出来。

一问做完后，聊天里通常只需要说明：刚完成了什么、最重要的发现是什么、这个发现有什么用、下一步建议怎么走。想看细节时，再去对应的 Markdown、源码和结果文件里看。

如果这一问已经够了，就推进。还有值得验证的地方，再继续一轮。继续研究必须有明确目的，不能为了“显得研究很多”去堆模型和图。

没有新发现也很正常。比起硬编一个所谓创新点，直接说“这轮没有发现值得采用的新东西”更有用。

---

## Codex / Claude Code 会管理本地项目文件

如果使用的是 Codex、Claude Code 或其他本地 Agent，Skill 要主动把项目目录管理好，不能把脚本、临时 CSV、图片、下载文件和论文素材全部扔在根目录。

但它不会机械照抄固定目录。它会先看你原来的项目结构、题目数量、附件情况和你的命名习惯；你已经指定目录或组织方式时，以你的要求为准。

一个常见的结构大致是：

```text
<project-root>/
├── modeling_workspace/
│   ├── 00_原始输入/
│   │   ├── 赛题原文/
│   │   └── 原始附件/
│   ├── 01_共享资料/
│   │   ├── 清洗后数据/
│   │   ├── 中间数据/
│   │   ├── 文献与来源/
│   │   └── 建模决策/
│   ├── 问题1/
│   │   ├── 研究记录/
│   │   ├── src/
│   │   └── outputs/
│   ├── 问题2/
│   │   └── ...
│   ├── 问题N/
│   │   └── ...
│   └── 最终整合/
│       ├── 最终数据/
│       ├── 图表与表格/
│       ├── 论文素材/
│       └── 最终结果索引.md
└── deliverables/
    ├── 题目详解/
    ├── 参考论文/
    ├── 源码/
    └── 其他/
```

这里有几个底线：

- 原题和官方原始附件单独保留，尽量不改原文件；
- 清洗后的数据另存，不能直接覆盖原始 Excel / CSV；
- 清洗数据要能追到原文件、Sheet、字段和处理步骤；
- 每一问自己的代码和输出尽量放在自己的目录里；
- 最终整合区只收确认过的最终版本；
- `modeling_workspace/` 是工作区，`deliverables/` 是最终内部交付区，两者不要混为一谈；
- 不为了整理目录擅自删除、移动或覆盖用户已有文件。

目录本身不是目的。真正重要的是比赛做到第三天时，队员还能很快找到原题、清洗数据、问题二最终代码，以及哪一组结果才是最终版本。

---

## Stage 1：先看数据，再决定模型

第一阶段可以做轻量 Python 探索，包括缺失和异常检查、描述统计、趋势和季节性、相关性、可行域、baseline、聚类倾向以及候选模型前提的小实验。

每一问会比较真正有差异的候选方法。通常是 2–3 个，但没有必要为了数量硬凑第三个。

评分依然使用统一的 100 分框架，但分数必须有证据、理由和置信度。数据还没看清时只能给暂定判断，不能装得很精确。

---

## 每一问做完后，可以继续，也可以停

“停”不是没做完，而是当前问题已经按原流程完整闭环。

如果还想继续研究，AI 需要先说清楚四件事：研究什么、为什么值得、可能改变什么、什么时候停止。

扩展研究可以得到三种结果：

```text
MEANINGFUL_FINDING
NO_MEANINGFUL_FINDING
INCONCLUSIVE
```

后两种都可以接受。

---

## Run Ledger：别让旧结果混进论文

关键运行会记录 Run ID。每一问结束前需要明确：

```text
FINAL_RUN_ID = Rxxx
```

最终数字、预测、排名、路径、参数、结果表和正式图表，都应该从 Final Run 或关联的 Validation Run 读取。

如果模型重新跑过，旧 Run 会被标成 `SUPERSEDED`，而不是继续混在最后的结果里。随机算法也要记录种子和重复规则，不能跑很多次以后只挑最好看的一次。

---

## Evidence-first Figure：先想清楚图要说明什么

正式图不是“有一个 DataFrame 就画一张”。

A/B 级图在动手之前先明确：核心结论是什么，主证据是什么，每个 panel 的任务是什么，数据来自哪个 Run，不确定性怎么定义。

图分为：

- A 级：核心结果图；
- B 级：诊断和验证图；
- C 级：EDA 和调试图。

图的数量不设最低要求。少一张图不影响理解、验证和决策，那张图通常就没必要画。

正式图还要检查中文字体、坐标轴、单位、标签碰撞、论文缩放后的可读性，以及它是否真的使用了最终 Run 的数据。

---

## 正式比赛和旧题测试分开联网

| 模式 | 用途 | 联网规则 |
|---|---|---|
| `LIVE_RESEARCH_MODE` | 正式比赛 | 正常查论文、数据、参数、标准、算法和领域案例 |
| `BLIND_BENCHMARK_MODE` | 历年旧题测试 | 不用题号、题名、原文、附件特征去定位历史答案 |

旧题盲测仍然可以查通用理论、原始方法论文、官方数据和库文档。

如果意外打开了这道旧题的完整历史解答，会标记：

```text
ANSWER_LEAKAGE_DETECTED
```

这次测试就不能再说是完全独立完成的。

---

## 两种正式求解方式

| 模式 | 更适合 | 特点 |
|---|---|---|
| 逐题深度求解 | Codex / Claude Code / 正式比赛 | 一问一问完成，每问留下 Final Run 和完整证据链 |
| 一次性完整求解 | Chat / 前期快速参考 | 连续做完整题，但各问仍保留模型、代码和验证 |

实际运行如果推翻了前面选的路线，可以重新开路线比较，不会因为“前面已经定了”就硬做下去。

---

## 从代码到论文，结果要能追溯

最终结果链大致是：

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

如果 Final Run 换了，旧图、旧表和旧结论都会重新检查。

---

## 公式不能只“看起来像公式”

Markdown 教程使用标准 LaTeX：行内 `$...$`，独立公式 `$$...$$`。关键公式还要解释变量、单位、上下标、作用和代码对应。

Word / PDF 中不能直接把 `x_{icst}`、`\sum`、`\frac` 当普通字符串塞进去。Word 优先使用 OMML / Office 原生公式，符号说明表里的数学变量也要正确渲染。

---

## 内部四包，不等于官方提交

内部成果固定整理成：

```text
题目详解.zip
参考论文.zip
源码.zip
其他.zip
```

其中 `参考论文.zip` 是 AI 根据本次赛题写的内部参考论文，默认包含 Word 和 PDF。它是给队员理解、核查和手工重写用的，不能直接提交比赛。

Codex / Claude Code 本地运行时，未压缩的真实成果目录是主文件，ZIP 只是整理出来的副本。Chat / 云端交付则会额外检查压缩包兼容性。

---

## 队员写完论文后，再交回来检查

终稿复审不只是改错别字。它会重新对照原题、Final Run、代码、公式、图表、结果表和参考文献，检查：

- 问题一有没有误写成问题二的解法；
- 模型名称和公式是否对得上；
- 参数、单位、小数点和正负号有没有抄错；
- 正文数字和实际 Python 输出是否一致；
- 图表是不是旧版本；
- 摘要、正文和结论有没有各说各的；
- 解释有没有超过数据和模型能支持的范围；
- 错别字、病句、编号和引用问题。

如果模型或关键结果在终审时改了，会沿着代码、Final Run、图表、教程和论文重新同步，不只改一处文字。

---

## 规则按阶段加载

根目录的 `manifest.yaml` 负责按需加载规则。开始一道题时不用把所有 reference 一次性读进上下文。

例如：

```text
EDA → exploratory-research
绘图 → python-visualization + figure-evidence-contract
运行 → model-run-ledger
公式 → equation-rendering
文献 → source-verification
论文 → reference-paper-writing + consistency-sweep
终稿 → final-paper-audit
官方提交 → official-submission-policy
```

按需读取只是减少上下文负担，不会跳过对应质量检查。

---

## Quick Start

```bash
git clone https://github.com/zhu-hailin/cumcm-modeling-analyst.git
```

然后可以直接说：

```text
使用 cumcm-modeling-analyst 分析这道数学建模赛题。
```

正式比赛：

```text
这是实战赛题，按实战研究模式进行。
```

拿旧题测试：

```text
这是旧题盲测，不允许搜索或读取这道题的历史答案。
```

比赛过程中正常交流就行，例如：

```text
这一问还值得继续研究吗？
问题二最后用的是哪一次 Run？
这个结果为什么能信？
这问够了就继续下一问。
```

---

## 关键文件

```text
.
├── SKILL.md
├── manifest.yaml
├── README.md
├── CHANGELOG.md
├── agents/openai.yaml
├── assets/
│   ├── readme.png
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

## Search Keywords

CUMCM · 数学建模 · Mathematical Modeling · AI Skill · Agent Skill · Codex · Claude Code · Python Modeling · EDA · Model Selection · Evidence-first Figure · Run Ledger · Experiment Tracking · Visualization QA · Optimization · Prediction · Simulation · Literature Verification · Sensitivity Analysis · Robustness Analysis · Blind Benchmark · Paper Review

---

<div align="center">

如果这个项目对你有帮助，欢迎 Star。

发现 AI 会误解题意、混用旧 Run、画错图、编造来源、漏答原题或审错论文，也欢迎提 Issue / PR。

</div>