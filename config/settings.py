from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
VECTOR_DB_URI = os.getenv("VECTOR_DB_URI", "localhost:6333")
VECTOR_DB_TYPE = os.getenv("VECTOR_DB_TYPE", "qdrant")  # або "qdrant"