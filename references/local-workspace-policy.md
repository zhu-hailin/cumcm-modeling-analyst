# Codex 单赛题工作空间规范

## 适用范围

本规范适用于 Codex，以及具备同等本地文件读写能力、且用户明确要求采用该结构的本地 Agent。

Chat / 云端会话只负责附件交付时，不强制模拟完整本地目录。

如果本规范与旧版 `modeling_workspace/`、顶层 `deliverables/`、`run_all.py` 或英文临时脚本示例冲突，Codex 本地工作时以本规范和 `python-artifact-naming-policy.md` 为准。

---

## 1. 一个工作空间只对应一道赛题

根目录使用“年份-题号”或用户指定名称，例如：

```text
2022-C/
```

不要把 A、B、C 等不同赛题混在同一个工作空间里。

如果用户已经创建项目根目录，优先在现有目录内工作，不再套一层重复目录。目录命名、路径和已有工程习惯最终以用户要求为准。

---

## 2. 默认目录结构

```text
2022-C/
├─ README.md
│
├─ 00_problem/                 # 题目与官方附件
│  ├─ problem.pdf
│  ├─ attachments/
│  └─ official_template/
│
├─ 01_data/                    # 数据
│  ├─ raw/                     # 原始数据，不修改
│  ├─ processed/               # 清洗后的建模数据
│  └─ external/                # 外部补充数据
│
├─ 02_analysis/                # 建模分析与思路
│  ├─ security_audit/
│  ├─ problem_analysis.md
│  ├─ assumptions.md
│  ├─ symbols.md
│  ├─ model_plan.md
│  └─ qN_solution.md
│
├─ 03_code/                    # 正式 Python
│  ├─ common/                  # 公共函数
│  ├─ q1/                      # 问题一
│  ├─ q2/                      # 问题二
│  ├─ q3/                      # 问题三
│  ├─ qN/                      # 按实际问题数量继续
│  └─ 总运行.py                # 整题总入口
│
├─ 04_results/                 # 程序生成结果
│  ├─ figures/
│  ├─ tables/
│  ├─ data/
│  ├─ logs/
│  └─ VISUALIZATION_MANIFEST.md
│
├─ 05_paper/                   # 论文
│  ├─ outline.md
│  ├─ draft.docx
│  ├─ final.docx
│  └─ final.pdf
│
├─ 06_submission/              # 内部包与提交候选
│  ├─ internal_delivery/
│  ├─ paper.pdf
│  ├─ source_code.zip
│  └─ checklist.md
│
├─ 07_references/              # 查阅资料与论文
│  ├─ papers/
│  ├─ websites.md
│  └─ notes.md
│
└─ 99_temp/                    # 临时文件
```

这是默认骨架，不要求提前创建所有空文件。实际有几问就创建几个 `qN/`；没有问题四就不创建 `q4/`。

---

## 3. 初始化前先看用户现有项目

Codex 开始整理前先检查：

- 当前根目录是否已经存在；
- 用户是否已经放入题目、附件、模板、数据或代码；
- 实际有几问；
- 用户是否指定文件名、目录名和输出路径；
- 当前是新项目、旧项目迁移，还是继续现有工作区；
- 哪些文件属于用户原件，哪些是 AI 生成物。

处理原则：

1. 用户明确要求优先；
2. 已有合理结构直接复用；
3. 未经授权不删除、覆盖、移动或改名用户原件；
4. 需要整理时优先复制并保留来源映射；
5. 不为了形式整齐创建重复目录；
6. 中文源码命名遵循 `python-artifact-naming-policy.md`。

---

## 4. `README.md` 是工作区入口

根目录 `README.md` 用来让队员快速接手，不写成长篇论文。

至少记录：

- 赛题名称与题号；
- 文件安全审计状态；
- 当前进度和各问状态；
- 当前推荐路线；
- 每问主入口，例如 `03_code/q1/第一题.py`；
- 整题入口 `03_code/总运行.py`；
- 每问 `FINAL_RUN_ID`；
- 正式图、结果、论文和提交文件位置；
- 尚未解决的数据或模型风险。

重大路线变化、Final Run 替换、文件重命名或输出路径变化时同步更新。

---

## 5. `00_problem/`：官方原件归档区

