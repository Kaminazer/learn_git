from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams

# Підключення до Qdrant
client = QdrantClient(host="localhost", port=6333)

# Створення колекції
collection_name = "example_collection"
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=384, distance="Cosine"), 
)

print(f"Collection '{collection_name}' created!")