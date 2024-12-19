import asyncio
import logging
from telegram import Update
from app.bot import setup_bot

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='logs/bot.log'
)

def main():
    # Створюємо та запускаємо бота
    application = asyncio.get_event_loop().run_until_complete(setup_bot())
    
    # Запускаємо polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Bot stopped by user")
    except Exception as e:
        print(f"Error running bot: {e}")