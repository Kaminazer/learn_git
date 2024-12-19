from telegram import Update
from telegram.ext import ContextTypes
from app.models.model_switcher import ModelSwitcher
from app.vector_db.db_client import VectorDB

class MessageHandler:
    def __init__(self, model_switcher: ModelSwitcher, vector_db: VectorDB):
        self.model_switcher = model_switcher
        self.vector_db = vector_db
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        model = self.model_switcher.get_current_model()
        query_embedding = await model.embed_text(update.message.text)
        
        # Search vector DB
        similar_docs = await self.vector_db.search(query_embedding)
        
        # Generate response using language model
        response = await model.generate_response(
            update.message.text,
            {"similar_documents": similar_docs}
        )
        
        await update.message.reply_text(response)