from document_processing.persona_writer import PersonaWriter
from logs.logging_config import logger
from workflows.state import NodeState


class FormatterNode:
    """Node responsible for formatting extracted traits into a readable persona summary."""

    def __init__(self):
        self.writer = PersonaWriter()
        logger.info("FormatterNode initialized with PersonaWriter")

    async def process(self, state: NodeState) -> NodeState:
        try:
            if not state.selection:
                logger.warning("No traits available in state for formatting.")
                state.response = "Unable to generate persona summary due to missing traits."
                return state

            logger.info("Formatting traits into a final persona summary...")
            
            persona_text = (
                state.selection.content if hasattr(state.selection, "content") else str(state.selection)
            )
            self.writer.save_persona_to_txt(state.username, persona_text)

            logger.info("Persona summary successfully generated.")
            state.response = persona_text
            return state

        except Exception as e:
            logger.error(f"FormatterNode failed: {e}")
            state.error = str(e)
            return state
