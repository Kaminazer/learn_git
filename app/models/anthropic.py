from anthropic import Anthropic
from app.config.settings import ANTHROPIC_API_KEY

anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)

def get_anthropic_response(query: str) -> str:
    response = anthropic.completions.create(
        prompt=f"Обговори тему: {query}",
        max_tokens_to_sample=200
    )
    return response["completion"]
