# MedRS — đặc tả nâng cấp toàn diện đã chốt

## Phạm vi và ràng buộc chung

Một plugin, 28 skill canonical, `/medrs` là cổng vào duy nhất. Không thêm thư mục alias, không nhân bản preflight hoặc rule giữa các writer. R và Stata là ưu tiên; không bắt chạy nhiều runtime khi không cần. CK2/đề tài cơ sở giữ mức cơ bản theo câu hỏi nghiên cứu.

Nội dung canonical trong `skills/`; runtime cần cho Cowork nằm trong skill `scripts/`. Host không hỗ trợ phải báo rõ, không coi là PASS. Không tự gửi dữ liệu sang AI khác. Bản thảo riêng, dữ liệu người bệnh và log riêng không được xuất bản trong repo.

Giữ giới hạn hiện hành: description tối đa 60 từ/skill, gộp 1300 từ; frontmatter gộp 16384 byte. Mục tiêu thực tế là 45 từ/skill. Không tăng giới hạn để né lỗi kiểm định; migration keyword nằm trong guide, không nhét vào description.

## Quyết định tác giả

1. Triển khai toàn bộ rà soát P0–P3.
2. Tác giả xác nhận dữ liệu thật đã cập nhật thì sửa các nhãn mô phỏng lỗi thời ở bộ hiện hành và thông báo để kiểm lại. Nếu dữ liệu còn mô phỏng hoặc chưa có xác nhận thì không chuyển. Lịch sử nguồn gốc không bị xóa. Xác nhận của tác giả và kiểm chứng độc lập là hai trạng thái khác nhau; tín hiệu trùng dữ liệu không tự động chứng minh sai phạm.
3. Thiếu nguồn/kiểm chứng có thể tiếp tục viết nháp có điều kiện và marker, không khẳng định chắc chắn; không được công nhận nguồn/định dạng chính thức chưa xác minh là đạt.
4. Trước dự án luôn có README, `final/`, `history/YYYY-MM-DD/`, log và ghi chú thay đổi hằng ngày. Thay bộ cuối phải có bản lưu khôi phục được; không mất file tác giả sửa thủ công.
5. Phần độc lập chạy gate văn phong đầy đủ. Khi ráp toàn bản: preflight chung cho từng phần, một gate đầy đủ cho toàn bản. Sau sửa: kiểm lại phạm vi bị ảnh hưởng cộng nhất quán toàn bản. Không tải nguyên rule dài bảy lần.
6. Leader hỗ trợ handoff liên-AI và nghiệm thu bản trả về; chỉ chuyển ra ngoài khi có quyền riêng cho điểm đến và dữ liệu.
7. Thứ tự: Word/Zotero → nguồn gốc dữ liệu/thống kê → tìm/trích xuất y văn.
8. Mở rộng theo thứ tự nguồn HMU CKII/BSNT → appraisal quan sát → journal/reporting khác.

## Danh mục nghiệm thu

### P0 — trung thực và điều phối

- P0.1: provenance độc lập với đổi tên file; chuyển mô phỏng sang dữ liệu thật có xác nhận, dữ liệu thay thế và cảnh báo tác giả; lịch sử bất biến.
- P0.2: writer kế thừa prespecified/exploratory, multiplicity, deviation và giới hạn nhân quả; không tạo đóng góp vượt dữ liệu.
- P0.3: một lifecycle gate dùng chung; không nhận PENDING là đã kiểm.
- P0.4: migration map/current router thống nhất; protocol không đi nhầm writer toàn bản.

### P1 — bền vững khi sử dụng

