from pydantic import BaseModel, Field
from typing import List, Optional


class PersonaAttribute(BaseModel):
    """
    Represents a single attribute of a Reddit user's persona,
    such as name, age, personality traits, interests, etc
    """
    label: str = Field(..., description="Persona attribute such as Name, Age, Traits, etc")
    value: str = Field(..., description="Generated content for the attribute")
    citation: Optional[str] = Field(None, description="The cited Reddit content used for this attribute")


class UserPersona(BaseModel):
    """
    Represents a structured view of a Reddit user's persona,
    including their attributes, raw posts, and raw comments
    """
    username: str = Field(..., description="Reddit username")
    attributes: List[PersonaAttribute] = Field(..., description="List of persona attributes with values and citations")
    raw_posts: Optional[List[str]] = Field(None, description="Optional list of user posts")
    raw_comments: Optional[List[str]] = Field(None, description="Optional list of user comments")


class PersonaRequest(BaseModel):
    """
    Request model for initiating persona analysis for a given Reddit user
    """
    username: str = Field(..., description="Reddit username to analyze")


class PersonaResponse(BaseModel):
    """
    Response model containing both a human-readable persona summary
    and an optional structured representation
    """
    persona_summary: str = Field(..., description="Generated persona as formatted text")
    persona_json: Optional[UserPersona] = Field(None, description="Structured JSON representation of the persona")
