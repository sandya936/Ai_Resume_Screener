from app.core.config import settings
from app.providers.llm.base import BaseLLMProvider
from app.providers.llm.gemini import GeminiLLMProvider
from app.providers.llm.openai import OpenAILLMProvider
from app.providers.llm.mock import MockDeterministicLLMProvider


class LLMProviderFactory:
    @staticmethod
    def get_provider(provider_name: str = None) -> BaseLLMProvider:
        selected = (provider_name or settings.DEFAULT_LLM_PROVIDER).lower()
        if selected == "gemini":
            return GeminiLLMProvider()
        elif selected == "openai":
            return OpenAILLMProvider()
        elif selected == "mock":
            return MockDeterministicLLMProvider()
        else:
            return MockDeterministicLLMProvider()
