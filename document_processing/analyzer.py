from core.prompt_templates import PromptBuilder
from core.llm import LLMManager
from logs.logging_config import logger


class PersonaAnalyzer:
    """
    Orchestrates persona generation from Reddit data using LLMs
    Combines posts and comments into a structured prompt and uses a language model to produce a descriptive persona summary
    """

    def __init__(self):
        """
        Initializes the PersonaAnalyzer with a low-temperature LLM,
        & a prompt builder for constructing structured persona prompts
        """
        self.llm = LLMManager.get_llm(temperature=0.3)
        self.prompt_builder = PromptBuilder()
        logger.info("PersonaAnalyzer initialized")

    def analyze_user(self, username: str, posts: list[str], comments: list[str]) -> str:
        """
        Fetchess prompt from PromptBuilder & invokes LLM to generate persona

        Args:
            username (str): Reddit handle
            posts (list[str]): Fetched Reddit posts
            comments (list[str]): Fetched Reddit comments

        Returns:
            str: Description of persona
        """
        try:
            prompt = self.prompt_builder.get_persona_prompt(username, posts, comments)
            logger.info(f"Sending prompt to LLM for user: {username}")
            result = self.llm.invoke(prompt).content
            logger.info(f"Successfully built {username}'s Persona Card")
            return result

        except Exception as e:
            logger.error(f"Couldn't analyze user {username}: {e}")
            raise
