from typing import TypedDict, Optional, Annotated
from langgraph.graph import add_messages

class CouncilState(TypedDict):
    messages: Annotated[list, add_messages]
    next_speaker: str
    current_round: int
    final_verdict: Optional[str]
    start_time: Optional[float]  # Unix timestamp for timeout tracking
