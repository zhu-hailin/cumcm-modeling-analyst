# cumcm-modeling-analyst

面向全国大学生数学建模竞赛及同类赛事的赛题分析 Skill。

它默认采用两阶段工作流：

1. 先分析题目背景、拆解子问题、主动检索并核验文献与数据来源，给出候选路线和推荐指数；
2. 用户确认路线后，再按锁定方案一次性完成整题的建模、验证、稳健性分析和论文结构设计。

## 核心能力

- 题目背景与题意解析
- 子问题拆解与依赖关系
- 各问推荐解法和具体算法
- 多套候选路线及推荐指数
- 中文优先的真实文献与数据来源核验
- 队友新增论文的持续审查
- 敏感性、鲁棒性和基线验证设计
- 论文结构与 Coding Agent 实现规格

默认不生成可执行代码。

## 目录

```text
.
├── SKILL.md
├── CHANGELOG.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── AI_USAGE_LOG_TEMPLATE.md
│   ├── FULL_ANALYSIS_TEMPLATE.md
│   ├── LITERATURE_LEDGER_TEMPLATE.md
│   ├── MODELING_DECISION_STATE_TEMPLATE.md
│   ├── PAPER_REVIEW_TEMPLATE.md
│   ├── STAGE1_STRATEGY_BRIEF_TEMPLATE.md
│   └── STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md
└── references/
    ├── competition-compliance.md
    ├── full-analysis-protocol.md
    ├── model-route-map.md
    ├── paper-evaluation-protocol.md
    ├── source-verification-policy.md
    └── two-stage-workflow.md
```

## 使用方式

将整个仓库作为 Skill 目录使用，入口文件为 `SKILL.md`。

新赛题默认先进入 `STAGE_1_ANALYSIS`；确认方案后，再进入 `STAGE_2_LOCKED`。

> 比赛期间应以当年组委会和本赛区最新规则为准，并保留真实的 AI 使用记录。
