# MODELING_DECISION_STATE

> 用于跨会话保存当前阶段、路线、解题模式和逐题进度，只记录已确认事实和决策。

## 当前阶段

`STAGE_1_ANALYSIS / WAITING_FOR_CONFIRMATION / STAGE_2_QUESTION_BY_QUESTION / STAGE_2_ONE_PASS / PAPER_REVIEW / ROUTE_REOPEN_REQUIRED / INTERNAL_DELIVERY / INTERNAL_DELIVERY_COMPLETE / FINAL_PAPER_AUDIT / OFFICIAL_SUBMISSION_EXPORT`

## 赛题

- 名称：
- 题号：
- 附件状态：
- 搜索模式：`LIVE_RESEARCH_MODE / BLIND_BENCHMARK_MODE`

## 第二阶段解题模式

- 用户选择：`QUESTION_BY_QUESTION / ONE_PASS / 尚未选择`
- 当前正在处理的问题：
- 已完成问题：
- 待处理问题：

## 当前各问路线

| 问题 | 核心任务 | 当前方法 | 推荐指数 | 状态 | 与前后问接口 | 备注 |
|---|---|---|---:|---|---|---|

## 整体主路线

- 主路线：
- 推荐指数：
- 确认依据：
- 备用路线：
- 切换条件：

## 探索性研究摘要

| 问题/全局 | 关键探索证据 | 对模型选择的影响 | 对推荐分的调整 |
|---|---|---|---|

## 问题级交接记录

| 已完成问题 | 向下一问传递的变量/结果 | 对应文件 | 下一问必须注意 | 是否导致路线调整 |
|---|---|---|---|---|

## Visualization 状态

- `VISUALIZATION_MANIFEST.md`：未开始 / 进行中 / 已完成
- 中文字体 QA：
- 论文尺寸 QA：
- Visual QA：
- 启发式算法收敛证据：适用 / 不适用 / 已完成 / 缺失

## 已纳入文献

| 文献 ID | 用途 | 推荐指数 | 核验层级/链接状态 | 是否改变路线 |
|---|---|---:|---|---|

## 未解决证据缺口

## 已拒绝方案及原因

## 第二阶段完成情况

| 问题/部分 | 状态 | 代码状态 | 验证状态 | 图表/表格状态 | 教程状态 | 备注 |
|---|---|---|---|---|---|---|

## 原题回查

- 是否重新读取原题：
- Requirement Traceability：
- 是否仍有遗漏要求：

## 内部交付

- 四个内部 ZIP：
- 未压缩成果目录（本地模式）：
- ZIP 真实解压预检：
- `INTERNAL_DELIVERY_COMPLETE`：是 / 否

## 组员终稿复审

- 终稿文件：
- 审核状态：未开始 / P0/P1 待修 / 二审中 / 通过

## 官方提交导出

- 是否为正式比赛：
- 当年官方规则是否重新核验：
- 官方导出状态：未开始 / 进行中 / `OFFICIAL_SUBMISSION_EXPORT_FAILED` / 已完成
- 实际导出文件：

## 最后更新
