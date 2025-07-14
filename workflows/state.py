from enum import Enum
from typing import Annotated, Optional, List

from langchain.schema import Document
from pydantic import BaseModel, Field

from core.reducer import Reducer


class ReadyState(str, Enum):
    """Explicit states used for document flow control."""
    WAITING = "waiting"
    COMPLETE = "complete"
    RESET = "reset"


class NodeState(BaseModel):
    """State passed between LangGraph nodes during Reddit persona generation."""

    username: Annotated[Optional[str], Reducer.update] = None
    posts: Annotated[Optional[List[str]], Reducer.update] = Field(default_factory=list)
    comments: Annotated[Optional[List[str]], Reducer.update] = Field(default_factory=list)
    query: Annotated[Optional[str], Reducer.update] = None
    documents: Annotated[Optional[List[str]], Reducer.update] = None
    selection: Annotated[Optional[dict], Reducer.update] = None
    response: Annotated[Optional[str], Reducer.update] = None
    error: Annotated[Optional[str], Reducer.update] = None

    # Optional metadata
    language: Annotated[Optional[str], Reducer.update] = None

    # Conversation history from Reddit thread (if multi-turn later)
    conversation_history: Annotated[
        list[dict[str, str]], lambda curr, new: Reducer.append_and_trim(curr, new, max_length=5)
    ] = Field(default_factory=list)

    # Routing or flow control
    is_query_valid: Annotated[bool, Reducer.update] = True
    is_aggregated: Annotated[bool, Reducer.update] = False
    needs_rewrite: Annotated[bool, Reducer.update] = False

    # Outputs and context
    selection: Annotated[Optional[str], Reducer.update] = None
    response: Annotated[Optional[str], Reducer.update] = None
    error: Annotated[Optional[str], Reducer.update] = None
    stream_values: Annotated[dict, Reducer.update] = Field(default={})

    # Document-related state
    documents: Annotated[list[Document], Reducer.update] = Field(default_factory=list)
    retrieval_attempts: Annotated[int, Reducer.increment_one] = 0


class InputState(BaseModel):
    """Initial input to the graph from frontend or API layer."""
    query: str
    conversation_history: list[dict[str, str]] = Field(default_factory=list)


class OutputState(BaseModel):
    """Final output from the LangGraph pipeline."""
    response: str
