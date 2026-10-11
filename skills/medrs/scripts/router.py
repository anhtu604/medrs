"""Portable routing decisions for the canonical skill tree."""

from dataclasses import dataclass
import re
import unicodedata


def _normalized(text):
    return unicodedata.normalize("NFC", text.casefold()).strip()


def _mentions(text, term):
    return re.search(r"(?<![\w-])" + re.escape(term.casefold()) + r"(?![\w-])", text) is not None


@dataclass(frozen=True)
class RoutingRequest:
    text: str
    attachments: tuple[str, ...] = ()


@dataclass(frozen=True)
class RoutingDecision:
    entrypoint: str
    canonical: str
    mode: str
    availability: str


def route_request(request, legacy_map, active_skills):
    text = _normalized(request.text)
    colon = re.search(r"/medrs:([a-z][a-z0-9-]+)", text)
    if colon:
        name = colon.group(1)
        target = legacy_map.get(name, {}).get("canonical", name)
        if target in active_skills:
            return RoutingDecision("medrs", target, "explicit", "AVAILABLE")
        return RoutingDecision("medrs", "medrs", "unknown-explicit-skill", "UNAVAILABLE")
    # Remove explicitly negated action clauses, not their remaining positive tasks.
    text = re.sub(r"(?:^|[;,])\s*(?:không|don't|do not)\s+[^;,]+", "", text)
    # Explicit canonical invocations take precedence over incidental keywords.
    explicit = re.findall(r"(?:/|\$)([a-z][a-z0-9-]+)", text)
    for name in explicit:
        if name != "medrs" and name in active_skills:
            return RoutingDecision("medrs", name, "explicit", "AVAILABLE")
    for legacy_name, target in legacy_map.items():
        if _mentions(text, legacy_name):
            canonical = target["canonical"]
            availability = "AVAILABLE" if canonical in active_skills else "NOT_IN_ACTIVE_SLICE"
            return RoutingDecision("medrs", canonical, target["mode"], availability)

    # Specific requested actions outrank contextual nouns such as Methods/STROBE.
    action_routes = (
        (r"(?:tìm|search|find)\s+(?:tài liệu|nguồn|y văn|literature|sources)", "tim-y-van", "database-search"),
        (r"(?:viết|sửa|viết lại|rút gọn|write|revise|shorten)\s+(?:(?:phần|the)\s+)?(?:ppnc|phương pháp|methods)", "viet-phuong-phap", "draft-section"),
        (r"(?:viết|sửa|viết lại|rút gọn|write|revise|shorten)\s+(?:(?:phần|the)\s+)?(?:bàn luận|discussion)", "viet-ban-luan", "draft-section"),
        (r"(?:viết|sửa|rút gọn|write|revise|shorten)\s+(?:(?:phần|the)\s+)?(?:tổng quan|literature review)", "viet-tong-quan", "thematic-synthesis"),
        (r"(?:viết|sửa|write|revise)\s+(?:(?:phần|the)\s+)?(?:kết quả|results)", "viet-ket-qua", "draft-from-verified-results"),
        (r"(?:viết|sửa|write|revise)\s+(?:(?:phần|the)\s+)?(?:đặt vấn đề|introduction)", "viet-dat-van-de", "draft-section"),
    )
    candidates = []
    for pattern, skill, mode in action_routes:
        match = re.search(r"(?<!\w)" + pattern + r"(?!\w)", text)
        if match and not re.search(r"(?:không|don't|do not)\s*$", text[:match.start()]):
            candidates.append((match.start(), skill, mode))
    if candidates:
        _, skill, mode = min(candidates)
        return RoutingDecision("medrs", skill, mode,
                               "AVAILABLE" if skill in active_skills else "NOT_IN_ACTIVE_SLICE")

    early_routes = (
        (("diễn giải output", "diễn giải kết quả", "interpret results", "interpret output"),
         "phan-tich-so-lieu", "interpret-supplied-output"),
        (("nghiệm thu", "lên kế hoạch", "lập kế hoạch toàn bộ", "hướng dẫn từng bước",
          "điều phối dự án", "final acceptance", "project plan", "leader"),
         "leader-nghien-cuu", "plan-and-accept"),
        (("viết phương pháp", "viết ppnc", "phần phương pháp", "write the methods"),
         "viet-phuong-phap", "draft-section"),
        (("tính cỡ mẫu", "sample size", "lập kế hoạch phân tích", "soạn kế hoạch phân tích", "develop analysis plan"),
         "co-mau-va-ke-hoach-phan-tich", "prespecify"),
        (("thiết kế nghiên cứu", "soạn đề cương", "study design"),
         "de-cuong-va-thiet-ke", "design"),
        (("đạo đức nghiên cứu", "research ethics", "đồng thuận nghiên cứu"),
         "dao-duc-va-quan-tri-du-lieu", "ethics"),
        (("research passport", "hồ sơ nghiên cứu"), "ho-so-nghien-cuu", "update-project"),
        (("sửa comment", "xử lý comment", "sửa theo comment", "reviewer comments"),
         "phan-bien-va-chinh-sua", "revision"),
        (("sửa mục lục", "giãn dòng", "căn bảng", "bullet", "word styles"),
         "dinh-dang-tai-lieu", "word-mechanics"),
        (("tìm tài liệu", "tìm nguồn", "search literature"),
         "tim-y-van", "database-search"),
        (("phân tích số liệu", "phân tích dữ liệu", "analyze data"),
         "phan-tich-so-lieu", "analysis"),
    )
    for phrases, skill, mode in early_routes:
        if any(_mentions(text, phrase) for phrase in phrases):
            return RoutingDecision("medrs", skill, mode,
                                   "AVAILABLE" if skill in active_skills else "NOT_IN_ACTIVE_SLICE")

    adoption_phrases = (
        "đang viết dở",
        "bản thảo hiện có",
        "tiếp tục luận văn",
        "existing draft",
        "continue my thesis",
        "adopt existing",
    )
    supported_attachment = any(name.casefold().endswith((".docx", ".md", ".txt")) for name in request.attachments)
    if supported_attachment and any(phrase in text for phrase in adoption_phrases):
        return RoutingDecision("medrs", "ho-so-nghien-cuu", "adopt-existing-project", "AVAILABLE")

    style_audit_phrases = (
        "kiểm văn phong",
        "soát văn phong",
        "kiểm lập luận",
        "style audit",
        "audit the academic prose",
    )
    if any(phrase in text for phrase in style_audit_phrases):
        availability = "AVAILABLE" if "kiem-van-phong" in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("medrs", "kiem-van-phong", "full-audit", availability)

    if any(phrase in text for phrase in ("p nhỏ nhất", "smallest p", "p-value đẹp", "p value đẹp")):
        availability = "AVAILABLE" if "phan-tich-so-lieu" in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision(
            "medrs", "phan-tich-so-lieu", "refuse-significance-driven-selection", availability
        )

    if any(phrase in text for phrase in ("diễn giải output", "interpret the output", "interpret regression output")):
        availability = "AVAILABLE" if "phan-tich-so-lieu" in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("medrs", "phan-tich-so-lieu", "interpret-supplied-output", availability)

    if any(phrase in text for phrase in ("đổi font", "căn lề", "số trang", "mục lục và số trang", "word formatting", "định dạng luận văn", "format thesis")):
        skill = "dinh-dang-tai-lieu"
        availability = "AVAILABLE" if skill in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("medrs", skill, "word-mechanics", availability)

    if any(phrase in text for phrase in ("bố cục các chương", "sắp xếp lại bố cục", "reorder thesis sections", "semantic structure")):
        skill = "bo-cuc-tai-lieu"
        availability = "AVAILABLE" if skill in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("medrs", skill, "semantic-restructure", availability)

    pre_submission_phrases = (
        "tự phản biện",
        "tự review",
        "tự rà soát",
        "self-review",
        "review độc lập",
        "hai vòng",
        "kiểm chứng bản thảo",
        "kiểm tra trước khi nộp",
        "validate the manuscript",
        "submission readiness",
    )
    if any(phrase in text for phrase in pre_submission_phrases):
        skill = "tu-phan-bien"
        availability = "AVAILABLE" if skill in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("medrs", skill, "pre-submission-review", availability)

    guideline_phrases = (
        "chuẩn báo cáo",
        "đối chiếu consort",
        "consort",
        "spirit",
        "strobe",
        "prisma checklist",
        "checklist prisma",
        "tripod",
        "stard",
        "coreq",
        "care checklist",
        "cheers",
        "arrive 2.0",
        "arrive guideline",
        "chuẩn arrive",
        "prisma-p",
        "reporting guideline",
        "reporting checklist",
    )
    if any(phrase in text for phrase in guideline_phrases):
        skill = "kiem-chuan-bao-cao"
        availability = "AVAILABLE" if skill in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("medrs", skill, "guideline-compliance", availability)

    citation_routes = (
        (("kiểm tra trích dẫn", "check my citations", "citation faithfulness", "trích dẫn có trung thực"), "verify-faithfulness"),
        (("gắn trích dẫn", "chèn trích dẫn", "insert citations", "add citations"), "insert-citations"),
        (("zotero", "thư viện trích dẫn", "bibtex", "csl-json"), "library-read"),
    )
    for phrases, mode in citation_routes:
        if any(phrase in text for phrase in phrases):
            skill = "quan-ly-trich-dan"
            availability = "AVAILABLE" if skill in active_skills else "NOT_IN_ACTIVE_SLICE"
            return RoutingDecision("medrs", skill, mode, availability)

    figure_phrases = (
        "biểu đồ công bố",
        "vẽ biểu đồ",
        "publication figure",
        "publication-quality figure",
        "forest plot",
        "kaplan-meier",
        "kaplan meier",
    )
    if any(phrase in text for phrase in figure_phrases):
        skill = "bieu-do-cong-bo"
        availability = "AVAILABLE" if skill in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("medrs", skill, "design-figure", availability)

    review_routes = (
        (("trả lời phản biện", "response to reviewers", "point-by-point"), "response-to-reviewers"),
        (("nhận xét phản biện luận văn", "thesis examination", "thesis examiner"), "thesis-examination"),
        (("revise and resubmit", "sửa bài sau phản biện", "revision round"), "revision"),
    )
    for phrases, mode in review_routes:
        if any(phrase in text for phrase in phrases):
            skill = "phan-bien-va-chinh-sua"
            availability = "AVAILABLE" if skill in active_skills else "NOT_IN_ACTIVE_SLICE"
            return RoutingDecision("medrs", skill, mode, availability)

    r_code_phrases = ("script r", "r script", "mã r", "code r")
    if any(phrase in text for phrase in r_code_phrases):
        availability = "AVAILABLE" if "phan-tich-r" in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("medrs", "phan-tich-r", "generate-code", availability)

    stata_code_phrases = ("stata do-file", "stata do file", "do-file stata", "lệnh stata")
    if any(phrase in text for phrase in stata_code_phrases):
        availability = "AVAILABLE" if "phan-tich-stata" in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("medrs", "phan-tich-stata", "generate-code", availability)

    article_routes = (
        (("điều phối viết toàn bộ", "assemble the medical manuscript", "orchestrate the manuscript"), "viet-ban-thao-y-hoc", "orchestrate"),
        (("kết luận và khuyến nghị", "conclusion and recommendations"), "viet-ket-luan-khuyen-nghi", "draft-section"),
        (("final abstract", "tóm tắt cuối", "viết tóm tắt"), "viet-tom-tat", "draft-last"),
        (("phần discussion", "write the discussion", "viết bàn luận"), "viet-ban-luan", "draft-section"),
        (("write the results", "viết kết quả", "phần kết quả"), "viet-ket-qua", "draft-from-verified-results"),
        (("tổng quan y văn", "literature review"), "viet-tong-quan", "thematic-synthesis"),
        (("write the introduction", "viết đặt vấn đề", "phần mở đầu"), "viet-dat-van-de", "draft-section"),
    )
    for phrases, skill, mode in article_routes:
        if any(phrase in text for phrase in phrases):
            availability = "AVAILABLE" if skill in active_skills else "NOT_IN_ACTIVE_SLICE"
            return RoutingDecision("medrs", skill, mode, availability)

    if any(phrase in text for phrase in ("tổng hợp bằng chứng", "synthesize the evidence", "evidence synthesis")):
        availability = "AVAILABLE" if "tong-hop-bang-chung" in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("medrs", "tong-hop-bang-chung", "synthesize", availability)

    appraisal_routes = (
        (("rob 2", "rob2", "nguy cơ sai lệch rct"), "rob2"),
        (("grade certainty", "độ chắc chắn grade", "đánh giá grade"), "grade"),
        (("cerqual",), "cerqual"),
    )
    for phrases, mode in appraisal_routes:
        if any(phrase in text for phrase in phrases):
            skill = "danh-gia-chat-luong-bang-chung"
            availability = "AVAILABLE" if skill in active_skills else "NOT_IN_ACTIVE_SLICE"
            return RoutingDecision("medrs", skill, mode, availability)

    if any(phrase in text for phrase in ("mạng trích dẫn", "citation network", "citation graph")):
        availability = "AVAILABLE" if "tim-y-van" in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("medrs", "tim-y-van", "citation-network", availability)

    if any(phrase in text for phrase in ("tìm y văn", "literature search", "search pubmed")):
        availability = "AVAILABLE" if "tim-y-van" in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("medrs", "tim-y-van", "database-search", availability)

    clinical_advice = ("uống thuốc", "điều trị cho tôi", "chẩn đoán cho tôi", "what medicine", "diagnose me")
    research_terms = ("nghiên cứu", "luận văn", "đề cương", "research", "thesis", "protocol")
    if any(phrase in text for phrase in clinical_advice) and not any(term in text for term in research_terms):
        return RoutingDecision("medrs", "NONE", "out-of-scope-clinical-advice", "OUT_OF_SCOPE")
    return RoutingDecision("medrs", "medrs", "classify", "AVAILABLE")


