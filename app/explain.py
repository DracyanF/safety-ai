def explain_patrol_recommendation(rec: dict) -> str:
    """
    Generate a human-readable explanation for a patrol recommendation.
    """
    area = rec["area"]
    score = rec["risk_score"]
    priority = rec["priority"]
    trend = rec["trend"]
    units = rec["patrol_units"]
    time_window = rec["recommended_time"]
    incidents = rec["supporting_incidents"]

    incident_count = len(incidents)

    # Count severity levels
    severity_counts = {}
    for inc in incidents:
        sev = inc.get("severity", "low")
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    severity_text = ", ".join(
        f"{count} {sev}-severity"
        for sev, count in severity_counts.items()
    )

    explanation = (
        f"{area} has been classified as a {priority.lower()} priority area "
        f"with a risk score of {score}. "
        f"This assessment is based on {incident_count} reported incidents "
        f"in the selected time window, including {severity_text} crimes. "
    )

    if trend == "rising":
        explanation += (
            "Crime frequency in this area is increasing compared to the previous period, "
            "which elevates the risk level. "
        )
    elif trend == "declining":
        explanation += (
            "Crime frequency in this area is decreasing compared to the previous period, "
            "which slightly reduces the overall risk. "
        )
    else:
        explanation += (
            "Crime frequency in this area has remained stable over time. "
        )

    explanation += (
        f"Based on this analysis, the system recommends deploying {units} patrol unit(s) "
        f"during {time_window} to mitigate potential risks."
    )

    return explanation
