from .chatgpt import ChatGPT
# from .anthropic import AnthropicModel  # To be implemented
# from .deepseek import DeepSeekModel    # To be implemented

class ModelSwitcher:
    def __init__(self):
        self.models = {
            "chatgpt": ChatGPT(),
            # Add other models when implemented
        }
        self.current_model = "chatgpt"
    
    def switch_model(self, model_name: str) -> bool:
        if model_name in self.models:
            self.current_model = model_name
            return True
        return False
    
    def get_current_model(self):
        return self.models[self.current_model]
