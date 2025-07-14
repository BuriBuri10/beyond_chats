import praw
from typing import List, Tuple
from configs.app_config import AppConfig
from logs.logging_config import logger

class RedditScraper:
    """
    RedditScraper handles fetching Reddit posts and comments for a given user
    using the PRAW(Python Reddit API Wrapper) library

    Configuration values are retrieved from AppConfig:
        > REDDIT_CLIENT_ID
        > REDDIT_CLIENT_SECRET
        > REDDIT_USER_AGENT
    """
    def __init__(self):
        """
        Initializes the Reddit API client with credentials from AppConfig
        Asserts that all required credentials are present
        """
        config = AppConfig.get_config_instance()

        client_id = config.get("REDDIT_CLIENT_ID")
        client_secret = config.get("REDDIT_CLIENT_SECRET")
        user_agent = config.get("REDDIT_USER_AGENT")

        assert client_id, "Missing REDDIT_CLIENT_ID"
        assert client_secret, "Missing REDDIT_CLIENT_SECRET"
        assert user_agent, "Missing REDDIT_USER_AGENT"

        print(f"[DEBUG] Using client_id={client_id}, user_agent={user_agent}")

        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

    def fetch_user_data(self, username: str, limit: int = 10) -> Tuple[List[str], List[str]]:
        """
        Fetches a limited number of recent Reddit posts and comments from a user

        Args:
            username (str): The Reddit username to fetch data for
            limit (int): The number of posts and comments to fetch (default: 10)

        Returns:
            Tuple[List[str], List[str]]:
                - List of formatted post strings(title+body)
                - List of comment body strings

        Logs:
            Info: On successful fetch of posts/comments
            Error: On exceptions or errors
        """
        posts = []
        comments = []

        try:
            redditor = self.reddit.redditor(username)

            for submission in redditor.submissions.new(limit=limit):
                content = f"Title: {submission.title}\nBody: {submission.selftext}"
                posts.append(content)

            for comment in redditor.comments.new(limit=limit):
                comments.append(comment.body)

            logger.info(f"Fetched {len(posts)} posts and {len(comments)} comments for user: {username}")

        except Exception as e:
            logger.error(f"Error fetching data for user {username}: {str(e)}")

        return posts, comments
