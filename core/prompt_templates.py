from logs.logging_config import logger
from workflows.graphs.persona.prompts import persona_prompt

class PromptBuilder:
    """
    Builds structured prompts for LLMs to generate Reddit user personas

    It combines user posts and comments into a single prompt with a consistent 
    format, guiding the LLM to output structured persona information
    """

    def __init__(self):
        """
        Initializes the PromptBuilder and logs its creation
        """
        logger.info("PersonaPromptBuilder initialized")

    def get_persona_prompt(self, username: str, posts: list[str], comments: list[str]) -> str:
        """
        Clean a single post or comment by stripping URLs and truncating.

        Args:
            text (str): Raw Reddit post or comment.
            max_len (int): Maximum length for individual text entries.

        Returns:
            str: Cleaned and truncated text.
        """
        try:
            # Truncates combined text to avoid token explosins that free tier can't handle
            joined_text = "\n".join(posts + comments)[:2000]

            prompt = f"""
                From the following Reddit posts/comments, extract a detailed user persona.
                Based on the following Reddit posts and comments from user `{username}`, create a detailed user persona. 
                Include: Name, Occupation, Location, Traits, Behaviours, Motivations, Frustrations, and Goals.

                Structure the output nicely and clearly.
                
                For each **attribute** (Name, Age, Occupation, Location, Traits, Behaviors, Motivations, Frustrations, Goals):

                - Write the value in plain language.
                - Under each value, include: `Cited from: "<exact post or comment excerpt>"`.
                - For multi-value fields (like Traits, Behaviors, etc.), format as bullet points with their citations below them.
                - Remove those annoying astersiks from the output.

                Use this structure:

                </> Name: ...
                Cited from: "..."

                </> Age: ...
                Cited from: "..."

                </> Occupation: ...
                Cited from: "..."

                </> Location: ...
                Cited from: "..."

                </> Traits:
                • Trait 1
                    ↳ Cited from: "..."
                ...

                </> Motivations:
                • Motivation 1
                    ↳ Cited from: "..."

                </> Frustrations:
                • Frustration 1
                    ↳ Cited from: "..."

                </> Goals:
                • Goal 1
                    ↳ Cited from: "..."

                Now analyze this Reddit content and create the persona:
                -------------------------------------------------------

                {joined_text}
                
                """.strip()

            return prompt

        except Exception as e:
            logger.error(f"Failed to analyze user {username}: {e}")
            raise
