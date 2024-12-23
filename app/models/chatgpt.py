import openai
from app.models.language_model import LanguageModel
from config.settings import OPENAI_API_KEY

class ChatGPT(LanguageModel):
    def __init__(self):
        openai.api_key = OPENAI_API_KEY
    
    async def generate_response(self, prompt: str, context: dict) -> str:
        """
        Генерує відповідь за допомогою GPT-4.
        """
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are analyzing vector database content."},
                    {"role": "user", "content": f"Context: {context}\n\nPrompt: {prompt}"}
                ]
            )
            return response.choices[0].message['content']
        except Exception as e:
            raise RuntimeError(f"Failed to generate response: {e}")
    
  async def embed_text(self, text: str) -> list[float]:
        """
        Генерує embeddings для тексту, використовуючи новий API.
        """
        try:
            response = await openai.Embedding.acreate(
                model="text-embedding-ada-002",  # Поточна модель для embeddings
                input=text
            )
            return response["data"][0]["embedding"]
        except Exception as e:
            raise RuntimeError(f"Помилка генерації embeddings: {e}")
