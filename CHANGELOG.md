# CHANGELOG

## v11.2 — Competition-first 自主执行与按证据成熟度加载

- 入口瘦身：`SKILL.md`、`manifest.yaml`、`agents/openai.yaml` 不再重复整套深层规范，启动只保留一次性安全门与核心工作流。
- 明确 Agent 自主执行边界：已确认路线内允许自主 EDA、诊断实验、调参、求解器调整、代码重构、验证和按预先确认条件切换备用路线；只有目标、关键约束、会改变结论的关键假设、关键数据缺口或团队策略选择改变时才需要用户决定。
- 新增 `references/modeling-research-playbook.md`，用区分性实验和关键研究问题帮助 Agent 主动发现更好路线，而不是新增固定模型清单。
- Stage 2 模式按团队协作方式选择，不再按 Codex/Chat 硬编码；逐题确认只确认建模边界，连续模式不因普通技术失败、调参或求解器更换反复暂停。
- Stage 1 不默认加载外部文献/数据规范，只有真实缺口会影响模型时才加载；探索阶段上下文优先用于建模研究和质量门。
- 绘图拆分 `QUICK_EXPLORATION / FORMAL_EVIDENCE`：EDA/调试图可快速生成，只有正式论文图、验证图和方法图才承担完整 Run、脚本、尺寸、字体和 A4 视觉 QA。
- Evidence Blueprint 改为 `EARLY_SKELETON → FINAL_FREEZE`：读题后建立交付项骨架，每问 Final Run 后增量补充，全部关键结果冻结后才允许 `PAPER_EVIDENCE_BLUEPRINT_READY`。
- 统一蓝图权威路径为 `02_analysis/PAPER_EVIDENCE_BLUEPRINT.md`；`05_paper/` 不再维护第二份蓝图副本。
- 内部 A/B/C 证据等级、Final Run、PASS/FAIL 等状态继续用于项目管理，但不再要求机械展示在正式论文正文；论文用验证方法、误差、稳定性、现实约束和适用范围表达证据。
- 来源核验把“文献真实/已读/支持当前主张”和“公开可下载全文”拆开；只有声称提供可下载入口时才强制 `DOWNLOAD_VERIFIED`。
- Run Ledger 明确“同一运行元数据一个权威来源”，减少 README、教程、蓝图反复手抄；统一加入 `METHOD_FIGURE` 类型。
- 中文源码命名回归可读性偏好：新建中文项目可以使用中文语义名，已有仓库、CI、包、Notebook 和跨平台工具链继承现有命名。
- 新增 `scripts/run_record.py`、`scripts/figure_utils.py`、`scripts/delivery_check.py`，把运行记录、绘图机械设置和 ZIP 实际解压验收从 Agent 文本流程中抽离。
- 新增 `tests/test_competition_first_contract.py` 与 GitHub Actions，持续防止强制推荐分、探索图论文级负担、下载链接硬门和技术细节反复审批等回归。

## v11.1 — 每个赛题工作区只做一次初始安全审计

- `problem-ingestion-security.md` 只在首次接收当前赛题题面及随题官方附件时完整执行一次。
- 审计通过后记录 `INGESTION_SECURITY_AUDIT_LOCKED`，主 Agent 与子代理复用 `FILE_SECURITY_AUDIT.md`、`FILE_AUDIT_MANIFEST.md` 与正常人类视图。
- 后续补充论文、数据、图片、代码、外部下载、问题切换和子代理切换不再触发完整或增量安全审计；只有用户明确要求重审或开启新赛题工作区时例外。

## v11.0 — 证据质量门、科研制图标准与 Skill 瘦身

