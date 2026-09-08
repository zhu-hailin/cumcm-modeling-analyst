# 逐题深度求解模板

状态：STAGE_2_QUESTION_BY_QUESTION。Stage 2 唯一求解方式：每问先讨论再求解。
确认的是建模边界，模板不是逐项播报脚本；已确认的事项不再重复询问。

## 问题 {k}：研究与确认

- Requirement / 原题动作、对象、单位、范围：
- 必须给出的直接答案：
- 硬约束、关键假设与尚未解决的歧义：
- 数据结构、正式输入与上游 Final Run：
- 关键困难、当前机制判断和小实验：
- 主路线、baseline/合理参照、必要备用路线及切换条件：
- 选优理由：效果、解释性、稳定性、可行性、成本的实际取舍：
- 关键验证；必要时的灵敏度/创新对照：
- 向下一问交付的文件、字段、单位：

确有多条有价值路线时再列表比较；证据不足时不用虚假精确评分。

QUESTION_PLAN_CONFIRMATION：确认本问目标、假设、路线和重要约束。用户已明确确认当前问方案时引用记录直接执行；整题路线认可不代替后问确认。
自主边界以 [核心流程](../references/core-workflow.md) 为准。

## 正式实现与验证

- 变量、公式、约束、参数及其代码映射；
- 输入处理规则、运行入口和依赖；
- 真实运行及 FINAL_RUN_ID；必要 Validation Run；
- 直接答案、关键数值/规则、验证结果、不确定性和适用条件；
- 正式下游接口与结果版本。

实现按 [代码规范](../references/python-code-documentation-policy.md)：
新建中文项目的 Python 文件名、docstring、人工注释和 processed/result 表头简体中文优先；raw 原字段不变，转换保留映射。
多阶段脚本用区域注释定位数据清洗、核心建模（写明模型名）、求解、验证与导出；不机械凑区域。

按 [运行账本](../references/model-run-ledger.md) 记录重要运行，使用新输出路径。命令退出成功不等于结果已验证。
按 [建模质量门](../references/modeling-quality-gates.md) 分别判断 SCIENTIFIC_VALIDITY 与 CONTEST_TASK_COMPLETION。
灵敏度分析与创新验证采用 [研究 Playbook](../references/modeling-research-playbook.md) 的按需设计。

## 图表与问题详解

探索图轻量；正式图按 [绘图规范](../references/python-visualization-policy.md) 升级：
默认单图单文件、图1/图2独立编号；组合面板仅为必要科学比较的例外。结果表保持可编辑。

更新 02_analysis/q{k}_solution.md：
直接答案 → 为什么建模 → 公式和代码 → 如何运行 → 结果为何可信 → 限制 → 下游使用什么。
关键结果优先用简洁表格，避免只藏在日志或长附录中。

## 本问完成检查

- 原题每个交付项有答案或有依据的 NOT_IDENTIFIABLE；
- 数据、前提、baseline/参照、现实约束和结论强度通过检查；
- 真实运行与结果可追溯，未混入旧产物；解析推导明确记录不适用项；
- 代码中文可读性、正式图独立编号、字段映射与现有工程兼容；
- 后问可从正式文件读取接口，科学有效性与完成度已分别判断。

当前路线失效且无已授权备用路线时标记 ROUTE_REOPEN_REQUIRED；否则交付本问并停止，等待用户进入下一问方案讨论。下一问方案单独确认，不自动求解后续所有问题。
