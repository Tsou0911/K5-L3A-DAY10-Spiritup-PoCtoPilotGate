"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def _effective_policy(ctx):
    policies = ctx.tools.lookup_policies()
    return H.effective_policy(policies, ctx.as_of) or next(
        (p for p in policies if p.get("index_active")), None
    )


def _valid_approval(ctx, approval_id: str | None, order_id: str, ticket_id: str, amount_vnd: int) -> bool:
    if not approval_id:
        return False
    rows = ctx.tools.lookup_approvals(approval_id=approval_id)
    if not rows:
        return False
    a = rows[0]
    return (
        a.get("status") == "valid"
        and (a.get("expires_at") or "") >= ctx.as_of
        and a.get("order_id") == order_id
        and a.get("ticket_id") == ticket_id
        and int(a.get("max_vnd") or 0) >= amount_vnd
    )


def pre_guard(ctx):
    """Cổng 1: ghim phiên bản chính sách đang hiệu lực theo ngày as_of (không lệ thuộc cờ index_active)."""
    pol = _effective_policy(ctx)
    if pol:
        ctx.log("pin_effective_policy", policy_id=pol["policy_id"])
        return Verdict.allow(policy_id=pol["policy_id"])
    return Verdict.allow()


def _gate_issue_refund(ctx, action):
    """Cổng 2: chặn ghi đúp sổ cái, đối chiếu quyền lợi DB & bên chịu phí, kiểm tra phê duyệt & trần ngày."""
    order_id = action.get("order_id")
    ticket_id = action.get("ticket_id")
    if ctx.tools.ledger_rows(ticket_id=ticket_id) or ctx.tools.ledger_rows(order_id=order_id):
        ctx.log("block_duplicate_refund", ticket_id=ticket_id, order_id=order_id)
        return Verdict.deny("đã có khoản hoàn cho đơn hoặc ticket này trong sổ cái")

    order = ctx.tools.lookup_order(order_id)
    pol = _effective_policy(ctx)
    if not order or not pol:
        return Verdict.escalate("thiếu dữ liệu đơn hàng hoặc chính sách hiệu lực")

    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    db_delay = H.db_delay_days(parcel, ctx.as_of)
    cause = parcel.get("delay_cause") or ("CARRIER" if db_delay > 0 else None)
    entitlement = H.entitlement_vnd(pol, order, db_delay, cause)

    if entitlement <= 0:
        ctx.log("block_refund_no_entitlement", db_delay=db_delay, cause=cause)
        return Verdict.deny("không đủ điều kiện hoàn tiền theo tracking DB và chính sách hiệu lực")

    proposed_amount = int(action.get("amount_vnd") or 0)
    proposed_payer = action.get("payer", "LOGIX")
    final_amount = min(proposed_amount, entitlement) if proposed_amount > 0 else entitlement
    final_payer = "LOGIX"

    has_valid_approval = _valid_approval(
        ctx, action.get("approval_id"), order_id, ticket_id, final_amount
    )
    if final_amount > pol["auto_limit_vnd"] and not has_valid_approval:
        ctx.log("escalate_invalid_or_missing_approval", amount_vnd=final_amount)
        return Verdict.escalate("vượt hạn mức tự động, thiếu phê duyệt hợp lệ")

    limits = ctx.tools.ops_limits()
    cust_cap = limits.get("max_auto_refund_per_customer_per_day_vnd")
    if cust_cap is not None and not has_valid_approval:
        cust_today = sum(
            r["amount_vnd"]
            for r in ctx.tools.ledger_rows(customer_id=order["customer_id"])
            if not r.get("approval_id")
        )
        if cust_today + final_amount > cust_cap:
            ctx.log("escalate_customer_daily_cap", customer_id=order["customer_id"], total=cust_today + final_amount)
            return Verdict.escalate("vượt trần hoàn tự động trong ngày cho một khách, chuyển người duyệt")

    max_strikes = limits.get("max_auto_strikes_per_carrier_per_day")
    if max_strikes is not None and H.carrier_at_fault(pol, parcel, db_delay) and not has_valid_approval:
        first_carrier = order["parcels"][0]["carrier_id"]
        strikes = len(ctx.tools.fault_rows(carrier_id=first_carrier))
        if strikes >= max_strikes:
            ctx.log("escalate_carrier_strike_limit", carrier_id=first_carrier, strikes=strikes)
            return Verdict.escalate("đạt trần lỗi tự động trong ngày của hãng, chuyển người duyệt trước khi ghi")

    if final_amount != proposed_amount or proposed_payer != final_payer:
        ctx.log("clamp_refund_to_db", proposed=proposed_amount, final=final_amount, payer=proposed_payer)
        return Verdict.modify(
            "điều chỉnh số tiền và bên chịu phí theo quyền lợi DB",
            amount_vnd=final_amount,
            payer=final_payer,
        )
    return Verdict.allow()


