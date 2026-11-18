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

## HoVaTen-MSSV

### Phần việc phụ trách

Vai trong bàn; câu nào của đề, mục nào của phiếu A/B/C, file nào (`lab10/guards.py`, `config/operating_gates.json`, …).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.
