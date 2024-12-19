from pymilvus import connections, Collection, utility
from pymilvus import CollectionSchema, FieldSchema, DataType
import numpy as np
from .base import VectorDBBase
import logging
from typing import List, Dict, Any
from config.settings import VECTOR_DB_URI

class MilvusDB(VectorDBBase):
    def __init__(self, collection_name="skynet_test"):
        self.collection_name = collection_name
        self.dim = 1536  # Розмірність для embeddings з OpenAI
        self.logger = logging.getLogger(__name__)
        self.collection = None
        
        # Парсинг URI
        self.host = "localhost"
        self.port = "19530"
        if VECTOR_DB_URI:
            try:
                from urllib.parse import urlparse
                parsed = urlparse(VECTOR_DB_URI)
                self.host = parsed.hostname or "localhost"
                self.port = str(parsed.port) if parsed.port else "19530"
            except Exception as e:
                self.logger.error(f"Failed to parse VECTOR_DB_URI: {e}")

    async def connect(self) -> bool:
        try:
            # Спробуємо підключитися, якщо з'єднання вже існує - перепідключимося
            try:
                connections.disconnect("default")
            except:
                pass
            
            connections.connect(
                alias="default",
                host=self.host,
                port=self.port
            )
            
            # Перевіряємо підключення
            if utility.has_collection(self.collection_name):
                self.collection = Collection(self.collection_name)
                self.collection.load()
                self.logger.info(f"Successfully connected to Milvus and loaded collection {self.collection_name}")
            else:
                self.logger.warning(f"Collection {self.collection_name} does not exist")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to connect to Milvus: {str(e)}")
            return False

    async def init_collection(self):
        try:
            if not connections.has_connection("default"):
                if not await self.connect():
                    raise ConnectionError("Failed to connect to Milvus")

            # Перевіряємо чи існує колекція
            if utility.has_collection(self.collection_name):
                self.collection = Collection(self.collection_name)
                self.collection.load()
                self.logger.info(f"Using existing collection: {self.collection_name}")
                return

            # Якщо колекції немає - створюємо нову
            fields = [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=self.dim),
                FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="metadata", dtype=DataType.VARCHAR, max_length=65535)
            ]
            
            schema = CollectionSchema(fields=fields, description="Document embeddings collection")
            self.collection = Collection(self.collection_name, schema)
            
            # Створення індексу
            index_params = {
                "metric_type": "COSINE",
                "index_type": "IVF_FLAT",
                "params": {"nlist": 1024}
            }
            self.collection.create_index(field_name="vector", index_params=index_params)
            self.collection.load()
            self.logger.info(f"Created new collection and index: {self.collection_name}")
        
        except Exception as e:
            self.logger.error(f"Failed to initialize collection: {str(e)}")
            raise

    async def search(self, vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        try:
            if not self.collection or not connections.has_connection("default"):
                if not await self.connect():
                    return []

            search_params = {
                "metric_type": "COSINE",
                "params": {"nprobe": 10}
            }
            
            results = self.collection.search(
                data=[vector],
                anns_field="vector",
                param=search_params,
                limit=limit,
                output_fields=["text", "metadata"]
            )

            hits = []
            for hit in results[0]:
                hits.append({
                    "score": hit.score,
                    "text": hit.entity.get("text"),
                    "metadata": hit.entity.get("metadata")
                })
            return hits

        except Exception as e:
            self.logger.error(f"Search failed: {str(e)}")
            return []

    async def insert(self, vectors: List[List[float]], metadata: List[Dict[str, Any]]) -> bool:
        try:
            if not self.collection or not connections.has_connection("default"):
                if not await self.connect():
                    return False

            # Підготовка даних для вставки
            texts = [m.get("text", "") for m in metadata]
            metadata_strings = [str(m) for m in metadata]
            
            entities = [
                vectors,  # vector field
                texts,   # text field
                metadata_strings  # metadata field
            ]

            insert_result = self.collection.insert(entities)
            self.logger.info(f"Successfully inserted {len(vectors)} vectors")
            return True

        except Exception as e:
            self.logger.error(f"Insert failed: {str(e)}")
            return False