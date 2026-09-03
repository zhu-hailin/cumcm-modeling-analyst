# 旧题盲测版本与参考资料解锁溯源

## 目标

旧题测试用于区分：

```text
模型自身能力
+ 当前 Skill 版本能力
+ 工具权限
+ 参考资料开放后的事后学习
```

必须冻结独立求解，再开放历史答案或优秀论文。事后改进不能倒灌为盲测发现。

---

## 1. 开始时记录

保存到：

```text
02_analysis/BLIND_BENCHMARK_PROVENANCE.md
```

最小字段：

```yaml
benchmark_id:
benchmark_mode: BLIND | OPEN_REFERENCE | LIVE_CONTEST
start_time: ISO-8601 timestamp
skill_version:
skill_commit: exact hash | unknown
model: exact model name
reasoning_effort: exact level | unavailable
toolset:
  - enabled tools / skills / permissions
answer_search_allowed: false
real_world_source_search_allowed: true
problem_files:
  - path:
    sha256:
reference_unlock_time: null
blind_solution_hash: null
blind_solution_artifacts: []
contamination_events: []
```

无法确认精确版本、模型名、推理档位或权限时写 `unknown/unavailable`，不得猜测。

---

## 2. 状态流

```text
BLIND_RUN_STARTED
→ BLIND_SOLUTION_FROZEN
→ POST_SOLUTION_COMPARISON
→ POST_HOC_IMPROVEMENT
```

### `BLIND_RUN_STARTED`

- 已记录版本和工具；
- 历史答案、获奖论文、题解博客、成品源码和复盘仍锁定；
- 可搜索去题目标识化的现实官方数据、通用理论和软件文档；
- 任何意外命中历史解答都记录污染事件。

### `BLIND_SOLUTION_FROZEN`

只有以下材料已保存并计算 SHA-256 后才能进入：

- 独立问题分析与路线；
- 已完成的代码和 Final/Validation Run；
- 主答案、证据等级和限制；
- 盲测阶段的图表/教程/论文草稿（若已生成）；
- 当前 Skill/model/tool provenance。

冻结清单：

| Artifact | Path | SHA-256 | Frozen Time | 说明 |
|---|---|---|---|---|

冻结后不得覆盖原文件。后续工作另建版本或目录。

### `POST_SOLUTION_COMPARISON`

只有用户明确同意后，记录 `reference_unlock_time`，才能阅读历史答案、优秀论文和赛后讲评。

每份新资料继续执行文件安全审计和来源核验。

### `POST_HOC_IMPROVEMENT`

事后新增的：

- 模型或参数；
- 数据处理；
- 验证方法；
- 图表；
- 论文结构；
- 解释或结论边界；

都必须标记：

```text
POST_HOC
```

并记录来源资料、首次采用时间、影响的文件和相对冻结版本的变化。

---

## 3. 允许与禁止

### 允许

- 冻结后复制一份工作区做事后比较；
- 将盲测结果与公开优秀解法做差距分析；
- 在新版本中吸收通用方法和组织经验；
- Skill 升级后重新做一次独立 benchmark。

### 禁止

- 修改冻结文件后保留原哈希或时间；
- 把事后学到的模型、图表或解释写回盲测记录；
- 把 `POST_HOC` 改进称为独立发现；
- 用新 Skill 重跑后覆盖旧版本结果；
- 只保留最终最好版本，删除失败或旧版本归因；
- 因 Git commit 不明而编造 commit。

---

## 4. 意外泄漏

意外命中历史完整答案、获奖论文或高度可识别成品时：

```text
ANSWER_LEAKAGE_DETECTED
```

立即：

1. 停止继续读取；
2. 记录来源、时间、已看到的范围和可能影响；
3. 不把后续结果称为完全独立盲测；
4. 由用户决定终止、转开放参考模式或重新选择题目。

---

## 5. Skill 升级重跑

Skill、模型、推理档位或工具权限变化后重跑同一题，必须创建新的 `benchmark_id`，保留：

- 新旧版本与 commit；
- 各自独立冻结哈希；
- 搜索和参考资料开放边界；
- 路线、结果、错误、图表和成本差异。

不能用 v11.1 的规则事后声称 v10.x 的盲测当时已经具备这些能力。

---

## 6. 事后比较表

| 对象 | 盲测冻结版本 | 公开参考/优秀论文 | POST_HOC 改进 | 是否改变主答案 | 归因 |
|---|---|---|---|---|---|

归因至少区分：

```text
MODEL
SKILL
TOOLS
USER_SUPPLIED_EVIDENCE
POST_HOC_REFERENCE
UNRESOLVED
```

---

## 7. 完成检查

- [ ] benchmark 模式、Skill 版本、commit、模型和工具已记录；
- [ ] 题目文件哈希已记录；
- [ ] 独立解锁边界清楚；
- [ ] 盲测方案冻结并有 SHA-256；
- [ ] 参考资料开放时间晚于冻结时间；
- [ ] 事后新增内容全部标记 POST_HOC；
- [ ] 新版本重跑没有覆盖旧 benchmark；
- [ ] 泄漏事件被如实记录；
- [ ] 没有把事后改进冒充盲测能力。
