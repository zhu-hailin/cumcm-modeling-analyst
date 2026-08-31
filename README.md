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

数学建模比赛最麻烦的地方通常不是“不会写一个模型名字”，而是题目没读透、附件没看清、不同小问接不上，或者代码已经改了，论文和图表还停在旧版本。

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
当前问题方案讨论与确认
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
| 逐题方案确认 | 每问先讨论，允许队员补论文、数据和想法，确认后再写最终代码 |
| 跨问建模 | 明确上一问的哪些结果会进入下一问，避免各问各做各的 |
| Python 实跑 | 最终数字来自真实运行，不从聊天记忆或旧截图里抄 |
| Run Ledger | 记录关键运行，明确每一问最终采用哪一次 Run |
| Evidence-first Figure | 先确定图要说明什么，再决定画什么 |
| 图表 QA | 检查数据完整性、中文、单位、标签、尺寸和 Run 版本 |
| 文献与数据核验 | 核验 DOI、链接、全文、现实数据、参数和统计口径 |
| 原题回查 | 做完后重新逐条核对题目有没有真正回答完整 |
| Consistency Sweep | 查数字、单位、模型名、图表、摘要、正文和结论有没有串版本 |
| 终稿复审 | 检查错别字、公式、思路、解释、串题、结果和图表错误 |

---

## 比赛时怎么交流

AI 可以做很多后台工作，但不需要每次都把几十段分析贴出来。

每一问先研究方案，再问队员有没有论文、参考文献、额外数据、老师建议或自己的想法。队员确认后，AI 才生成正式代码、Final Run、图表、结果表和问题详解。

一问正式完成后，聊天里通常只需要说明：刚完成了什么、最重要的发现是什么、这个发现有什么用、下一步怎么走。想看细节时，再去对应的 Markdown、源码和结果文件里看。

如果这一问已经够了，就推进。还有值得验证的地方，再继续一轮。继续研究必须有明确目的，不能为了“显得研究很多”去堆模型和图。

没有新发现也很正常。比起硬编一个所谓创新点，直接说“这轮没有发现值得采用的新东西”更有用。

---

## Codex 使用一个单赛题工作空间

Codex 在本地执行时，一个根目录只对应一道已经选定的赛题，例如：

```text
2022-C/
```

不会再额外套一层 `modeling_workspace/`，也不会默认在根目录旁边再建 `deliverables/`。代码、数据、结果、论文和提交材料都在这个单赛题工作空间中按职责归档。

默认结构：

```text
2022-C/
├─ README.md
│
├─ 00_problem/                 # 题目与官方附件
│  ├─ problem.pdf
│  ├─ attachments/
│  └─ official_template/
│
├─ 01_data/                    # 数据
│  ├─ raw/                     # 原始数据，不修改
│  ├─ processed/               # 清洗后的建模数据
│  └─ external/                # 外部补充数据
│
├─ 02_analysis/                # 建模分析与思路
│  ├─ problem_analysis.md
│  ├─ assumptions.md
│  ├─ symbols.md
│  └─ model_plan.md
│
├─ 03_code/                    # 正式代码
│  ├─ common/                  # 公共函数
│  ├─ q1/                      # 问题一
│  ├─ q2/                      # 问题二
│  ├─ q3/                      # 问题三
│  ├─ q4/                      # 问题四，没有就删除
│  └─ run_all.py               # 总运行入口
│
├─ 04_results/                 # 程序生成的结果
│  ├─ figures/                 # 论文图片
│  ├─ tables/                  # 论文表格
│  ├─ data/                    # 数值结果
│  └─ logs/                    # 运行日志
│
├─ 05_paper/                   # 论文
│  ├─ outline.md
│  ├─ draft.docx
│  ├─ final.docx
│  └─ final.pdf
│
├─ 06_submission/              # 最终提交文件
│  ├─ paper.pdf
│  ├─ source_code.zip
│  └─ checklist.md
│
├─ 07_references/              # 查阅的资料和论文
│  ├─ papers/
│  ├─ websites.md
│  └─ notes.md
│
└─ 99_temp/                    # 临时文件，完成后可清空
```

这是一套默认骨架，不要求提前创建所有空文件。实际有几问，就创建几个 `qN/`；没有问题四就删除 `q4/`，超过四问则继续增加。

几个不能混的边界：

- `00_problem/` 保存题目、官方附件和官方模板，不写入程序输出；
- `01_data/raw/` 保存不修改的原始数据；
- 清洗、合并、单位统一和特征构造后的数据进入 `01_data/processed/`；
- 网络补充的真实数据进入 `01_data/external/`，并记录发布机构、链接、日期、口径和用途；
- 每问正式代码进入 `03_code/qN/`，公共函数进入 `03_code/common/`；
- 图、表、数值结果和运行日志统一进入 `04_results/`，不散落在根目录或代码目录；
- AI 第一次生成的论文是内部参考稿，不能直接冒充 `final.docx` / `final.pdf`；
- `06_submission/` 只放经过审核的提交候选和内部打包结果；
- 下载并实际查阅的论文进入 `07_references/papers/`；
- 临时脚本、缓存、转换文件和预览图进入 `99_temp/`，最终成果不能只留在这里。

