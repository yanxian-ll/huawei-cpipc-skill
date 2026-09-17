# paper-lint

`paper_lint.py` 是面向华为杯数学建模论文草稿的**启发式静态审稿器**。它只使用 Python 标准库，不判断数学模型是否正确，也不声称某篇论文能否获奖；它负责把终稿中值得人工复核的位置尽量提前暴露出来。

## 快速使用

```bash
python tools/paper_lint.py paper.tex
python tools/paper_lint.py paper.md
python tools/paper_lint.py section.txt --fragment
```

机器可读输出：

```bash
python tools/paper_lint.py paper.tex --json
```

用于 CI：

```bash
# 默认：发现 BLOCKER 时返回非 0
python tools/paper_lint.py paper.tex

# MAJOR 也使 CI 失败
python tools/paper_lint.py paper.tex --fail-on major

# 只看报告，不影响退出码
python tools/paper_lint.py paper.tex --fail-on none
```

如果输入文本包含官方允许出现身份信息的封面，可临时关闭匿名检查：

```bash
python tools/paper_lint.py paper.txt --allow-identity
```

更推荐的做法仍然是：只对第二页开始的匿名正文做 lint。

## 当前检查项

### BLOCKER

- `TODO / FIXME / TBD / XXX / 待补 / ??` 等终稿占位符；
- 邮箱；
- 队伍编号/队号字段；
- 队员、作者、导师等身份字段；
- 正文中可能出现的大学、学院、研究院、实验室、研究中心名称。

匿名检查有意偏保守。论文在正文中合法引用外部高校或研究机构时，也可能触发人工复核；这类提示应人工确认，而不是机械删除。

### MAJOR

- “由图可知 / 如图所示”但附近没有量化证据；
- 2026 摘要未明显体现方法/模型；
- 2026 摘要未明显体现结果与结论；
- 2026 摘要未明显体现创新点/具体改进；
- 未检出关键词；
- 摘要和结论高度相似；
- 摘要或结论中的关键数值在正文其他位置无法追溯；
- 正文引用 `[n]` 但参考文献表缺少 `[n]`；
- LaTeX `\cite{key}` 缺少对应 `\bibitem{key}`；
- LaTeX 图表引用指向不存在的 `\label{fig:...}` / `\label{tab:...}`；
- 完整论文模式下缺少摘要、问题分析、结论或参考文献等核心章节。

### MINOR

- “显著 / 鲁棒 / 稳定 / 最优 / 普适 / 完全证明”等强评价词附近未检出量化或检验证据；
- “随着……发展”“具有重要意义”等泛化背景套话；
- “首先 / 其次 / 然后 / 最后”大量重复，疑似流程目录式写作；
- 某个问题对应内容中未识别到明确的结果/最终回答语句；
- 普通文本中的图/表题注疑似从未在正文引用；
- LaTeX 图/表 `\label` 从未被正文引用；
- 参考文献条目从未在正文引用；
- 长句在全文机械重复；
- 摘要和结论中等程度相似。

## 设计原则

1. **宁可提示“需要复核”，不自动判定论文错误。** 自然语言和 LaTeX 写法很多，正则检查一定存在误报与漏报。
2. **不检查数学正确性。** 目标函数、约束、证明、统计检验、代码输出仍需团队人工验证。
3. **不编造缺失证据。** lint 发现某数字无法追溯时，应回到代码/表格/实验结果核对，而不是给它补一个“合理数字”。
4. **官方规则优先。** 当前摘要检查按 2026 华为杯要求设计；未来年份应先核对当届通知再调整规则。
5. **输出给人和 Agent 都能读。** 默认文本报告适合人工终稿检查，`--json` 适合 Codex/Agent 后续自动修订工作流。

## 推荐工作流

```text
模型与代码完成
    ↓
固定关键结果和图表
    ↓
写结果与分析 / 结论
    ↓
写模型建立与求解
    ↓
最后写摘要
    ↓
paper-lint --fail-on none
    ↓
人工处理 BLOCKER → MAJOR → MINOR
    ↓
重新跑 lint
    ↓
人工检查 PDF 格式、匿名、公式、图表、引用
    ↓
锁定最终 PDF / MD5
```

`paper-lint` 不能替代 `references/review-checklist.md`，两者应配合使用：脚本负责自动扫明显模式，清单负责语义、数学和官方规则层面的人工终审。
