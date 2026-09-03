# Codex 单赛题工作空间规范

## 目标

Codex、Claude Code 等可读写本地目录的 Agent，必须让题目、数据、分析、代码、结果、论文和提交材料可追溯，而不是把脚本、图片和临时表格散落在根目录。

用户现有工程、路径和命名优先。未经授权，不删除、覆盖、移动或改名用户原件。

---

## 1. 默认结构

一个根目录只对应一道已选赛题：

```text
2022-C/
├─ README.md
├─ 00_problem/                 # 题目、官方附件、官方模板
├─ 01_data/
│  ├─ raw/                     # 原始数据副本，不修改
│  ├─ processed/               # 清洗/变换/特征数据
│  └─ external/                # 外部真实数据
├─ 02_analysis/
│  ├─ security_audit/
│  ├─ problem_analysis.md
│  ├─ assumptions.md
│  ├─ symbols.md
│  ├─ model_plan.md
│  ├─ PAPER_EVIDENCE_BLUEPRINT.md
│  ├─ BLIND_BENCHMARK_PROVENANCE.md
│  └─ qN_solution.md
├─ 03_code/
│  ├─ common/
│  ├─ q1/
│  ├─ q2/
│  └─ 总运行.py或现有稳定入口
├─ 04_results/
│  ├─ figures/
│  ├─ tables/
│  ├─ data/
│  ├─ logs/
│  └─ VISUALIZATION_MANIFEST.md
├─ 05_paper/
├─ 06_submission/
├─ 07_references/
└─ 99_temp/
```

不提前创建没有实际用途的空目录。题目有几问就创建几个 `qN/`。

已有仓库、CI、包模块、Notebook 或工具链采用其他合理结构时，映射职责即可，不强制套模板或改成中文文件名。

---

## 2. 根 README 是接手入口

工作区 `README.md` 只记录队员接手需要的信息：

- 赛题、当前进度和各问状态；
- 文件安全审计状态；
- 运行模式：LIVE_CONTEST / BLIND / OPEN_REFERENCE；
- Skill 版本与 commit、模型、推理档位和工具权限（可取得时）；
- 每问主入口和 `FINAL_RUN_ID`；
- 当前主路线、重大风险和待确认事项；
- Evidence Blueprint、结果、论文和提交文件位置；
- 关键运行命令。

路线、Final Run、入口或输出路径变化时同步更新。无法取得精确信息时写 unknown/unavailable，不猜测。

---

## 3. 原题与数据边界

### `00_problem/`

只保存官方原题、附件和模板。原件不被清洗脚本或审计流程覆盖。

### `01_data/raw/`

保存程序实际读取的原始数据副本、解压后的原始表或按 Sheet 导出的原始内容，必须能映射回官方附件，不写入清洗结果。

### `01_data/processed/`

保存清洗、合并、单位统一、零值/缺失处理和特征构造后的数据。每个重要文件能追到来源文件/Sheet/字段、处理脚本、规则、单位变化和使用它的 Run。

### `01_data/external/`

保存从政府、统计机构、对象官网、行业机构或其他可靠来源取得的外部原始数据。记录发布机构、URL、获取日期、时间/空间范围、单位、口径、许可、处理脚本和实际用途。

严禁把假设、插值、估计或仿真冒充观测数据。

---

## 4. 分析与版本溯源

### `security_audit/`

保存正常人类视图、隐藏对象可见化图、Evidence ID、哈希、OCR 对照和安全报告。安全审计图不属于论文结果图。

### `problem_analysis.md / assumptions.md / symbols.md / model_plan.md`

分别维护题意与跨问关系、假设及风险、符号/单位/代码映射、候选路线与用户确认。

### `BLIND_BENCHMARK_PROVENANCE.md`

旧题盲测记录 Skill/commit、模型、推理档位、工具、搜索边界、题目哈希、冻结时间、冻结产物 hash 和参考资料开放时间。开放参考后的改进另建版本并标记 POST_HOC。

### `PAPER_EVIDENCE_BLUEPRINT.md`

各问 Final/Validation Run 冻结后建立。每个原题交付项登记主答案、证据等级、科学有效性、竞赛完成度、正文位置、主表/图/公式、独立验证、限制和跨问接口。

---

## 5. 代码与结果

正式源码进入 `03_code/`，遵循项目现有命名和 `python-code-documentation-policy.md`。新建中文赛题项目可使用 `第一题.py` 等中文语义名；已有工程优先保持既有约定。

要求：

- 路径相对项目根目录；
- 不硬编码个人绝对路径；
- 不覆盖 raw/官方附件；
- 正式输出统一写入 `04_results/`；
- 临时调试进入 `99_temp/`；
- 关键运行登记 Run Ledger；
- 每问明确 Final Run；
- 旧结果标记或归档，不能与当前最终结果混用。

`04_results/figures/` 按 paper / method / validation / exploration / ai_communication 分用途；普通表格进入 `tables/`，不截图冒充可编辑表格。

---

## 6. 论文与提交

`05_paper/` 保存提纲、AI 内部参考稿和队员重写稿。AI 第一次生成的稿件不得冒充队员最终论文。

`06_submission/` 只放经过审核的内部包和官方提交候选。内部四包可以放在：

```text
06_submission/internal_delivery/
```

真正上传文件以当年官方、赛区和系统规则为准。不要把整个工作区原样压缩成官方源码包，也不要混入 AI 沟通图、安全审计缓存和无关旧 Run。

---

## 7. 临时文件与清理

`99_temp/` 可存放临时下载、解包缓存、转换文件、一次性脚本和预览图。

最终代码、数据、证据、图表和报告不能只存在临时目录。清理前确认没有正式成果依赖其中内容。

---

## 8. 每问/全题检查

- [ ] 根目录没有散落唯一正式脚本、CSV 或图片；
- [ ] 原题、官方附件和 raw 数据未被覆盖；
- [ ] raw / processed / external 分层清楚；
- [ ] 外部数据有来源和口径；
- [ ] 本问代码入口、Final Run 和结果路径可定位；
- [ ] 图、表、数值和日志进入 `04_results/`；
- [ ] 盲测版本和参考资料开放边界已记录（适用时）；
- [ ] Evidence Blueprint 在论文写作前完成；
- [ ] 草稿、队员终稿、内部包和官方候选没有混淆；
- [ ] 用户原文件未被擅自破坏；
- [ ] 根 README 与实际目录一致。
