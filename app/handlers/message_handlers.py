from telegram import Update
from telegram.ext import ContextTypes
from app.models.model_switcher import ModelSwitcher
from app.vector_db.db_client import QdrantDB

class MessageHandler:
    def __init__(self, model_switcher: ModelSwitcher, vector_db: QdrantDB):
        self.model_switcher = model_switcher
        self.vector_db = vector_db
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_message = update.message.text

        # Отримуємо активну модель
        model = self.model_switcher.get_current_model()
        if not model:
            await update.message.reply_text("Будь ласка, оберіть модель AI командою /switch_model.")
            return

        try:
            # Генеруємо embedding для запиту
            query_embedding = await model.embed_text(user_message)

            # Шукаємо схожі документи у векторній базі
            similar_docs = self.vector_db.search(query_embedding)

            if not similar_docs:
                await update.message.reply_text("Не вдалося знайти відповідну інформацію в завантажених файлах.")
                return

            # Формуємо відповідь за допомогою AI
            response = await model.generate_response(
                prompt=user_message,
                context={"similar_documents": similar_docs}
            )

            # Відправляємо відповідь користувачу
            await update.message.reply_text(response)
        except Exception as e:
            await update.message.reply_text(f"Сталася помилка при обробці вашого запиту: {e}")
