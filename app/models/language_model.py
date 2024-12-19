from abc import ABC, abstractmethod

class LanguageModel(ABC):
    @abstractmethod
    async def generate_response(self, prompt: str, context: dict) -> str:
        pass
    
    @abstractmethod
    async def embed_text(self, text: str) -> list[float]:
        pass
