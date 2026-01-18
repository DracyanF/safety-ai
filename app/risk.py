from collections import defaultdict
from qdrant_client.models import Filter, FieldCondition, Range
from app.qdrant_client import client, COLLECTION_NAME
from app.utils import unix_days_ago
from app.trends import detect_trends

SEVERITY_MAP = {
    "low": 1,
    "medium": 2,
    "high": 3
}

TREND_BONUS = {
    "rising": 10,
    "stable": 0,
    "declining": -5
}

def compute_risk_scores(
    days: int = 30,
    frequency_weight: int = 5,
    severity_weight: int = 7
):
    """
    Compute risk scores per area based on frequency, severity, and trend.
    """
    # 1️⃣ Fetch recent incidents
    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="timestamp",
                    range=Range(gte=unix_days_ago(days))
                )
            ]
        ),
        limit=1000,
        with_payload=True
    )

    points = response.points

    # 2️⃣ Aggregate per area
    area_stats = defaultdict(lambda: {
        "count": 0,
        "severity_sum": 0,
        "incidents": []
    })

    for p in points:
        payload = p.payload
        area = payload["area"]
        severity = payload.get("severity", "low")

        area_stats[area]["count"] += 1
        area_stats[area]["severity_sum"] += SEVERITY_MAP.get(severity, 1)
        area_stats[area]["incidents"].append(payload)

    # 3️⃣ Get trend info
    trends = detect_trends(window_days=days // 2)
    trend_map = {t["area"]: t["trend"] for t in trends}

    # 4️⃣ Compute risk scores
    risk_results = []

    for area, stats in area_stats.items():
        count = stats["count"]
        avg_severity = stats["severity_sum"] / max(count, 1)
        trend = trend_map.get(area, "stable")

        risk_score = (
            (count * frequency_weight)
            + (avg_severity * severity_weight)
            + TREND_BONUS.get(trend, 0)
        )

        risk_results.append({
            "area": area,
            "risk_score": round(risk_score, 2),
            "crime_count": count,
            "avg_severity": round(avg_severity, 2),
            "trend": trend,
            "incidents": stats["incidents"]
        })

    # Sort by risk descending
    risk_results.sort(key=lambda x: x["risk_score"], reverse=True)

    return risk_results
