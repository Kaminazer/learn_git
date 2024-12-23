import os
from telegram import Update
from telegram.ext import ContextTypes
from app.models.model_switcher import ModelSwitcher
from app.utils.xml_parser import parse_xml
from app.vector_db.db_client import QdrantDB
from sentence_transformers import SentenceTransformer

class CommandHandler:
    def __init__(self, model_switcher: ModelSwitcher, vector_db: QdrantDB):
        self.model_switcher = model_switcher
        self.vector_db = vector_db
        self.temp_dir = "temp"  # Тимчасова директорія для завантажених файлів
        os.makedirs(self.temp_dir, exist_ok=True)

        # Ініціалізація моделі Sentence Transformers
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Використовуйте іншу модель за потреби

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Вітаю! Я бот для аналізу векторної бази даних. "
            "Надішліть XML файл або використовуйте /switch_model для зміни моделі."
        )

    async def switch_model(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("Будь ласка, вкажіть модель: chatgpt, anthropic, або deepseek.")
            return
        
        model_name = context.args[0].lower()
        if self.model_switcher.switch_model(model_name):
            await update.message.reply_text(f"Модель змінено на {model_name}")
        else:
            await update.message.reply_text("Невідома модель.")

    async def handle_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        document = update.message.document
        if not document.file_name.endswith(".xml"):
            await update.message.reply_text("Будь ласка, надішліть файл у форматі XML.")
            return

        # Завантаження файлу
        file_path = os.path.join(self.temp_dir, document.file_name)
        await document.get_file().download(file_path)
        await update.message.reply_text("Файл отримано. Починаю обробку...")

        try:
            # Парсинг XML файлу
            texts = parse_xml(file_path)

            # Генерація векторів embeddings за допомогою Sentence Transformers
            vectors = self.embedding_model.encode(texts, convert_to_tensor=True).tolist()
            metadata = [{"text": text} for text in texts]

            # Додавання у векторну базу
            if self.vector_db.insert(vectors=vectors, metadata=metadata):
                await update.message.reply_text(f"Дані успішно завантажено у векторну базу ({len(vectors)} записів).")
            else:
                await update.message.reply_text("Помилка завантаження даних у векторну базу.")
        except Exception as e:
            await update.message.reply_text(f"Помилка обробки файлу: {e}")
        finally:
            os.remove(file_path)  # Видалення тимчасового файлу після обробки
