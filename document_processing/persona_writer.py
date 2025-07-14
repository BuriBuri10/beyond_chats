from pathlib import Path
from logs.logging_config import logger

class PersonaWriter:
    """
    Handles saving generated persona summaries to text files

    Attributes:
        output_dir (Path): Directory where persona files'll get saved
    """
    def __init__(self, output_dir: str = "outputs"):
        """
        Initializes the PersonaWriter with the specified output directory.

        Args:
            output_dir (str): Directory path where output files will be saved.
                              Defaults to "outputs".
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_persona_to_txt(self, username: str, persona_text: str) -> Path:
        """
        Saves the persona text to a '.txt' file - named after Reddit username

        Args:
            username (str): Reddit username for which the persona was generated
            persona_text (str): The formatted persona summary text

        Returns:
            Path: The full path to the saved persona file

        Raises:
            Exception: If the file could not be written
        """
        output_file = self.output_dir / f"{username}_persona.txt"
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(persona_text)
            logger.info(f"Saved the Persona Card to {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Couldn't save persona for {username}: {e}")
            raise
