# README 展示资源

本目录仅用于产品介绍，不包含赛题答案、论文实测数据或获奖承诺，不作为建模输入或证据。

| 文件 | 用途 |
|---|---|
| [hero-cumcm-modeling-analyst.svg](hero-cumcm-modeling-analyst.svg) | v12介绍图：国赛实战经验、可选单代理/三角色、论证、Python赛中制图与交付 |
| [cumcm-readme-workflow.svg](cumcm-readme-workflow.svg) | v12流程图：选择、逐问确认、三角色反馈、图表说明、四项验收和交付 |
| [source/hero.svg](source/hero.svg) / [source/workflow.svg](source/workflow.svg) | 同次生成的可编辑文字母版 |
| [生成脚本](../../scripts/render_readme_assets.py) | 两图的唯一生成源，修改内容时从此重生成全部版本 |

## 生成与查看

使用Python、matplotlib和本机合法可用的中文字体。脚本优先查找Noto Sans CJK SC、Microsoft YaHei或Source Han Sans SC，也可用 `--font-file` 指定。仓库不分发字体二进制。

```bash
python scripts/render_readme_assets.py --preview-dir /path/to/readme-preview
```

正式SVG将文字转为矢量路径，浏览器无需安装中文字体；source母版保留文字。本次实际使用Microsoft YaHei，hero为1600×830，workflow为1600×1340的PNG预览及同宽高比SVG。介绍图是文档图形，不宣称完成nature-figure科研图验收。

预览检查文字与连线无遮挡、角色可选、后问独立确认、论文与图表随问推进；核对README的图片链接和alt文字。版本变化同时更新本清单、源码和两个导出，不手改路径化文字。

旧题结果图不作为默认展示，以免泄露盲测答案。历史 `assets/readme.png` 保留兼容但不再被当前README引用。
