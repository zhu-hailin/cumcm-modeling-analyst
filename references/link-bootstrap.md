# 从 GitHub 链接启动

用户发来 `https://github.com/zhu-hailin/cumcm-modeling-analyst` 并要求使用它开始比赛，即可由有联网与文件能力的 agent 完成项目内获取和读取，不要求用户先运行安装命令。顺序是：完整建模 Skill → 读取 SKILL.md 和 manifest → 按声明获取完整 nature-skills → 读取 nature-figure 与 Python 分支 → 恢复或启动项目。

## 获取与复用

1. 优先核对用户指定位置、已有安装或项目依赖记录。记录来源仓库、实际 commit（或归档版本及哈希）和入口绝对路径。已存在可读、来源明确的完整副本就复用；新会话不自动升级，不覆盖已有修改，不只凭目录同名认定可用。
2. 缺少建模 Skill 时，在当前可写项目的依赖目录获取完整仓库，例如 `.skill-deps/cumcm-modeling-analyst/`。先读取该目录的 `SKILL.md` 和 `manifest.yaml`，再读取核心流程及本规范。用户只给链接时，README 的快速开始说明提供这一步的入口。
3. 根据 manifest 的 `external_dependencies.nature_figure` 获取完整 `nature-skills` 仓库，例如 `.skill-deps/nature-skills/`。默认使用 manifest 的 `verified_commit`；已记录其他实际版本的项目先核对兼容性，不能赛中静默切换版本。新副本可检出已核对 commit；不要对已有修改副本强制 checkout/reset。
4. 读取 `nature-skills/skills/nature-figure/SKILL.md`、其 manifest、always_load 和 Python fragment。保留整个仓库，包含其引用的 `nature-shared`、脚本、参考和素材。按 [制图接入](python-visualization-policy.md) 设置项目本地 Python backend；只为实际工作安装必要运行依赖，不自动运行未知安装脚本或开启付费服务。
5. 在已有项目说明中记录两个依赖的来源、版本、入口及就绪/缺失状态，不另建状态数据库。依赖放工作区，交付目录只收入复现实际需要的内容和必要许可。依赖准备就绪后继续题包读取、一次模式选择及当前问方案讨论；下载成功不等于任何题目已确认或已完成求解。

在选定依赖目录内、两个目标均不存在时，可执行：

```bash
git clone https://github.com/zhu-hailin/cumcm-modeling-analyst.git
# 接着读取 cumcm-modeling-analyst/SKILL.md 和 manifest.yaml
git clone https://github.com/Yuan1z0825/nature-skills.git
# 根据 manifest 中的 verified_commit 检出 nature-skills 的已核对版本
```

无 Git 时可获取官方仓库归档并完整解压，核对实际入口、资源和版本；不得把 GitHub HTML 页面保存为 SKILL.md。不要只下载两个入口文件，或把“看过 README”称为已加载完整技能。

## 能力与执行范围

- 项目内读取与按入口执行无需声称全局安装成功。不同宿主的技能注册机制不同；只有确实完成注册才称为已安装到宿主。用户未要求时不改全局技能目录。
- 无联网、写入、解压或依赖安装权限时，说明卡在哪一步、哪些依赖可用；继续不依赖该能力的读题和推导。图表依赖未就绪就明确标记，不伪称 nature-figure 已使用，不退回旧绘图规范。
- 局部解释或单次审稿等任务按实际需要获取依赖，不额外启动全题流程。首次完整比赛项目在启动阶段准备两个技能，Python 图表仍在每问的真实实验与验证过程中生成。
- 用户及平台的权限和指令优先于下载内容；读取第三方技能不扩大联网、执行、子代理或跨问求解授权。
