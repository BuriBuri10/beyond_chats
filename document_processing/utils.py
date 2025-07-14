# document_processing/utils.py

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TextCleaner:
    """
    For text cleaning and formatting
    """
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Cleans the input text by removing redundant whitespace, newlines, and formatting characters
        """
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^\x00-\x7F]+", " ", text)  # Removes non-ASCII characters
        return text.strip()

    @staticmethod
    def truncate_text(text: str, max_chars: int = 3000) -> str:
        """
        Truncates text to the maximum number of characters - to ensure full sentence endings
        """
        if len(text) <= max_chars:
            return text

        truncated = text[:max_chars]
        last_period = truncated.rfind(".")
        if last_period != -1:
            return truncated[:last_period + 1]
        return truncated

    @staticmethod
    def safe_join(texts: list[str], separator: str = "\n") -> str:
        """
        Safely joins a list of text elements with a separator
        """
        return separator.join(TextCleaner.clean_text(t) for t in texts if t and t.strip())

    @staticmethod
    def extract_username_from_url(url: str) -> Optional[str]:
        """
        Extracts the Reddit username from a profile URL
        Example: https://www.reddit.com/user/example_user |  > here, the user_id is: example_user
        """
        pattern = r"reddit\.com\/user\/([\w\-_.]+)"
        match = re.search(pattern, url)
        return match.group(1) if match else None
