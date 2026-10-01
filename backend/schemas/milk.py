from backend.schemas.common import parse_date, parse_decimal


def validate_milk_record(data):
    record_date = parse_date(data.get("date"))
    quantity = parse_decimal(data.get("quantity"), "quantity")
    if quantity <= 0:
        raise ValueError("quantity must be greater than zero")
    return {"date": record_date, "quantity": quantity}
