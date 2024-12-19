from telegram import Update
from telegram.ext import ContextTypes
from app.models.model_switcher import ModelSwitcher

class CommandHandler:
    def __init__(self, model_switcher: ModelSwitcher):
        self.model_switcher = model_switcher
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Вітаю! Я бот для аналізу векторної бази даних. "
            "Використовуйте /switch_model для зміни моделі."
        )
    
    async def switch_model(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text(
                "Будь ласка, вкажіть модель: chatgpt, anthropic, або deepseek"
            )
            return
        
        model_name = context.args[0].lower()
        if self.model_switcher.switch_model(model_name):
            await update.message.reply_text(f"Модель змінено на {model_name}")
        else:
            await update.message.reply_text("Невідома модель")