import json
from uuid import uuid4
from qdrant_client.models import PointStruct
from app.embeddings import get_text_embedding
from app.qdrant_client import client, COLLECTION_NAME

def ingest_crime_reports(path="sample_data/crime_reports.json"):
    with open(path) as f:
        data = json.load(f)

    points = []

    for item in data:
        vector = get_text_embedding(item["description"])

        payload = {
            "incident_id": item["incident_id"],
            "description": item["description"],
            "crime_type": item["crime_type"],
            "area": item["area"],
            "location": {
                "lat": float(item["location"]["lat"]),
                "lon": float(item["location"]["lon"])
            },
            "timestamp": item["timestamp"],
            "severity": item["severity"]
        }

        points.append(
            PointStruct(
                id=str(uuid4()),
                vector=vector,
                payload=payload
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"✅ Ingested {len(points)} crime incidents with geo-location")
