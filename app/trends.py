from collections import defaultdict
from qdrant_client.models import Filter, FieldCondition, Range
from app.qdrant_client import client, COLLECTION_NAME
from app.utils import unix_days_ago, unix_days_range

def detect_trends(
    window_days: int = 15
):
    """
    Detect crime trends by comparing recent vs previous windows.
    """
    # Time ranges
    recent_gte = unix_days_ago(window_days)
    prev_gte, prev_lt = unix_days_range(window_days, window_days * 2)

    # Fetch recent incidents
    recent_resp = client.query_points(
        collection_name=COLLECTION_NAME,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="timestamp",
                    range=Range(gte=recent_gte)
                )
            ]
        ),
        limit=1000,
        with_payload=True
    )

    # Fetch previous incidents
    prev_resp = client.query_points(
        collection_name=COLLECTION_NAME,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="timestamp",
                    range=Range(gte=prev_gte, lt=prev_lt)
                )
            ]
        ),
        limit=1000,
        with_payload=True
    )

    # Aggregate counts per area
    recent_counts = defaultdict(int)
    prev_counts = defaultdict(int)

    for p in recent_resp.points:
        recent_counts[p.payload["area"]] += 1

    for p in prev_resp.points:
        prev_counts[p.payload["area"]] += 1

    # Compute trends
    trends = []

    all_areas = set(recent_counts) | set(prev_counts)

    for area in all_areas:
        r = recent_counts.get(area, 0)
        p = prev_counts.get(area, 0)

        if r > p:
            trend = "rising"
        elif r < p:
            trend = "declining"
        else:
            trend = "stable"

        trends.append({
            "area": area,
            "recent_count": r,
            "previous_count": p,
            "trend": trend,
            "delta": r - p
        })

    return trends
