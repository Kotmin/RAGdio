

from app.core.config import Config
from app.adapters.llms.base import ChatModelAdapter

from app.adapters.llms.openai_adapter import OpenAIChatAdapter
from app.adapters.llms.ollama_adapter import OllamaChatAdapter
from app.adapters.llms.deepseek_adapter import DeepSeekChatAdapter



# from app.adapters.llms.local_adapter import LocalChatAdapter  # optional

def get_chat_model() -> ChatModelAdapter:
    model_name = Config.LLM_PROVIDER_TYPE.lower()

    if model_name == "openai":
        return OpenAIChatAdapter()
    if model_name == "ollama":
        return OllamaChatAdapter()
    if model_name == "deepseek":
        return DeepSeekChatAdapter()
    # if model_name == "local":
    #     return LocalChatAdapter()
    else:
        raise ValueError(f"Unsupported LLM backend: {model_name}")
