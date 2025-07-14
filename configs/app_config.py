import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional


# class AppConfig:
#     """
#     Singleton config class to load environment variables and define global settings

#     Attributes:
#         configs (dict): A dictionary of loaded environment variables
#         GROQ_API_KEY (str): Loaded Groq API key for LLM integration
#         GROQ_MODEL_NAME (str): Default model name used by Groq
#     """
#     _instance = None
#     _env_loaded = False
#     # GROQ_MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"
#     GROQ_MODEL_NAME: Optional[str] = None  # Will be set during _load_configs()

#     def __init__(self):
#         """
#         Initializes the configuration by locating and loading the .env file
#         Raises exception if an instance already exists (singleton enforcement)
#         """
#         if AppConfig._instance is not None:
#             raise Exception("This is a singleton class and can't be instantiated more than once")

#         # env_path = None
#         # curr_path = Path(__file__).resolve()
#         # for parent in curr_path.parents:
#         #     candidate = parent / ".env"
#         #     if candidate.exists():
#         #         env_path = candidate
#         #         break

#         # if not env_path:
#         #     raise FileNotFoundError(".env file not found in any parent directories.")

#         # load_dotenv(env_path, override=True)
#         # print(f"[DEBUG] Loaded .env from: {env_path}")
#         # self._load_configs()
#         # AppConfig._instance = self

#         # If required environment variable not already present, try to load from .env
#         if not os.getenv("GROQ_API_KEY"):
#             env_path = None
#             curr_path = Path(__file__).resolve()
#             for parent in curr_path.parents:
#                 candidate = parent / ".env"
#                 if candidate.exists():
#                     env_path = candidate
#                     break

#             if not env_path:
#                 raise FileNotFoundError(".env file not found and GROQ_API_KEY not set in environment.")

#             load_dotenv(env_path, override=True)
#             print(f"[DEBUG] Loaded .env from: {env_path}")
#         else:
#             print("[DEBUG] Using environment variables already set (Docker mode)")

#         self._load_configs()
#         AppConfig._instance = self

#     def _load_configs(self):
#         """
#         helper to load all environment variables into a dictionary
#         """
#         self.configs = dict(os.environ)
#         self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
#         self.GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "meta-llama/llama-4-scout-17b-16e-instruct")

#     @staticmethod
#     def get_config_instance():
#         """
#         Returns the singleton instance of AppConfig, creating one if necessary

#         Returns:
#             AppConfig: The singleton config instance
#         """
#         if AppConfig._instance is None:
#             AppConfig()
#         return AppConfig._instance

#     def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
#         """
#         Retrieves a configuration value by key

#         Args:
#             key (str): The environment variable name
#             default (Optional[str]): Optional default value if key is not found

#         Returns:
#             Optional[str]: The corresponding environment value or default
#         """
#         return self.configs.get(key, default)

#     def set(self, key: str, value: str):
#         """
#         Manually sets or overrides a config value

#         Args:
#             key (str): Configuration key to set
#             value (str): Value to assign to the key
#         """
#         self.configs[key] = value


# if __name__ == "__main__":
#     config = AppConfig.get_config_instance()
#     print("Loaded .env successfully")
#     print("GROQ model:", config.get("GROQ_MODEL_NAME", "not set"))

class AppConfig:
    """
     Singleton config class to load environment variables and define global settings

     Attributes:
         configs (dict): A dictionary of loaded environment variables
         GROQ_API_KEY (str): Loaded Groq API key for LLM integration
         GROQ_MODEL_NAME (str): Default model name used by Groq
    """
    _instance = None
    GROQ_MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"

    def __init__(self):
        """
         Initializes the configuration by locating and loading the .env file
         Raises exception if an instance already exists (singleton enforcement)
        """
        if AppConfig._instance is not None:
            raise Exception("This is a singleton class and can't be instantiated more than once")

        # Skipping .env loading if all needed variables are already set in environment
        if os.getenv("GROQ_API_KEY") and os.getenv("REDDIT_CLIENT_ID") and os.getenv("REDDIT_CLIENT_SECRET"):
            print("[DEBUG] Using existing environment variables (Docker mode)")
        else:
            # Fallback to searching for .env only in dev mode
            env_path = None
            curr_path = Path(__file__).resolve()
            for parent in curr_path.parents:
                candidate = parent / ".env"
                if candidate.exists():
                    env_path = candidate
                    break

            if not env_path:
                raise FileNotFoundError(".env file not found and required variables not set in environment.")

            load_dotenv(env_path, override=True)
            print(f"[DEBUG] Loaded .env from: {env_path}")

        self._load_configs()
        AppConfig._instance = self

    def _load_configs(self):
        """
         helper to load all environment variables into a dictionary
        """
        self.configs = dict(os.environ)
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME")

    @staticmethod
    def get_config_instance():
        """
         Returns:
              AppConfig: The singleton config instance
        """
        if AppConfig._instance is None:
            AppConfig()
        return AppConfig._instance

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
         Retrieves a configuration value by key

         Args:
             key (str): The environment variable name
             default (Optional[str]): Optional default value if key is not found

         Returns:
             Optional[str]: The corresponding environment value or default
        """
        return self.configs.get(key, default)

    def set(self, key: str, value: str):
        """
         Manually sets or overrides a config value

         Args:
              key (str): Configuration key to set
              value (str): Value to assign to the key
        """
        self.configs[key] = value