from typing import Any, Optional, Dict
from threading import Lock

from langchain_core.language_models import BaseLanguageModel
from langchain_groq import ChatGroq

from configs.app_config import AppConfig
from logs.logging_config import logger


class LLM:
    """
    Groq LLM handler for generating personas - since I don't have paid subscription of any LLM model

    Overlooks instantiation & configuration of the Groq LLM.

    This class uses LangChain's 'ChatGroq' wrapper & supports structured output formats if specified
    Reads model configuration and API keys from app_config.py

    Attributes:
        config (AppConfig): Application configuration instance to access credentils like API keys and model names
    """

    def __init__(self, config: AppConfig):
        """
        Initializes the LLM handler with configuration

        Args:
            config (AppConfig): Loaded config with Groq credentials and model name
        """
        self.config = config

    def get_llm(self,
                temperature: float = 0.3,
                model_kwargs: Optional[Dict[str, Any]] = None, 
                structured_output: Optional[Any] = None) -> BaseLanguageModel:
         """
            Returns a Groq LLM instance with optional structured output and config overrides

            Args:
                temperature (float): Sampling temperature for text generation
                model_kwargs (Optional[Dict[str, Any]]): Additional keyword args passed to the model
                structured_output (Optional[Any]): Optional structured output schema

            Returns:
                BaseLanguageModel: Configured Groq chat model instance
         """
         
         model_kwargs = model_kwargs or {}

         llm = ChatGroq(
            model=self.config.GROQ_MODEL_NAME,
            api_key=self.config.get("GROQ_API_KEY"),
            temperature=temperature,
            **model_kwargs
            )

         if structured_output:
             return llm.with_structured_output(structured_output)
         
         return llm


class LLMManager:
    """
    Singleton manager for Groq LLM instance
    Ensures that the LLM is instantiated only once and reused across the app
    """
    _instance = None
    _llm = None
    _lock = Lock()

    def __new__(cls):
        """
        Ensures only one instance of LLMManager exists
        Initializes LLM lazily with app_config
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                config = AppConfig.get_config_instance()
                cls._instance._llm = LLM(config)
        return cls._instance

    @classmethod
    def get_llm(cls,
                temperature: float = 0.3,
                model_kwargs: Optional[Dict[str, Any]] = None,
                structured_output: Optional[Any] = None) -> BaseLanguageModel:
        """
        Innterface to retrieve the shared Groq LLM instance

        Args:
            temperature (float): Sampling temperature for text generation
            model_kwargs (Optional[Dict[str, Any]]): Additional arguments for model configuration
            structured_output (Optional[Any]): Optional structured output schema

        Returns:
            BaseLanguageModel: The configured LLM instance
        """
        
        return cls()._llm.get_llm(temperature=temperature,
                                  model_kwargs=model_kwargs,
                                  structured_output=structured_output
                                )
