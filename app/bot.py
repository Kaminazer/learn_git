from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config.settings import TELEGRAM_TOKEN
from app.models.model_switcher import ModelSwitcher
from app.vector_db.db_client import VectorDB
from app.handlers.command_handlers import CommandHandler as CustomCommandHandler
from app.handlers.message_handlers import MessageHandler as CustomMessageHandler
import logging

async def setup_bot():
    # Initialize components
    try:
        vector_db = VectorDB()
        if not await vector_db.connect():
            logging.error("Could not connect to vector database. Starting without vector DB functionality.")
            vector_db = None
    except Exception as e:
        logging.error(f"Error initializing vector DB: {str(e)}")
        vector_db = None

    model_switcher = ModelSwitcher()
    
    # Initialize handlers
    command_handler = CustomCommandHandler(model_switcher)
    message_handler = CustomMessageHandler(model_switcher, vector_db)
    
    # Setup application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", command_handler.start))
    application.add_handler(CommandHandler("switch_model", command_handler.switch_model))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler.handle_message))
    
    return application