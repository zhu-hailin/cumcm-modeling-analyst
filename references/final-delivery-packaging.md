# INTERNAL_DELIVERY：内部四包与打包规范

## 目标

全部问题完成、结果通过验证、参考论文生成并完成一致性检查后，进入：

```text
INTERNAL_DELIVERY
```

固定生成：

```text
题目详解.zip
参考论文.zip
源码.zip
其他.zip
```

它们用于队伍学习、复核、复现、人工重写论文和终稿审核，不等于官方比赛提交文件。

正式比赛需要上传时，必须在队员人工重写论文并完成终稿审核后，再执行 `OFFICIAL_SUBMISSION_EXPORT`。

---

# 1. Codex 本地保存位置

Codex 工作区遵循：

- `local-workspace-policy.md`
- `python-code-documentation-policy.md`
- `python-artifact-naming-policy.md`

未指定其他位置时，内部包保存到：

```text
06_submission/internal_delivery/
├─ 题目详解.zip
├─ 参考论文.zip
├─ 源码.zip
├─ 其他.zip
└─ MANIFEST.md
```

打包源文件继续保留在正式工作目录中。ZIP 是筛选后的副本，不得打包后删除原文件。

---

# 2. `题目详解.zip`

推荐：

```text
题目详解/
├─ 00_赛题总览.md
├─ 问题1/
│  └─ 问题1_完整教程.md
├─ 问题2/
│  └─ 问题2_完整教程.md
└─ 问题N/
   └─ 问题N_完整教程.md
```

每问教程至少串起：

```text
题意
→ 输入输出
→ 数据与来源
→ 模型选择理由
→ 变量、公式和假设
→ 中文源码文件
→ FINAL_RUN_ID
→ 实际结果
→ 图像用途分类
→ 图表和表格
→ 验证
→ 下一问接口
```

教程中的代码路径必须指向真实中文文件，例如：

```text
03_code/q1/第一题.py
03_code/q1/第一题_模型求解.py
03_code/q1/论文图/第一题_预测结果图.py
```

不能继续引用已经不存在的 `main.py`、`run_all.py` 或旧文件名。

---

# 3. `参考论文.zip`

默认：

```text
参考论文/
├─ 数学建模参考论文.docx
└─ 数学建模参考论文.pdf
```

AI 参考论文是内部参考稿，不得冒充队员最终参赛论文。

论文必须：

- 基于各问最终模型和 `FINAL_RUN_ID`；
- 使用最终 Python 结果；
- 图表来自最终 `VISUALIZATION_MANIFEST.md`；
- 论文图能追到中文绘图脚本；
- 表格与 `04_results/tables/` 一致；
- 公式在 Word/PDF 中正确渲染；
- 引用真实可核验；
- 通过最终一致性检查。

禁止进入参考论文：

```text
AI_COMMUNICATION_ONLY
SECURITY_AUDIT_ONLY
SUPERSEDED Run 图表
Stage 1 临时旧图
没有 Figure Contract / Run / 中文绘图脚本证据链的结果图
```

AI 沟通图不能靠删除角标或改名进入论文，必须重新生成正式论文图。

---

# 4. `源码.zip`

推荐：

```text
源码/
├─ README.md
├─ requirements.txt
├─ 总运行.py
├─ common/
│  ├─ 数据读取.py
│  ├─ 数据清洗.py
│  ├─ 绘图工具.py
│  ├─ 评价指标.py
│  └─ 结果导出.py
├─ q1/
│  ├─ 第一题.py
│  ├─ 第一题_数据处理.py
│  ├─ 第一题_模型求解.py
│  ├─ 第一题_结果验证.py
│  └─ 论文图/
│     ├─ 第一题_预测结果图.py
│     └─ 第一题_残差诊断图.py
├─ q2/
│  └─ 第二题.py
├─ qN/
├─ data/
│  ├─ processed/
│  └─ external/
├─ results/
│  ├─ figures/
│  ├─ tables/
│  └─ data/
└─ VISUALIZATION_MANIFEST.md
```

要求：

- 每问主入口使用 `第一题.py / 第二题.py / ...`；
- 总入口使用 `总运行.py`；
- 辅助模块使用“问题编号 + 中文职责”命名；
- 所有论文候选图附带同语义中文绘图脚本；
- 正式源码注释有用、准确，与当前实现一致；
- 源码不包含 Skill、聊天、内部状态、提示词或 AI 水印；
- `总运行.py` 在合理环境中能够复现最终流程；
- 普通结果表使用 CSV/XLSX，不全部截图成 PNG；
- 不把 `99_temp/`、缓存、无用旧模型和过期结果打包。

### 技术文件名例外

`__init__.py`、`pyproject.toml`、`requirements.txt` 等工具链名称可以保留。普通建模脚本不属于例外。

### AI 沟通图

AI 沟通图及其脚本默认不进入官方源码候选。

如果对队伍内部复盘有价值，可以在内部包中保留，但必须放在明确目录：

```text
源码/内部沟通材料/AI沟通图/
```

并继续保留：

```text
文件名前缀：AI沟通图_
图面标记：AI内部沟通图｜非论文材料
用途类型：AI_COMMUNICATION_ONLY
```

