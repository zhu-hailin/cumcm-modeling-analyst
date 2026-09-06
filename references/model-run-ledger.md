# 模型运行账本与结果来源追踪规范

## 目标

只记录**会影响决策或正式成果的重要运行**，让最终结果可追溯，同时避免把每次 debug 都变成文档负担。

> 结果必须能追到一次真实运行；同一运行元数据只维护一个权威来源。

---

## 1. 保存位置

```text
04_results/logs/
├─ RUN_LEDGER.md
└─ runs/
   ├─ R001.md
   ├─ R002.md
   └─ ...
```

可使用 `scripts/run_record.py` 辅助生成轻量运行记录；它只是自动记录工具，不替代模型判断。

---

## 2. 什么必须记录

以下运行若发生，应进入账本：

- 会决定路线的 baseline / 关键诊断实验；
- 最终模型、最终参数、最终预测或优化；
- 最终 Monte Carlo / 仿真；
- 会改变证据强度的敏感性、鲁棒性或压力场景；
- 启发式算法的重要多 seed 实验；
- 会进入论文的统计检验；
- 生成正式核心图表的数据运行；
- 路线重开前后用于决定是否切换的实验。

以下内容默认不必进入正式账本：

- 语法修复；
- 一次性 debug；
- 无决策价值的临时调试运行；
- 不影响模型/结论的重复尝试。

这些可以留普通终端日志或 `99_temp/`。

---

## 3. RUN_LEDGER 最小字段

| Run ID | 问题 | 目的 | 代码入口 | 输入/配置 | seed/重复 | 输出目录 | 关键结论 | 状态 |
|---|---|---|---|---|---|---|---|---|

状态：

```text
EXPLORATORY
BASELINE
CANDIDATE
FINAL
VALIDATION
REJECTED
SUPERSEDED
```

如果时间戳不能可靠取得，不伪造精确时间；Run ID 足以提供顺序。

---

## 4. 重要运行详细记录

真正影响模型或正式成果的运行，可以建立 `runs/Rxxx.md`：

```markdown
# Rxxx

- 对应问题：
- 目的：
- 状态：
- 代码入口：
- Git commit / 文件版本（可取得时）：
- 输入数据与配置：
- 关键参数：
- seed / 重复次数：
- 运行命令：
- 输出目录：
- 关键结果：
- 关联 Validation Run：
- 生成正式图 / 表：
- 对模型决策的影响：
- 被哪个 Run 替代：
```

不得把未实际执行的计划写成 Run。

---

## 5. 最终结果

进入问题完成状态前明确：

```text
FINAL_RUN_ID = Rxxx
```

最终数值、排名、路径、预测、参数、表格和论文数据图从该 Final Run 或明确关联的 Validation Run 读取。

禁止从旧截图、聊天历史、旧 CSV 或 `SUPERSEDED` Run 手抄最终数字。

README、问题详解和 Evidence Blueprint **引用 Final Run ID 与入口即可**；除非用户阅读需要，不要在多个文件重复手写完整参数表和命令。

---

## 6. 结果替换

新运行取代旧结果时：

- 旧 Run 标记 `SUPERSEDED`；
- 记录替代它的新 Run；
- 更新正式结果、图表和 Evidence Blueprint；
- 下游问题实际依赖该结果时重跑；
- 已生成参考论文时执行一致性检查。

不要删除有决策价值的旧运行后假装它从未存在；无意义 debug 可以清理。

---

## 7. 随机算法

GA、PSO、ACO、SA、随机仿真、Bootstrap 等至少记录：

- seed 或种子策略；
- 重复次数；
- 停止条件；
- 必要的集中趋势与离散指标；
- 代表性方案的选择规则。

不得只挑最好的一次结果冒充稳定表现。

---

## 8. 与图表的关系

`VISUALIZATION_MANIFEST.md` 的正式用途类型统一为：

```text
PAPER_FIGURE
METHOD_FIGURE
VALIDATION_FIGURE
EXPLORATION_FIGURE
AI_COMMUNICATION_ONLY
SECURITY_AUDIT_ONLY
```

数据图使用真实 Run ID；`METHOD_FIGURE` 允许 `Run ID = N/A（方法结构图）`，但必须指向最终模型计划、代码步骤和方法版本。

核心证据链：

```text
论文结论 / 直接答案
↕
正式图 / 表
↕
Visualization Manifest
↕
Final / Validation Run
↕
代码入口 + 输入数据 + 输出文件
```

探索图无需逐张登记，除非它影响路线决策并需要保留。

---

## 9. 与论文的关系

论文作者读取冻结的 Final/Validation 结果和 Evidence Blueprint，不重新计算核心结果，不从聊天手抄数字。

摘要、正文、表格和结论允许显示精度不同，但底层值必须来自同一 Final/Validation 证据链，并采用统一舍入规则。

内部 Run ID 可用于项目管理和附录复现；正式论文正文不需要机械展示 `FINAL_RUN_ID`、`SUPERSEDED` 等内部状态词。

---

## 10. 失败运行什么时候值得记录

只有失败改变了决策时记录，例如：

- 原路线不可行；
- 数值方法不稳定；
- 计算规模无法在比赛预算内完成；
- baseline 明显优于复杂模型；
- 关键假设被真实数据推翻。

这种运行标记 `REJECTED`，并写清它触发了什么路线调整。