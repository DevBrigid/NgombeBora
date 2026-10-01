from backend.schemas.common import parse_date, parse_decimal

FINANCE_CATEGORIES = {"milk_sales", "livestock_sales", "feed", "vet", "breeding_cost", "labor", "equipment", "other"}


def validate_finance_entry(data):
    entry_type = data.get("type")
    if entry_type not in ("income", "expenditure"):
        raise ValueError("type must be income or expenditure")
    category = str(data.get("category", "")).strip()
    if category not in FINANCE_CATEGORIES:
        raise ValueError("Choose a valid finance category")
    amount = parse_decimal(data.get("amount"), "amount")
    if amount <= 0:
        raise ValueError("amount must be greater than zero")
    return {"date": parse_date(data.get("date")), "type": entry_type, "category": category,
            "amount": amount, "note": (data.get("note") or "").strip() or None}
