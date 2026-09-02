# Codex 单赛题工作空间规范

## 适用范围

适用于 Codex 及用户要求采用同类本地目录的 Agent。Chat 只交付附件时，不强制模拟完整本地工程。

一个根目录只处理一道已经选定的赛题。用户已有合理结构或明确指定路径时，以用户为准；未经允许不移动、覆盖、删除或改名用户原件。

---

## 1. 默认骨架

```text
2022-C/
├─ README.md
├─ 00_problem/                 # 原题、官方附件、官方模板
│  ├─ problem.pdf
│  ├─ attachments/
│  └─ official_template/
├─ 01_data/
│  ├─ raw/                     # 原始数据副本，不修改
│  ├─ processed/               # 清洗与特征数据
│  └─ external/                # 网络补充的真实数据
├─ 02_analysis/
│  ├─ security_audit/
│  ├─ problem_analysis.md
│  ├─ assumptions.md
│  ├─ symbols.md
│  ├─ model_plan.md
│  └─ qN_solution.md
├─ 03_code/
│  ├─ common/
│  ├─ q1/
│  ├─ q2/
│  ├─ qN/
│  └─ 总运行.py
├─ 04_results/
│  ├─ figures/
│  ├─ tables/
│  ├─ data/
│  ├─ logs/
│  └─ VISUALIZATION_MANIFEST.md
├─ 05_paper/
│  ├─ outline.md
│  ├─ draft.docx
│  ├─ final.docx
│  └─ final.pdf
├─ 06_submission/
│  ├─ internal_delivery/
│  └─ checklist.md
├─ 07_references/
│  ├─ papers/
│  ├─ websites.md
│  └─ notes.md
└─ 99_temp/
```

按实际问题数量创建 `qN/`，不提前制造大量空文件夹。不要再套一层 `modeling_workspace/` 或顶层 `deliverables/`。

---

## 2. 初始化原则

开始前检查：

- 当前根目录和用户已有文件；
- 实际问题数量；
- 哪些是官方原件、用户成果和 AI 生成物；
- 用户指定的命名、路径和工具链；
- 当前是新项目、迁移还是继续已有工程。

整理时：

1. 用户要求优先；
2. 合理结构直接复用；
3. 需要迁移时优先复制并记录来源映射；
4. 不为“看起来整齐”破坏已有可运行工程；
5. 不把临时文件散落在根目录。

---

## 3. 原题与数据边界

### `00_problem/`

保存官方原题、附件和模板。原文件保持不变，不写入程序输出。所有新文件先经过读题前或增量安全审计。

### `01_data/raw/`

保存建模程序读取的原始数据副本或官方压缩包解压后的原始表，不做清洗修改。若来自 `00_problem/attachments/`，记录两者对应关系。

### `01_data/processed/`

保存清洗、合并、单位统一、缺失处理和特征构造后的数据。每个重要文件至少可追溯到：

```text
原文件 / Sheet / 字段
→ 处理脚本与规则
→ 单位和口径变化
→ 使用问题与 Run ID
```

### `01_data/external/`

保存网络补充的真实数据。同步在 `07_references/websites.md` 或数据说明中记录发布机构、URL、获取日期、范围、单位、口径、处理脚本和用途。

禁止：覆盖原始 Excel/CSV、把清洗值写回 `raw/`、把插值/假设/仿真数据冒充观测数据。

---

## 4. 分析、源码与结果

### `02_analysis/`

- `security_audit/`：文件安全报告与证据；
- `problem_analysis.md`：题意、动作词、边界、单位和各问依赖；
- `assumptions.md`：采用、修改和废弃的假设；
- `symbols.md`：符号、单位和代码映射；
- `model_plan.md`：候选方案、评分、切换条件和用户确认；
- `qN_solution.md`：本问正式完成后的完整教程。

### `03_code/`

正式源码遵循 `python-code-documentation-policy.md`：

```text
03_code/q1/第一题.py
03_code/q2/第二题.py
03_code/总运行.py
```

复杂问题使用 `第一题_数据处理.py`、`第一题_模型求解.py`、`第一题_结果验证.py` 等中文职责名。公共读取、清洗、评价和导出逻辑进入 `common/`。

### `04_results/`

代码生成的图、表、数值和日志集中存放，不写回代码目录：

```text
04_results/
├─ figures/qN/{paper,validation,exploration,ai_communication}/
├─ tables/qN/
├─ data/qN/
├─ logs/{RUN_LEDGER.md,runs/}
└─ VISUALIZATION_MANIFEST.md
```

每个最终结果都能追到中文代码入口、输入数据和 `FINAL_RUN_ID`。旧 Run 的产物明确归档或标记过期。

科研图的脚本、用途目录、Manifest 和 AI 沟通图标记统一遵循 `python-visualization-policy.md`。

---

## 5. 论文、资料与提交

### `05_paper/`

`draft.docx` 或清楚的参考稿名称用于 AI 内部参考论文。`final.docx/final.pdf` 只在队员已经理解、核查并人工重写后使用，不能让 AI 初稿冒充终稿。

### `06_submission/`

`internal_delivery/` 保存四个内部包。真正官方提交文件只在终稿复审后，按当年官网、赛区和提交系统规则生成，不在目录模板中永久写死。

### `07_references/`

- `papers/`：实际下载并阅读过的论文、标准和报告；
- `websites.md`：机构、URL、访问日期、核验状态和用途；
- `notes.md`：资料具体帮助了哪一问和哪个参数/模型。

### `99_temp/`

只放一次性下载、转换、解压、调试和预览文件。任何唯一正式成果不得只存在这里；清理前确认没有复现依赖。

---

## 6. 根目录 README

工作区 `README.md` 是队员接手入口，至少记录：

- 赛题与当前进度；
- 文件安全审计状态；
- 各问方案与完成状态；
- 中文代码入口和运行命令；
- 各问 `FINAL_RUN_ID`；
- 最终数据、图表、论文和提交候选位置；
- 尚未解决的风险。

路线、Run、文件名或路径改变时同步更新。

---

## 7. 工作区验收

每问完成和整题交付前检查：

- [ ] 根目录没有散落临时脚本、CSV 和图片；
- [ ] 官方原件、raw、processed、external 严格分开；
- [ ] 外部数据有真实来源；
- [ ] 正式源码名称、注释和运行入口清楚；
- [ ] 正式输出集中在 `04_results/`；
- [ ] 每问结果能追到 `FINAL_RUN_ID`；
- [ ] 论文图、验证图、内部沟通图和安全审计图没有混放；
- [ ] 草稿、队员终稿、内部四包和官方提交候选没有混淆；
- [ ] 用户原文件未被擅自破坏；
- [ ] README 与实际目录一致。

目录服务于协作和追溯，不是为了摆一个漂亮的空架子。