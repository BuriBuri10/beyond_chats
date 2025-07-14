from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from workflows.workflow import PersonaWorkflow

router = APIRouter()

class PersonaRequest(BaseModel):
    reddit_url: str

@router.post("/generate-persona")
async def generate_persona(data: PersonaRequest):
    """
    Endpoint to generate a persona based on a user's Reddit activity
    Extracts the username from the given Reddit profile URL, then runs the persona workflow using LangGraph.

    Args:
        data (PersonaRequest): Contains the Reddit URL of the user

    Returns:
        dict: A dictionary with the generated persona under the key 'persona'
    """
    try:
        username = data.reddit_url.strip().split("/")[-2]
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Reddit URL")

    workflow = PersonaWorkflow()
    result = await workflow.run(username=username)

    if result and result.get("response"):
        return {"persona": result["response"]}

    raise HTTPException(status_code=500, detail=result.get("error", "Persona generation failed"))
