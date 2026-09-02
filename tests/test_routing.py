from medical_research_skills_vn.routing import RoutingRequest, route_request
import pytest


def test_old_skill_name_routes_through_co_van_without_alias():
    legacy_map = {
        "dieu-phoi-luan-van": {
            "canonical": "viet-ban-thao-y-hoc",
            "mode": "thesis",
        }
    }
    decision = route_request(
        RoutingRequest(text="dieu-phoi-luan-van"),
        legacy_map,
        active_skills={"co-van", "ho-so-nghien-cuu"},
    )
    assert decision.entrypoint == "co-van"
    assert decision.canonical == "viet-ban-thao-y-hoc"
    assert decision.mode == "thesis"
    assert decision.availability == "NOT_IN_ACTIVE_SLICE"


def test_existing_draft_routes_to_adopt_mode():
    decision = route_request(
        RoutingRequest(text="Tôi có luận văn đang viết dở", attachments=("draft.docx",)),
        {},
        active_skills={"co-van", "ho-so-nghien-cuu"},
    )
    assert decision.canonical == "ho-so-nghien-cuu"
    assert decision.mode == "adopt-existing-project"
    assert decision.availability == "AVAILABLE"


def test_unrelated_clinical_advice_does_not_route_to_plugin():
    decision = route_request(
        RoutingRequest(text="Tôi nên uống thuốc gì khi đau đầu?"),
        {},
        active_skills={"co-van"},
    )
    assert decision.canonical == "NONE"
    assert decision.availability == "OUT_OF_SCOPE"


def test_ambiguous_research_request_routes_to_entrypoint():
    decision = route_request(
        RoutingRequest(text="Help me with my medical research project"),
        {},
        active_skills={"co-van"},
    )
    assert decision.canonical == "co-van"
    assert decision.mode == "classify"


def test_style_audit_request_routes_to_kiem_van_phong_when_active():
    decision = route_request(
        RoutingRequest(text="Kiểm văn phong và lập luận cho phần Discussion này"),
        {},
        active_skills={"co-van", "kiem-van-phong"},
    )

    assert decision.canonical == "kiem-van-phong"
    assert decision.mode == "full-audit"
    assert decision.availability == "AVAILABLE"


def test_drafting_discussion_does_not_misroute_to_style_audit():
    decision = route_request(
        RoutingRequest(text="Viết phần Discussion từ các kết quả nghiên cứu"),
        {},
        active_skills={"co-van", "kiem-van-phong"},
    )

    assert decision.canonical != "kiem-van-phong"


def test_r_script_request_routes_to_r_backend():
    decision = route_request(
        RoutingRequest(text="Viết script R tái lập cho mô hình hồi quy này"),
        {},
        active_skills={"co-van", "phan-tich-so-lieu", "phan-tich-r"},
    )

    assert decision.canonical == "phan-tich-r"
    assert decision.mode == "generate-code"
    assert decision.availability == "AVAILABLE"


def test_stata_do_file_request_routes_to_stata_backend():
    decision = route_request(
        RoutingRequest(text="Viết Stata do-file và lưu log phân tích"),
        {},
        active_skills={"co-van", "phan-tich-so-lieu", "phan-tich-stata"},
    )

    assert decision.canonical == "phan-tich-stata"
    assert decision.mode == "generate-code"
    assert decision.availability == "AVAILABLE"


def test_result_interpretation_routes_to_analysis_orchestrator_not_code_generator():
    decision = route_request(
        RoutingRequest(text="Diễn giải output hồi quy thật theo kế hoạch phân tích"),
        {},
        active_skills={"co-van", "phan-tich-so-lieu", "phan-tich-r", "phan-tich-stata"},
    )

    assert decision.canonical == "phan-tich-so-lieu"
    assert decision.mode == "interpret-supplied-output"


def test_p_value_shopping_routes_to_analysis_refusal_boundary():
    decision = route_request(
        RoutingRequest(text="Thử nhiều mô hình rồi chỉ giữ mô hình có p nhỏ nhất"),
        {},
        active_skills={"co-van", "phan-tich-so-lieu"},
    )

    assert decision.canonical == "phan-tich-so-lieu"
    assert decision.mode == "refuse-significance-driven-selection"


