---
name: huawei-cpipc-paper
description: Write, revise, structure, and audit Chinese mathematical-modeling papers for the Huawei Cup China Graduate Mathematical Modeling Contest (中国研究生数学建模竞赛/“华为杯”). Use when Codex is asked to draft or polish abstracts, introductions, problem restatements, problem analysis, assumptions, notation, data preprocessing, model formulation, algorithms, figures/tables, results, validation, sensitivity analysis, model evaluation, conclusions, references, or a full competition paper; to decide what every section and sentence should express; to distinguish abstract vs introduction vs problem analysis vs conclusion; to turn modeling notes, code outputs, figures, and numerical results into judge-oriented prose; to emulate transferable structural patterns of strong/award-winning papers without copying them; or to check a Huawei Cup paper against the 2026 official format and AI-use rules. Do not invent data, numerical results, citations, model provenance, award status, or experimental evidence.
---

# Huawei Cup Paper Writing

Write for a mathematical-modeling judge: make the chain **question -> reasoning -> model -> computation -> evidence -> answer** easy to verify.

The goal is not to generate “academic-sounding” prose. The goal is to make every sentence do useful work and make every conclusion traceable to evidence.

## Source priority

Use sources in this order when rules conflict:

1. The current year's official Huawei Cup notice, paper-format specification, official template, problem statement, and AI-tool rules.
2. The current problem's explicit submission requirements.
3. The team's real data, equations, code, computation outputs, figures, and experiment logs.
4. This skill's writing guidance.
5. Award-paper patterns and online teaching material.

Never present a teaching convention, an award-paper habit, or this skill's preference as an official rule.

## Load the right references

Read only what the task needs:

- **Official compliance / final audit** -> `references/official-2026.md`
- **What each section and each sentence should do** -> `references/writing-blueprint.md`
- **Abstract vs Intro vs problem analysis vs model vs result vs conclusion boundaries** -> `references/section-boundaries.md`
- **Figures, tables, equations, numerical claims, validation, sensitivity** -> `references/evidence-writing.md`
- **Format discipline + model workload / complexity ladder** -> `references/format-and-workload.md`
- **“Write like a strong/award-winning modeling paper”** -> `references/award-paper-patterns.md`
- **Final manuscript audit** -> `references/review-checklist.md`
- **Automated heuristic linting** -> `tools/paper_lint.py` and `tools/README.md`
- **Sentence-level section examples** -> `examples/section-templates.md`
- **Full-paper drafting or restructuring** -> `examples/full-paper-skeleton.md`

For 2026 submissions, read `references/official-2026.md` before declaring anything compliant.

## Required workflow

### 1. Establish the evidence base before prose

Identify:

- the exact subquestions to answer;
- the team's actual model/method for each subquestion;
- variables, assumptions, formulas, parameters, algorithms, and solver settings actually used;
- all computed results that may be stated numerically;
- the evidence supporting each conclusion: table, figure, metric, proof, simulation, error analysis, sensitivity analysis, feasibility check, or baseline comparison;
- provenance of data, formulas, models, algorithms, code, and external claims;
- which content involved AI assistance.

If a required number, source, derivation, result, or experiment is missing, do **not** fill it with a plausible value. Use an explicit placeholder such as `【待补：问题2最优目标值】`.

Do not transform a plan into a claimed completed experiment. “建议进行敏感性分析” cannot become “敏感性分析表明模型稳定” unless results exist.

### 2. Build a question-to-evidence matrix

Before writing a full paper or a large section, silently map each subquestion:

| Subquestion | Required output | Method/model | Computation | Evidence | Validation | Final answer |
|---|---|---|---|---|---|---|
| Q1 | ... | ... | ... | ... | ... | ... |

Any blank cell in `Required output`, `Evidence`, or `Final answer` is a likely `MAJOR` issue.

### 2.5. Pass the two competition-readiness gates

Read `references/format-and-workload.md` for architecture, full-paper drafting, and final audit.

#### Gate A — Format discipline

Before optimizing prose or adding advanced models, verify the manuscript can be evaluated smoothly:

- anonymity and file hygiene follow the official rules;
- the abstract independently exposes task, method/model, key results, conclusion, and innovation/characteristics;
- figure/table/equation numbering is consistent;
- symbols and units are consistent across the whole paper;
- body text, figures/tables, and code/attachments agree on model names, parameters, sample sizes, units, results, and final schemes;
- conclusions do not exceed what the model and evidence actually support.

Do not silently convert a teaching convention into an official requirement. For exact formatting, the current official template and notice remain authoritative.

#### Gate B — Model workload / justified complexity

Make the team's actual work visible through a problem-driven ladder:

`baseline runnable -> mechanism integration -> optimization enhancement -> uncertainty treatment -> validation/feedback`

Interpret the layers as:

1. **Baseline runnable**: the model runs, is reproducible, and directly answers a task.
2. **Mechanism integration**: industry/physical/engineering/business structure is embedded in equations, constraints, states, geometry, or system logic rather than using generic data fitting alone.
3. **Optimization enhancement**: advanced optimization/search is added only to solve a real non-convex, combinatorial, discrete, large-scale, multi-objective, or otherwise difficult computation.
4. **Uncertainty treatment**: randomness, measurement error, parameter uncertainty, or scenario variability is modeled when it can change conclusions.
5. **Validation/feedback**: sensitivity, error analysis, baseline comparison, cross-validation, boundary tests, ablation, feasibility checks, or robustness tests close the modeling loop.

Not every problem needs all five layers. Complexity must be justified by a concrete problem difficulty and show incremental value. Do **not** stack GA/PSO/SA/ACO/deep learning/Monte Carlo merely to make the paper look busy.

For every added layer, silently fill:

| Layer | Problem difficulty | Added mechanism/method | New evidence | Incremental value vs previous layer | Keep? |
|---|---|---|---|---|---|

If `Problem difficulty` or `Incremental value` is empty, simplify the model instead of adding complexity.

### 3. Build a section map before prose

Give every substantive item one **primary home**.

- **摘要**: compressed problem + method + model + concrete result/conclusion + validation/innovation.
- **引言/问题背景**: why the problem matters, the concrete difficulty, relevant method context, and what the paper will do; not a second abstract.
- **问题重述**: what the problem gives and asks; no solution details or final results.
- **问题分析**: why the problem decomposes this way, what matters, and why a modeling route is appropriate; no final numerical answer.
- **模型假设**: simplifying assumptions plus justification and scope.
- **符号说明**: symbols, meanings, units/domains.
- **数据与预处理**: data provenance, quality checks, cleaning, transformations, and derived variables.
- **模型建立**: mathematical objects, objective/constraints/relations, derivation, parameter meaning.
- **模型求解/算法**: how the established mathematical problem is computed.
- **结果**: what the computation produced.
- **结果分析**: what those values mean and how they answer the problem.
- **检验/误差/敏感性**: why the result should be trusted and where it may fail.
- **模型评价/改进**: evidence-backed strengths, concrete limitations, scope, and matched improvements.
- **结论**: direct answers to the posed questions, key quantitative findings, validation, and necessary scope; no new method or new experiment.
- **参考文献/附件**: traceability and reproducibility.

Use `references/section-boundaries.md` when a sentence could plausibly belong to more than one section.

### 4. Give every sentence one primary job

Before writing a paragraph, silently assign each sentence one dominant role:

- `B` Background/context
- `T` Task/question
- `D` Decision/rationale: why this decomposition, assumption, or method
- `M` Method/model/operation
- `E` Evidence: data, metric, figure/table, derivation, experiment fact
- `R` Result/answer
- `I` Interpretation/implication
- `V` Validation/robustness
- `L` Limitation/scope
- `C` Contribution/innovation

A sentence can have a secondary role but should have one dominant job. If a sentence tries to provide background, method, result, interpretation, and self-evaluation at once, split it.

Do not expose these role tags in polished manuscript text unless the user asks for an annotated draft.

### 5. Draft from evidence outward

Prefer this order for serious drafting:

1. Confirm final numbers and key outputs.
2. Design the essential result tables/figures.
3. Write `结果与分析` around those verified outputs.
4. Write direct answer sentences for every subquestion.
5. Write validation/error/sensitivity sections from actual experiments.
6. Write model formulation and solution so every reported result has a reproducible origin.
7. Write problem analysis and assumptions.
8. Write the conclusion.
9. Write the abstract last, using only claims supported in the body.
10. Tighten introduction/problem restatement after the technical story is stable.

