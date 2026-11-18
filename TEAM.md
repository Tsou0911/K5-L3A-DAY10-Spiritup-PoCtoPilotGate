# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): Spiritup
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-Spiritup-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S5

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Vũ Lê Đức | 2A202603683 | Kỹ sư cổng | |
|   2 | Lê Hữu Toàn | 2A202603660 | Vận hành và pháp lý | x |
|   3 | Nguyễn Đức Trọng | 2A202603644 | Sản phẩm và kinh doanh | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## VuLeDuc-2A202603683

### Phần việc phụ trách

Vai **Kỹ sư cổng** (`Vũ Lê Đức` – MSSV `2A202603683`). Phụ trách: câu 1.3 (Phiếu A mục A2), câu 2.1–2.2, 2.6–2.8 và đóng góp nhánh Kỹ thuật ở câu 2.5 (Phiếu B mục B0, B1, B2, B6, B7.1–B7.3), câu 3.0–3.1 (trace), 3.4–3.6 (Phiếu C mục C0, C1, C2, C6, C7, C8, phần bằng chứng kỹ thuật ở C12), cùng 2 file code `lab10/guards.py` và `lab10/monitors.py`.

### Đóng góp cụ thể

- **Vòng 1 (CP3):** Kiểm tra và xử lý lỗi lệch CRLF/LF khi verify hash bản tiêu chí đã ký (`6d9fc42f`); chạy đánh giá mốc `base`, trace và lập bảng soát 2 lỗi chìm cho `T-002@55`; viết 3 cổng phòng ngừa trong `lab10/guards.py` (`pre_guard` ghim chính sách hiệu lực `H.effective_policy`, `_gate_issue_refund` đối chiếu quyền lợi DB + chặn `directive` + chặn ghi đúp + kiểm tra phê duyệt & trần `ops_limits` 300k/khách và 2 lỗi/hãng, `_gate_carrier_fault` & `_gate_notify_carrier` đồng bộ tracking DB); viết 2 behavioral test `--adhoc` (`O-1002`, `O-1001`); chạy kiểm thử vòng 1 và chốt `lab10.checkpoint` (`fd9e7ea0`). Có dùng trợ lý AI hỗ trợ rà code, kiểm tra trace và rà soát câu chữ trong phiếu.
- **Vòng 2 (`S5`, CP4–CP5):** Phân tích trace `S5-02@11`, `S5-21@11`, `S5-50@11`, `S5-51@11`, `S5-70@11`; cập nhật `_gate_issue_refund` trong `lab10/guards.py` khấu trừ tổng đã hoàn theo `ledger_rows(order_id)` để xử lý đúng đơn hoàn một phần (`S5-21`: 12.000đ) mà vẫn chặn hoàn trùng; thêm 2 chỉ số theo dõi mới vào `lab10/monitors.py` (`max_warehouse_cost_per_ticket_vnd` và `duplicate_or_llm_budget_guard_rate`) đều sáng đèn khi có sự cố `S5`.

### Bằng chứng

- Commit: `aac8bd5` (chốt cổng vòng 1), `ed25b35` / `c7b4516` (hoàn thiện CP4 phần Kỹ sư cổng).
- Mã lần chạy:
  - Bộ nền `base`: `R-base-before-20261118-212936-bde05c` (`pass_rate 0.9909`), `R-base-prepared-20261118-224518-a0af40` (`1.0`), `R-base-after-20261118-230406-fa276c` (`1.0`, `unittest` 13/13 OK).
  - Thẻ `S5`: `R-S5-prepared-20261118-230425-fa276c` (`0.9667`), `R-S5-after-20261118-230403-fa276c` (`1.0`, `150/150` đạt, `under_refund_vnd = 0`), `R-S5-grade-20261118-232040-fa276c` (`2 criteria ✅`, `5 regression ✅`, `6 monitor ✅`, `ticket còn hỏng: không`).
- Dòng trong phiếu: Phiếu A (`A2`), Phiếu B (`B0–B2`, `B6`, `B7.1–B7.3`), Phiếu C (`C0–C2`, `C6–C8`, `C12` phần bằng chứng kỹ thuật).

### Exit ticket

