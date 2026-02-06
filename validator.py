def find_missing_fields(claim_data: dict) -> list:
    """
    Check for missing mandatory fields.
    """
    missing = []

    for field in MANDATORY_FIELDS:
        if not claim_data.get(field):
            missing.append(field)

    return missing
def validate_consistency(claim_data: dict) -> list:
    """
    Check for inconsistent or invalid values.
    """
    issues = []

    damage = claim_data.get("estimated_damage")

    if damage:
        try:
            damage_value = float(damage)
            if damage_value <= 0:
                issues.append("estimated_damage_invalid")
        except ValueError:
            issues.append("estimated_damage_not_numeric")

    return issues



MANDATORY_FIELDS = [
    "policy_number",
    "date_of_loss",
    "estimated_damage",
    "claim_type",
    "description"
]