def route_plan(request, legacy_map, active_skills):
    """Retain every compound-request clause and assign an owner; never execute it."""
    clauses = [part.strip(" -•") for part in re.split(
        r"\n+|;|\s+(?:rồi|then|sau đó)\s+|\s+(?:và|and)\s+(?=(?:sửa|viết|kiểm|tìm|căn|nghiệm|update|check|write|search|format)\b)|,\s*(?=(?:sửa|viết|kiểm|tìm|căn|nghiệm|update|check|write)\b)",
        request.text, flags=re.IGNORECASE
    ) if part.strip(" -•")]
    tasks = []
    for index, clause in enumerate(clauses or [request.text]):
        decision = route_request(RoutingRequest(clause, request.attachments), legacy_map, active_skills)
        tasks.append({"id": f"T{index + 1}", "request": clause, "skill": decision.canonical,
                      "mode": decision.mode, "availability": decision.availability})
    destinations = {task["skill"] for task in tasks}
    needs_leader = len(destinations) > 1 or "leader-nghien-cuu" in destinations
    coordinator = "leader-nghien-cuu" if needs_leader else "medrs"
    return {"entrypoint": "medrs", "coordinator": coordinator,
            "coordinator_available": coordinator in active_skills,
            "tasks": tasks, "execution_order": "resolve dependencies before execution",
            "unresolved": [task["id"] for task in tasks if task["skill"] == "medrs"]}


if __name__ == "__main__":
    import argparse
    import json
    import sys
    from pathlib import Path
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("text")
    args = parser.parse_args()
    skills_dir = Path(__file__).resolve().parents[2]
    active = {path.parent.name for path in skills_dir.glob("*/SKILL.md")}
    import yaml
    mapping_path = skills_dir / "medrs/references/legacy-skill-map.yaml"
    mapping = yaml.safe_load(mapping_path.read_text(encoding="utf-8"))["legacy"]
    print(json.dumps(route_plan(RoutingRequest(args.text), mapping, active), ensure_ascii=False, indent=2))
