from document_processing.analyzer import PersonaAnalyzer
from logs.logging_config import logger
from workflows.state import NodeState


class AnalyzerNode:
    """Node responsible for analyzing Reddit posts to extract traits."""

    def __init__(self):
        self.analyzer = PersonaAnalyzer()
        logger.info("AnalyzerNode initialized with PersonaAnalyzer")

    async def process(self, state: NodeState) -> NodeState:
        try:
            if not state.documents:
                logger.warning("No documents found in state for analysis.")
                state.response = "No Reddit posts available to analyze."
                return state

            logger.info(f"Analyzing {len(state.documents)} Reddit posts...")

            traits = self.analyzer.analyze_user(
                username=state.username,
                posts=state.posts,
                comments=state.comments
            )

            state.selection = traits
            logger.info("Persona traits extracted.")
            return state

        except Exception as e:
            logger.error(f"AnalyzerNode failed: {e}")
            state.error = str(e)
            return state
