# 第二阶段解题模式

## 模式选择

第一阶段完成精简分析、探索性研究、逐问推荐和整题路线后，如果用户尚未指定，让用户选择：

1. **逐题深度求解**：推荐 Codex / 本地正式比赛；
2. **一次性完整求解**：适合 Chat / 前期快速获取整题参考。

选择只影响研究组织与交互节奏，不降低质量底线。

两种模式只要生成正式 Python，都必须执行：

[python-code-documentation-policy.md](python-code-documentation-policy.md)

代码不仅要实际运行，还要有真实有效的模块说明、关键函数 docstring 和必要建模注释，并保持源码纯净。

---

# 模式 A：逐题深度求解

状态：`STAGE_2_QUESTION_BY_QUESTION`。

使用 [../assets/QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md](../assets/QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md)。

逐题模式每一问分成两个连续阶段：

```text
A. 方案研究与讨论
        ↓
QUESTION_PLAN_CONFIRMATION
        ↓ 用户确认
B. 正式实现与成果固化
        ↓
进入下一问
```

## A. 方案研究与讨论

先完成：

```text
本问要求回查
→ 上下关联探索
→ 必要问题级探索
→ 外部数据 / 文献检索与核验
→ 候选方案复核
→ 推荐模型、关键公式框架与假设
→ 风险 / 数据缺口 / 可验证性判断
```

这一步的目标是把方案谈清楚，**不是立即开始写最终代码**。

聊天窗口只需要自然说明：

- 我目前更推荐什么；
- 为什么；
- 还有什么风险或数据缺口；
- 哪些地方值得和队员再讨论；
- 是否还需要补论文、文献、数据、老师意见或其他资料。

然后进入：

```text
QUESTION_PLAN_CONFIRMATION
```

AI 应自然询问用户类似：

> 这一问的方案我基本梳理清楚了。你们还有没有论文、参考文献、额外数据、老师建议或者想调整的思路要补充？如果没有，我就按现在这个方案正式写代码、跑结果并整理问题 {k} 详解。

不要机械复刻固定句式，但必须表达同样的确认含义。

### 确认前禁止提前固化成果

用户明确确认前，不应直接生成：

- 最终生产级 Python；
- 最终 Run；
- A/B 级正式图表；
- 最终结果表；
- 问题 {k} 完整教程/详解；
- 向下一问的最终交接文件。

允许继续做支撑方案判断的轻量探索、数据核验、小规模实验和文献检索，但这些不能冒充最终成果。

用户补充资料后，先吸收、核验并重新讨论方案；如果补充内容改变路线，应更新推荐和理由，再等待确认。

用户说“就这样”“按这个做”“执行”“没补充了”等明确确认后，才进入正式实现。

## B. 正式实现与成果固化

确认后执行：

```text
最终模型/公式定稿
→ 图前证据契约
→ 可视化与结果表计划
→ 带有效注释的 Python 正式实现
→ 代码注释与源码纯净度检查
→ 实际运行
→ RUN_LEDGER / FINAL_RUN_ID
→ A/B/C 图表与结果表
→ Visualization Manifest
→ 验证 / Visual QA
→ 代码解析
→ 本问资料/文献整理
→ 问题 {k} 完整详解
→ 本问最终答案
→ 下一问交接
```

正式源码至少满足：

- 非平凡模块有模块 docstring；
- 关键数据、清洗、模型、目标函数、约束、验证、绘图和导出函数/类有准确 docstring；
- 单位、口径、边界、数值稳定、随机种子、停止条件和非显然逻辑有必要注释；
- 注释与代码、公式、参数、单位和路径一致；
- 不逐行翻译显然 Python 语法；
- 不保留大段注释旧代码和影响结果的 `TODO/FIXME/pass`；
- 不混入 Skill、聊天、内部状态、提示词和 AI 水印。

完成并通过关键验收后，本问成果才算固化，然后自然进入问题 `k+1` 的“方案研究与讨论”。

如果正式运行暴露重大问题，例如 baseline 明显更优、关键假设失效、数据口径错误、约束不可行或数值不稳定，触发 `ROUTE_REOPEN_REQUIRED`，回到讨论状态，而不是硬把错误方案做完。

## 外部数据

逐题研究中只要发现现实数据缺口，按 [external-data-research-policy.md](external-data-research-policy.md) 主动检索真实来源。

找不到可靠数据时必须在方案确认前告诉用户，不得为了让代码能跑而编一个值。

## 可视化要求

正式实现后完整遵循 [python-visualization-policy.md](python-visualization-policy.md)。

- A 级核心结果图回答“最终得到什么”；
- B 级诊断图回答“为什么相信”；
- C 级探索图仅保留真正有价值的中间证据；
- 不规定固定数量；
- 中文论文候选图默认中文；
- 普通 DataFrame 优先 CSV/XLSX + Word 原生表格；
- 图表更新 `VISUALIZATION_MANIFEST.md`；
- 启发式算法依赖结论时提供必要收敛/重复实验稳定性证据；
- 绘图代码注释重点说明证据、数据源和区间定义，不逐行解释常规 Matplotlib API。

## 是否继续扩展研究

逐题模式不再机械地在每问完成后再次强制询问“是否扩展研究”。

默认规则：

- 正式结果正常、验证通过、没有新的重要风险 → 固化本问并进入下一问；
- 如果实际结果出现新的、有决策价值的问题 → 主动和用户讨论是否继续研究；
- 扩展必须说明研究什么、为什么值得、可能改变什么、什么时候停止。

合法结局：

- `MEANINGFUL_FINDING`
- `NO_MEANINGFUL_FINDING`
- `INCONCLUSIVE`

禁止为了扩展研究堆模型、堆图或制造结果。

---

# 模式 B：一次性完整求解

状态：`STAGE_2_ONE_PASS`。

使用 [../assets/STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md](../assets/STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md)。

按问题依赖连续完成整题，同样要求每问模型、公式、带有效注释的可读 Python、实际结果、合理 A/B/C 图表、结果表、Manifest、验证和上下问接口完整。

一次性模式不强制每问单独等待 `QUESTION_PLAN_CONFIRMATION`；如果用户选择该模式，就代表授权沿已确认整题路线连续执行。但遇到重大数据缺口、路线失效或需要用户补充关键资料时仍应暂停沟通。

遇到路线失效、重大风险、异常结果时主动提醒；真实结果推翻路线时触发 `ROUTE_REOPEN_REQUIRED`。

---

# 代码失败状态

正式代码缺少必要说明、注释错误或与实现不一致：

```text
PYTHON_CODE_DOCUMENTATION_FAILED
```

源码混入 Skill、提示词、聊天记录、内部状态、隐藏注入原文或 AI 水印：

```text
SOURCE_CODE_CONTAMINATION_DETECTED
```

修复并重新运行必要入口后，才允许把结果固化为 Final Run 或进入源码交付。

---

# 全部问题完成后

无论模式 A/B：

1. 重新读取原题；
2. 完成 Requirement Traceability；
3. 完成正式 Python、注释、公式、结果、图表和 Manifest 一致性检查；
4. 生成整题模型总览图；
5. 基于最终结果撰写 AI 参考论文；
6. 进入 `INTERNAL_DELIVERY`，生成四个内部成果包；
7. 队员人工重写正式论文后进入 `FINAL_PAPER_AUDIT`；
8. 正式比赛需要提交时，再按当年规则执行 `OFFICIAL_SUBMISSION_EXPORT`。

内部四包不是官方提交格式。
