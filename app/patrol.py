from app.risk import compute_risk_scores

def recommend_patrols(
    days: int = 30
):
    """
    Generate patrol recommendations based on risk scores.
    """
    risk_results = compute_risk_scores(days=days)

    recommendations = []

    for r in risk_results:
        score = r["risk_score"]
        area = r["area"]
        trend = r["trend"]

        if score >= 60:
            units = 3 if trend == "rising" else 2
            priority = "HIGH"
            time_window = "6 PM – 11 PM"
        elif score >= 30:
            units = 1
            priority = "MEDIUM"
            time_window = "7 PM – 10 PM"
        else:
            units = 0
            priority = "LOW"
            time_window = "Random patrols"

        recommendations.append({
            "area": area,
            "risk_score": score,
            "priority": priority,
            "patrol_units": units,
            "recommended_time": time_window,
            "trend": trend,
            "supporting_incidents": r["incidents"]
        })

    return recommendations