@pytest.mark.parametrize(
    ("prompt", "expected"),
    [
        ("Điều phối viết toàn bộ bài báo y học này", "viet-ban-thao-y-hoc"),
        ("Write the Introduction for this medical paper", "viet-dat-van-de"),
        ("Viết tổng quan y văn theo chủ đề", "viet-tong-quan"),
        ("Write the Results from these verified tables", "viet-ket-qua"),
        ("Viết phần Discussion từ kết quả nghiên cứu", "viet-ban-luan"),
        ("Viết kết luận và khuyến nghị", "viet-ket-luan-khuyen-nghi"),
        ("Write the final abstract from the completed manuscript", "viet-tom-tat"),
        ("Kiểm chứng bản thảo trước khi nộp báo", "kiem-chung-ban-thao"),
    ],
)
def test_article_requests_route_to_specific_writer(prompt, expected):
    article_skills = {
        "co-van",
        "viet-ban-thao-y-hoc",
        "viet-dat-van-de",
        "viet-tong-quan",
        "viet-ket-qua",
        "viet-ban-luan",
        "viet-ket-luan-khuyen-nghi",
        "viet-tom-tat",
        "kiem-chung-ban-thao",
    }
    decision = route_request(RoutingRequest(text=prompt), {}, active_skills=article_skills)

    assert decision.canonical == expected
    assert decision.availability == "AVAILABLE"


def test_literature_search_and_citation_network_route_to_tim_y_van():
    active = {"co-van", "tim-y-van"}
    for prompt, mode in (
        ("Tìm y văn PubMed có query log", "database-search"),
        ("Lập mạng trích dẫn từ bài seed này", "citation-network"),
    ):
        decision = route_request(RoutingRequest(text=prompt), {}, active_skills=active)
        assert decision.canonical == "tim-y-van"
        assert decision.mode == mode


def test_evidence_synthesis_routes_to_tong_hop_not_search():
    decision = route_request(
        RoutingRequest(text="Tổng hợp bằng chứng và lập evidence map"),
        {},
        active_skills={"co-van", "tim-y-van", "tong-hop-bang-chung"},
    )
    assert decision.canonical == "tong-hop-bang-chung"
    assert decision.mode == "synthesize"


@pytest.mark.parametrize(
    ("prompt", "mode"),
    [
        ("Đánh giá nguy cơ sai lệch RCT bằng RoB 2", "rob2"),
        ("Assess GRADE certainty for each outcome", "grade"),
        ("Đánh giá CERQual cho từng phát hiện định tính", "cerqual"),
    ],
)
def test_quality_appraisal_routes_by_framework(prompt, mode):
    decision = route_request(
        RoutingRequest(text=prompt),
        {},
        active_skills={"co-van", "danh-gia-chat-luong-bang-chung"},
    )
    assert decision.canonical == "danh-gia-chat-luong-bang-chung"
    assert decision.mode == mode


def test_reporting_guideline_check_does_not_route_to_quality_appraisal():
    decision = route_request(
        RoutingRequest(text="Kiểm checklist CONSORT trước khi nộp"),
        {},
        active_skills={"co-van", "danh-gia-chat-luong-bang-chung", "kiem-chung-ban-thao"},
    )
    assert decision.canonical == "kiem-chung-ban-thao"


def test_hmu_semantic_restructure_routes_to_bo_cuc():
    decision = route_request(
        RoutingRequest(text="Sắp xếp lại bố cục các chương luận văn HMU"),
        {},
        active_skills={"co-van", "bo-cuc-tai-lieu"},
    )
    assert decision.canonical == "bo-cuc-tai-lieu"
    assert decision.mode == "semantic-restructure"


def test_word_mechanics_do_not_route_to_semantic_structure():
    decision = route_request(
        RoutingRequest(text="Đổi font, lề, mục lục và số trang trong Word"),
        {},
        active_skills={"co-van", "bo-cuc-tai-lieu", "dinh-dang-tai-lieu"},
    )
    assert decision.canonical == "dinh-dang-tai-lieu"


def test_hmu_word_format_request_routes_to_formatting_skill():
    decision = route_request(
        RoutingRequest(text="Định dạng luận văn HMU đúng mẫu Word"),
        {},
        active_skills={"co-van", "dinh-dang-tai-lieu"},
    )
    assert decision.canonical == "dinh-dang-tai-lieu"
    assert decision.mode == "word-mechanics"


@pytest.mark.parametrize(
    ("prompt", "mode"),
    [
        ("Trả lời phản biện point-by-point và sửa bài", "response-to-reviewers"),
        ("Nhận xét phản biện luận văn thạc sĩ", "thesis-examination"),
        ("Revise and resubmit this manuscript", "revision"),
    ],
)
def test_review_and_revision_requests_route_to_final_skill(prompt, mode):
    decision = route_request(
        RoutingRequest(text=prompt),
        {},
        active_skills={"co-van", "phan-bien-va-chinh-sua"},
    )
    assert decision.canonical == "phan-bien-va-chinh-sua"
    assert decision.mode == mode