def _gate_carrier_fault(ctx, action):
    """Cổng 3a: chặn ghi lỗi oan / ghi lặp cho hãng, đối chiếu tracking DB và nguyên nhân ghi nhận."""
    order_id = action.get("order_id")
    parcel_id = action.get("parcel_id")
    if ctx.tools.fault_rows(order_id=order_id, parcel_id=parcel_id):
        ctx.log("block_duplicate_fault", order_id=order_id, parcel_id=parcel_id)
        return Verdict.deny("kiện hàng này đã được ghi lỗi hãng trước đó")

    order = ctx.tools.lookup_order(order_id)
    pol = _effective_policy(ctx)
    if not order or not pol:
        return Verdict.deny("thiếu dữ liệu đơn hàng hoặc chính sách hiệu lực")

    parcel = next((p for p in order["parcels"] if p["parcel_id"] == parcel_id), None)
    if parcel is None:
        return Verdict.deny("không tìm thấy kiện hàng trong tracking DB")

    db_delay = H.db_delay_days(parcel, ctx.as_of)
    if not H.carrier_at_fault(pol, parcel, db_delay):
        ctx.log("block_wrongful_fault", db_delay=db_delay, cause=parcel.get("delay_cause"))
        return Verdict.deny("không đủ căn cứ ghi lỗi hãng theo tracking DB và chính sách hiệu lực")

    if action.get("delay_days") != db_delay or action.get("carrier_id") != parcel.get("carrier_id"):
        ctx.log("fix_fault_to_db", delay_days=db_delay, carrier_id=parcel.get("carrier_id"))
        return Verdict.modify(
            "đồng bộ số ngày trễ và mã hãng theo tracking DB",
            delay_days=db_delay,
            carrier_id=parcel["carrier_id"],
        )
    return Verdict.allow()


def _gate_notify_carrier(ctx, action):
    """Cổng 3b: đồng bộ số ngày trễ gửi cho hãng với tracking DB."""
    payload = dict(action.get("payload") or {})
    order = ctx.tools.lookup_order(payload.get("order_id"))
    if not order:
        return Verdict.allow()
    parcel_id = payload.get("parcel_id")
    parcel = next((p for p in order["parcels"] if p["parcel_id"] == parcel_id), None) or H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    db_delay = H.db_delay_days(parcel, ctx.as_of)
    if "delay_days" in payload and payload["delay_days"] != db_delay:
        payload["delay_days"] = db_delay
        ctx.log("fix_notify_delay_to_db", delay_days=db_delay)
        return Verdict.modify("đồng bộ delay_days thông báo hãng theo tracking DB", payload=payload)
    return Verdict.allow()


def write_gate(ctx, action):
    tool = action.get("tool")
    if tool == "issue_refund":
        return _gate_issue_refund(ctx, action)
    if tool == "file_carrier_fault":
        return _gate_carrier_fault(ctx, action)
    if tool == "notify_carrier":
        return _gate_notify_carrier(ctx, action)
    return Verdict.allow()