Codex 会先查看用户已有目录、命名和文件。用户明确指定的结构优先，已有合理工程直接复用，不会为了套模板擅自移动、删除、覆盖或改名原文件。

详细规则见：`references/local-workspace-policy.md`。

---

## Stage 1：先看数据，再决定模型

第一阶段可以做轻量 Python 探索，包括缺失和异常检查、描述统计、趋势和季节性、相关性、可行域、baseline、聚类倾向以及候选模型前提的小实验。

每一问会比较真正有差异的候选方法。通常是 2–3 个，但没有必要为了数量硬凑第三个。

评分依然使用统一的 100 分框架，但分数必须有证据、理由和置信度。数据还没看清时只能给暂定判断，不能装得很精确。

---

## 逐题模式：先讨论，再实现

每一问按下面的节奏推进：

```text
研究本问题意、数据和候选方案
↓
和队员讨论推荐模型、假设、风险和验证方法
↓
询问是否补充论文、数据、老师建议或自己的想法
↓
队员确认当前方案
↓
写正式 Python、执行 Final Run、生成图表和表格
↓
完成本问详解并固化结果
↓
进入下一问
```

用户确认前，可以做 EDA、小规模实验和数据检索，但不能把这些中间代码或结果冒充最终成果。

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

关键运行会记录 Run ID。Codex 默认维护：

```text
04_results/logs/
├─ RUN_LEDGER.md
└─ runs/
```

每一问结束前需要明确：

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

Codex 把正式图、表和数值集中保存到：

```text
04_results/figures/
04_results/tables/
04_results/data/
```

正式图还要检查中文字体、坐标轴、单位、标签碰撞、论文缩放后的可读性，以及它是否真的使用了最终 Run 的数据。

---

## 缺现实数据时，先上网查，不能编

题目需要机场起降架次、人口、气象、交通流、价格、行业参数等现实数据，而附件没有给出时，AI 会主动检索真实来源。

中国现实场景默认优先：

```text
中国官方 / 法定统计
→ 对象官方
→ 国内行业与科研资料
→ 国际权威来源
→ 二次来源只作线索
```

找不到可靠数据时，会明确报告缺口并讨论代理变量、区间分析、模型调整或显式假设，不会为了让代码跑起来补一个“合理值”。

外部原始数据保存在 `01_data/external/`，网页和来源记录保存在 `07_references/websites.md`。

---

## 正式比赛和旧题测试分开联网

| 模式 | 用途 | 联网规则 |
|---|---|---|
| `LIVE_RESEARCH_MODE` | 正式比赛 | 正常查论文、数据、参数、标准、算法和领域案例 |
| `BLIND_BENCHMARK_MODE` | 历年旧题测试 | 不用题号、题名、原文、附件特征去定位历史答案 |

旧题盲测仍然可以查通用理论、原始方法论文、官方现实数据和库文档。

如果意外打开了这道旧题的完整历史解答，会标记：

```text
ANSWER_LEAKAGE_DETECTED
```

这次测试就不能再说是完全独立完成的。

---

## 两种正式求解方式

| 模式 | 更适合 | 特点 |
|---|---|---|
| 逐题深度求解 | Codex / 正式比赛 | 每问先讨论确认，再实现并留下 Final Run 和完整证据链 |
| 一次性完整求解 | Chat / 前期快速参考 | 连续做完整题，但各问仍保留模型、代码和验证 |

实际运行如果推翻前面选的路线，可以重新开路线比较，不会因为“前面已经定了”就硬做下去。

---

## 从代码到论文，结果要能追溯

最终结果链大致是：

```text
原题要求
↕
01_data 中的真实数据
↕
03_code 中的最终模型 / 参数
↕
FINAL_RUN_ID
↕
04_results 中的图 / 表 / 数值
↕
VISUALIZATION_MANIFEST.md
↕
05_paper 中的论文表述
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

Codex 未收到其他路径要求时，保存在：

```text
06_submission/internal_delivery/
```

其中 `参考论文.zip` 是 AI 根据本次赛题写的内部参考论文，默认包含 Word 和 PDF。它是给队员理解、核查和手工重写用的，不能直接提交比赛。

真正准备上传的文件放在 `06_submission/`，并按当年官方、赛区和提交系统要求重新核验，不把某一年的格式永久写死。

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
Codex 工作区 → local-workspace-policy
EDA → exploratory-research
现实数据 → external-data-research
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
这一问还有什么资料需要补？
先和我讨论方案，不要立刻写最终代码。
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
    ├── local-workspace-policy.md
    ├── search-mode-policy.md
    ├── exploratory-research.md
    ├── external-data-research-policy.md
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

CUMCM · 数学建模 · Mathematical Modeling · AI Skill · Agent Skill · Codex · Claude Code · Python Modeling · Modeling Workspace · EDA · Model Selection · Evidence-first Figure · Run Ledger · Experiment Tracking · Visualization QA · Optimization · Prediction · Simulation · Literature Verification · Sensitivity Analysis · Robustness Analysis · Blind Benchmark · Paper Review

---

<div align="center">

如果这个项目对你有帮助，欢迎 Star。

发现 AI 会误解题意、混用旧 Run、画错图、编造数据或来源、漏答原题、弄乱项目目录或审错论文，也欢迎提 Issue / PR。

</div>