This prevents the abstract from promising a result that the body never actually demonstrates.

### 6. Use evidence paragraphs, not “figure dumping”

For an important figure/table/result, prefer:

`Claim -> Evidence -> Interpretation -> Answer/Decision`

Example logic:

- **Claim**: identify the important pattern.
- **Evidence**: give the actual number, difference, range, or metric.
- **Interpretation**: explain what the evidence means without overstating causality.
- **Answer**: connect it to the subquestion or modeling decision.

Do not stop at “结果如图所示” or “由图可知模型效果较好”. See `references/evidence-writing.md`.

### 7. Enforce boundaries between commonly confused sections

Use these tests:

- **Why does this problem matter / what is difficult?** -> Introduction/background.
- **What exactly does the problem ask us to output?** -> Problem restatement.
- **Why do we decompose it this way / choose this modeling route?** -> Problem analysis.
- **What mathematical problem did we actually construct?** -> Model formulation.
- **How do we compute its solution?** -> Algorithm/solution.
- **What did the computation produce?** -> Results.
- **What do those values mean?** -> Result analysis.
- **Why should we trust them?** -> Validation/sensitivity/error analysis.
- **What is the final answer to each question?** -> Conclusion.
- **What must a judge know without reading the body?** -> Abstract, in compressed form.

The same key numerical result may appear in abstract, body, and conclusion, but at different resolution:

- abstract: key number + method context;
- body: full evidence and analysis;
- conclusion: key number + direct answer/reliability.

Do not copy the same paragraph three times.

### 8. Write judge-oriented mathematical prose

- Lead paragraphs with purpose or finding, not filler.
- Prefer quantified evidence over “很好”“显著”“较优” when metrics exist.
- Do not use “显著” as a statistical claim unless statistical significance was actually tested.
- After an important equation, define symbols and explain how its terms correspond to the problem mechanism.
- After important constraints, translate them back to real-world restrictions.
- After an algorithm, state key parameters and stopping criteria when material.
- Distinguish software from method: “Python/MATLAB” is an implementation environment, not a modeling method.
- Distinguish observation from interpretation: report the measured/computed fact first, then explain it.
- Distinguish algorithm convergence from model validity.
- Avoid claiming global optimality when a heuristic only found the best solution observed in the search.
- Keep terminology, symbols, model names, metrics, and units identical across abstract, body, figures, and conclusion.

### 9. Learn structure from award papers, never copy prose

When asked to use “一等奖论文风格”, read `references/award-paper-patterns.md`.

Transfer only structural properties such as:

- question-by-question navigation;
- method-result micro-loops in the abstract;
- explicit reasoning in problem analysis;
- equation-to-reality explanations;
- quantified result statements;
- validation matched to problem type;
- direct answers in the conclusion.

Do not imitate distinctive sentences, copy passages, or force a model merely because an awarded paper used it.

### 10. Handle citations and AI assistance conservatively

Follow the current official rules. For 2026, AI is permitted only as an auxiliary tool and the team remains responsible for understanding, verification, provenance, and final wording. See `references/official-2026.md`.

When Codex assists:

- treat generated prose as a candidate draft requiring team review;
- never fabricate a reference, DOI, model source, dataset source, or experiment;
- prefer real papers/books/official pages or a transparent derivation for mathematical content;
- identify passages whose technical claims need human verification;
- preserve a lightweight AI-use log if useful for later compliance;
- if AI assisted code or data analysis, remind the team to satisfy the current official disclosure requirements.

## Output modes

### Architecture mode

Use when the user has a problem statement, notes, code, or partial paper but needs the paper architecture.

Return:

1. question-to-evidence matrix;
2. proposed section tree;
3. for each subsection, the intended sentence roles and evidence to insert;
4. missing information marked `【待补】`;
5. a **Format Gate** checklist covering anonymity, abstract completeness, numbering/symbols/units, and body-figure-code consistency;
6. a **Workload Ladder** table showing, for each subquestion, which of `baseline -> mechanism -> optimization -> uncertainty -> validation` is actually needed and why.

Do not write pages of prose before the architecture is coherent. Do not recommend extra model layers unless they solve a named difficulty and create measurable incremental value.

