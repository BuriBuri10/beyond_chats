from core.reddit_scraper import RedditScraper
from core.llm import LLMManager
from core.prompt_templates import PromptBuilder
from document_processing.persona_writer import format_persona_text
from models.persona_model import Persona
from configs.app_config import AppConfig


class PersonaService:
    """
    Service class to orchestrate Reddit scraping, persona generation, and formatting.
    """

    def __init__(self, username: str):
        self.username = username
        self.scraper = RedditScraper()
        self.llm = LLMManager.get_llm(provider="groq", temperature=0.3)
        self.prompt_builder = PromptBuilder()
        self.config = AppConfig.get_config_instance()

    def generate_persona(self) -> str:
        """
        Main method to generate the persona text for the Reddit user.
        Returns:
            str: Final formatted persona with citations.
        """
        # Step 1: Fetch posts and comments
        posts, comments = self.scraper.fetch_user_content(self.username)

        # Step 2: Build the LLM prompt
        prompt = self.prompt_builder.build_persona_prompt(self.username, posts, comments)

        # Step 3: Run LLM to get raw persona response
        raw_persona = self.llm.invoke(prompt)

        # Step 4: Format it into clean structured output
        formatted = format_persona_text(raw_persona, self.username)

        return formatted


from core.reddit_scraper import RedditScraper
from core.llm import LLMManager
from core.prompt_templates import PersonaPrompt
from document_processing.analyzer import PersonaAnalyzer
from document_processing.persona_writer import PersonaWriter
from document_processing.utils import extract_username_from_url


class PersonaService:
    def __init__(self):
        self.scraper = RedditScraper()
        self.analyzer = PersonaAnalyzer()
        self.writer = PersonaWriter()
        self.llm = LLMManager.get_llm(provider="groq", temperature=0.3)
        self.prompt_template = PersonaPrompt()

    def generate_persona(self, reddit_url: str) -> str:
        username = extract_username_from_url(reddit_url)
        if not username:
            raise ValueError("Invalid Reddit profile URL provided.")

        posts, comments = self.scraper.fetch_user_content(username)
        if not posts and not comments:
            raise ValueError("No user data found to analyze.")

        combined_text = self.analyzer.reduce(posts, comments)
        prompt = self.prompt_template.build_prompt(username=username, text=combined_text)

        result = self.llm.invoke(prompt)
        formatted_persona = self.writer.format_result(result, username)

        return formatted_persona
