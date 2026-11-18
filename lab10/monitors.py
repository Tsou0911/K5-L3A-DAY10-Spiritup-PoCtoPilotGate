"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def _trial_review_cost_vnd(trial):
    kind = trial.get("review_kind")
    if not kind:
        return 0
    if kind == "escalated":
        return 10000
    has_note = any(e.get("type") == "decision_note" for e in trial.get("events", []))
    return 4000 if has_note else 10000


def max_warehouse_cost_per_ticket_vnd(trials):
    """Chi phí mỗi ticket lớn nhất theo từng kho đã biết (tiền máy + công người duyệt/kiểm lại)."""
    by_wh = {}
    for t in trials:
        wh = t.get("warehouse")
        if not wh:
            continue
        cost = (t.get("cost_vnd") or 0) + _trial_review_cost_vnd(t)
        by_wh.setdefault(wh, []).append(cost)
    if not by_wh:
        return 0.0
    return max(sum(cs) / len(cs) for cs in by_wh.values())


def duplicate_or_llm_budget_guard_rate(trials):
    """Tỉ lệ lần chạy chạm cổng chặn hoàn lặp hoặc cổng trần ngân sách LLM mỗi ticket."""
    hits = 0
    for t in trials:
        evs = t.get("events", [])
        hit = any(
            (e.get("type") == "guard" and e.get("kind") == "block_duplicate_refund")
            or (e.get("type") == "business_gate" and e.get("gate") == "cost_budget_per_ticket_vnd")
            for e in evs
        )
        hits += int(hit)
    return hits / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "max_warehouse_cost_per_ticket_vnd": max_warehouse_cost_per_ticket_vnd,
    "duplicate_or_llm_budget_guard_rate": duplicate_or_llm_budget_guard_rate,
}
STARTER_MONITORS = ("escalation_rate",)
