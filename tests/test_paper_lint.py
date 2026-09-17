import importlib.util
from pathlib import Path
import sys
import unittest

MODULE_PATH = Path(__file__).parents[1] / "tools" / "paper_lint.py"
spec = importlib.util.spec_from_file_location("paper_lint", MODULE_PATH)
paper_lint = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = paper_lint
spec.loader.exec_module(paper_lint)


class PaperLintTests(unittest.TestCase):
    def codes(self, text, **kwargs):
        return {issue.code for issue in paper_lint.lint_text(text, **kwargs)}

    def test_placeholders_are_blockers(self):
        text = "# 摘要\n结果为【待补：RMSE】。\n# 问题分析\n分析。\n# 结论\n结论。\n# 参考文献\n"
        issues = paper_lint.lint_text(text)
        self.assertTrue(any(i.code == "PLACEHOLDER" and i.severity == "BLOCKER" for i in issues))

    def test_identity_email_is_blocker(self):
        text = "# 摘要\n联系邮箱 abc@example.com\n# 问题分析\n分析。\n# 结论\n结论。\n# 参考文献\n"
        self.assertIn("IDENTITY_EMAIL", self.codes(text))

    def test_vague_figure_sentence_is_major(self):
        text = "# 摘要\n摘要。\n# 问题分析\n分析。\n# 结果与分析\n由图可知模型效果较好。\n# 结论\n结论。\n# 参考文献\n"
        issues = paper_lint.lint_text(text)
        self.assertTrue(any(i.code == "VAGUE_FIGURE_TABLE" and i.severity == "MAJOR" for i in issues))

    def test_quantified_figure_sentence_is_not_vague(self):
        text = "# 摘要\n摘要。\n# 问题分析\n分析。\n# 结果与分析\n由图 3 可知，RMSE 为 0.82，较基准下降 14.2%。\n# 结论\n结论。\n# 参考文献\n"
        self.assertNotIn("VAGUE_FIGURE_TABLE", self.codes(text))

    def test_broken_latex_float_ref(self):
        text = r"""# 摘要
摘要。
# 问题分析
见图 \ref{fig:missing}。
# 结论
结论。
# 参考文献
"""
        self.assertIn("BROKEN_FLOAT_REFERENCE", self.codes(text))

    def test_missing_reference_entry(self):
        text = "# 摘要\n依据已有研究[2]。\n# 问题分析\n分析。\n# 结论\n结论。\n# 参考文献\n[1] A, B.\n"
        self.assertIn("MISSING_REFERENCE_ENTRY", self.codes(text))

    def test_fragment_mode_does_not_require_sections(self):
        issues = paper_lint.lint_text("这是一个结果段。", full_paper=False)
        self.assertFalse(any(i.code == "MISSING_SECTION" for i in issues))

    def test_abstract_requirements_are_checked(self):
        text = "# 摘要\n本文讨论该问题。\n# 问题分析\n分析。\n# 结论\n结论。\n# 参考文献\n"
        codes = self.codes(text)
        self.assertIn("ABSTRACT_MISSING_METHOD", codes)
        self.assertIn("ABSTRACT_MISSING_RESULT", codes)
        self.assertIn("ABSTRACT_MISSING_INNOVATION", codes)
        self.assertIn("MISSING_KEYWORDS", codes)

    def test_plain_figure_caption_without_reference(self):
        text = "# 摘要\n建立模型并得到结果，提出改进方法。\n关键词：模型\n# 问题分析\n分析。\n# 结果与分析\n图 1：结果曲线\n# 结论\n得到结论。\n# 参考文献\n"
        self.assertIn("UNREFERENCED_PLAIN_FLOAT", self.codes(text))

    def test_similarity_flags_near_copy(self):
        shared = "本文针对调度问题建立模型并得到关键结果。最优方案总成本为123.45元，较基准下降12.3%。敏感性分析表明核心方案保持稳定。"
        text = f"# 摘要\n{shared}\n# 问题分析\n这里解释建模路线。\n# 结论\n{shared}\n# 参考文献\n"
        self.assertIn("ABSTRACT_CONCLUSION_DUPLICATION", self.codes(text))


if __name__ == "__main__":
    unittest.main()
