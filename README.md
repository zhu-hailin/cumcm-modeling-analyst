<p align="center">
  <a href="assets/readme-showcase/hero-cumcm-modeling-analyst.svg">
    <img src="assets/readme-showcase/hero-cumcm-modeling-analyst.svg" alt="CUMCM Modeling Analyst：让建模思路成为可信成果。逐题确认、真实求解、证据驱动写作。" width="100%" />
  </a>
</p>

<div align="center">

# CUMCM Modeling Analyst

**面向数学建模竞赛的 AI 协作 Skill**

读懂题目 · 研究模型 · 逐题求解 · 验证结果 · 组织论文

[![Version](https://img.shields.io/badge/version-11.4-0F766E?style=flat-square)](CHANGELOG.md)
[![Validation](https://github.com/zhu-hailin/cumcm-modeling-analyst/actions/workflows/validate.yml/badge.svg)](https://github.com/zhu-hailin/cumcm-modeling-analyst/actions/workflows/validate.yml)
[![Python](https://img.shields.io/badge/helper_tools-Python_3.11%2B-3776AB?style=flat-square)](requirements-tools.txt)

[核心能力](#capabilities) · [工作流程](#workflow) · [快速开始](#quick-start) · [质量与边界](#quality) · [工具与维护](#development)

</div>

把赛题、数据与已有思路，逐步转化为**队员能理解、能复核、能继续使用的建模成果**。模型怎么选，由问题与证据决定；Skill 负责组织研究、明确协作边界，并让代码、结果、图表和论文保持一致。

> AI 生成的内部参考论文不能直接提交。参赛队员须理解、核验并自行重写，实际比赛始终以当年官方规则为准。

<a id="capabilities"></a>

## 从题意到成果，每一步都有交付

| 环节 | 你会得到什么 | 重点 |
|---|---|---|
| 读题与拆解 | 题意解析、交付清单、约束与跨问依赖 | 先回答对的问题 |
| 建模路线 | 机制分析、合理基线、候选比较与选优理由 | 解释为什么用这个模型 |
| 逐题求解 | 当前问代码、真实结果、独立验证与简洁交接 | 每问确认后推进，完成后暂停 |
| 科研图表 | 清晰结果表、模型对比图、必要的灵敏度分析图 | 一图一意，图与数据可追溯 |
| 参考论文 | 证据蓝图、内部参考稿、终稿复审建议 | 主答案醒目，论证连贯 |

只需要审题、改图、解释模型或复审论文？可以直接从对应任务进入，不必重走全流程。

<a id="workflow"></a>

## 全题先看清，解题逐问推进

<p align="center">
  <a href="assets/readme-showcase/cumcm-readme-workflow.svg">
    <img src="assets/readme-showcase/cumcm-readme-workflow.svg" alt="工作流程：初始题包审计与拆题，研究并比较路线；当前问方案确认后真实求解、独立验证、交付暂停。用户决定进入下一问并单独确认。全题证据齐备且需要完整稿时，冻结证据，生成内部参考论文，再由队员重写与复审。" width="100%" />
  </a>
</p>

<p align="center"><sub>点击查看高清 SVG · 图中为通用流程示意，不含旧题答案或实测成绩</sub></p>

**整题路线认可，不代替每问方案确认。** 已确认的本问内，代码修复、调参、求解器调整和验证可以自主进行；改变目标、关键假设或现实约束时，再交由团队决定。

初始题包只审计一次，锁定后复用。小任务按规模保留必要成果；仅改字、改图时，只更新受影响部分。详见[核心工作流](references/core-workflow.md)。

<a id="quick-start"></a>

## 快速开始

### 1. 获取 Skill

```bash
git clone https://github.com/zhu-hailin/cumcm-modeling-analyst.git
```

将仓库目录放入所用 Agent 支持的 Skill 位置，或让 Agent 明确读取本地入口。**仅克隆仓库不代表已经在所有应用中完成注册。** 不同工具的发现与加载方式以其实际支持为准。

### 2. 提供题目，先做分析

准备题面、官方附件，以及有助于核对公式或版面的正常可见截图，然后使用：

```text
请读取本地 cumcm-modeling-analyst/SKILL.md，
并按 manifest.yaml 加载当前阶段需要的规范。

使用这个 Skill 分析我提供的数学建模赛题：
先完成必要的初始题包审计、全题拆解与路线研究，
说明每问交付项、候选模型、选优理由、风险和跨问接口。
现在先不进入正式求解，等我确认当前问方案。
```

### 3. 确认当前问，再实现与验证

```text
确认第一问采用刚刚讨论的方案。
请完成本问实现、真实运行、独立验证与必要图表，
给出直接答案、适用边界和简洁交接。
第一问完成后暂停，不自动求解第二问。
```

能否读取 PDF、解析表格、执行 Python、联网和交付文件，取决于当前环境的实际能力。没有运行能力时，Skill 可以继续分析与可核查推导，并输出实施规格；需要计算的结果必须标为“待运行”。

<details>
<summary><strong>旧题训练：开启盲测边界</strong></summary>

```text
这是旧题盲测。独立成果冻结前，
不允许定位或读取历史答案、获奖论文或讲评；
可以核验通用理论、软件文档和去题目标识化的现实资料。
冻结后，等我明确同意，再开展历史答案对比。
```

先冻结独立方案和产物，再开放参考。事后学到的改进标为 POST_HOC，不回写成独立发现。README 展示图不使用真实旧题答案，避免污染后续训练。

详见[盲测与溯源规范](references/blind-benchmark-provenance.md)。

</details>

## 让建模优势真正进入论文

- **模型比较有理由**：在相同数据与评价口径下比较有价值的路线；不机械凑模型数量，也不把更换求解算法冒充新模型。
- **灵敏度分析能解释决策**：说明扰动依据、结果变化和失效边界；区分“固定方案承压”与“允许调整后重新优化”。
- **创新点有证据**：明确改了什么、为什么适合题目、相比基线改善了什么；必要时通过对照或消融验证。
- **摘要与主结果优先**：摘要凝练每问方法、关键结果与结论；重要数字集中呈现，前后问通过真实接口自然衔接。

代码文件名、区域注释和结果字段简体中文优先；正式科研图默认**单图单文件，图 1、图 2 独立编号**。探索图保持轻量，定稿图再检查字体、单位、误差、尺寸和清晰度。

Word 与 LaTeX 按团队与交付需求选择，最终以公式排版、页面可读性和官方要求验收。详细规则见[科研绘图](references/python-visualization-policy.md)、[参考论文写作](references/reference-paper-writing.md)与[公式规范](references/equation-rendering-policy.md)。

<a id="quality"></a>

## 质量，靠可核查的证据

| 检查 | 保证什么 | 不代表什么 |
|---|---|---|
| 真实运行记录 | 代码、输入、输出与版本可追溯 | 程序成功不等于模型正确 |
| 独立验证 | 复算约束、检查泛化或给出适用的数学证据 | 最好一次结果不代表稳定性能 |
| 原题覆盖检查 | 科学有效性与任务完成度分别判断 | 解释缺数据不等于已交付要求的答案 |
| 文件与论文验收 | 实际解压、解析内容、核对数字与版面 | 文件能打开不等于论文达到获奖水平 |

求解器达到时限但留下完整候选解时，可以独立验证后采用；没有最优性证明，就只称“当前最佳已验证可行解”。数据、文献或工具不足时说明具体缺口，不编造观测、引用、Run 或下载链接。

完整内部交付可组织为题目详解、参考论文、源码和其他材料四包；只要其中一项，就验收该项。已有队员终稿可以直接复审，不强制补造内部参考稿或四包。必要的 AI 披露、引用与许可信息必须保留。

这是一套协作与证据管理方法，**不是获奖保证，也不能替代队员判断**。

<a id="development"></a>

## 工具与维护

入口保持简洁，细则按需加载。赛题工作区与 Skill 仓库分开管理，一个工作区只对应一道赛题。

| 入口 | 用途 |
|---|---|
| [SKILL.md](SKILL.md) / [manifest.yaml](manifest.yaml) | Skill 入口与阶段路由 |
| [references/](references/) | 建模、运行、绘图、论文与交付规范 |
| [assets/](assets/) | 逐题求解、证据蓝图和审稿模板 |
| [run_record.py](scripts/run_record.py) | 重要运行记录、来源快照与新产物检查 |
| [figure_utils.py](scripts/figure_utils.py) | 中文字体检测、多格式保存与默认防覆盖 |
| [delivery_check.py](scripts/delivery_check.py) | ZIP 解压、关键文件与 DOCX/PDF 内容检查 |
| [tests/](tests/) | 路由、运行、交付、绘图回归与独立试用请求 |

<details>
<summary><strong>辅助工具：依赖与调用示例</strong></summary>

辅助工具要求 Python 3.11+。在 Skill 仓库中安装其依赖：

```bash
python -m pip install -r requirements-tools.txt
```

赛题模型另行维护自己的依赖。Windows 中文终端可启用 Python UTF-8 模式，例如 PowerShell 的 `$env:PYTHONUTF8="1"`。

以下示例假设 Skill 仓库与赛题工作区为同级目录，命令在**赛题工作区**执行。输入与脚本须已存在，求解脚本须支持 `--output-dir` 并创建输出目录：

```bash
python ../cumcm-modeling-analyst/scripts/run_record.py \
  --root . --problem Q1 --purpose "最终模型候选" --status FINAL \
  --input 01_data/processed/第一题.csv \
  --output "{run_dir}/结果.csv" \
  -- python 03_code/q1/第一题.py --output-dir "{run_dir}"
```

每次运行使用新产物路径；缺失输入、已有输出、空产物和失败命令不能固化为正式结果。`--status FINAL` 仅声明用途，科学有效性与完成度仍需验证。`--code` 可补充实际使用的共用模块，`--timeout` 可设置运行预算。

`figure_utils.py` 提供 `apply_readable_defaults` 与 `save_figure`。保存主干中的小数点会完整保留，默认不覆盖已有图；明确替换派生图时才使用 `overwrite=True`。

对已生成的参考论文包进行机械验收：

```bash
python ../cumcm-modeling-analyst/scripts/delivery_check.py \
  06_submission/internal_delivery/参考论文.zip
```

默认参考论文包要求 DOCX 与 PDF；其他命名可指定 `--profile reference-paper`。仅交付某一格式时，按实际范围选普通包检查并用 `--require` 指定文件。工具检查不代替数学复核、公式/图表视觉检查或源码实际复现。

</details>

<details>
<summary><strong>运行全部仓库检查</strong></summary>

在 Skill 仓库中执行：

```bash
python scripts/quick_validate.py
python tests/test_competition_first_contract.py
python tests/test_old_problem_forward_contract.py
python tests/test_helper_tools.py
python tests/test_reliability.py
python tests/test_figures.py
```

GitHub Actions 在 Ubuntu / Windows、Python 3.11 / 3.12 上运行检查。测试覆盖路由、实际运行、压缩包和 PNG/SVG/PDF 导出，不把静态通过率当作建模得分。

[独立试用请求](tests/scenarios.json)可用于新会话中的行为验证；微型题表现不等于完整限时比赛表现。

</details>

<details>
<summary><strong>v11.4 更新重点</strong></summary>

- 赛时优先可用答案、关键验证和队员接手，长篇教学按需补充。
- 初始审计条件加载，审计锁定后复用；小任务不强建完整赛事目录。
- 按修改影响范围重跑，不因改字或配色重算所有模型。
- 明确不可识别结果、任务完成度与限时候选解的处理边界。
- 修复小数点图名截断与覆盖，新增绘图行为测试。

完整历史见 [CHANGELOG.md](CHANGELOG.md)。

</details>

---

发现题意误读、错误选模、数据泄漏、结果串版或交付问题？欢迎提交 [Issue](https://github.com/zhu-hailin/cumcm-modeling-analyst/issues) 或 [Pull Request](https://github.com/zhu-hailin/cumcm-modeling-analyst/pulls)，并附最小复现材料。

**把时间留给能改善答案的研究，把证据留给需要理解它的人。**
