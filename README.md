# huawei-cpipc-skill

面向 **“华为杯”中国研究生数学建模竞赛** 的 Codex / Agent Skill，重点解决论文架构、逐句写作、结果表达、改写和终稿审查。

当前版本按 **2026 年第二十三届中国研究生数学建模竞赛** 官方规则整理；未来年份使用前，应重新核对当年官方公告、论文模板、赛题要求与 AI 使用规定。

## 核心目标

它不是“自动生成一篇看起来像数模论文的长文”，而是强制论文形成可检查的证据链：

`题目要求 -> 问题分析 -> 模型 -> 求解 -> 数值证据 -> 验证 -> 最终回答`

并进一步规定：

`每一节回答一个问题；每一句承担一个主要职责；每一个结论都能找到证据。`

## Skill 结构

```text
huawei-cpipc-skill/
├── SKILL.md
├── README.md
├── references/
│   ├── official-2026.md
│   ├── writing-blueprint.md
│   ├── section-boundaries.md
│   ├── evidence-writing.md
│   ├── award-paper-patterns.md
│   └── review-checklist.md
└── examples/
    ├── section-templates.md
    └── full-paper-skeleton.md
```

### 每个文件负责什么

- `SKILL.md`：Agent 执行入口、工作流和模式选择。
- `references/official-2026.md`：2026 官方硬约束，和教学经验严格分离。
- `references/writing-blueprint.md`：摘要、Intro、问题重述、问题分析、模型、结果、结论等逐节逐句写法。
- `references/section-boundaries.md`：专门解决摘要 / Intro / 问题分析 / 模型建立 / 结果 / 结论之间的边界和重复。
- `references/evidence-writing.md`：公式、图、表、数值、误差、敏感性分析怎么写成证据链。
- `references/award-paper-patterns.md`：从公开获奖作品、获奖经验和写作教学中抽象出的可迁移结构；不是官方评分规则，也不复制获奖论文措辞。
- `references/review-checklist.md`：BLOCKER / MAJOR / MINOR 级终稿审查。
- `examples/section-templates.md`：单章节句子职责模板。
- `examples/full-paper-skeleton.md`：从摘要到附件的完整论文骨架。

## 句子职责体系

Skill 在写段落前会先在内部判断每句话的主职责：

- `B` Background：背景
- `T` Task：问题/任务
- `D` Decision：分析判断、拆题逻辑、方法选择理由
- `M` Method：模型、方法、算法、操作
- `E` Evidence：数据、表、图、指标、推导、实验事实
- `R` Result：结果/直接答案
- `I` Interpretation：结果意味着什么
- `V` Validation：检验、误差、稳健性
- `L` Limitation：局限、适用范围
- `C` Contribution：创新、贡献

正式论文不会保留这些标签。标签只用来控制逻辑。

一个低质量长句往往是：

```text
T + D + M + R + I + C
```

即一句话同时说任务、为什么这么做、用了什么、结果多少、说明什么、还自称创新。

Skill 会把它拆成多个职责明确的句子。

## 摘要 / Intro / 问题分析 / 结论怎么区分

| 部分 | 它真正回答的问题 | 主职责 |
|---|---|---|
| 摘要 | 做了什么？怎么做？算出什么？可靠吗？创新在哪里？ | `T M R E V C` |
| Intro / 问题背景 | 为什么值得研究？具体困难是什么？本文准备做什么？ | `B T D C` |
| 问题重述 | 题目到底给了什么、要求交付什么？ | `B T` |
| 问题分析 | 为什么这样拆题？为什么选择这条建模路线？ | `T D M V` |
| 模型建立 | 数学上到底建立了什么？ | `D M` |
| 模型求解 | 这个数学问题具体怎么算？ | `D M` |
| 结果 | 算出了什么？ | `R E` |
| 结果分析 | 数字说明什么？ | `E I R` |
| 检验/敏感性 | 为什么应该相信这个答案？ | `M E V I` |
| 结论 | 最终对每一问的直接答案是什么？ | `R E V I L` |

同一个关键数字可以同时出现在摘要、正文和结论，但粒度不同：

```text
摘要：模型 + 关键数字
正文：完整图表 + 对比 + 解释 + 验证
结论：直接答案 + 关键数字 + 可靠性
```

不能把摘要换几个词直接复制成结论。

## 一个结果段落应该怎么写

Skill 默认把重要图表写成：

```text
Claim
  ↓
Evidence
  ↓
Interpretation
  ↓
Answer / Decision
```

例如：

```text
[Claim] 方案 C 在保持服务约束的同时取得最低成本。
[Evidence] 其总成本为 XXX，较方案 A 下降 XX%，平均等待时间为 XXX，仍低于上限 XXX。
[Interpretation] 因此成本下降并非通过明显牺牲等待时间获得。
[Answer] 问题二最终采用方案 C。
```

正式稿删除 `[Claim]` 等标签。

Skill 会尽量避免：

```text
由图可知结果较好。
模型具有很强的鲁棒性。
算法取得了显著提升。
```

而要求用实际数值、基准和扰动范围替代形容词。

## 公式应该怎么写

关键公式建议形成：

