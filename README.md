# NOTE: beyond_chats

## RedditPsyche
## To run the executable python script, open the terminal & run: 
> python -m workflows.workflow


A modular, production-ready application that analyzes Reddit user activity and generates a psychological or behavioral persona based on their posts and comments. Built using LangGraph, FastAPI, and integrates LLMs via Groq or other providers.

## Features

- Reddit Scraping: Fetches user posts and comments via PRAW.
- LLM-Powered Analysis: Uses prompts to extract personality traits.
- Persona Generation: Outputs formatted summaries and optionally structured JSON personas.
- Modular Architecture: template.py contains the scaffolding/skeleton of the entire project's architecture. Clean separation of concerns using folders like core/, document_processing/, workflows/, etc.
- FastAPI Interface: Submit Reddit usernames via a REST API.
- Output Storage: Saves persona summaries as .txt files in the outputs/ folder.
- LangGraph Workflow: Defines nodes for scraper → analyzer → formatter.

## Project Structure
BeyondChats/
│
├── api/ # FastAPI application
│ └── routes/ # API route handlers
│
├── core/ # Core utilities & LLM integration
│ ├── llm.py # LLM client setup
│ ├── reddit_scraper.py # Reddit API wrapper (PRAW)
│ └── prompt_templates.py # Persona prompt builder
│
├── document_processing/
│ ├── analyzer.py # Calls LLM to extract traits
│ ├── persona_writer.py # Writes persona text to file
│ └── utils.py # Helper functions
│
├── models/ # Pydantic models for validation
│ └── persona_model.py
│
├── services/ # Service layer for business logic
│ └── persona_service.py
│
├── workflows/ # LangGraph workflow definitions
│ ├── graphs/persona/ # Persona-specific node logic
│ ├── state.py # State schema for LangGraph
│ └── workflow.py # Main PersonaWorkflow runner
│
├── outputs/ # Saved persona .txt files
│
├── logs/ # Logging configuration
│
├── .env # Reddit API credentials
├── requirements.txt
└── README.md

## But how does it even work?
1. Input: User provides a Reddit profile link (e.g. - https://www.reddit.com/user/Hungry-Move-6603/)
2. Scraping: PRAW collects their most recent posts and comments.
3. LLM Analysis: The texts are analyzed via a language model using a crafted persona-extraction prompt.
4. Formatting: The resulting traits are converted into a human-readable persona.
5. Output: A .txt file is saved, and the persona is returned via API.
6. & the graph structure of the LangGraph architecture gets saved in the root directory.
7. Start the terminal & run:
   > python -m workflows.workflow

## API Usage

### Run the FastAPI Server in terminal with the following command
>   uvicorn api.main:app --reload
>   Access FastAPI Swagger UI at: http://localhost:8000/docs

### POST/api/generate-persona
> Request body:

{
  "reddit_url": "https://www.reddit.com/user/kojied/"
}

> Response

{
  "persona": "This user appears to be confident, opinionated, and deeply engaged with discussions around tech and policy..."
}

_____________________________________________________________________________________________________________________________


## How to Set it up

### 1 - Clone the repo
git clone https://github.com/your-username/beyond_chats.git
cd beyond_chats/BeyondChats

### 2 - Create .env file
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USER_AGENT=your_user_agent
GROQ_API_KEY=your_groq_key

### 3 - Install dependencies
pip install -r requirements.txt

### 4 - Run the LangGraph workflow
python -m workflows.workflow

### 5 - Example Output
Sample file saved in the folder - 'outputs'

Username: spez

Key Traits:
- Analytical and skeptical
- Comfortable with controversy
- Occasionally humorous but assertive

Inferred from:
- 10 posts
- 10 comments

______________________________________________________________________________________________________________________________________

## Docker Containerization

Conainerized the FastAPI app in a portable Docker container.
How to use it:

### 1 - Install docker desktop & start the terminal

### 2 - Create a Docker Image with (in the terminal):
> docker build -t reddit-persona-generator .

### 3 - Intialize the container with (again, in the terminal):
> docker run -d -p 8000:8000 --env-file .env reddit-persona-generator

### 4 - Click on it & try out the whole workflow:
> http://localhost:8000/docs

______________________________________________________________________________________________________________________________________

## Tech Stack
 > LangGraph – DAG graph-based LLM pipelines
 > LangChain – LLM orchestration
 > Groq – LLM provider
 > FastAPI – RESTful API
 > PRAW – Reddit scraping
 > Docker - Containerization
 > Pydantic – Data validation
 > Logging – Structured runtime logs

______________________________________________________________________________________________________________________________________

## </> by Sailendra -- Happy Building!



