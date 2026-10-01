from backend.schemas.common import parse_date, parse_decimal, require_name


def validate_purchased_cow(data):
    sex = data.get("sex")
    if sex not in ("male", "female"):
        raise ValueError("sex must be male or female")
    return {"name": require_name(data.get("name")), "sex": sex,
            "breed": (data.get("breed") or "").strip() or None,
            "date_of_birth": parse_date(data.get("date_of_birth"), "date_of_birth", False)}


def validate_newborn(data):
    sex = data.get("sex")
    if sex not in ("male", "female"):
        raise ValueError("sex must be male or female")
    if not data.get("mother_id"):
        raise ValueError("Select a mother from the herd")
    sire_id = data.get("sire_id") or None
    sire_external = (data.get("sire_external") or "").strip() or None
    if sire_id and sire_external:
        raise ValueError("Choose an existing sire or an outside bull, not both")
    return {"name": require_name(data.get("name")), "sex": sex,
            "breed": (data.get("breed") or "").strip() or None,
            "mother_id": data.get("mother_id"), "sire_id": sire_id,
            "sire_external": sire_external,
            "date_of_birth": parse_date(data.get("date_of_birth"), "date_of_birth"),
            "birth_weight": parse_decimal(data.get("birth_weight"), "birth_weight", False)}