```text
为什么需要这个量/模型
        ↓
变量定义
        ↓
核心公式
        ↓
每一项的现实意义
        ↓
约束与赛题条件的对应
        ↓
参数来源/估计方式
        ↓
求解算法
        ↓
数值结果
        ↓
结果解释与答题句
```

因此下面这种写法会被标为高风险：

```text
根据相关理论，可以得到如下模型：
...
利用 Python 求解得到结果。
```

Skill 会要求补：模型来源或推导、变量含义、现实对应、参数来源，以及真正的求解方法。Python/MATLAB 只是实现环境，不是建模方法。

## “一等奖论文风格”是什么意思

这里不做文风模仿，也不复制获奖论文。

`award-paper-patterns.md` 只迁移这些结构性特征：

- 评委能按赛题子问题快速导航；
- 摘要每一问形成“方法 + 结果”的微闭环；
- 问题分析明确解释为什么选择该路线；
- 公式能翻译回现实问题；
- 图表后直接说关键数字与含义；
- 验证方式匹配题型，而不是机械凑敏感性分析；
- 结论逐问给出最终答案。

不会因为某篇一等奖论文用了神经网络，就建议所有题都用神经网络。

## 使用模式

### 1. Architecture mode：先搭整篇论文

```text
使用 huawei-cpipc-paper skill 的 Architecture mode。
下面是赛题、当前模型、代码输出和已有结果。
先建立“每一问 -> 方法 -> 结果 -> 证据 -> 验证”的矩阵，再设计论文目录。
对每个小节列出应该出现的句子职责，不要先生成长篇正文。
```

适合比赛前半段和论文结构重构。

### 2. Draft mode：写某一节

```text
使用 huawei-cpipc-paper skill。
这是问题二、模型公式、求解输出和图表。
写“问题二模型建立、求解、结果与分析”。
每个关键公式后解释现实含义；每张关键图表形成 Claim -> Evidence -> Interpretation -> Answer。
缺少的数据用【待补】。
```

### 3. 摘要模式

```text
使用 huawei-cpipc-paper skill。
这是全部问题的真实模型、最终数字和验证结果。
先在内部给每句话分配 T/M/R/E/V/C 职责，再写 2026 华为杯摘要。
每一问至少出现“方法 + 关键结果”，禁止编造数字。
```

### 4. Boundary audit：区分摘要 / Intro / 结论

```text
使用 Boundary audit mode。
逐句检查下面的摘要、Introduction、问题分析和结论。
输出：当前章节 -> 句子职责 -> 最合适章节 -> 原因 -> 修改后表达。
特别检查同一段话是否只是换词重复。
```

### 5. Evidence mode：把代码输出/图表变成论文文字

```text
使用 Evidence mode。
下面是问题三的表格、运行日志和图。
不要重新讲算法常识；提炼每个结果的关键发现、真实数值、比较基准、解释和最终答题句。
```

### 6. Audit mode：最终审稿

```text
使用 huawei-cpipc-paper skill 的 Audit mode。
按 2026 华为杯官方要求审查全文。
先报 BLOCKER，再报 MAJOR、MINOR。
重点检查匿名、AI 使用、模型/公式来源、每问证据链、图表解释，以及摘要-正文-结论数字一致性。
```

## 官方依据（2026）

- 开赛公告：<https://www.cmathc.org.cn/cpmcm/news/642.html>
- 论文格式规范：<https://www.cmathc.org.cn/cpmcm/news/644.html>
- 人工智能工具及输出使用规定：<https://www.cmathc.org.cn/cpmcm/news/643.html>

2026 官方明确要求摘要包含**建模思路、主要方法、模型、结果与结论、创新点、关键词**；AI 可以作为辅助工具，但不得替代独立思考和核心创新，AI 相关数据分析、代码和模型/公式来源须按官方要求处理。

## 优秀论文与写作教学参考

这些来源用于抽象写作模式，不属于 2026 官方要求：

- 中国研究生数学建模竞赛优秀论文归档（2004–2023）：<https://www.cmathc.org.cn/cpmcm/lw/529.html>
- 2021 华为杯 E 题一等奖公开论文/代码仓库（仓库作者自述）：<https://github.com/hiyouga/HuaweiCup2021-MCM-ProblemE>
- 2024 华为杯一等奖公开摘要/经验仓库（仓库作者自述）：<https://github.com/jfbbcom/Experience-Sharing-of-the-21st-Huawei-Cup-China-Graduate-Students-Mathematical-Modeling-Competiti>
- 数学建模清风——论文写作方法教程：<https://www.bilibili.com/video/BV1Na411w7c2/>
- 安徽建筑大学公开教学《如何写好数学建模竞赛答卷》：<https://www.ahjzu.edu.cn/slx/2010/0714/c6703a52132/page.htm>

若这些经验与当年华为杯规则冲突，以当年官方材料为准。

## 最重要的安全阀

Skill 明确禁止：

- 编造实验结果、精度、百分比、最优值；
- 编造参考文献、DOI、作者或数据来源；
- 给来源不明的 AI 公式套假引用；
- 把没有做过的敏感性分析写成已经验证；
- 把启发式搜索得到的结果无依据地写成“已证明全局最优”；
- 把摘要和结论写成两份几乎相同的文字；
- 复制获奖论文原句来制造“一等奖风格”。

缺少证据时输出 `【待补：具体内容】`，而不是补一个“合理”的数字。
