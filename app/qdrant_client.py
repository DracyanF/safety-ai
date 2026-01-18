from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(url="http://localhost:6333")

COLLECTION_NAME = "crime_incidents"

def create_collection():
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=1536,
            distance=Distance.COSINE
        )
    )
