# 第二阶段解题模式

## 模式选择

第一阶段完成精简分析、探索性研究、逐问推荐和整题路线后，如果用户尚未指定，让用户选择：

1. **逐题深度求解**：推荐 Codex / 本地正式比赛；
2. **一次性完整求解**：适合 Chat / 前期快速获取整题参考。

选择只影响研究组织与交互节奏，不降低质量底线。

---

# 模式 A：逐题深度求解

状态：`STAGE_2_QUESTION_BY_QUESTION`。

使用 [../assets/QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md](../assets/QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md)。

每问后台完整闭环：

```text
要求回查
→ 上下关联探索
→ 必要问题级探索
→ 最终模型/公式
→ 可视化计划
→ Python 实现与实际运行
→ A/B/C 图表与结果表
→ Visualization Manifest
→ 验证 / Visual QA
→ 代码解析
→ 本问资料/文献
→ 本问答案
→ 下一问交接
→ 阶段闸门
```

### 可视化要求

完整遵循 [python-visualization-policy.md](python-visualization-policy.md)。

- A 级核心结果图回答“最终得到什么”；
- B 级诊断图回答“为什么相信”；
- C 级探索图仅保留真正有价值的中间证据；
- 不规定固定数量；
- 中文论文候选图默认中文；
- 普通 DataFrame 优先 CSV/XLSX + Word 原生表格；
- 图表更新 `VISUALIZATION_MANIFEST.md`；
- 启发式算法依赖结论时提供必要收敛/重复实验稳定性证据。

### 阶段闸门

只有本问已经完整可交付后才讨论是否继续扩展研究。

扩展必须能说明：研究什么、为什么值得、可能改变什么、什么时候停止。

合法结局：

- `MEANINGFUL_FINDING`
- `NO_MEANINGFUL_FINDING`
- `INCONCLUSIVE`

禁止为了扩展研究堆模型、堆图或制造结果。

---

# 模式 B：一次性完整求解

状态：`STAGE_2_ONE_PASS`。

使用 [../assets/STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md](../assets/STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md)。

按问题依赖连续完成整题，同样要求每问模型、公式、Python、实际结果、合理 A/B/C 图表、结果表、Manifest、验证和上下问接口完整。

遇到路线失效、重大风险、异常结果时主动提醒；真实结果推翻路线时触发 `ROUTE_REOPEN_REQUIRED`。

---

# 全部问题完成后

无论模式 A/B：

1. 重新读取原题；
2. 完成 Requirement Traceability；
3. 完成全局结果、公式、图表、Manifest 一致性检查；
4. 生成整题模型总览图；
5. 基于最终结果撰写 AI 参考论文；
6. 进入 `INTERNAL_DELIVERY`，生成四个内部成果包；
7. 队员人工重写正式论文后进入 `FINAL_PAPER_AUDIT`；
8. 正式比赛需要提交时，再按当年规则执行 `OFFICIAL_SUBMISSION_EXPORT`。

内部四包不是官方提交格式。
