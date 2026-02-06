def route_claim(claim_data: dict, missing_fields: list, inconsistencies: list):
    """
    Apply routing rules and return (route, reasoning, confidence).
    """

    description = (claim_data.get("description") or "").lower()
    claim_type = (claim_data.get("claim_type") or "").lower()
    damage = claim_data.get("estimated_damage")

    confidence = 0.95  # default high confidence

    # -------------------------
    # Rule 1: Missing Fields
    # -------------------------
    if missing_fields:
        confidence = 0.60
        return (
            "Manual Review",
            f"Mandatory fields missing: {', '.join(missing_fields)}.",
            confidence
        )

    # -------------------------
    # Rule 2: Inconsistencies
    # -------------------------
    if inconsistencies:
        confidence = 0.65
        return (
            "Manual Review",
            f"Data inconsistencies detected: {', '.join(inconsistencies)}.",
            confidence
        )

    # -------------------------
    # Rule 3: Fraud Keywords
    # -------------------------
    fraud_keywords = ["fraud", "staged", "inconsistent"]

    for word in fraud_keywords:
        if word in description:
            confidence = 0.85
            return (
                "Investigation Flag",
                f"Description contains suspicious keyword: '{word}'.",
                confidence
            )

    # -------------------------
    # Rule 4: Injury Claims
    # -------------------------
    if claim_type == "injury":
        confidence = 0.90
        return (
            "Specialist Queue",
            "Claim type is injury and requires specialist handling.",
            confidence
        )

    # -------------------------
    # Rule 5: Fast Track
    # -------------------------
    if damage:
        try:
            damage_value = float(damage)
            if damage_value < 25000:
                confidence = 0.92
                return (
                    "Fast-track",
                    f"Estimated damage {damage_value} is below 25,000 threshold.",
                    confidence
                )
        except ValueError:
            pass

    # -------------------------
    # Default
    # -------------------------
    confidence = 0.75
    return (
        "Manual Review",
        "Claim does not meet fast-track criteria.",
        confidence
    )
