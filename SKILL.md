---
name: huawei-cpipc-paper
description: Write, revise, and audit Chinese mathematical-modeling papers for the Huawei Cup China Graduate Mathematical Modeling Contest (中国研究生数学建模竞赛/“华为杯”). Use when Codex is asked to draft or polish abstracts, introductions, problem restatements, problem analysis, assumptions, notation, data preprocessing, model formulation, algorithms, results, validation, sensitivity analysis, model evaluation, conclusions, references, or a full competition paper; to distinguish what belongs in each section; to turn modeling notes/results into judge-oriented prose; or to check a Huawei Cup paper against the 2026 official format and AI-use rules. Do not invent data, numerical results, citations, model provenance, or experimental evidence.
---

# Huawei Cup Paper Writing

Write for a mathematical-modeling judge: make the chain **question -> reasoning -> model -> computation -> evidence -> answer** easy to verify.

## Source priority

Use sources in this order when rules conflict:

1. The current year's official Huawei Cup notice, paper-format specification, official template, problem statement, and AI-tool rules.
2. The current problem's explicit submission requirements.
3. This skill's writing guidance.
4. Online teaching material and stylistic conventions.

For 2026 hard constraints, read `references/official-2026.md` before drafting or auditing a submission. For section-by-section and sentence-by-sentence writing, read `references/writing-blueprint.md`. For final review, read `references/review-checklist.md`.

Never present a teaching convention as an official rule.

## Required workflow

### 1. Establish the evidence base

Before drafting, identify:

- the exact subquestions to answer;
- the team's actual model/method for each subquestion;
- all computed results that may be stated numerically;
- the evidence supporting each conclusion: table, figure, metric, proof, simulation, error analysis, or sensitivity analysis;
- the provenance of data, formulas, models, algorithms, code, and external claims;
- which content involved AI assistance.

If a required number, source, derivation, or result is missing, do **not** fill it with a plausible value. Insert an explicit placeholder such as `【待补：问题2最优目标值】` or ask for the missing evidence when interaction is possible.

### 2. Build a section map before prose

Map every substantive item to one primary home. Avoid explaining the same thing fully in multiple sections.

- **摘要**: compressed problem + method + model + concrete result/conclusion + innovation.
- **引言/问题背景** (only when the chosen structure needs it): why the problem matters, relevant context, and what the paper will do; not a second abstract.
- **问题重述**: what the problem asks; no solution details and no results.
- **问题分析**: why the problem decomposes as it does and why a modeling route is appropriate; no final numerical answer.
- **模型假设**: simplifying assumptions plus justification/scope.
- **符号说明**: symbols, meanings, units/domains.
- **数据与预处理**: data provenance, cleaning, transformations, derived variables, quality checks.
- **模型建立**: mathematical objects, objective/constraints/relations, derivation, parameter meaning.
- **模型求解/算法**: how the established model is computed.
- **结果与分析**: what the computation produced, quantitative evidence, and what it means for the subquestion.
- **检验/误差/敏感性**: whether conclusions survive validation, error, or perturbation.
- **模型评价/改进**: strengths, limitations, applicable scope, possible improvements.
- **结论**: direct answers to the posed questions and the most important validated findings; no new method or new experiment.
- **参考文献/附件**: traceability and reproducibility.

### 3. Give every sentence one primary job

Before writing a paragraph, silently assign each sentence one of these roles:

- `B` Background/context
- `T` Task/question
- `D` Decision/rationale (why this decomposition or method)
- `M` Method/model/operation
- `E` Evidence (data, metric, figure/table, derivation)
- `R` Result/answer
- `I` Interpretation/implication
- `V` Validation/robustness
- `L` Limitation/scope
- `C` Contribution/innovation

A sentence may have a secondary role, but it should have one dominant job. If a sentence tries to provide background, method, result, and evaluation at once, split it.

Use the allowed/forbidden sentence-role patterns in `references/writing-blueprint.md`.

### 4. Draft from evidence outward

Prefer the order:

1. Write the key result table/figure and verified numbers.
2. Draft `结果与分析` and `结论`.
3. Draft `模型建立与求解` so every reported result has a reproducible origin.
4. Draft `问题分析` and assumptions.
5. Draft the `摘要` last, using only content already supported in the paper.
6. Draft or tighten the `引言/问题重述` after the technical story is stable.

This prevents the abstract and conclusion from promising results the body does not support.

