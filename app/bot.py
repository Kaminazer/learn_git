from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config.settings import TELEGRAM_TOKEN
from app.models.model_switcher import ModelSwitcher
from app.vector_db.db_client import QdrantDB
from app.handlers.command_handlers import CommandHandler as CustomCommandHandler
from app.handlers.message_handlers import MessageHandler as CustomMessageHandler
import logging

async def setup_bot():
    try:
        # Ініціалізація векторної бази даних
        vector_db = QdrantDB(collection_name="chatbot_data")
        vector_db.connect()
        vector_db.init_collection()  # Ініціалізація колекції, якщо її ще немає
    except Exception as e:
        logging.error(f"Помилка під час ініціалізації векторної БД: {str(e)}")
        vector_db = None

    # Ініціалізація перемикача моделей
    model_switcher = ModelSwitcher()

    # Ініціалізація обробників
    command_handler = CustomCommandHandler(model_switcher=model_switcher, vector_db=vector_db)
    message_handler = CustomMessageHandler(model_switcher=model_switcher, vector_db=vector_db)

    # Створення додатку Telegram
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Додавання обробників
    application.add_handler(CommandHandler("start", command_handler.start))
    application.add_handler(CommandHandler("switch_model", command_handler.switch_model))
    application.add_handler(MessageHandler(filters.Document.ALL, command_handler.handle_file))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler.handle_message))

    return application
