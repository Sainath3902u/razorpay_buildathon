def calculate_recovery(
    amount_at_risk: float,
    action_result: dict
) -> float:

    if not action_result.get(
        "recovered",
        False
    ):

        return 0.0

    return round(
        float(amount_at_risk),
        2
    )