不得把它与论文图混放。

---

# 5. `其他.zip`

推荐：

```text
其他/
├─ AI使用说明/
│  └─ AI_USAGE_LOG.md
├─ 建模分析/
│  ├─ problem_analysis.md
│  ├─ assumptions.md
│  ├─ symbols.md
│  └─ model_plan.md
├─ 文件安全审计/
├─ 运行与实验/
│  ├─ RUN_LEDGER.md
│  └─ 重要运行记录/
├─ 文献与来源/
├─ 数据来源与处理/
├─ 一致性检查/
├─ 环境与复现/
├─ 赛时协作记录/
└─ AI内部沟通图/             # 只有确有复盘价值时保留
```

AI 沟通图在 `其他.zip` 中仍必须保持文件名和图面标记。安全审计图单独放在“文件安全审计”，不能与模型图混淆。

---

# 6. 图像 Manifest 与用途验收

打包前检查 `04_results/VISUALIZATION_MANIFEST.md` 至少包含：

| 图号 | 文件 | 用途类型 | 问题 | Run ID | 数据源 | 生成脚本 | 图面标记 | 进入论文 | 进入官方提交 |
|---|---|---|---|---|---|---|---|---|---|

约束：

- `PAPER_FIGURE` 才可作为论文核心候选；
- `VALIDATION_FIGURE` 按价值决定是否入文；
- `EXPLORATION_FIGURE` 默认不入文；
- `AI_COMMUNICATION_ONLY` 不进入论文和官方提交；
- `SECURITY_AUDIT_ONLY` 只进入内部审计材料。

失败状态：

```text
FIGURE_PURPOSE_MARKING_FAILED
AI_COMMUNICATION_FIGURE_LEAKED
```

---

# 7. 中文文件名验收

打包前检查：

- 每问主入口中文命名；
- 总入口为 `总运行.py`；
- 论文图脚本和输出图使用相同中文语义主干；
- 文件名没有“最终版、最新版、真的最终版”等版本词；
- 中文源码统一 UTF-8；
- 运行命令、教程、Run Ledger 和 Manifest 使用同一真实路径；
- ZIP 内中文文件名真实解压后不乱码；
- 解压后的中文源码能够运行。

失败状态：

```text
PYTHON_FILENAME_POLICY_FAILED
```

---

# 8. 跨成果一致性验收

打包前执行 `final-consistency-sweep.md`，至少核对：

```text
原题与附件
↔ 数据
↔ 中文源码与注释
↔ 各问 FINAL_RUN_ID
↔ 图像用途与中文绘图脚本
↔ 结果表
↔ 题目详解
↔ 参考论文
↔ 四个内部包
```

重点检查旧文件名、旧 Run、旧图、图像用途泄漏、注释与公式不一致、摘要正文结论冲突。

重大冲突：

```text
CROSS_ARTIFACT_CONSISTENCY_FAILED
```

---

# 9. ZIP 完整性预检

每个 ZIP 至少执行：

1. 源目录和关键文件检查；
2. ZIP CRC / entry 结构检查；
3. 实际解压到 `99_temp/zip_check/` 或其他临时目录；
4. 从解压副本检查文件名、数量、大小、0 字节、DOCX/PDF、中文源码、数据、图表和表格；
5. 真实运行解压后的 `总运行.py` 或合理的最小复现入口；
6. 推荐使用 `MANIFEST.md + SHA-256` 做打包前后对账；
7. 验收后再清理临时目录。

异常：

```text
DELIVERY_INTEGRITY_FAILED
```

---

# 10. 官方提交兼容副本

工作区和内部源码包默认保留中文语义文件名。

如果当年官方提交系统明确不支持中文文件名，可以在 `06_submission/` 生成经过验证的兼容副本，并在 `checklist.md` 中记录：

- 中文原文件名；
- 兼容文件名；
- 映射原因；
- 修改的导入路径；
- 实际运行验证结果。

不得偷偷替换工作区中文源码，也不得让论文、Run Ledger 和 Manifest 指向不存在的旧路径。

---

# 11. 内部最终验收

- [ ] 原题、原始数据、清洗数据和外部数据分层正确；
- [ ] 每问正式代码为中文语义文件名；
- [ ] 总入口为 `总运行.py`；
- [ ] 源码注释与纯净度通过；
- [ ] 每问最终结果能追到 `FINAL_RUN_ID`；
- [ ] 每张论文图有同语义中文绘图脚本；
- [ ] AI 沟通图三层标记完整；
- [ ] AI 沟通图没有进入参考论文和官方候选；
- [ ] 图、表、数据和日志集中在正式目录；
- [ ] 参考论文 DOCX/PDF 存在、非空、可打开；
- [ ] 四个 ZIP 已真实解压验证；
- [ ] 中文文件名在解压环境中正常；
- [ ] 重大跨成果冲突已解决；
- [ ] 用户原文件没有被擅自覆盖、删除或改名。

全部通过：

```text
INTERNAL_DELIVERY_COMPLETE
```

不要把这一状态描述成“官方提交已经准备完成”。
