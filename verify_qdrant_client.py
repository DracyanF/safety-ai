from qdrant_client import QdrantClient
print(f"Has search: {hasattr(QdrantClient, 'search')}")
print(f"Has query_points: {hasattr(QdrantClient, 'query_points')}")
