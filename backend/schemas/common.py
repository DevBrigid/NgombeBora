from datetime import date
from decimal import Decimal, InvalidOperation


def parse_date(value, field="date", required=True):
    if not value:
        if required:
            raise ValueError(f"{field} is required")
        return None
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field} must use YYYY-MM-DD")


def parse_decimal(value, field, required=True):
    if value in (None, "") and not required:
        return None
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{field} must be a valid number")
    if not result.is_finite() or result < 0:
        raise ValueError(f"{field} must be zero or greater")
    return result


def require_name(value):
    name = str(value or "").strip()
    if not name:
        raise ValueError("name is required")
    return name