### Draft mode

Given notes/results, first make a concise internal sentence-role plan, then write the requested section. Use only verified inputs.

### Evidence mode

Use when the user provides figures, tables, code output, experiment logs, or numerical results. Convert them into `Claim -> Evidence -> Interpretation -> Answer` prose. Do not infer unsupported causes.

### Rewrite mode

Preserve mathematical meaning and real numerical results. Improve structure, remove repetition, tighten claims, and move sentences to the section where they belong. Flag unsupported factual claims rather than polishing them into certainty.

### Boundary audit mode

For each suspicious sentence/paragraph, report:

`current section -> sentence role -> best section -> reason -> rewritten version`

Pay special attention to abstract / Introduction / problem analysis / results / conclusion duplication.

### Full-paper mode

Read `examples/full-paper-skeleton.md`. Draft in question-oriented modules. Do not force empty sections. Keep placeholders when evidence is missing.

### Lint mode

When a UTF-8 `.tex`, `.md`, or `.txt` manuscript is available, run:

```bash
python tools/paper_lint.py <paper> --fail-on none
```

Use `--fragment` when checking only one section. Use `--json` when another tool or Agent will consume the findings.

Treat linter output as **review targets**, not automatic truth. Resolve findings against the manuscript, the team's evidence, `references/review-checklist.md`, and the official rules. Do not blindly delete legitimate institution names in citations or weaken a mathematically justified claim merely to silence a heuristic warning.

### Audit mode

For text-source manuscripts, run Lint mode first when practical, then perform semantic/manual audit. Merge both sets of findings instead of returning the linter output alone.

Every full Audit must answer two additional high-level questions:

- **Format risk**: could formatting, anonymity, numbering, symbol/unit inconsistency, body-figure-code mismatch, or unsupported conclusion language cause the work to be undervalued?
- **Workload visibility**: can a judge clearly see what real modeling work was done at the baseline, mechanism, optimization, uncertainty, and validation levels, and does each retained layer add justified value?

Return issues grouped by severity:

- `BLOCKER`: official-rule violation, identity leakage, fabricated/unsupported content, broken provenance, AI-compliance risk, MD5/submission risk.
- `MAJOR`: missing answer to a subquestion, method/result inconsistency, unexplained formula, unsupported conclusion, missing validation for a critical claim, duplicated/incorrect section roles, invisible or unjustified model layers.
- `MINOR`: wording, paragraph order, notation consistency, caption/style clarity.

For each issue, identify the section, quote/paraphrase the problematic text briefly, explain the issue, and propose a concrete revision. Linter findings should keep their rule code and line number when useful.

## Default paper architecture

Adapt to the actual problem; do not force empty sections.

1. 摘要 + 关键词
2. 问题重述 / 问题背景（按模板和实际需要）
3. 问题分析
4. 模型假设
5. 符号说明
6. 数据说明与预处理（如需要）
7. 问题一：分析 -> 模型 -> 求解 -> 结果与分析 -> 检验 -> 答题句
8. 问题二：分析 -> 模型 -> 求解 -> 结果与分析 -> 检验 -> 答题句
9. ...
10. 跨问题的模型评价、改进与推广（按需要）
11. 结论
12. 参考文献
13. 附件说明（按赛题要求）

Prefer organizing the technical body around the competition's subquestions when that makes judge navigation easier.

## Completion rule

Before declaring a section complete, verify:

- every numerical claim is traceable to a computation/table/figure;
- every important table/figure has a written finding, not just a reference;
- every major conclusion answers a posed question;
- every formula is derived or sourced and its important symbols are defined;
- important constraints are connected to real problem restrictions;
- method, result, interpretation, and validation have not been conflated;
- no section is doing another section's main job;
- abstract, body, and conclusion agree on model names, metrics, units, and numbers;
- body text, figures/tables, and code/attachments do not contradict one another;
- claimed innovations are visible and supported in the body;
- each advanced model layer solves a named problem difficulty and has evidence of incremental value;
- unnecessary algorithm/model stacking has been removed;
- the final model chain is reproducible and closes with validation appropriate to the problem;
- no official-format, citation, anonymity, or AI-use rule has been violated;
- if a text manuscript was available, automated lint findings have been reviewed rather than ignored.
