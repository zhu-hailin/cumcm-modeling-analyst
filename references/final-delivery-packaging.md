# INTERNAL_DELIVERY：内部四包

## 目标

全部问题、Final Run、建模证据门、图表 QA、公式和一致性检查通过后，生成：

```text
题目详解.zip
参考论文.zip
源码.zip
其他.zip
```

它们用于队员学习、复核、复现、人工写论文和赛后留档，**不等于官方提交文件**。

Codex 未指定其他位置时保存到：

```text
06_submission/internal_delivery/
```

本地正式目录是主成果，ZIP 是筛选后的副本。打包后不得删除原文件。

---

## 1. `题目详解.zip`

推荐：

```text
题目详解/
├─ 00_赛题总览.md
├─ 问题1/问题1_完整教程.md
├─ 问题2/问题2_完整教程.md
└─ 问题N/问题N_完整教程.md
```

每问教程至少串起：

```text
题意与数据结构
→ 数据处理与来源
→ 候选方案和选模依据
→ 变量、公式和假设
→ 中文源码与运行命令
→ FINAL_RUN_ID
→ 结果、图表和表格
→ 独立验证与现实约束
→ 限制
→ 向后问传递什么
```

文本使用 UTF-8 Markdown，公式遵循 `equation-rendering-policy.md`，数字只来自对应 Final/Validation Run。

---

## 2. `参考论文.zip`

默认：

```text
参考论文/
├─ 数学建模参考论文.docx
└─ 数学建模参考论文.pdf
```

这是 AI 根据本次赛题认真撰写的内部参考论文，不是网上论文合集，也不能因为外部全文无法下载而留空。

必须：

- 基于最终模型、数据、Final/Validation Run；
- 只使用通过 `VISUALIZATION_MANIFEST.md` 和科研图 QA 的图；
- 图、表、数字、模型名和结论一致；
- 公式在 Word/PDF 中正确渲染；
- 文献和数据来源真实可核验；
- 通过 `final-consistency-sweep.md`。

> AI 参考论文必须由队员理解、核查并人工重写，禁止直接提交。

---

## 3. `源码.zip`

推荐：

```text
源码/
├─ README.md
├─ requirements.txt
├─ 总运行.py
├─ common/
├─ q1/
│  ├─ 第一题.py
│  └─ 论文图/
├─ q2/
│  └─ 第二题.py
├─ data/
│  ├─ processed/
│  └─ external/
├─ results/
│  ├─ figures/
│  ├─ tables/
│  └─ data/
└─ VISUALIZATION_MANIFEST.md
```

包含：

- 每问中文主入口和实际需要的辅助模块；
- `总运行.py`；
- 有效 docstring 和建模注释；
- 所有进入论文的中文绘图脚本；
- 必要验证脚本；
- 复现所需且允许分发的数据、依赖和结果。

默认不包含：

- `99_temp/`；
- 无用旧代码、缓存和过期 Run；
- Skill 提示词、聊天记录和 AI 水印；
- `AI_COMMUNICATION_ONLY` 图片及脚本；
- `SECURITY_AUDIT_ONLY` 图片；
- 许可不允许再分发的外部数据。

源码必须真实运行，能复现对应 Final Run。外部数据不能再分发时，提供官方获取说明和处理脚本。

---

## 4. `其他.zip`

推荐：

```text
其他/
├─ AI使用说明/AI_USAGE_LOG.md
├─ 建模分析/
│  ├─ problem_analysis.md
│  ├─ assumptions.md
│  ├─ symbols.md
│  └─ model_plan.md
├─ 运行与实验/
│  ├─ RUN_LEDGER.md
│  └─ 重要运行记录/
├─ 文献与来源/
│  ├─ websites.md
│  └─ notes.md
├─ 数据来源与处理/
├─ 文件安全审计/
├─ 一致性检查/
└─ 环境与复现/
```

安全审计材料只用于内部核查，不进入官方论文或普通科学图清单。内部 AI 日志保持真实完整；正式 AI 使用说明按当年官方规则另行导出。

有复盘价值的 AI 沟通图可以放入明确的内部目录，但必须保留 `AI沟通图_` 文件名、图面角标和用途说明。

---

## 5. 打包前质量门

确认：

- [ ] 原题 Requirement Traceability 完成；
- [ ] 每问有明确 `FINAL_RUN_ID`；
- [ ] `MODELING_EVIDENCE_GATE_FAILED` 已解决；
- [ ] 源码命名、注释、纯净度和真实运行通过；
- [ ] 论文图能追到中文脚本、数据和 Run；
- [ ] 分辨率、矢量版本、最终尺寸、字体、单位、颜色和误差通过；
- [ ] AI 沟通图和安全审计图未混入论文；
- [ ] Markdown 与 Word/PDF 公式通过；
- [ ] 文献、数据和链接真实；
- [ ] 跨成果重大冲突已解决；
- [ ] DOCX/PDF 存在、非空且可打开。

---

## 6. ZIP 完整性

每个 ZIP 必须：

1. 检查打包源文件存在且非 0 字节；
2. 执行 CRC/entry 结构测试；
3. 实际解压到 `99_temp/zip_check/` 或新的临时目录；
4. 从解压副本检查路径、中文文件名、数量、大小、文件可读性；
5. 验证 DOCX/PDF、Python、图表和数据；
6. 推荐用 `MANIFEST.md + SHA-256` 对账；
7. 验收后再清理临时解压目录。

不能只看源目录或只跑 `unzip -t` 就声称用户一定能使用。

失败：

```text
DELIVERY_INTEGRITY_FAILED
```

---

## 7. 与官方提交的边界

```text
INTERNAL_DELIVERY_COMPLETE
→ 队员理解、核查并人工重写论文
→ FINAL_PAPER_AUDIT
→ 核验当年官方、赛区和提交系统规则
→ OFFICIAL_SUBMISSION_EXPORT
```

不得把 `参考论文.zip` 中的 AI 稿直接复制为官方论文，也不得把内部四包误称为已经可以上传的官方文件。

全部内部验收通过后才标记：

```text
INTERNAL_DELIVERY_COMPLETE
```