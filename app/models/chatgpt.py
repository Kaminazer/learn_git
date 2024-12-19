from openai import AsyncOpenAI
from app.models.language_model import LanguageModel
from config.settings import OPENAI_API_KEY

class ChatGPT(LanguageModel):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    
    async def generate_response(self, prompt: str, context: dict) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are analyzing vector database content."},
                {"role": "user", "content": f"Context: {context}\n\nPrompt: {prompt}"}
            ]
        )
        return response.choices[0].message.content
    
    async def embed_text(self, text: str) -> list[float]:
        response = await self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding