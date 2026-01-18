from app.embeddings import get_text_embedding
from app.qdrant_client import client, COLLECTION_NAME
from app.utils import unix_days_ago


from qdrant_client.models import Filter, FieldCondition, Range, GeoRadius, GeoPoint

def search_similar_crimes(
    query: str,
    lat: float | None = None,
    lon: float | None = None,
    radius_km: float | None = None,
    days: int | None = None,
    limit: int = 5,
):
    query_embedding = get_text_embedding(query)

    must_conditions = []

    if days is not None:
        must_conditions.append(
            FieldCondition(
                key="timestamp",
                range=Range(
                    gte=unix_days_ago(days)
                )
        )
    )


    # 📍 Location filter
    if lat is not None and lon is not None and radius_km is not None:
        must_conditions.append(
            FieldCondition(
                key="location",
                geo_radius=GeoRadius(
                    center=GeoPoint(lat=lat, lon=lon),
                    radius=radius_km * 1000  # km → meters
                )
            )
        )

    query_filter = Filter(must=must_conditions) if must_conditions else None

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        query_filter=query_filter,
        limit=limit,
        with_payload=True
    )

    return list(response.points)
