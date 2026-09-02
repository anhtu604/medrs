"""Portable routing decisions for the canonical skill tree."""

from dataclasses import dataclass


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
    text = request.text.casefold().strip()
    for legacy_name, target in legacy_map.items():
        if legacy_name.casefold() in text:
            canonical = target["canonical"]
            availability = "AVAILABLE" if canonical in active_skills else "NOT_IN_ACTIVE_SLICE"
            return RoutingDecision("co-van", canonical, target["mode"], availability)

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
        return RoutingDecision("co-van", "ho-so-nghien-cuu", "adopt-existing-project", "AVAILABLE")

    style_audit_phrases = (
        "kiểm văn phong",
        "soát văn phong",
        "kiểm lập luận",
        "style audit",
        "audit the academic prose",
    )
    if any(phrase in text for phrase in style_audit_phrases):
        availability = "AVAILABLE" if "kiem-van-phong" in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("co-van", "kiem-van-phong", "full-audit", availability)

    if any(phrase in text for phrase in ("p nhỏ nhất", "smallest p", "p-value đẹp", "p value đẹp")):
        availability = "AVAILABLE" if "phan-tich-so-lieu" in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision(
            "co-van", "phan-tich-so-lieu", "refuse-significance-driven-selection", availability
        )

    if any(phrase in text for phrase in ("diễn giải output", "interpret the output", "interpret regression output")):
        availability = "AVAILABLE" if "phan-tich-so-lieu" in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("co-van", "phan-tich-so-lieu", "interpret-supplied-output", availability)

    if any(phrase in text for phrase in ("đổi font", "căn lề", "số trang", "mục lục và số trang", "word formatting", "định dạng luận văn", "format thesis")):
        skill = "dinh-dang-tai-lieu"
        availability = "AVAILABLE" if skill in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("co-van", skill, "word-mechanics", availability)

    if any(phrase in text for phrase in ("bố cục các chương", "sắp xếp lại bố cục", "reorder thesis sections", "semantic structure")):
        skill = "bo-cuc-tai-lieu"
        availability = "AVAILABLE" if skill in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("co-van", skill, "semantic-restructure", availability)

    review_routes = (
        (("trả lời phản biện", "response to reviewers", "point-by-point"), "response-to-reviewers"),
        (("nhận xét phản biện luận văn", "thesis examination", "thesis examiner"), "thesis-examination"),
        (("revise and resubmit", "sửa bài sau phản biện", "revision round"), "revision"),
    )
    for phrases, mode in review_routes:
        if any(phrase in text for phrase in phrases):
            skill = "phan-bien-va-chinh-sua"
            availability = "AVAILABLE" if skill in active_skills else "NOT_IN_ACTIVE_SLICE"
            return RoutingDecision("co-van", skill, mode, availability)

    r_code_phrases = ("script r", "r script", "mã r", "code r")
    if any(phrase in text for phrase in r_code_phrases):
        availability = "AVAILABLE" if "phan-tich-r" in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("co-van", "phan-tich-r", "generate-code", availability)

    stata_code_phrases = ("stata do-file", "stata do file", "do-file stata", "lệnh stata")
    if any(phrase in text for phrase in stata_code_phrases):
        availability = "AVAILABLE" if "phan-tich-stata" in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("co-van", "phan-tich-stata", "generate-code", availability)

    article_routes = (
        (("kiểm chứng bản thảo", "validate the manuscript", "submission readiness"), "kiem-chung-ban-thao", "validate"),
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
            return RoutingDecision("co-van", skill, mode, availability)

    if any(phrase in text for phrase in ("tổng hợp bằng chứng", "synthesize the evidence", "evidence synthesis")):
        availability = "AVAILABLE" if "tong-hop-bang-chung" in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("co-van", "tong-hop-bang-chung", "synthesize", availability)

    appraisal_routes = (
        (("rob 2", "rob2", "nguy cơ sai lệch rct"), "rob2"),
        (("grade certainty", "độ chắc chắn grade", "đánh giá grade"), "grade"),
        (("cerqual",), "cerqual"),
    )
    for phrases, mode in appraisal_routes:
        if any(phrase in text for phrase in phrases):
            skill = "danh-gia-chat-luong-bang-chung"
            availability = "AVAILABLE" if skill in active_skills else "NOT_IN_ACTIVE_SLICE"
            return RoutingDecision("co-van", skill, mode, availability)

    if any(phrase in text for phrase in ("checklist consort", "checklist strobe", "checklist prisma")):
        skill = "kiem-chung-ban-thao"
        availability = "AVAILABLE" if skill in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("co-van", skill, "reporting-guideline", availability)

    if any(phrase in text for phrase in ("mạng trích dẫn", "citation network", "citation graph")):
        availability = "AVAILABLE" if "tim-y-van" in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("co-van", "tim-y-van", "citation-network", availability)

    if any(phrase in text for phrase in ("tìm y văn", "literature search", "search pubmed")):
        availability = "AVAILABLE" if "tim-y-van" in active_skills else "NOT_IN_ACTIVE_SLICE"
        return RoutingDecision("co-van", "tim-y-van", "database-search", availability)

    clinical_advice = ("uống thuốc", "điều trị cho tôi", "chẩn đoán cho tôi", "what medicine", "diagnose me")
    research_terms = ("nghiên cứu", "luận văn", "đề cương", "research", "thesis", "protocol")
    if any(phrase in text for phrase in clinical_advice) and not any(term in text for term in research_terms):
        return RoutingDecision("co-van", "NONE", "out-of-scope-clinical-advice", "OUT_OF_SCOPE")
    return RoutingDecision("co-van", "co-van", "classify", "AVAILABLE")