- **Điều học được:** Cổng cấp hệ thống nằm ngoài model (đối chiếu sổ cái + tracking DB) mới ngăn được lỗi chìm và lệch đối soát tài chính; đồng thời phải tách giữa "chặn hoàn trùng" và "khấu trừ phần đã hoàn" (`S5-21`), và phải tách chi phí theo từng phân khúc kho (`HCM-B2B`) thay vì nhìn trung bình toàn hệ thống.
- **Điều còn chưa chắc:** Với `MockLLM` và mô phỏng ca làm việc hiện tại, chưa đo được biến thiên ngôn ngữ thực tế, độ trễ đồng bộ sổ cái thời gian thực giữa các kênh CSKH và nhịp dồn hàng chờ giờ cao điểm khi chạy thật.

## LeHuuToan-2A202603660

### Phần việc phụ trách

Vai **Vận hành và pháp lý** – **Trưởng nhóm** (`Lê Hữu Toàn` – MSSV `2A202603660`). Phụ trách: khởi tạo repo và thiết lập `TEAM.md` (CP1); câu 1.2, 1.4 (Phiếu A mục A1–A2) và ký đẩy tiêu chí (CP2); câu 2.4, 2.10 gồm HAZOP vòng 1, checklist 9 nhóm việc, cổng `operations` & `legal` trong `config/operating_gates.json`, Runbook 1–3 và giờ cao điểm (Phiếu B mục B4–B5, B7.5–B7.6); mở rộng dữ liệu sự cố `S5` tại mục C3 (`C3.5`), C4 (HAZOP thẻ), C5 (câu 3.3), C9–C11 (Fault tree sau sửa, Risk register, cập nhật checklist, Runbook 4–5) và tổng hợp `submission/submission.json` (CP4–CP5).

### Đóng góp cụ thể

- **CP1–CP2:** Lập danh sách thành viên, phân vai và ghi nhận thẻ `S5`; viết mục tiêu cho chị Oanh, chị Hạnh (`A1`), telemetry production (`A2`), và thực hiện ký + đẩy commit `Sign acceptance criteria` (`4f7a8ed`).
- **CP3:** Phân tích HAZOP vòng 1 trên `file_carrier_fault` (`B4`), lập checklist 9 nhóm việc có PIC (`B5`), cấu hình cổng `operations` (`NV-TUNG`, `NV-HANH`, 1 người trực, 6 ca/giờ, SLA 60 phút, 4 điều kiện dừng, `#ops-logix-refund-alerts`) và `legal` (chặn `customer_note`, bắt buộc `delay_cause`), hoàn thiện Runbook 1–3 và kịch bản giờ cao điểm (`B7.5–B7.6`).
- **CP4–CP5:** Đối chiếu bản đồ dữ liệu `S5` (`C3.5`), lập HAZOP thẻ trên `issue_refund` (`C4`), nêu giả định môi trường (`C5` câu 3.3), cập nhật Fault tree sau sửa (`C9`), thêm Risk register (`C10`), cập nhật checklist & Runbook 4–5 (`C11`), soạn `Ba dòng bắt buộc` trong `C12` và điền `submission/submission.json`.

### Bằng chứng

- Commit: `4f7a8ed` (Sign acceptance criteria), `ad2235a` (Add S5), `6eb82c5` (Form B), `c7a8be6` / `b121ab8` / `d0009ec` / `b324a2e` (Form C & `submission.json`).
- Mã lần chạy đối chiếu: `R-S5-after-20261118-235344-2fd8ef`, `R-S5-grade-20261118-235351-2fd8ef`.
- Mục phiếu: Phiếu A (`A1`, `A2`), Phiếu B (`B4`, `B5`, `B7.5–B7.6`), Phiếu C (`C3–C5`, `C9–C12`).

### Exit ticket

- **Điều học được:** Cổng kỹ thuật không thay thế được quy trình vận hành và ranh giới pháp lý: muốn kiểm soát chi phí, SLA 60 phút và khiếu nại bên thứ ba thì phải gắn rõ PIC, điều kiện dừng và ngưỡng chuyển tay trong `operating_gates.json` lẫn Runbook.
- **Điều còn chưa chắc:** Tải thực tế theo giờ tại 4 kho bán lẻ vào ngày sale (khi tăng gấp 3) có đủ với 1 người trực hay cần bổ sung người dự phòng thường xuyên hơn.

