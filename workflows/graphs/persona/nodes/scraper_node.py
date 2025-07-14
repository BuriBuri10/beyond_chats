from core.reddit_scraper import RedditScraper
from workflows.state import NodeState
from logs.logging_config import logger

from langchain_core.documents import Document


class ScraperNode:
    """
    Node responsible for scraping Reddit posts from the provided username
    """

    def __init__(self):
        self.scraper = RedditScraper()
        logger.info("ScraperNode Initialized with RedditScraper")

    async def process(self, state: NodeState) -> NodeState:
        try:
            handle = state.username.strip()
            logger.info(f"Scraping Reddit data for: {handle}")
            
            posts, comments = self.scraper.fetch_user_data(handle)
            combined = posts + comments

            if not combined:
                logger.warning(f"No Reddit data found for: {handle}")
                state.response = f"Could not find any Reddit posts for user '{handle}'."
                return state

            state.posts = posts
            state.comments = comments
            state.documents = [Document(page_content=text) for text in combined]

            logger.info(f"Scraped {len(state.documents)} documents for user: {handle}")
            return state

        except Exception as e:
            logger.error(f"ScraperNode failed: {e}")
            state.error = str(e)
            return state

