from qdrant_client import QdrantClient, models
from config.settings import VECTOR_DB_URI
import logging
from typing import List, Dict, Any

class QdrantDB:
    def __init__(self, collection_name="default_collection"):
        self.collection_name = collection_name
        self.dim = 1536  # Dimension for embeddings, adjust as needed
        self.logger = logging.getLogger(__name__)

        # Parse URI
        self.url = VECTOR_DB_URI or "http://localhost:6333"
        self.client = QdrantClient(url=self.url)

    def connect(self) -> bool:
        self.logger.info("Connected to Qdrant")
        return True

    def init_collection(self):
        try:
            self.logger.info(f"Initializing collection: {self.collection_name}")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=self.dim, distance=models.Distance.COSINE),
            )
            self.logger.info(f"Collection {self.collection_name} initialized successfully")
        except Exception as e:
            if "already exists" in str(e).lower():
                self.logger.info(f"Collection {self.collection_name} already exists")
            else:
                self.logger.error(f"Failed to initialize collection: {str(e)}")
                raise

    def insert(self, vectors: List[List[float]], metadata: List[Dict[str, Any]]) -> bool:
        try:
            self.logger.info(f"Inserting into collection: {self.collection_name}")
            points = [
                models.PointStruct(id=i, vector=vector, payload=meta)
                for i, (vector, meta) in enumerate(zip(vectors, metadata))
            ]
            self.client.upsert(collection_name=self.collection_name, points=points)
            self.logger.info(f"Successfully inserted {len(vectors)} vectors")
            return True
        except Exception as e:
            self.logger.error(f"Insert failed: {str(e)}")
            return False
