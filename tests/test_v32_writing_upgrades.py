from pathlib import Path


ROOT = Path(__file__).parents[1]


def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8")


def assert_has(text, *phrases):
    for phrase in phrases:
        assert phrase in text, phrase


def test_conclusion_three_ideas():
    assert_has(read("skills/viet-ket-luan-khuyen-nghi/SKILL.md"),
               "trả lời câu hỏi", "trong giới hạn", "nghiên cứu gì", "không bắt buộc ba đoạn")


def test_abstract_standalone_check():
    assert_has(read("skills/viet-tom-tat/references/abstract-lifecycle.md"),
               "vì sao cần nghiên cứu", "phát hiện quan trọng nhất", "ý nghĩa", "không cần đọc toàn văn",
               "khoảng tin cậy")


def test_thesis_to_article_steps():
    text = read("skills/viet-ban-thao-y-hoc/references/thesis-to-article.md")
    assert_has(text, "một câu hỏi trung tâm", "Phương pháp và Kết quả trước", "thứ tự tác giả", "phạm vi đồng ý",
               "](../../dao-duc-va-quan-tri-du-lieu/SKILL.md)", "](../../phan-tich-so-lieu/SKILL.md)")
    assert_has(read("skills/viet-ban-thao-y-hoc/SKILL.md"),
               "](references/thesis-to-article.md)", "](references/journal-selection.md)")


def test_journal_selection_verifies_official_pages():
    assert_has(read("skills/viet-ban-thao-y-hoc/references/journal-selection.md"),
               "Elsevier Journal Finder", "Springer Nature Journal Suggester", "Wiley Journal Finder",
               "Taylor & Francis", "aims & scope", "Scopus", "phí công bố", "ngày kiểm", "3–5")


def test_review_panel_disagreement_first():
    assert_has(read("skills/tu-phan-bien/references/reconciliation.md"),
               "bất đồng trước", "đồng thuận không đồng nghĩa với đúng", "không quy đồng thuận thành mức tin cậy")


def test_quick_seed_search_mode():
    assert "## Quick-seed mode" in read("skills/tim-y-van/SKILL.md")
    assert_has(read("skills/tim-y-van/references/retrieval-contract.md"), "Similar articles", "CSV", "không thay thế")
