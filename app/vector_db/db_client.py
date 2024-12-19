from .milvus_client import MilvusDB
from config.settings import VECTOR_DB_TYPE
import logging

class VectorDB:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_type = VECTOR_DB_TYPE.lower() if VECTOR_DB_TYPE else "milvus"
        
        if self.db_type == "milvus":
            self.client = MilvusDB()  # Використовуємо skynet_test за замовчуванням
        else:
            raise ValueError(f"Unsupported vector database type: {self.db_type}")
    
    async def connect(self):
        return await self.client.connect()
    
    async def init_collection(self):
        await self.client.init_collection()
    
    async def search(self, vector, limit=5):
        return await self.client.search(vector, limit)
    
    async def insert(self, vectors, metadata):
        return await self.client.insert(vectors, metadata)