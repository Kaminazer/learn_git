from abc import ABC, abstractmethod
from typing import List, Dict, Any

class VectorDBBase(ABC):
    @abstractmethod
    async def connect(self) -> bool:
        pass
    
    @abstractmethod
    async def init_collection(self):
        pass
    
    @abstractmethod
    async def search(self, vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    async def insert(self, vectors: List[List[float]], metadata: List[Dict[str, Any]]) -> bool:
        pass