`00_problem/` 只保存原题、官方附件和官方模板。

硬性规则：

- 官方原件不得被清洗脚本直接修改；
- 不把程序输出写回官方附件；
- 不在该目录放 AI 生成表格、截图或临时文件；
- 原文件名尽量保留，必要重命名时记录映射；
- 所有文件先通过读题前安全审计。

---

## 6. `01_data/`：原始、清洗和外部数据分层

### `raw/`

保存建模程序实际读取的原始数据副本，内容不修改。

若数据来自 `00_problem/attachments/`：

- `00_problem/attachments/` 是官方归档原件；
- `01_data/raw/` 可以放供代码读取的副本、解压后的原始文件或按 Sheet 导出的原始表；
- 必须说明两者对应关系；
- 不得把清洗结果写入 `raw/`。

### `processed/`

保存清洗、合并、单位统一、缺失处理和特征构造后真正用于模型的数据。

每个重要文件至少能追溯：

- 来源文件、Sheet 和字段；
- 处理脚本；
- 清洗步骤；
- 单位与口径变化；
- 被哪些问题和 Run 使用。

不允许只留下来源不明的 `final_data.xlsx`。

### `external/`

保存从网络、政府网站、行业机构、对象官网或其他真实来源补充的数据。

至少记录发布机构、原始链接、下载日期、范围、字段、单位、口径、处理脚本和实际用途。外部数据不得由 AI 凭空补值。

---

## 7. `02_analysis/`：分析、教程与安全证据

### `security_audit/`

保存读题前和增量文件安全审计的报告、Manifest、正常视图、隐藏对象可见化图和 OCR 对照。

审计图属于 `SECURITY_AUDIT_ONLY`，不能混入模型结果图或论文。

### `problem_analysis.md`

记录题意拆解、动作词、输入输出、约束、边界、单位和各问依赖。

### `assumptions.md`

记录采用、修改和废弃的假设及其依据、适用范围和风险。

### `symbols.md`

维护统一符号、单位、上下标和中文源码变量映射。

### `model_plan.md`

记录各问候选方法、推荐指数、主路线、备用路线、切换条件、用户确认和跨问接口。

### `qN_solution.md`

当前问题正式完成后保存完整教程，说明题意、数据、公式、中文源码、Final Run、图表、验证和下一问接口。

---

## 8. `03_code/`：正式 Python 与中文命名

完整遵循：

- `python-code-documentation-policy.md`
- `python-artifact-naming-policy.md`

### 每问主入口

```text
03_code/q1/第一题.py
03_code/q2/第二题.py
03_code/q3/第三题.py
```

复杂问题可拆为：

```text
03_code/q1/
├─ 第一题.py
├─ 第一题_数据处理.py
├─ 第一题_模型求解.py
├─ 第一题_结果验证.py
├─ 第一题_结果导出.py
├─ 论文图/
│  └─ 第一题_实际值与预测值对比图.py
└─ AI沟通图/
   └─ AI沟通图_第一题_候选模型比较.py
```

### `common/`

公共模块使用中文语义名称，例如：

```text
数据读取.py
数据清洗.py
绘图工具.py
评价指标.py
结果导出.py
```

### `总运行.py`

作为整题总入口，按问题依赖顺序调用各问最终流程。

要求：

- 路径尽量相对根目录；
- 不把输出散落到代码目录；
- 输出统一写入 `04_results/`；
- 运行失败有清楚日志；
- 不硬编码本机私人绝对路径；
- 所有中文源码保存为 UTF-8；
- 交付前真实执行 `python "03_code/总运行.py"` 或等价命令；
- 技术文件如 `__init__.py`、`requirements.txt` 可保留规范名称。

---

## 9. `04_results/`：结果与图像用途分层

所有正式代码生成的结果集中写入这里。

推荐：

```text
04_results/
├─ figures/
│  ├─ q1/
│  │  ├─ paper/
│  │  ├─ validation/
│  │  ├─ exploration/
│  │  └─ ai_communication/
│  ├─ q2/
│  └─ final/
├─ tables/
│  ├─ q1/
│  ├─ q2/
│  └─ final/
├─ data/
│  ├─ q1/
│  ├─ q2/
│  └─ final/
├─ logs/
│  ├─ RUN_LEDGER.md
│  └─ runs/
└─ VISUALIZATION_MANIFEST.md
```

