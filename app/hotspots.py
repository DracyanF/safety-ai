from collections import defaultdict
from qdrant_client.models import Filter, FieldCondition, Range
from app.qdrant_client import client, COLLECTION_NAME
from app.utils import unix_days_ago

def detect_hotspots(
    days: int = 30,
    threshold: int = 3
):
    """
    Detect crime hotspots by aggregating incidents by area.
    """
    # 1️⃣ Fetch recent incidents
    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="timestamp",
                    range=Range(
                        gte=unix_days_ago(days)
                    )
                )
            ]
        ),
        limit=1000,  # enough for demo
        with_payload=True
    )

    points = response.points

    # 2️⃣ Aggregate by area
    area_counts = defaultdict(list)

    for point in points:
        payload = point.payload
        area = payload["area"]
        area_counts[area].append(payload)

    # 3️⃣ Identify hotspots
    hotspots = []

    for area, incidents in area_counts.items():
        if len(incidents) >= threshold:
            hotspots.append({
                "area": area,
                "incident_count": len(incidents),
                "incidents": incidents
            })

    return hotspots