## NguyenDucTrong-2A202603644

### Phần việc phụ trách

Vai **Sản phẩm và kinh doanh** (`Nguyễn Đức Trọng` – MSSV `2A202603644`). Phụ trách: câu 1.1, 1.6 và `config/acceptance_criteria.json` (Phiếu A mục A1, A4); câu 2.3 (bản đồ dữ liệu & ví dụ drift `REFUND-v4`), đóng góp lăng kính Kinh doanh ở câu 2.5 (B6), câu 2.9 (`business.*` trong `config/operating_gates.json`, B7.4) và chốt quyết định Gate 1 v1 (B8); câu 3.2 (Specification thẻ `S5`, C5), bổ sung dòng Kinh doanh ở C1 & C10, điều chỉnh `business.pilot_scope` loại `HCM-B2B`, và quyết định Gate 1 v2 (`C12`).

### Đóng góp cụ thể

- **CP2:** Xác định mục tiêu cấp hệ thống (`1.1`), viết đủ các câu tiêu chí thành công dạng "Nếu … thì …", ranh giới đầu ra (ngân sách 2.000.000đ/ngày, 300.000đ/khách/ngày, lỗi thứ 3/hãng/ngày), `decision_rule` cho cả 4 quyết định và lịch xem lại `30/11/2026` vào `config/acceptance_criteria.json` và Phiếu A (`A4`).
- **CP3:** Hoàn thiện bản đồ dữ liệu và phân tích concept drift `REFUND-v3` → `REFUND-v4` ngày `01/12/2026` (`B3`); thiết lập các ngưỡng `business` (`daily_refund_cap_vnd: 2000000`, `cost_budget_per_ticket_vnd: 1500`, `roi_min: 0.1`) ở `B7.4` và chọn giữ `all` ở vòng 1 sau khi kiểm chứng thử `10%` bị lỗ phí giữ chỗ (`10.667đ/ticket`, `ROI -0,06`), chốt quyết định v1 `Tiếp tục` (`B8`).
- **CP4–CP5:** Phân tích unit economics theo kho cho thẻ `S5`, chốt Specification câu 3.2 (`C5`), bổ sung phân tích & Risk register kinh doanh (`C1`, `C10`), chỉnh `business.pilot_scope` trong `config/operating_gates.json` loại `HCM-B2B` về làm tay (giữ `["CT", "DN", "HCM", "HN"]`, giúp chi phí `S5` giảm từ `6.491đ` xuống `3.897đ/ticket` và `ROI` tăng từ `0,54` lên `1,57`), và chốt quyết định v2 **`Thu hẹp`** (`C12`).

### Bằng chứng

- Commit: `e6c6a0c` (add 2.3), `84ad545` (add 2.9), và các cập nhật `config/acceptance_criteria.json`, `config/operating_gates.json`, Phiếu A/B/C.
- Mã lần chạy: `R-base-prepared-20261118-224518-a0af40` (v1), `R-S5-after-20261118-235344-2fd8ef` và `R-S5-grade-20261118-235351-2fd8ef` (v2: `3 visible ✅`, `ROI = 1.57`, `coverage = 0.6`).
- Mục phiếu: Phiếu A (`A1`, `A4–A5`), Phiếu B (`B3`, `B6`, `B7.4`, `B8`), Phiếu C (`C1`, `C5` câu 3.2, `C10`, `C12`).

### Exit ticket

- **Điều học được:** Chỉ số trung bình toàn hệ thống có thể che lấp một phân khúc lỗ nặng (`HCM-B2B` tốn `10.382đ > 10.000đ` làm tay); quyết định `Thu hẹp` cắt phân khúc có unit economics âm giúp tổng tiết kiệm và ROI tăng mạnh ngay lập tức.
- **Điều còn chưa chắc:** Khi triển khai thực tế và chuyển sang `REFUND-v4` ngày `01/12/2026` (hạn mức tự động hạ từ `200.000đ` xuống `100.000đ`), tỉ lệ chuyển duyệt ở 4 kho bán lẻ có tăng làm giảm ROI dưới mức `0,1` hay không.
