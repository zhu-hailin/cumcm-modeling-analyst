# README 展示资源清单

本目录只服务 GitHub README 展示，不作为赛题输入、模型训练数据、论文证据目录或官方答案库。

## 当前资源

| 文件 | 用途 | 生成方式 | 是否含赛题结果 |
|---|---|---|---|
| [hero-cumcm-modeling-analyst.svg](hero-cumcm-modeling-analyst.svg) | v11.4 介绍图：逐题确认、真实求解、证据驱动写作 | 深蓝 / 青绿 SVG，文字转路径，1440 × 660 | 否 |
| [cumcm-readme-workflow.svg](cumcm-readme-workflow.svg) | v11.4 流程图：阅读拆题、研究选模、逐题确认与暂停、证据冻结与内部参考稿 | SVG 阶段卡片与有向连接，文字转路径，1280 × 1540 | 否 |
| [source/hero.svg](source/hero.svg) | 介绍图可编辑母版 | 保留真实文字与原生矢量对象 | 否 |
| [source/workflow.svg](source/workflow.svg) | 流程图可编辑母版 | 保留真实文字与原生矢量对象 | 否 |

## 视觉与维护

介绍图和流程图共用深蓝、青绿、浅灰白的配色与字体层级。缩减旧流程图中的密集小字、具体模型组合和星级推荐，不用示意内容暗示实测效果。介绍图的网络结构只是抽象图形，不是模型结果。

字体采用 [Noto Sans CJK SC](https://github.com/notofonts/noto-cjk/tree/main/Sans)，使用其 Regular 与 Bold 字重。仓库不分发字体文件；正式展示 SVG 已将文字转为矢量路径，不依赖访问者安装中文字体，同时保留 title / desc；README 提供对应文字说明和 alt 文本。修改文字应编辑 source 母版，而非手改导出路径。

本次使用 Inkscape 1.2.2 导出。安装上述字体后，在仓库根目录执行：

```bash
inkscape assets/readme-showcase/source/hero.svg --export-text-to-path --export-plain-svg --export-filename=assets/readme-showcase/hero-cumcm-modeling-analyst.svg
inkscape assets/readme-showcase/source/workflow.svg --export-text-to-path --export-plain-svg --export-filename=assets/readme-showcase/cumcm-readme-workflow.svg
```

导出后实际渲染核对：文字与箭头无遮挡、各阶段符合当前 Skill、下一问独立确认、参考稿不可直接提交。另检查 README 图片路径、导航与折叠区。没有更改行为规则时不单独提升 Skill 版本。

## 为什么不直接放入旧题结果图

实施材料中包含若干 2022 C 题旧题测试图。它们能够展示真实产物，但也会暴露题目分析结果，可能污染后续 `BLIND_BENCHMARK_MODE`。

因此当前 README 只保留不含赛题答案的项目宣传图与通用流程图。旧题结果只有在同时满足以下条件时才适合公开：

1. 明确标记题目、测试日期、Skill/模型版本和是否为盲测；
2. 先冻结独立结果，再开放参考资料；
3. 在图旁说明它不是官方答案、获奖证明或未知题性能保证；
4. 不把开放参考后的 `POST_HOC` 改进包装成独立发现；
5. 图能追到真实代码、数据与 Final/Validation Run；
6. 用户确认公开不会影响其后续测试计划。

若以后公开案例，建议单独放入 `docs/cases/<年份-题号>/`，README 只展示缩略图和可复核边界，不把案例结果混入 Skill 启动上下文。

## 使用边界

- 展示图不得被 Agent 当作当前赛题资料或建模证据；
- 不进入 `always_load`；
- 不进入当前项目的 `01_data/`、`04_results/` 或论文素材；
- 宣传图更新时同步更新本清单；
- 科研结果图仍必须由 Python、Graphviz、NetworkX、GeoPandas 等确定性工具从真实结果生成。