### 5. Enforce separation between commonly confused sections

Use these tests:

- If a sentence answers **“为什么值得研究/本文要做什么”**, it belongs to introduction/background.
- If it answers **“题目具体要求交付什么”**, it belongs to problem restatement.
- If it answers **“为什么这样拆题/为什么选择这条路线”**, it belongs to problem analysis.
- If it answers **“数学上到底建立了什么”**, it belongs to model formulation.
- If it answers **“怎么算出来”**, it belongs to solution/algorithm.
- If it answers **“算出了什么、证据是什么”**, it belongs to results.
- If it answers **“结果是否可靠”**, it belongs to validation/sensitivity/error analysis.
- If it answers **“最终对每个问题的回答是什么”**, it belongs to conclusion.
- If it must allow a judge to understand the whole paper without reading the body, it may belong to the abstract, but only in compressed form.

Do not use the conclusion as an abstract copied to the end. Do not use the introduction as a long background essay.

### 6. Write judge-oriented mathematical prose

- Lead paragraphs with the claim or purpose, not with filler.
- Prefer quantified evidence over adjectives such as “很好”“显著”“较优” when a metric is available.
- After an important equation, explain the variables and why the equation corresponds to the problem mechanism.
- After an algorithm description, state stopping criteria, key parameters, and reproducibility details when material.
- After a result table/figure, state the main finding in text; do not force the judge to infer it.
- Distinguish observation from interpretation: first state the measured/computed fact, then explain what it implies.
- Keep terminology and symbols identical across abstract, body, figures, and conclusion.
- Avoid unsupported superlatives such as “最优”“完全证明”“普适” unless mathematically justified.

### 7. Handle citations and AI assistance conservatively

Follow the current official rules. For 2026 specifically, the official rules permit AI as an auxiliary tool but require the team to understand and reasonably use AI output; final submitted wording must be expressed in the team's own language. Models, formulas, and quoted material need reliable traceable sources or derivations. AI-assisted code and data analysis have explicit disclosure requirements; see `references/official-2026.md`.

When Codex assists with a competition paper:

- treat generated prose as a **candidate draft**, not unreviewed submission-ready authorship;
- never fabricate a reference to make a statement look sourced;
- prefer a real paper/book/official webpage over citing an AI system for mathematical content;
- preserve a lightweight AI-use log (tool/model, task, what was accepted, what was manually changed/verified) if useful for later compliance;
- tell the team which passages require human technical verification or rewriting when the distinction matters.

## Output modes

### Draft mode

When given notes/results, first make a concise section outline with the intended sentence roles, then write the requested section. Do not expose internal role tags in the polished final text unless the user asks for an annotated version.

### Rewrite mode

Preserve mathematical meaning and numerical results. Improve structure, remove repetition, tighten claims, and move sentences to the section where they belong. Flag any sentence whose factual support is missing.

### Audit mode

Return issues grouped by severity:

- `BLOCKER`: official-rule violation, identity leakage, unsupported/fabricated content, broken provenance, MD5/submission risk.
- `MAJOR`: missing answer to a subquestion, method/result inconsistency, unexplained formula, conclusion unsupported by evidence, duplicated sections.
- `MINOR`: wording, paragraph order, notation consistency, caption/style clarity.

For each issue, identify the section, quote or paraphrase the problematic sentence briefly, explain the problem, and propose a concrete revision.

## Default paper architecture

Adapt to the actual problem; do not force empty sections.

1. 摘要 + 关键词
2. 问题重述 / 问题背景（按模板和实际需要）
3. 问题分析
4. 模型假设
5. 符号说明
6. 数据说明与预处理（如需要）
7. 问题一：模型建立、求解、结果与分析
8. 问题二：模型建立、求解、结果与分析
9. ...
10. 模型检验 / 误差分析 / 敏感性分析（可按问题分散写）
11. 模型评价、改进与推广（按需要）
12. 结论
13. 参考文献
14. 附件说明（按赛题要求）

Prefer organizing the technical body around the competition's subquestions when that makes judge navigation easier.

## Completion rule

Before declaring a section complete, verify:

- every numerical claim is traceable to a computation/table/figure;
- every major conclusion answers a posed question;
- every formula is derived or sourced and its symbols are defined;
- no section is doing another section's job;
- abstract, body, and conclusion agree on model names and numbers;
- no official-format or AI-use rule has been violated.