### 论文图

论文候选图进入 `paper/`，并有对应中文绘图脚本，例如：

```text
03_code/q1/论文图/第一题_预测结果图.py
04_results/figures/q1/paper/第一题_预测结果图.png
04_results/figures/q1/paper/第一题_预测结果图.svg
```

### AI 沟通图

AI 沟通图进入 `ai_communication/`，文件名以 `AI沟通图_` 开头，并在图面显示：

```text
AI内部沟通图｜非论文材料
```

Manifest 记录 `AI_COMMUNICATION_ONLY`、不进入论文、不进入官方提交。

### 其他要求

- 表格进入 `tables/`；
- 数值、模型对象和跨问接口进入 `data/`；
- 每个最终结果能追到代码、输入和 `FINAL_RUN_ID`；
- 新 Run 替代旧 Run 后，旧产物明确归档或标记过期；
- AI 沟通图不能简单改名后进入论文。

---

## 10. `05_paper/`：论文工作区

`outline.md` 保存提纲、章节负责人、图表位置、公式清单和待补内容。

AI 第一次生成的内部参考稿使用 `draft.docx` 或明确的参考论文名称。`final.docx`、`final.pdf` 只有在队员人工理解、核查和重写后才使用。

论文中不得混入：

- `AI_COMMUNICATION_ONLY`；
- `SECURITY_AUDIT_ONLY`；
- Stage 1 旧图；
- `SUPERSEDED` Run 的图表；
- 没有中文绘图脚本和 Manifest 证据链的结果图。

---

## 11. `06_submission/`：内部包与官方提交候选

默认：

```text
06_submission/
├─ internal_delivery/
│  ├─ 题目详解.zip
│  ├─ 参考论文.zip
│  ├─ 源码.zip
│  └─ 其他.zip
├─ paper.pdf
├─ source_code.zip
└─ checklist.md
```

这些官方文件名只是默认示例。正式比赛必须先核验当年官网、赛区和提交系统规则。

如果官方系统不支持中文文件名，可以生成一份兼容副本，并在 `checklist.md` 中记录中文名到兼容名的映射和运行验证。工作区中文源码不被偷偷替换。

AI 沟通图及其脚本默认不进入官方源码候选。

---

## 12. `07_references/`：资料与论文

`papers/` 保存实际下载并阅读过的论文、标准、报告和官方文档。

`websites.md` 记录网站标题、发布机构、URL、访问日期、页面/下载状态和用途。

`notes.md` 记录每份资料帮助了哪一问、支撑哪个参数或模型、是否进入最终参考文献。

文件型资料先做增量安全审计，再允许阅读和引用。

---

## 13. `99_temp/`：真正的临时区

可存放临时下载、一次性转换、调试图片、测试脚本、解压缓存和中间预览。

规则：

- 最终代码、数据、图表和正式引用不能只存在这里；
- 有复现价值的文件迁移到正式目录；
- 交付前清理明显无用内容；
- 清理前确认正式成果不依赖该目录。

---

## 14. 文件管理验收

Codex 在每问完成和整题结束时检查：

- [ ] 原题、附件和模板位于 `00_problem/`；
- [ ] 原始、清洗和外部数据严格分开；
- [ ] 正式 Python 使用 `第一题.py / 第二题.py / ...` 和中文职责名；
- [ ] 整题入口为 `总运行.py`；
- [ ] 技术性英文文件名都有真实理由；
- [ ] 论文图脚本与输出图语义主干一致；
- [ ] AI 沟通图有目录、文件名、图面和 Manifest 标记；
- [ ] AI 沟通图和审计图没有进入论文或官方提交；
- [ ] 输出集中在 `04_results/`；
- [ ] 每问结果能追到 `FINAL_RUN_ID`；
- [ ] 论文草稿与终稿命名没有混淆；
- [ ] `99_temp/` 没有唯一正式成果；
- [ ] 用户文件没有被擅自覆盖、删除或改名；
- [ ] 实际目录与根目录 `README.md` 一致。

目录服务于比赛协作和结果追溯，不是为了摆出一个好看的空架子。
