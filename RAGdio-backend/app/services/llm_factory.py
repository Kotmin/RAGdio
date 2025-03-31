

from app.core.config import Config
from app.adapters.llms.base import ChatModelAdapter

from app.adapters.llms.openai_adapter import OpenAIChatAdapter


# from app.adapters.llms.local_adapter import LocalChatAdapter  # optional

def get_chat_model() -> ChatModelAdapter:
    model_name = Config.LLM_PROVIDER_TYPE.lower()

    if model_name == "openai":
        return OpenAIChatAdapter()
    # elif model_name == "local":
    #     return LocalChatAdapter()
    else:
        raise ValueError(f"Unsupported LLM backend: {model_name}")
