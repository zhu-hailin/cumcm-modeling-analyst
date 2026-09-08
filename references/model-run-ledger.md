# 模型运行账本与结果来源

只记录会改变路线、主答案、正式图表或论文结论的重要运行；普通 debug 留终端日志或临时目录。
最终结果必须追到真实运行，同一事实只维护一个权威记录。

## 1. 记录结构与旧项目兼容

使用 scripts/run_record.py 时：

```text
04_results/logs/
├─ RUN_LEDGER.md              # 从 JSON 重建的阅读索引
└─ runs/
   ├─ R001.json               # 权威记录
   └─ R001/
      ├─ stdout.log
      ├─ stderr.log
      └─ artifacts/           # 本次独立输出
```

已有项目采用 Rxxx.md 或其他可靠账本时可沿用，不为本规范批量迁移。使用工具后不得另手改一份 Markdown 配置表；补充结论、质量门结论或 SUPERSEDED 状态在权威记录维护，再重建索引：

```bash
python scripts/run_record.py --root . --rebuild-ledger
```

并行运行各自预留目录与编号，不覆盖对方记录。并行任务全部结束后重建一次索引，避免中途索引暂时不完整。

已有人工/旧版 RUN_LEDGER.md 时原文件保持不动，新工具使用 RUN_LEDGER.generated.md 并打印实际索引位置；旧的 Markdown-only 运行不会被自动迁移成 JSON。若备用索引也被人工占用，保留原件并报告冲突。

## 2. 重要运行的内容

至少可定位：

- Run ID、问题、目的与状态；
- 实际运行命令、代码入口/版本和关键配置；
- 执行前输入文件/目录及 hash，seed/重复规则；
- 输出文件、大小、hash 和关联 Validation Run；
- 对建模决策的影响、关键结果、替代关系。

状态：EXPLORATORY / BASELINE / CANDIDATE / FINAL / VALIDATION / REJECTED / SUPERSEDED。
工具自动记录命令中的本地 .py；共用模块、配置及其他依赖通过 --code/--input 明确声明。输入目录记录文件清单与 hash，不能只记目录存在。
代码目录忽略 Python 自动生成的 __pycache__、.pyc/.pyo；实际源码变更仍使核验失败，输入数据目录不采用该忽略规则。
未记录的依赖不能声称已经验证；不把源代码 hash 当成完整环境锁定。

## 3. 本次运行与旧产物严格分离

推荐正式脚本接受 --output-dir，或读取 CUMCM_OUTPUT_DIR。工具在命令和 --output 中将 {run_dir} 替换为本次新目录，并提供 CUMCM_RUN_ID：

```bash
python scripts/run_record.py --root . --problem Q1 --purpose "最终模型候选" \
  --status FINAL --input 01_data/processed/第一题.csv \
  --code 03_code/common --output "{run_dir}/结果.csv" \
  -- python 03_code/q1/第一题.py --output-dir "{run_dir}"
```

只声明实际存在的输入/共用代码。没有 common/ 时删去对应 --code 参数。
求解脚本自行创建输出父目录。旧入口也可声明一个全新的固定输出路径；已有文件/目录被拒绝，避免旧结果冒充新运行。不得自动删除旧成果来绕过检查。

工具执行前保存输入/代码快照，执行后核对是否被修改；缺失输入、已有输出、输出为空、非零退出或超时均拒绝固化。
为匹配本次计算预算可设置 --timeout 秒数；命令启动失败也保留 REJECTED 记录。
日志流式写入文件，结果完整性检查不等于对整个命令的文件访问实施沙箱。

目录输出只检查存在非空内容；关键结果必须逐文件 --output 声明，不能只给一个含无关文件的大目录。

## 4. 程序成功不等于科学验证

分开记录：

| 判断 | 含义 | 谁负责 |
|---|---|---|
| execution_status | 命令是否成功执行 | 运行工具 |
| artifact_integrity | 声明产物是否通过本次来源/非空检查 | 运行工具 |
| scientific_validity | 模型、数据、验证及现实约束是否支持结论 | 建模质量门 |
| contest_task_completion | 原题交付项是否回答完整 | Requirement 回查 |

--status FINAL 只声明本次运行用途；工具不会自动通过后两项，它们初始为 NOT_ASSESSED。
只有机械检查通过、质量门为 PASS 或有依据的 QUALIFIED，且对应交付项满足后，才在蓝图登记 FINAL_RUN_ID。
纯解析推导/证明可记 Run 不适用，并给可核查推导；数据计算和数值实验不能借此豁免真实运行。

## 5. 结果替换与下游失效

新运行取代旧运行时：

1. 旧记录标 SUPERSEDED 并登记新 Run，保留历史产物；
2. 更新对应 Requirement 的 FINAL_RUN_ID；
3. 沿实际依赖重跑已确认且已求解的后问，重新生成受影响图表；尚未确认的后问仍先讨论方案；
4. 更新蓝图、问题详解与已写论文，再核对内部包。

下游接口记录上游 Run、正式文件/字段/单位和实际读取位置。不能从聊天、截图或同名旧 CSV 手抄数字。
可将运行专属产物复制到正式 data/tables/figures 便于阅读，但记录源 Run 与 hash，避免把整理副本当成新运行。

## 6. 随机算法的两个不同目标

评价 GA/PSO/仿真/Bootstrap 等性能时，报告重复次数、seed 策略、停止条件、分布/离散程度和失败情况，不能只展示最好一次冒充稳定表现。
优化题的最终交付方案可以从多次运行中选择最好的已验证可行解；同时保留该选择规则和整体表现，不把它声称为典型性能或已证明的全局最优。

## 7. 图表与论文引用

数据图引用 Final/Validation Run、正式数据与绘图脚本。
METHOD_FIGURE 可使用 Run ID=N/A（方法结构图），但必须追到已确认模型计划、代码步骤及 CURRENT/SUPERSEDED 方法版本。
图像类型以 python-visualization-policy.md 为权威定义。

README、问题详解与蓝图只引用权威 Run，不多份手抄完整参数。论文用结果和验证证据论证，正文无需展示内部状态标签。
