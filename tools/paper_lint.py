#!/usr/bin/env python3
"""Heuristic linter for Huawei Cup mathematical-modeling papers.

The linter is intentionally conservative: it finds review targets rather than
claiming that a paper is correct or incorrect. It uses only Python's standard
library and works with Markdown, LaTeX, and plain-text exports.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple

SEVERITY_ORDER = {"BLOCKER": 0, "MAJOR": 1, "MINOR": 2}
FAIL_RANK = {"none": 99, "minor": 2, "major": 1, "blocker": 0}


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    line: int
    message: str
    excerpt: str = ""


@dataclass(frozen=True)
class Section:
    title: str
    start_line: int
    end_line: int
    text: str


PLACEHOLDER_PATTERNS = [
    re.compile(r"\b(?:TODO|FIXME|TBD)\b", re.I),
    re.compile(r"(?<![A-Za-z])XXX(?![A-Za-z])", re.I),
    re.compile(r"【?待补(?::|：|】|\b)"),
    re.compile(r"\?\?+|？？+"),
]

IDENTITY_PATTERNS = [
    ("IDENTITY_EMAIL", re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I), "检测到邮箱地址"),
    ("IDENTITY_TEAM", re.compile(r"(?:队伍编号|参赛队号|参赛队编号|队号)\s*[:：]?\s*[A-Za-z0-9_-]{4,}"), "检测到队伍编号/队号"),
    ("IDENTITY_PERSON", re.compile(r"(?:队员|参赛人员|作者|导师|指导教师)\s*[:：]"), "检测到人员身份字段"),
    ("IDENTITY_ORG", re.compile(r"[\u4e00-\u9fff]{2,}(?:大学|学院|研究院|实验室|研究中心)"), "检测到可能的单位/实验室名称"),
]

VAGUE_EVIDENCE = re.compile(r"(?:由|从|根据)?(?:图|表)\s*[0-9一二三四五六七八九十-]*\s*(?:可知|可以看出|看出|显示|表明)|如(?:图|表)所示")
CLAIM_WORDS = re.compile(r"显著|明显优于|鲁棒|稳健|稳定性(?:较好|很好|强)|效果(?:较好|很好)|性能(?:较好|很好)|最优|全局最优|普适|完全证明|证明了")
EVIDENCE_HINTS = re.compile(r"(?:\d+(?:\.\d+)?\s*(?:%|‰|元|秒|分钟|小时|天|个|次|km|m|kg|℃)|p\s*[<=>]|置信区间|误差|RMSE|MAE|MSE|R\^?2|准确率|召回率|F1|AUC|方差|标准差|灵敏度|敏感性|扰动|对比|基准|表\s*\d|图\s*\d)", re.I)
ABSTRACT_METHOD_HINTS = re.compile(r"模型|方法|算法|建立|构建|采用|求解|拟合|优化|预测")
ABSTRACT_RESULT_HINTS = re.compile(r"结果|得到|表明|确定|预测为|最优|误差|准确率|提升|下降|提高|降低")
ABSTRACT_INNOVATION_HINTS = re.compile(r"创新|特点|改进|提出|引入|构造|设计|耦合|自适应|修正")
GENERIC_BACKGROUND_RE = re.compile(r"随着.{0,20}(?:快速|不断|迅速)?发展|具有(?:十分|非常|重要的)?现实意义|具有重要意义")

CITATION_RE = re.compile(r"(?<!\[)\[(\d{1,3})\](?!\])")
BIB_ENTRY_RE = re.compile(r"^\s*\[(\d{1,3})\]\s+", re.M)
LATEX_CITE_RE = re.compile(r"\\cite\w*\{([^}]+)\}")
LATEX_BIBITEM_RE = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}")
LATEX_LABEL_RE = re.compile(r"\\label\{((?:fig|tab):[^}]+)\}")
LATEX_REF_RE = re.compile(r"\\(?:ref|autoref|cref|Cref)\{((?:fig|tab):[^}]+)\}")

NUMBER_RE = re.compile(r"(?<![A-Za-z0-9])[-+]?\d+(?:\.\d+)?(?:%|‰)?")


def _clean_heading(raw: str) -> str:
    title = re.sub(r"[*_`#{}]", "", raw).strip()
    title = re.sub(r"^\s*(?:\d+(?:\.\d+)*|[一二三四五六七八九十]+)[、.．\s]+", "", title)
    return title.strip()


def extract_sections(text: str) -> List[Section]:
    lines = text.splitlines()
    heads: List[Tuple[int, str]] = []
    md = re.compile(r"^\s*#{1,6}\s+(.+?)\s*$")
    tex = re.compile(r"^\s*\\(?:section|subsection|subsubsection)\*?\{(.+?)\}\s*$")
    numbered = re.compile(r"^\s*(?:\d+(?:\.\d+){0,3}|[一二三四五六七八九十]+)[、.．\s]+([^。；，]{1,40})\s*$")
    bare = re.compile(r"^\s*(摘要|关键词|问题重述|问题分析|模型假设|符号说明|数据(?:说明|预处理)?|模型(?:建立|求解|检验|评价)|结果(?:与分析)?|敏感性分析|误差分析|结论|参考文献|附录|附件)\s*$")

    for idx, line in enumerate(lines, 1):
        match = md.match(line) or tex.match(line) or numbered.match(line) or bare.match(line)
        if match:
            heads.append((idx, _clean_heading(match.group(1))))

    sections: List[Section] = []
    for i, (start, title) in enumerate(heads):
        end = heads[i + 1][0] - 1 if i + 1 < len(heads) else len(lines)
        body = "\n".join(lines[start:end])
        sections.append(Section(title=title, start_line=start, end_line=end, text=body))
    return sections


def _find_section(sections: Sequence[Section], keywords: Sequence[str]) -> Optional[Section]:
    for section in sections:
        if any(word in section.title for word in keywords):
            return section
    return None


def _normalize_similarity(text: str) -> str:
    text = re.sub(r"\\(?:cite|ref|label)\w*\{[^}]*\}", "", text)
    text = re.sub(r"[`*_#>$|\\{}\[\]()]", "", text)
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[，。！？；：、,.!?;:\-—]", "", text)
    return text


def _sentences_with_offsets(text: str) -> Iterable[Tuple[int, str]]:
    lines = text.splitlines()
    for line_no, line in enumerate(lines, 1):
        for sentence in re.split(r"(?<=[。！？；!?;])\s*", line):
            sentence = sentence.strip()
            if sentence:
                yield line_no, sentence


def _excerpt(line: str, limit: int = 120) -> str:
    line = " ".join(line.strip().split())
    return line if len(line) <= limit else line[: limit - 1] + "…"


def _issue(issues: List[Issue], severity: str, code: str, line: int, message: str, excerpt: str = "") -> None:
    issues.append(Issue(severity, code, max(line, 1), message, _excerpt(excerpt)))


def check_placeholders(lines: Sequence[str], issues: List[Issue]) -> None:
    for i, line in enumerate(lines, 1):
        if any(p.search(line) for p in PLACEHOLDER_PATTERNS):
            _issue(issues, "BLOCKER", "PLACEHOLDER", i, "终稿中仍存在待补/TODO/XXX/?? 占位内容", line)


def check_identity(lines: Sequence[str], issues: List[Issue], allow_identity: bool) -> None:
    if allow_identity:
        return
    in_reference = False
    for i, line in enumerate(lines, 1):
        stripped = _clean_heading(line)
        if "参考文献" in stripped:
            in_reference = True
        if in_reference:
            continue
        for code, pattern, message in IDENTITY_PATTERNS:
            if pattern.search(line):
                _issue(issues, "BLOCKER", code, i, f"{message}；匿名稿需人工确认是否泄露身份", line)


def check_vague_evidence(lines: Sequence[str], issues: List[Issue]) -> None:
    for i, line in enumerate(lines, 1):
        if VAGUE_EVIDENCE.search(line) and not EVIDENCE_HINTS.search(line):
            _issue(
                issues,
                "MAJOR",
                "VAGUE_FIGURE_TABLE",
                i,
                "图表分析只有“由图/表可知”式描述，附近未检测到量化证据；补充指标、数值、对比和答题含义",
                line,
            )


def check_claim_language(lines: Sequence[str], issues: List[Issue]) -> None:
    for i, line in enumerate(lines, 1):
        if CLAIM_WORDS.search(line) and not EVIDENCE_HINTS.search(line):
            _issue(
                issues,
                "MINOR",
                "UNSUPPORTED_EVALUATION",
                i,
                "检测到“显著/鲁棒/最优/稳定”等评价词，但本句未见量化或检验证据；请核验措辞强度",
                line,
            )


def check_abstract_requirements(text: str, sections: Sequence[Section], issues: List[Issue]) -> None:
    abstract = _find_section(sections, ["摘要"])
    if not abstract:
        return
    body = abstract.text
    if not ABSTRACT_METHOD_HINTS.search(body):
        _issue(issues, "MAJOR", "ABSTRACT_MISSING_METHOD", abstract.start_line, "摘要中未明显识别到建模思路/主要方法/模型描述；按 2026 要求人工补核")
    if not ABSTRACT_RESULT_HINTS.search(body):
        _issue(issues, "MAJOR", "ABSTRACT_MISSING_RESULT", abstract.start_line, "摘要中未明显识别到结果与结论表达；不要只列方法")
    if not ABSTRACT_INNOVATION_HINTS.search(body):
        _issue(issues, "MAJOR", "ABSTRACT_MISSING_INNOVATION", abstract.start_line, "摘要中未明显识别到创新点/具体改进表达；按 2026 要求人工补核")
    if "关键词" not in text:
        _issue(issues, "MAJOR", "MISSING_KEYWORDS", abstract.end_line, "全文未检出“关键词”；2026 摘要要求包含关键词")


def check_style_smells(lines: Sequence[str], issues: List[Issue]) -> None:
    connector_hits = []
    for i, line in enumerate(lines, 1):
        if GENERIC_BACKGROUND_RE.search(line):
            _issue(issues, "MINOR", "GENERIC_BACKGROUND", i, "检测到泛化背景套话；确认该句是否提供了与赛题直接相关的信息", line)
        connector_hits.extend((i, word) for word in ("首先", "其次", "然后", "最后") if word in line)
    if len(connector_hits) >= 8:
        _issue(issues, "MINOR", "FLOW_CONNECTOR_OVERUSE", connector_hits[7][0], f"全文检测到“首先/其次/然后/最后”共 {len(connector_hits)} 次；检查是否写成流程目录式叙述")


def check_question_answer_cues(sections: Sequence[Section], issues: List[Issue]) -> None:
    question_re = re.compile(r"问题\s*(?:[一二三四五六七八九十]+|\d+)")
    answer_re = re.compile(r"最终|因此|结果|得到|确定|方案|排序|预测|答案|可得")
    question_indexes = [i for i, sec in enumerate(sections) if question_re.search(sec.title)]
    for pos, idx in enumerate(question_indexes):
        sec = sections[idx]
        next_idx = question_indexes[pos + 1] if pos + 1 < len(question_indexes) else len(sections)
        block = "\n".join(s.text for s in sections[idx:next_idx])
        if len(_normalize_similarity(block)) >= 60 and not answer_re.search(block):
            _issue(issues, "MINOR", "QUESTION_WITHOUT_ANSWER_CUE", sec.start_line, f"“{sec.title}”对应内容中未检出明确的结果/最终回答语句；确认该问是否真正闭环")


def check_plain_float_mentions(lines: Sequence[str], issues: List[Issue]) -> None:
    for kind in ("图", "表"):
        occurrences = Counter()
        caption_lines = {}
        pat = re.compile(rf"{kind}\s*(\d+)")
        caption = re.compile(rf"^\s*{kind}\s*(\d+)\s*[：:、.．\s]")
        for i, line in enumerate(lines, 1):
            for n in pat.findall(line):
                occurrences[n] += 1
            m = caption.match(line)
            if m:
                caption_lines[m.group(1)] = (i, line)
        for n, (line_no, line) in caption_lines.items():
            if occurrences[n] == 1:
                _issue(issues, "MINOR", "UNREFERENCED_PLAIN_FLOAT", line_no, f"{kind}{n} 疑似只有题注出现一次，正文未检出对应引用", line)


def check_abstract_conclusion_similarity(sections: Sequence[Section], issues: List[Issue]) -> None:
    abstract = _find_section(sections, ["摘要"])
    conclusion = _find_section(sections, ["结论", "总结"])
    if not abstract or not conclusion:
        return
    a = _normalize_similarity(abstract.text)
    c = _normalize_similarity(conclusion.text)
    if len(a) < 50 or len(c) < 50:
        return
    ratio = SequenceMatcher(None, a, c, autojunk=False).ratio()
    if ratio >= 0.62:
        _issue(
            issues,
            "MAJOR",
            "ABSTRACT_CONCLUSION_DUPLICATION",
            conclusion.start_line,
            f"摘要与结论文本相似度约 {ratio:.0%}，疑似重复；结论应以逐问答案、可靠性和边界为主",
            conclusion.title,
        )
    elif ratio >= 0.48:
        _issue(
            issues,
            "MINOR",
            "ABSTRACT_CONCLUSION_SIMILARITY",
            conclusion.start_line,
            f"摘要与结论文本相似度约 {ratio:.0%}，建议人工检查是否存在大段复述",
            conclusion.title,
        )


def _meaningful_numbers(text: str) -> List[str]:
    result: List[str] = []
    for token in NUMBER_RE.findall(text):
        plain = token.rstrip("%‰")
        try:
            val = abs(float(plain))
        except ValueError:
            continue
        if token.endswith(("%", "‰")) or "." in plain or val >= 10:
            result.append(token)
    return result


def check_summary_number_traceability(text: str, sections: Sequence[Section], issues: List[Issue]) -> None:
    abstract = _find_section(sections, ["摘要"])
    conclusion = _find_section(sections, ["结论", "总结"])
    if not sections:
        return
    for section, name in [(abstract, "摘要"), (conclusion, "结论")]:
        if not section:
            continue
        body_without = text[:]
        body_without = body_without.replace(section.text, "", 1)
        missing = [n for n in _meaningful_numbers(section.text) if n not in body_without]
        for number in sorted(set(missing))[:8]:
            _issue(
                issues,
                "MAJOR",
                "UNTRACED_SUMMARY_NUMBER",
                section.start_line,
                f"{name}中的数值“{number}”未在其他正文中检出；核对是否有正文证据或数字不一致",
                section.title,
            )


def check_citations(text: str, sections: Sequence[Section], issues: List[Issue]) -> None:
    ref_section = _find_section(sections, ["参考文献"])
    if ref_section:
        body = text[: text.find(ref_section.text)] if ref_section.text in text else text
        cited = {int(x) for x in CITATION_RE.findall(body)}
        entries = {int(x) for x in BIB_ENTRY_RE.findall(ref_section.text)}
        for num in sorted(cited - entries):
            _issue(issues, "MAJOR", "MISSING_REFERENCE_ENTRY", ref_section.start_line, f"正文引用 [{num}]，但参考文献列表未找到对应条目")
        for num in sorted(entries - cited):
            _issue(issues, "MINOR", "UNCITED_REFERENCE", ref_section.start_line, f"参考文献 [{num}] 未在正文中检出引用")

    latex_cites = set()
    for group in LATEX_CITE_RE.findall(text):
        latex_cites.update(x.strip() for x in group.split(",") if x.strip())
    bibitems = set(LATEX_BIBITEM_RE.findall(text))
    if bibitems:
        for key in sorted(latex_cites - bibitems):
            _issue(issues, "MAJOR", "MISSING_BIBITEM", 1, f"LaTeX 引用了文献键“{key}”，但未检出对应 \\bibitem")
        for key in sorted(bibitems - latex_cites):
            _issue(issues, "MINOR", "UNCITED_BIBITEM", 1, f"\\bibitem{{{key}}} 未在正文中检出引用")


def check_latex_figure_table_refs(text: str, issues: List[Issue]) -> None:
    labels = set(LATEX_LABEL_RE.findall(text))
    refs = set(LATEX_REF_RE.findall(text))
    for label in sorted(labels - refs):
        _issue(issues, "MINOR", "UNREFERENCED_FLOAT", 1, f"图/表标签“{label}”存在，但正文未检出 \\ref/\\autoref/\\cref 引用")
    for ref in sorted(refs - labels):
        _issue(issues, "MAJOR", "BROKEN_FLOAT_REFERENCE", 1, f"正文引用图/表标签“{ref}”，但未检出对应 \\label")


def check_repeated_sentences(text: str, issues: List[Issue]) -> None:
    candidates: List[Tuple[int, str, str]] = []
    for line_no, sentence in _sentences_with_offsets(text):
        normalized = _normalize_similarity(sentence)
        if len(normalized) >= 28 and not sentence.lstrip().startswith(("[", "%")):
            candidates.append((line_no, sentence, normalized))
    counts = Counter(norm for _, _, norm in candidates)
    reported = 0
    for norm, count in counts.items():
        if count < 2:
            continue
        occurrences = [(ln, s) for ln, s, n in candidates if n == norm]
        _issue(
            issues,
            "MINOR",
            "REPEATED_SENTENCE",
            occurrences[1][0],
            f"同一句较长表述在全文重复 {count} 次；检查是否为摘要/正文/结论机械复用",
            occurrences[1][1],
        )
        reported += 1
        if reported >= 8:
            break


def check_section_presence(sections: Sequence[Section], issues: List[Issue], full_paper: bool) -> None:
    if not full_paper:
        return
    required = [
        ("摘要", ["摘要"]),
        ("问题分析", ["问题分析"]),
        ("结论", ["结论", "总结"]),
        ("参考文献", ["参考文献"]),
    ]
    for label, words in required:
        if not _find_section(sections, words):
            _issue(issues, "MAJOR", "MISSING_SECTION", 1, f"按完整论文检查时未识别到“{label}”章节；若采用等价标题请人工确认")


def lint_text(text: str, *, allow_identity: bool = False, full_paper: bool = True) -> List[Issue]:
    lines = text.splitlines()
    sections = extract_sections(text)
    issues: List[Issue] = []

    check_placeholders(lines, issues)
    check_identity(lines, issues, allow_identity)
    check_vague_evidence(lines, issues)
    check_claim_language(lines, issues)
    check_abstract_requirements(text, sections, issues)
    check_style_smells(lines, issues)
    check_question_answer_cues(sections, issues)
    check_plain_float_mentions(lines, issues)
    check_abstract_conclusion_similarity(sections, issues)
    check_summary_number_traceability(text, sections, issues)
    check_citations(text, sections, issues)
    check_latex_figure_table_refs(text, issues)
    check_repeated_sentences(text, issues)
    check_section_presence(sections, issues, full_paper)

    return sorted(issues, key=lambda x: (SEVERITY_ORDER[x.severity], x.line, x.code))


def format_text_report(path: Path, issues: Sequence[Issue]) -> str:
    counts = Counter(i.severity for i in issues)
    out = [
        f"paper-lint: {path}",
        f"BLOCKER={counts['BLOCKER']}  MAJOR={counts['MAJOR']}  MINOR={counts['MINOR']}",
    ]
    if not issues:
        out.append("未发现当前规则覆盖的明显问题。仍需人工核验数学正确性、结果真实性和官方格式。")
        return "\n".join(out)
    current = None
    for issue in issues:
        if issue.severity != current:
            current = issue.severity
            out.extend(["", f"[{current}]"])
        out.append(f"L{issue.line:<4} {issue.code}: {issue.message}")
        if issue.excerpt:
            out.append(f"      > {issue.excerpt}")
    out.extend([
        "",
        "说明：paper-lint 是启发式审稿器，只定位需要人工复核的风险点，不替代官方规则检查、数学验证或人工审稿。",
    ])
    return "\n".join(out)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Lint Huawei Cup mathematical-modeling paper drafts.")
    parser.add_argument("paper", type=Path, help="Markdown/LaTeX/plain-text paper file")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument("--allow-identity", action="store_true", help="disable identity-leak checks (e.g. when linting an allowed cover page)")
    parser.add_argument("--fragment", action="store_true", help="lint a section fragment instead of requiring full-paper sections")
    parser.add_argument(
        "--fail-on",
        choices=("blocker", "major", "minor", "none"),
        default="blocker",
        help="exit non-zero when this severity or higher is found (default: blocker)",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        text = args.paper.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print("paper-lint 仅直接读取 UTF-8 文本；PDF/DOCX 请先导出为 Markdown/LaTeX/纯文本。", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"无法读取文件：{exc}", file=sys.stderr)
        return 2

    issues = lint_text(text, allow_identity=args.allow_identity, full_paper=not args.fragment)
    if args.json:
        payload = {
            "file": str(args.paper),
            "counts": dict(Counter(i.severity for i in issues)),
            "issues": [asdict(i) for i in issues],
            "disclaimer": "Heuristic review targets only; not a substitute for official-rule or mathematical verification.",
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(format_text_report(args.paper, issues))

    threshold = FAIL_RANK[args.fail_on]
    if any(SEVERITY_ORDER[i.severity] <= threshold for i in issues):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
