# Word / PDF / Markdown 公式渲染与验收规范

## 目标

数学建模公式必须既**写得正确**，也**解释得清楚**。

本规范同时约束 Markdown 教程/研究记录、最终 DOCX 和 PDF。

- Markdown：使用规范 LaTeX 数学环境；
- DOCX/PDF：必须呈现真正数学排版，禁止把 LaTeX 源码当普通文本。

失败状态：

- Markdown 公式格式/说明失败：`FORMULA_DOCUMENTATION_FAILED`
- Word/PDF 数学渲染失败：`FORMULA_RENDERING_FAILED`

修复前不得标记 `INTERNAL_DELIVERY_COMPLETE`。

---

# 1. 覆盖范围

适用于：行内变量、独立公式、目标函数、约束、分式、根式、求和、积分、极值、概率、期望、矩阵、向量、分段函数、希腊字母、上下标、公式编号、符号说明表、图表/表头中的数学变量和附录公式。

符号说明表不是例外。

---

# 2. Markdown 公式格式

## 行内公式

统一：

```markdown
$x_{icst}$
```

例如：

```markdown
其中，$x_{icst}$ 表示地块 $i$ 在年份 $t$、季次 $s$ 下种植作物 $c$ 的面积。
```

禁止把 `x_{icst}` 作为普通正文数学表达。

## 独立公式

完整公式统一：

```markdown
$$
Q_{cst}=\sum_p u_{pcs}x_{pcst}
$$
```

不要使用裸 LaTeX 行或代码块冒充公式。

## 复杂结构

使用标准 LaTeX，例如：

- `\frac{a}{b}`
- `\sqrt{x}`
- `\sum_{i=1}^{n}`
- `\int_a^b`
- `\max` / `\min`
- `\begin{bmatrix}...\end{bmatrix}`
- `\begin{cases}...\end{cases}`
- `\alpha` / `\beta` / `\omega` / `\Pi`

不得混用 Unicode 下标、普通下划线、LaTeX 和手工字符拼接模拟复杂公式。

---

# 3. Markdown 教程必须解释关键公式

每个真正用于求解的关键公式至少说明：

1. 公式在做什么；
2. 核心变量/参数；
3. 上下标含义；
4. 单位；
5. 为什么这样建模；
6. 与前后公式关系；
7. 对应源码位置。

例如：

```markdown
$$
Q_{cst}=\sum_p u_{pcs}x_{pcst}
$$

其中：
- $Q_{cst}$：总产量，单位斤；
- $u_{pcs}$：亩产量，单位斤/亩；
- $x_{pcst}$：种植面积，单位亩。

该式将“亩产量 × 种植面积”汇总为总产量，后续销售约束与利润目标都依赖 $Q_{cst}$。

代码对应：`question1/model.py::build_production_expression()`。
```

如果某问主要依赖规则/算法，没有复杂公式，应诚实说明，不为了“高级”硬造公式。

---

# 4. 符号、公式、代码一致

教程符号表、正文、Python 和最终论文必须互相对应。

避免：

- 同一符号不同含义；
- 大小写漂移；
- 同一参数单位前后不同；
- 公式变量与代码变量实际含义不一致。

数学名与工程变量名不同，应显式映射：

```markdown
数学符号 $x_{icst}$ 对应 `plant_area[i, c, s, t]`。
```

Markdown 符号表数学列必须处于 `$...$` 环境。

---

# 5. DOCX：必须是真正数学对象

最终 Word 优先使用 **OMML（Office Math Markup Language）**。

推荐可靠链路：

```text
Markdown / LaTeX 数学源
→ Pandoc 或可靠数学转换
→ DOCX / OMML
```

使用 `python-docx` 时禁止：

```python
paragraph.add_run(latex_string)
```

直接把 LaTeX 当普通文本写入。

应转换为 MathML/OMML 并插入 `m:oMath` / `m:oMathPara`，或构造合法 OMML。

不能用普通 `_`、花括号、字符拼接假装数学排版。

---

# 6. 公式图片仅作 fallback

无法稳定生成 OMML 时，可使用经过验证的高质量矢量公式作为兼容性 fallback，优先 SVG/EMF 等，最后才考虑高分辨率位图。

必须保证：清晰、不裁上下标、留白合理、字号协调、PDF 后仍清晰。

环境能稳定生成 OMML 时，不应为了省事把全部公式截图化。

---

# 7. 独立公式与编号

独立公式默认居中，间距合理，编号统一 `(1)、(2)...`，正文引用一致。

长公式可合理换行，但不能破坏数学结构；`max`、`min`、`s.t.`、求和上下限、矩阵和分段函数必须按数学规范呈现。

---

# 8. PDF

PDF 不得只是把公式错误的 Word 原样导出。

推荐：

```text
已通过公式验收的 DOCX
→ 可靠 PDF 导出
→ PDF 二次视觉检查
```

如果 Word→PDF 工具破坏公式、字体或上下标，应换导出方式，或从同一数学母稿独立生成 PDF。

Word/PDF 数学含义、公式编号、结果必须一致。

---

# 9. 自动残留扫描

最终 DOCX/PDF 检查高风险 LaTeX 残留：

```text
_{
^{
\frac
\sum
\prod
\int
\sqrt
\alpha
\beta
\omega
\Pi
\begin{
\left
\right
$...
\(...\)
\[...\]
```

同时结合上下文检查 `x_{...}` 等可疑普通文本，避免把路径下划线误报。

---

# 10. DOCX 结构验收

采用 OMML 时至少检查：

- `m:oMath / m:oMathPara` 实际存在；
- 数学对象数量与论文公式规模大致匹配；
- 符号说明表没有全部退化为普通字符串；
- 公式编号/引用正确。

只检测“文件能打开”不算公式验收。

---

# 11. 视觉验收

至少检查重要公式页：

- 上下标；
- 求和上下限；
- 分式/根式；
- 希腊字母；
- 裁切；
- 表格数学变量；
- 字号；
- Word/PDF 一致；
- 数学含义与模型一致。

数学意义正确但视觉坏掉也不能交付。

---

# 12. 内部交付质量门槛

必须满足：

- [ ] Markdown 行内公式使用 `$...$`
- [ ] Markdown 独立公式使用 `$$...$$`
- [ ] 无裸 LaTeX 数学表达
- [ ] 关键公式有用途、变量、单位、代码对应说明
- [ ] LaTeX 数学源语法正确
- [ ] DOCX 无普通文本式 LaTeX 残留
- [ ] 重要公式为 OMML 或验证过的高质量数学渲染
- [ ] 符号说明表正确
- [ ] 公式编号正确
- [ ] 自动残留扫描通过
- [ ] DOCX 结构检查通过
- [ ] Word/PDF 视觉检查通过
- [ ] Word/PDF 数学含义一致
- [ ] 公式与源码、模型定义、最终结果一致

任何关键项失败必须修复，不得把有明显公式问题的教程、Word 或 PDF 视为内部成果完成。