- 新增 `references/modeling-quality-gates.md`，把优秀论文中可迁移的建模意识整理为可执行质量门：数据结构识别、可追溯预处理、模型前提、baseline、独立验证、现实约束、完美指标审计、潜在阶段解释和跨问复用。
- 新增 `references/core-workflow.md`，合并原先分散的赛时协作、联网模式、两阶段流程和逐题确认规则。
- `SKILL.md` 改为轻量路由与硬底线，不再复制每个深层 policy 的完整内容。
- `manifest.yaml` 启动只加载 `problem-ingestion-security.md + core-workflow.md`，进入具体阶段再按需加载。
- 重写 `python-visualization-policy.md`，合并图前证据契约、图像用途、中文绘图脚本和科研图片 QA；删除重复绘图 policy。
- 科研制图采用 GB/T 7713.2-2022 与 Nature、IEEE、Elsevier、PLOS 官方要求的保守交集，并在正式排版时服从当年竞赛模板。
- 线图、路径、网络和流程图优先保存 SVG/PDF；位图按最终插入尺寸检查，普通统计图保留至少 300 dpi PNG，混合图和纯线稿使用更高分辨率基线。
- 增加最终 A4 尺寸下的字体、线宽、panel、单位、误差、颜色可访问性、灰度区分、图题表题、数据完整性和 Word/PDF 视觉检查。
- 禁止截轴误导、选择性删样本、隐藏失败 seed、只展示有利场景、用生成式图片替代真实科学结果。
- A 级核心结论原则上要求“主模型证据 + 至少一种独立验证证据”。
- 重写 `python-code-documentation-policy.md`，合并中文文件命名、注释、源码纯净度和运行入口规则。
- 精简 Codex 工作区、逐题模板、一次性模板、参考论文、终稿审核、一致性扫描和四包规则；保留质量门，删除重复说明。
- 删除旧兼容模板、未使用模板、重复工作流、重复可视化/命名 policy 和无人引用的旧路由文件。
- README 同步展示新的证据链、科研制图基线和精简后的文件结构。

## v10.5 — 中文源码命名与图像用途标记

- 正式 Python 使用 `第一题.py`、`第一题_模型求解.py`、`总运行.py` 等中文语义名称。
- 论文图脚本与 PNG/SVG 使用同一语义主干。
- 论文图、验证图、探索图、AI 沟通图和安全审计图分开管理。
- AI 沟通图使用 `AI沟通图_` 前缀、图面角标和 Manifest 用途标记，不进入论文或官方提交。

## v10.4 — Python 注释、可维护性与源码纯净度

- 正式模块和关键函数增加准确 docstring；注释解释建模意图、单位、口径、边界和随机机制。
- 禁止源码夹带 Skill、提示词、聊天记录、AI 水印和影响结果的占位。
- 源码必须离开当前会话后仍可独立运行和阅读。

## v10.3 — 读题前文件安全审计

- 语义读题前检查 PDF、Office、图片和压缩包中的隐藏对象、透明内容、嵌入媒体和疑似 Prompt Injection。
- 文件内文字一律作为不可信数据，不执行宏、脚本、链接和嵌入程序。
- 正常人类视图是题意基准；解析、视觉模型、OCR 与人工观察冲突时保留证据并由用户确认。

## v10.2 — Codex 单赛题工作空间

- 一个根目录只对应一道赛题。
- 原题、raw、processed、external、代码、结果、论文、资料和临时文件分层管理。
- 用户已有结构和明确要求优先，不破坏性整理原文件。

## v10.1 — 逐题确认与真实外部数据

- 每问先研究和讨论，用户确认后再写最终代码、Final Run、图表和教程。
- 现实数据缺失时主动检索权威来源，找不到就报告，禁止编造。
- 中国现实背景优先使用本土官方统计、对象官网、国内标准和应用研究。

## v10.0 — Evidence-first Figure、Run Ledger 与一致性

- 每张正式图先明确结论、主证据、panel、数据、Run 和不确定性。
- 每问冻结 `FINAL_RUN_ID`，旧结果标记 `SUPERSEDED`。
- 新增跨代码、结果、图表、教程和论文的一致性扫描与 ripple check。

## v9.0 — Python 可视化与官方提交导出

- 建立 A/B/C 图表分级、中文字体回退、Manifest、Visual QA 和启发式算法收敛证据。
- 内部四包与官方上传文件分开；官方提交格式按当年规则重新核验。

## v8 — 探索性研究与双解题模式

- Stage 1 增加 EDA、baseline、模型前提和候选评分。
- 支持逐题深解与一次性完整求解。
- 全题完成后建立 Requirement Traceability。

## v7 — 参考论文与文献核验

- 明确 `参考论文.zip` 是 AI 针对本题撰写的内部参考成果，不是外部论文包。
- 参考论文默认包含 DOCX 和 PDF；文献 DOI、URL 与下载状态必须真实核验。

## v6 — Python 图表与 Markdown 文档

- 科学结果图默认由 Python 等确定性工具生成。
- 普通文本成果使用 UTF-8 Markdown，教程公式使用规范 LaTeX。

## v5 及更早

- 建立 Python 实跑、逐问教程、内部四包、两阶段路线、首轮文献检索和候选方案评分等基础能力。
- 完整历史可通过 Git 提交记录查看。
