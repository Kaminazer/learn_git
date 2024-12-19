from qdrant_client import QdrantClient
from app.config.settings import VECTOR_DB_URL

qdrant_client = QdrantClient(url=VECTOR_DB_URL)

def perform_search(query: str):
    # Виконує пошук у векторній базі
    search_results = qdrant_client.search(
        collection_name="your_collection",
        query_vector=[0.1, 0.2, 0.3],  # Замініть на реальні вектори
        top=5
    )
    return [res['payload']['text'] for res in search_results]
