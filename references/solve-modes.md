# 第二阶段解题模式

## 模式选择

第一阶段完成精简分析、探索性研究、逐问推荐和整题路线后，如果用户尚未指定，让用户选择：

1. **逐题深度求解**：推荐 Codex / 本地正式比赛；
2. **一次性完整求解**：适合 Chat / 前期快速获取整题参考。

选择只影响研究组织与交互节奏，不降低质量底线。

正式 Python 同时遵循：

- `python-code-documentation-policy.md`
- `python-artifact-naming-policy.md`

---

# 模式 A：逐题深度求解

状态：`STAGE_2_QUESTION_BY_QUESTION`。

使用 `assets/QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md`。

每一问分成两个连续阶段：

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
→ 推荐模型、公式框架与假设
→ 风险 / 数据缺口 / 可验证性判断
```

这一步的目标是把方案谈清楚，不是立即开始写最终代码。

聊天只需要自然说明：

- 当前更推荐什么；
- 为什么；
- 还有什么风险或数据缺口；
- 哪些地方值得继续讨论；
- 是否需要补论文、文献、数据、老师意见或其他资料。

然后进入：

```text
QUESTION_PLAN_CONFIRMATION
```

用户补充文件后，先做增量文件安全审计，再读取和核验。只有用户明确表示“就这样、按这个做、执行、没补充了”等，才进入正式实现。

### 确认前禁止提前固化成果

用户确认前，不应直接生成：

- 最终生产级 Python；
- Final Run；
- A/B 级正式图；
- 最终结果表；
- 当前问题完整教程；
- 下一问最终交接文件。

允许继续做支撑方案判断的轻量探索、数据核验、小规模实验和文献检索，但不能冒充最终成果。

---

## B. 正式实现与成果固化

确认后执行：

```text
最终模型 / 公式定稿
→ 中文文件名与模块职责设计
→ 图前证据契约
→ 可视化与结果表计划
→ 带有效注释的中文命名 Python
→ 注释 / 纯净度 / 文件名检查
→ 实际运行
→ RUN_LEDGER / FINAL_RUN_ID
→ 论文图、验证图、探索图和结果表
→ AI 沟通图用途标记
→ Visualization Manifest
→ 验证 / Visual QA
→ 本问完整教程
→ 本问答案与下一问交接
```

### 中文源码

每问主入口默认：

```text
03_code/q1/第一题.py
03_code/q2/第二题.py
03_code/q3/第三题.py
```

整题入口默认：

```text
03_code/总运行.py
```

复杂问题使用 `第一题_数据处理.py`、`第一题_模型求解.py`、`第一题_结果验证.py` 等中文职责名。技术性文件名例外见 `python-artifact-naming-policy.md`。

### 论文图

每张论文候选图必须有同语义中文绘图脚本：

```text
03_code/q1/论文图/第一题_预测结果图.py
04_results/figures/q1/paper/第一题_预测结果图.png
04_results/figures/q1/paper/第一题_预测结果图.svg
```

### AI 沟通图

AI/Agent 中间沟通图必须：

```text
文件名前缀：AI沟通图_
图面标记：AI内部沟通图｜非论文材料
用途类型：AI_COMMUNICATION_ONLY
进入论文：否
进入官方提交：否
```

不得仅靠删标记、改名把内部图升级为论文图。

完成并通过关键验收后，本问成果才算固化，然后进入问题 `k+1` 的方案研究与讨论。

如果正式运行暴露重大问题，例如 baseline 更优、关键假设失效、数据口径错误、约束不可行或数值不稳定，触发：

```text
ROUTE_REOPEN_REQUIRED
```

回到讨论状态，不硬把错误方案做完。

---

## 外部数据

逐题研究中发现现实数据缺口时，按 `external-data-research-policy.md` 主动检索真实来源。

找不到可靠数据时必须在方案确认前告诉用户，不得为了让代码能跑而编一个值。

---

## 可视化要求

正式实现后执行：

- `python-visualization-policy.md`
- `figure-evidence-contract.md`
- `python-artifact-naming-policy.md`

图像用途至少区分：

```text
PAPER_FIGURE
VALIDATION_FIGURE
EXPLORATION_FIGURE
AI_COMMUNICATION_ONLY
SECURITY_AUDIT_ONLY
```

论文图和输出图使用相同中文语义主干；AI 沟通图进入独立目录并完整标记；普通 DataFrame 优先 CSV/XLSX + Word 原生表格。

---

## 是否继续扩展研究

逐题模式不在每问完成后机械追问“是否扩展研究”。

默认：

- 正式结果正常、验证通过、没有新重要风险 → 固化本问并进入下一问；
- 实际结果出现新的、有决策价值的问题 → 主动和用户讨论是否继续；
- 扩展必须说明研究什么、为什么值得、可能改变什么、什么时候停止。

合法结局：

```text
MEANINGFUL_FINDING
NO_MEANINGFUL_FINDING
INCONCLUSIVE
```

禁止为了扩展研究堆模型、堆图或制造结果。

---

# 模式 B：一次性完整求解

状态：`STAGE_2_ONE_PASS`。

使用 `assets/STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md`。

按问题依赖连续完成整题，同样要求每问模型、公式、中文命名 Python、实际结果、合理图表、结果表、Manifest、验证和上下问接口完整。

一次性模式不强制每问单独等待 `QUESTION_PLAN_CONFIRMATION`；但重大数据缺口、路线失效、文件安全冲突或需要用户补充关键资料时仍应暂停沟通。

一次性模式不能成为降低源码命名、注释、图像用途标记或可追溯性的理由。

---

# 失败状态

```text
PYTHON_CODE_DOCUMENTATION_FAILED
SOURCE_CODE_CONTAMINATION_DETECTED
PYTHON_FILENAME_POLICY_FAILED
FIGURE_PURPOSE_MARKING_FAILED
AI_COMMUNICATION_FIGURE_LEAKED
```

任一关键状态未解决，不得把本问标记完成。

---

# 全部问题完成后

无论模式 A/B：

1. 重新读取已审计原题；
2. 完成 Requirement Traceability；
3. 检查中文源码、注释、Final Run、图像用途、图表、教程和论文的一致性；
4. 生成真实整题模型总览图；
5. 基于最终结果撰写 AI 参考论文；
6. 进入 `INTERNAL_DELIVERY`，生成四个内部成果包；
7. 队员人工重写正式论文后进入 `FINAL_PAPER_AUDIT`；
8. 正式比赛需要提交时，再按当年规则执行 `OFFICIAL_SUBMISSION_EXPORT`。

内部四包不是官方提交格式。
