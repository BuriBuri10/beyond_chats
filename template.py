import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

# project_name = "reddit_persona_project"
BASE_DIR = Path(__file__).resolve().parent    # NOTE __> Getting the directory where this script exists

folders_and_files = {
    "api": ["main.py"],
    "api/routes": ["__init__.py", "persona.py"],

    "configs": ["__init__.py", "app_config.py"],

    "core": ["__init__.py", "llm.py", "prompt_templates.py", "reddit_scraper.py", "reducer.py"],

    "document_processing": ["__init__.py", "analyzer.py", "persona_writer.py", "utils.py"],

    "models": ["__init__.py", "persona_model.py"],

    "services": ["__init__.py", "persona_service.py"],

    "tests": ["test_scraper.py", "test_analyzer.py", "test_endpoints.py"],

    "logs": ["app.log"],

    "workflows": ["state.py", "workflow.py"],
    "workflows/graphs/persona/nodes": [
        "scraper_node.py",
        "analyzer_node.py",
        "formatter_node.py"
        ],
    "workflows/graphs/persona/prompts": ["persona_prompt.py"],
    "workflows/graphs/persona": ["__init__.py"]
}

base_files = [".env", ".env.example" "requirements.txt"]

# Generating folders and files
for folder, files in folders_and_files.items():
    for file in files:
        path = BASE_DIR / folder / file
        # path = Path(f"{folder}/{file}")
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.touch()
            logging.info(f"Created file: {path}")
        else:
            logging.info(f"File already exists: {path}")

for file in base_files:
    path = BASE_DIR / file
    # path = Path(file)
    if not path.exists():
        path.touch()
        logging.info(f"Created base file: {file}")
    else:
        logging.info(f"Base file already exists: {file}")

# Creating Dockerfile
dockerfile_content = """\
# Use official slim Python image
FROM python:3.11-slim

# Avoid .pyc files and buffer issues
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Launch FastAPI app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

dockerfile_path = Path("Dockerfile")
if not dockerfile_path.exists():
    dockerfile_path.write_text(dockerfile_content)
    logging.info("Created Dockerfile")
else:
    logging.info("Dockerfile already exists")

# Creating .dockerignore
dockerignore_content = """\
__pycache__/
*.pyc
*.pyo
*.pyd
.env
*.db
*.sqlite3
*.log
outputs/
"""

dockerignore_path = Path(".dockerignore")
if not dockerignore_path.exists():
    dockerignore_path.write_text(dockerignore_content)
    logging.info("Created .dockerignore")
else:
    logging.info(".dockerignore already exists")

# Creating docker-compose.yml
docker_compose_content = """\
version: "3.8"

services:
  reddit-persona-app:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - .:/app
    command: uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
"""

docker_compose_path = Path("docker-compose.yml")
if not docker_compose_path.exists():
    docker_compose_path.write_text(docker_compose_content)
    logging.info("Created docker-compose.yml")
else:
    logging.info("docker-compose.yml already exists")

