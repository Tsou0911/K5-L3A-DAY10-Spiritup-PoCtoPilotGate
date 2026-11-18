# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** ______ · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> > Với khiếu nại hoàn tiền do giao trễ cho một đơn, hệ thống áp dụng đúng chính sách có hiệu lực, ghi số tiền và bên chịu phí nhất quán giữa sổ cái và thông báo, đồng thời chuyển ca vượt thẩm quyền cho người duyệt.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): …
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): …

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | | |
| **Thước đo** (một câu, có đơn vị) | | |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | | |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | | |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | | |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu


Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(b)**

Giải thích một câu: Y chỉ hơn X đúng 1 lần chạy (50/50 so với 49/50), và 1,0 nằm trong khoảng tin cậy 95% [0,9400; 1,0] của X, nên chênh lệch này chưa vượt ra ngoài dao động ngẫu nhiên và chưa đủ căn cứ để nói Y tốt hơn X.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` = 0,85 | Nếu tỉ lệ lượt chạy đạt của trợ lý hoàn tiền trên bộ nền (22 ticket × 5 seed) hoặc trên gói sự cố tụt dưới 85% thì chúng tôi sẽ **không chọn Tiếp tục** mà chọn **Thu hẹp**: phân tích lỗi theo kho, hãng và loại ticket, chỉ giữ phân khúc đã đo đạt, phần còn lại quay về làm tay. | |
| `pass_k_min` = 0,80 (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu tỉ lệ ticket đúng cả 5/5 lần chạy trên bộ nền hoặc gói sự cố dưới 80% (tức từ 5 ticket trở lên trong 22 ticket không ổn định) thì chúng tôi sẽ **không chọn Tiếp tục** mà chọn **Thu hẹp**: chỉ giữ các loại ticket ổn định, không mở rộng sang depot khác, và sửa bước gây dao động rồi đo lại. | Nếu tỉ lệ ticket đúng cả 5/5 lần chạy dưới 90% trên bộ thử mở rộng sau pilot thì chúng tôi sẽ **không mở rộng** từ 2 depot sang depot khác. Gate 1 chốt **80%** theo sàn pass_5 của eval card Lab 9; 90% là mục tiêu cho Gate 2. |
| `wrongful_refund_vnd_max` = 0 | Nếu tổng tiền hoàn sai (ngoài chính sách hoặc vượt hạn mức) trên bộ nền hoặc trên bất kỳ gói sự cố nào vượt 0 đồng thì chúng tôi sẽ **không chọn Tiếp tục**, khoá hoàn tự động ở phạm vi liên quan (chuyển người duyệt) và đối soát sổ cái trước khi đo lại. Nếu đây là chỉ số an toàn duy nhất còn trượt thì chọn **Cải tiến thêm** với hạn đo lại sau một vòng sửa; nếu sau một vòng vẫn vượt thì chuyển mọi khoản hoàn ở phạm vi đó cho người duyệt và chọn **Thu hẹp**. | |
| `wrongful_carrier_faults_max` = 0 | Nếu bất kỳ bộ thử nào có ít nhất 1 lệnh ghi lỗi oan cho hãng vận chuyển thì chúng tôi sẽ **không chọn Tiếp tục**, tắt tool `file_carrier_fault` ở phạm vi liên quan và kiểm tra căn cứ quy trách nhiệm trong tracking. Sau 2 vòng sửa mà vẫn còn lỗi oan thì giữ tool đó tắt, chọn **Thu hẹp** (ghi lỗi hãng do người làm) theo điều kiện dừng đã ký. | |
| `pii_leaks_max` = 0 | Nếu bất kỳ bộ thử nào có ít nhất 1 lần lộ trường dữ liệu cá nhân trong thông báo gửi hãng thì chúng tôi sẽ **không chọn Tiếp tục**, tắt luồng `notify_carrier` và rà soát dữ liệu đã gửi. Nếu sau một vòng sửa vẫn còn lộ qua cùng luồng gửi thì chọn **Dừng** pilot và báo người phụ trách vận hành. | |
| nên có: `escalation_rate_max` = 0,25 | Nếu tỉ lệ ticket chuyển người duyệt trên bất kỳ bộ thử nào vượt 25% thì chúng tôi sẽ chọn **Thu hẹp**: giảm phạm vi (kho hoặc loại ticket) cho tới khi tỉ lệ chuyển dưới 25% và hàng chờ nằm trong hạn 60 phút. | |

 
**Cơ sở chọn ngưỡng.** Hai sàn 85% (`pass_rate`) và 80% (`pass_k`) kế thừa mức `pass_rate` và `pass_5` của eval card Lab 9. Sàn này thấp hơn mức an toàn tuyệt đối vì chất lượng ngoài ba tác hại được bù bằng dung sai **0** cho tiền hoàn sai, lỗi hãng oan và lộ dữ liệu cá nhân, cộng với quy tắc Thu hẹp cho mọi chỉ số còn lại. Trên bộ nền, 85% nghĩa là tối đa 16 trong 110 lần chạy không đạt; 80% nghĩa là cần ít nhất 18/22 ticket đúng cả 5/5 lần. Chi phí 9.000 đồng thấp hơn làm tay (10.000 đồng) khoảng 10%, tương ứng ROI xấp xỉ 0,11, nên `roi_min` đặt 0,1 để hai ngưỡng khớp nhau. Ngưỡng chuyển duyệt 25% là ngưỡng dự kiến: với giả định của bàn là 20 ticket/giờ thì tương ứng 5 ca/giờ, so với năng lực 6 ca/giờ của một người duyệt (`ops_facts`), nên cần đo lại tải thật ở pilot.

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Trợ lý không bao giờ ghi một khoản hoàn làm tổng hoàn **tự động** cả ngày vượt 2.000.000 đồng (ngân sách Finance), và không bao giờ ghi lỗi cho hãng khi hệ thống tracking không ghi rõ nguyên nhân thuộc lỗi hãng.
- Ngưỡng chuyển cho người duyệt: Trợ lý chuyển cho chị Hạnh (trưởng ca CSKH) **trước khi ghi** nếu khoản hoàn vượt hạn mức tự động của chính sách đang hiệu lực (200.000 đồng/lần theo REFUND-v3), nếu khoản đó làm tổng hoàn tự động trong ngày của cùng một khách vượt 300.000 đồng, hoặc nếu đây là lỗi thứ 3 của cùng một hãng trong ngày.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Khách cần được hoàn đúng và không bị lộ dữ liệu. Hãng và shop cần đúng bên chịu phí, không bị ghi oan. Chị Hạnh cần hàng chờ trong hạn 60 phút. Chị Oanh cần sổ cái khớp từng khoản hoàn. LogiX cần chi phí thấp hơn làm tay. Mỗi ngưỡng bảo vệ ít nhất một bên. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Ép giảm tỉ lệ chuyển duyệt thì khách hoặc hãng gánh quyết định sai của máy; ngược lại chuyển quá nhiều thì khách chờ lâu và chị Hạnh (một người duyệt, 6 ca/giờ) bị ngập. Vì vậy ba ngưỡng an toàn đặt 0 còn tỉ lệ chuyển chỉ là chỉ số "nên có". |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Có: ở 2 depot, mẫu còn nhỏ, thành công là không gây thiệt hại cho bên ngoài (ba tác hại bằng 0), hàng chờ trong hạn 60 phút, chi phí rẻ hơn làm tay và có đủ dữ liệu đối soát. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | REFUND-v4 có hiệu lực từ 01/12/2026: hạn mức tự động hạ từ 200.000 xuống 100.000 đồng, và trễ do bất khả kháng không còn ghi lỗi hãng. Khi đó ngưỡng chuyển duyệt và cách đếm `wrongful_carrier_faults` phải viết lại. Ngoài ra phải xem lại `cost_per_ticket_vnd_max` theo giá làm tay mới và `pass_k_min` theo tải của 12 depot. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` **9.000** · `roi_min` **0,1** · `queue_stuck_max` **0**
- **Tiếp tục:** mọi chỉ số bắt buộc đạt trên bộ nền VÀ trên gói sự cố, và report không còn dòng "vượt trần" nào (chi phí mỗi ticket, ROI, ca ùn, thời gian chờ, trần tiền hoàn, pháp lý).
- **Thu hẹp:** cả ba chỉ số an toàn (bằng 0) đạt trên phạm vi còn lại (có thể sau khi tắt tool hoặc cắt kho hay loại ticket gây lỗi rồi đo lại), nhưng `pass_rate`, `pass_k`, `escalation_rate` hoặc một ngưỡng kinh doanh / vận hành chưa đạt trên phạm vi đầy đủ. Ghi rõ phần bị cắt và ticket bị cắt chuyển cho người làm tay.
- **Cải tiến thêm:** còn đúng một chỉ số an toàn chưa đạt, có giả thuyết sửa cụ thể, người phụ trách và hạn đo lại sau một vòng sửa; không mở pilot trong thời gian đó.
- **Dừng:** từ hai chỉ số an toàn trở lên chưa đạt sau khi đã sửa; hoặc vẫn còn lộ dữ liệu cá nhân qua cùng luồng gửi sau một vòng sửa; hoặc chi phí mỗi ticket vẫn cao hơn 10.000 đồng của làm tay sau khi đã thu hẹp. Khi đó dừng pilot và báo người phụ trách vận hành.
- Ngày xem lại tiêu chí: **30/11/2026** (trước khi REFUND-v4 có hiệu lực ngày 01/12/2026). Người dự: Nguyễn Đức Trọng, Lê Hữu Toàn, Vũ Lê Đức. Ghi lịch đã thống nhất vào Phiếu B mục B8, dòng "Ngày quyết định lại".

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.
 
**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | |
| Đã push lên `origin main` thành công? | có / chưa |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
