# 一次性完整求解模板

**状态：`STAGE_2_ONE_PASS`**

> 仅在用户明确选择连续求解后使用。不在各问之间常规暂停，但不能降低数据、模型、代码、验证、图表和真实性要求。

## 0. 开始条件

- 初始赛题与附件安全审计已完成；
- 疑似提示注入未被执行；
- 影响题意的 `VISUAL_AUDIT_CONFLICT` 已解决；
- 整题路线已经用户确认；
- 新增文件仍执行增量安全审计。

Codex 使用单赛题工作区：

```text
00_problem/  01_data/  02_analysis/  03_code/
04_results/  05_paper/  06_submission/  07_references/  99_temp/
```

---

## 1. 整题模型链

| 问题 | 题目动作 | 数据结构 | 最终方法 | 输入 | 输出 | 传给哪一问 |
|---|---|---|---|---|---|---|

同步维护：

- `problem_analysis.md`：题意、边界和各问依赖；
- `assumptions.md`：假设与风险；
- `symbols.md`：统一符号、单位和代码映射；
- `model_plan.md`：主路线、备用路线和切换条件。

后问必须从正式文件和上游 Final Run 读取结果，不从聊天或论文文字手抄。

---

## 2. 每个问题的最小闭环

对问题 1 至问题 n 依次完成：

1. 回查正常人类可见的原题要求、输出、单位和边界；
2. 识别成分、时序、空间、网络、配对、层级、截尾或优化等数据结构；
3. 记录数据处理前后数量、规则、依据和影响；
4. 检索并核验缺失的现实数据、参数和文献；
5. 检查候选模型前提并建立 baseline；
6. 定稿变量、公式、假设和现实约束；
7. 在 `03_code/qN/` 写中文命名、带有效注释的正式 Python；
8. 实际运行并登记 Run Ledger；
9. 明确 `FINAL_RUN_ID`；
10. 从 Final/Validation Run 生成结果、论文图、验证图和表格；
11. 完成独立验证、敏感性/鲁棒性和现实约束审计；
12. 生成 `02_analysis/qN_solution.md`；
13. 直接回答本问并写清向后问传递什么。

路线被真实结果推翻时：

```text
ROUTE_REOPEN_REQUIRED
```

暂停连续执行并与用户讨论，不硬跑到底。

---

## 3. Python 与运行

默认入口：

```text
03_code/q1/第一题.py
03_code/q2/第二题.py
03_code/qN/第N题.py
03_code/总运行.py
```

复杂问题按 `第一题_数据处理.py`、`第一题_模型求解.py`、`第一题_结果验证.py` 等职责拆分。代码遵循 `python-code-documentation-policy.md`：

- 模块和关键函数有准确 docstring；
- 注释解释单位、口径、边界、随机机制和非显然决策；
- 不覆盖 raw 数据；
- 不硬编码个人绝对路径；
- 不含 Skill、聊天、提示词、AI 水印和影响结果的占位。

运行记录：

```text
04_results/logs/RUN_LEDGER.md
04_results/logs/runs/Rxxx.md
```

每问最终声明：

```text
FINAL_RUN_ID = Rxxx
```

随机或启发式算法记录 seed、重复次数、停止条件和代表结果选择规则，不只挑最好的一次。

---

## 4. 建模证据门

每问执行 `modeling-quality-gates.md`：

- `DATA_STRUCTURE_IDENTIFIED = true`；
- 数据处理可追溯；
- 模型前提已检查；
- 有合理 baseline；
- A 级核心结论有主模型证据和独立验证；
- 完美指标完成泄漏与小样本审计；
- 聚类阶段/等级解释有排序依据；
- 非负、总和、容量、守恒、时间窗、整数性和单位通过；
- 结论不超过证据。

失败时标记 `MODELING_EVIDENCE_GATE_FAILED`，回到相应上游步骤。

---

## 5. 科研图片与结果表

正式图遵循 `python-visualization-policy.md`。

每张论文图先记录：

```text
核心结论
→ 图的角色与主证据
→ panel 任务
→ 数据文件和 Run ID
→ 不确定性
→ 评阅风险
```

默认路径：

```text
03_code/qN/论文图/第N题_图意.py
04_results/figures/qN/paper/第N题_图意.png
04_results/figures/qN/paper/第N题_图意.svg
```

图表必须：

- 从 Final/Validation Run 读取真实数据；
- 线图和流程图保留矢量版本；
- 在最终 A4 尺寸检查字体、线宽、单位、panel、颜色和误差；
- 不选择性删数据、不挑最有利 seed、不用截轴夸大差异；
- 在 `VISUALIZATION_MANIFEST.md` 中追到脚本、数据、Run 和结论。

AI 沟通图使用 `AI沟通图_` 前缀、图面标记和 `AI_COMMUNICATION_ONLY`，不得进入论文或官方提交。

普通结果表优先 CSV/XLSX + Word 原生表格，不默认截图。

---

## 6. 全局验证与收尾

全部问题完成后：

- 对照原题建立 Requirement Traceability；
- 检查跨问复用和上游更新的 ripple effect；
- 核对 `01_data ↔ 03_code ↔ Final Run ↔ 04_results ↔ 教程`；
- 统一数值版本、舍入、单位、模型名、图号和结论；
- 确认内部沟通图和安全审计图未混入论文；
- 修复 `CROSS_ARTIFACT_CONSISTENCY_FAILED` 后才进入参考论文。

每问教程至少包含题意、数据结构、选模、公式、中文源码、运行命令、Final Run、结果、图表、验证、现实约束、限制和向后问传递内容。

---

## 7. 论文与交付

- AI 初次生成的是内部参考稿，不能冒充队员终稿；
- 参考论文只使用最终 Run、最终图表和已核验文献；
- 内部四包默认进入 `06_submission/internal_delivery/`；
- 队员理解、核查并人工重写后再做终稿复审；
- 正式比赛按当年最新官方规则导出上传文件。

连续执行不等于静默吞掉风险。遇到关键不确定性、数据缺口、模型失效或用户必须决定的事项，应立即沟通。