- P1.1: README/final/history/log, tiếp nhận dự án đang dở và quyết định đã chốt.
- P1.2: diff bản tác giả trả lại với bản giao gần nhất; comment ID/anchor, protected regions, handoff liên-AI có consent.
- P1.3: DOCX không mất field, footnote, XML order, caption hay vị trí hình; dùng anchor thay offset dễ lỗi.
- P1.4: style thực tế trên body/cover/table/caption/TOC/bibliography; ưu tiên style và numbering chuẩn; loại theme/direct-format xung đột có kiểm soát, không xóa nhấn mạnh có chủ ý.
- P1.5: Zotero field identity, bibliography cache, Track Changes và khóa truy cập/refresh; typed citation chuyển sang live field có đối chiếu nguồn.
- P1.6: registry provenance phát hiện tín hiệu đổi tên/reorder bằng digest có quy tắc, không lưu giá trị nhạy cảm trong log công khai.
- P1.7: biến liên tục mặc định, phân loại ngưỡng theo loại bằng chứng và protocol; mọi phân tích thử được ghi, không lựa p có lợi.
- P1.8: selection test theo thiết kế/giả định; Fisher, Wilson, OR/PR, dữ liệu ghép cặp, PH, mẫu thiếu, precision p; không biến EPV hay threshold kinh nghiệm thành luật tuyệt đối.
- P1.9: trích xuất đúng outcome-available N/group/time/adjustment, không dùng recruited N thay thế; bảng thứ cấp chỉ dẫn đường về nguồn gốc.
- P1.10: fallback truy cập theo host, query ledger, nguồn Việt Nam phù hợp; không tìm thấy khác không truy cập được.
- P1.11: R/Stata đầu ra theo ngày, log, lỗi macro/program và survival có fixture; chỉ gọi thực thi khi runtime có thật.
- P1.12: mâu thuẫn thiết kế giữa file phải hiện ra; table border theo nguồn/profile thực tế, không áp một mẫu cho mọi thesis/journal.

### P2 — mở rộng có nguồn

- P2.1: HMU CKII/BSNT, đại học, báo cáo cơ sở/bộ, trả lời hội đồng và bảo vệ: phân biệt quy định chính thức với convention; chưa có nguồn trình bày đúng thì `OFFICIAL_RULE_REQUIRED`.
- P2.2: ROBINS-I, ROBINS-E, JBI analytical cross-sectional/prevalence, QUADAS hiện hành và legacy, AMSTAR2. Coverage phải theo tài liệu gốc, phiên bản, quyền sử dụng, từng item thực chất. Phát hiện sơ bộ: JBI analytical có bản sửa 2026; QUADAS-3 được Bristol khuyến nghị. Chưa được coi đã triển khai.
- P2.3: PRISMA-ScR, RECORD, CROSS/CHERRIES, SRQR, SQUIRE2; profile báo VJPM/VJPH và cập nhật profile hiện có. Không dựng checklist từ trí nhớ, không sao chép trái giấy phép.
- P2.4: dự án con kế thừa Passport có phạm vi mục tiêu/biến/quần thể riêng; không đồng nhất mọi N, không nhận đóng góp hai lần.

### P3 — nhất quán phát hành

- Registry trạng thái có ngữ cảnh; NOT_RUN không tự đồng nhất UNPERFORMED; không coi unsupported là skip/pass.
- Bước clarity văn phong không làm biến đổi ý nghĩa; schema/style profile có đường dẫn thật.
- Loại lời hứa future slice lỗi thời, đồng bộ marketplace/README/phiên bản; schema Passport không tự bump theo package nếu không thay hợp đồng.
- README Cowork ngắn, hướng dẫn thực thi đúng phần được đóng gói; repo giữ tài liệu nhà phát triển riêng.
- Nghiệm thu file cuối sau refresh/save/reopen/render; hash thay thì bằng chứng cũ mất hiệu lực.

## Định nghĩa xong

Từng mục có test hành vi hoặc evidence review nguồn/semantic/visual thực tế, không chỉ kiểm từ khóa. Toàn bộ validator và test runner có log. ZIP Cowork được giải nén và chạy riêng không dựa root src/scripts. R/Stata/Word/UNO chưa chạy phải ghi chưa chạy. Nguồn thiếu không được fake pass; còn mục chặn thì báo phạm vi chưa hoàn thành, không tuyên bố full xong.

Giữ bản 3.1.0 làm mốc phục hồi, không cài hai bộ trigger trùng. Sau nghiệm thu mới đồng bộ phiên bản, đóng gói, cập nhật GitHub và cài lại trong phạm vi tác giả đã yêu cầu.
