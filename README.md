# huawei-cpipc-skill

面向 **“华为杯”中国研究生数学建模竞赛** 的 Codex / Agent Skill，重点解决论文写作、改写与终稿审查。

当前版本按 **2026 年第二十三届中国研究生数学建模竞赛** 官方规则整理；涉及未来年份时，应先核对当年官方公告、论文模板、赛题要求与 AI 使用规定。

## 这个 skill 主要解决什么

它不是“自动生成一篇看起来像数模论文的长文”，而是强制论文形成可检查的证据链：

`题目要求 -> 问题分析 -> 模型 -> 求解 -> 结果 -> 验证 -> 最终回答`

特别强化：

- 摘要每一句应该承担什么功能；
- Introduction / 问题背景与摘要的区别；
- 问题重述与问题分析的区别；
- 模型建立与模型求解的区别；
- 结果、分析、敏感性分析如何分开；
- 结论如何逐问给最终答案，而不是复制摘要；
- 如何减少“首先、其次、最后”“结果较好”等空泛表达；
- 如何检查数字、公式、文献和模型是否可追溯；
- 如何按 2026 华为杯 AI 使用规定处理 AI 辅助写作、数据分析和代码。

## Skill 结构

```text
huawei-cpipc-skill/
├── SKILL.md
├── README.md
├── references/
│   ├── official-2026.md
│   ├── writing-blueprint.md
│   └── review-checklist.md
└── examples/
    └── section-templates.md
```

`SKILL.md` 是入口。详细内容通过 references/examples 按需加载，避免把所有写作规范一次性塞进上下文。

## 句子职责体系

Skill 在写段落前会先在内部判断每句话的主职责：

- `B` Background：背景
- `T` Task：问题/任务
- `D` Decision：分析判断、方法选择理由
- `M` Method：模型、方法、算法
- `E` Evidence：数据、表、图、指标、推导
- `R` Result：结果/答案
- `I` Interpretation：解释
- `V` Validation：检验/稳健性
- `L` Limitation：局限/适用范围
- `C` Contribution：创新/贡献

正式论文不会保留这些标签。它们用于防止一句话同时写背景、方法、结果和自我评价，也用于区分不同章节。

## 摘要 / Intro / 问题分析 / 结论怎么区分

| 部分 | 核心问题 | 主要句子职责 |
|---|---|---|
| 摘要 | 做了什么、怎么做、算出什么、创新在哪里？ | `T M R E V C` |
| Intro / 问题背景 | 为什么值得研究？本文工作处在什么位置？ | `B T D C` |
| 问题重述 | 题目具体要求交付什么？ | `B T` |
| 问题分析 | 为什么这样拆题、为什么选这条建模路线？ | `T D M V` |
| 模型建立 | 数学上到底建立了什么？ | `D M` |
| 模型求解 | 这个模型具体怎么算？ | `D M` |
| 结果与分析 | 算出了什么？证据是什么？意味着什么？ | `R E I` |
| 检验/敏感性 | 结果可靠吗？参数变动会怎样？ | `M E V I` |
| 结论 | 最终对每个问题的回答是什么？ | `R E V I L` |

详细的逐句模板见 [`references/writing-blueprint.md`](references/writing-blueprint.md) 和 [`examples/section-templates.md`](examples/section-templates.md)。

## 使用方式

将本仓库目录作为一个 Skill 安装/放入 Codex 可读取的 skills 目录即可；仓库根目录已经包含标准 `SKILL.md`，其 YAML frontmatter 提供 `name` 和 `description`，符合当前 Codex skill 的基本结构。

OpenAI 的 Skill 结构说明：

- <https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md>
- <https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md>

## 推荐提示词

### 只写摘要

```text
使用 huawei-cpipc-paper skill。
这是赛题、我们的模型和最终结果。先给出摘要的句子职责规划，再写 2026 华为杯风格摘要。
不要编造任何数字；缺失内容用【待补】标记。
```

### 写某个问题的模型章节

```text
使用 huawei-cpipc-paper skill。
根据下面的问题二、变量定义、模型公式、求解代码输出和图表，写“问题二的模型建立、求解与结果分析”。
要求把模型建立、算法和结果分开写，每个关键公式后解释现实含义。
```

### 区分摘要、Intro、结论

```text
使用 huawei-cpipc-paper skill。
检查下面三个章节是否互相重复。逐句判断它属于摘要、Intro、问题分析还是结论；不属于当前章节的句子请移动并重写。
```

### 终稿审稿

```text
使用 huawei-cpipc-paper skill 的 Audit mode。
按 2026 华为杯官方要求审查这篇论文。
先报 BLOCKER，再报 MAJOR、MINOR；重点检查匿名、摘要、AI 使用、模型/公式来源、结果证据链、摘要-正文-结论数字一致性。
```

## 官方依据（2026）

- 开赛公告：<https://www.cmathc.org.cn/cpmcm/news/642.html>
- 论文格式规范：<https://www.cmathc.org.cn/cpmcm/news/644.html>
- 人工智能工具及输出使用规定：<https://www.cmathc.org.cn/cpmcm/news/643.html>

2026 官方明确要求摘要包含**建模思路、主要方法、模型、结果与结论、创新点、关键词**；AI 可作为辅助工具，但不得替代独立思考和核心创新，最终论文文字需由参赛队理解、核验并以自身语言定稿。

## 写作教学参考

写作策略综合了公开数学建模论文教学的常见经验，但这些内容不是官方规则：

- 数学建模清风——论文写作方法教程：<https://www.bilibili.com/video/BV1Na411w7c2/>
- 数学建模论文写作方法：<https://zhuanlan.zhihu.com/p/708627214>

若教学内容与当年华为杯规则冲突，以华为杯官方材料为准。

## 最重要的安全阀

Skill 明确禁止：

- 编造实验结果、精度、百分比；
- 编造参考文献、DOI、作者或数据来源；
- 给来源不明的 AI 公式套一个假引用；
- 把没有做过的敏感性分析写成已经验证；
- 把摘要和结论写成两份几乎相同的文字。

缺少证据时，应输出 `【待补：具体内容】`，而不是补一个“合理”的数字。
