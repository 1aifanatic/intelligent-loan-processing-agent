"""Minimal UiPath coded agent with a deterministic response."""

from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field


class AgentInput(BaseModel):
    """Input accepted by the coded agent."""

    message: str = Field(
        default="Hello",
        min_length=1,
        description="A message for the loan processing agent.",
    )


class AgentOutput(BaseModel):
    """Output returned by the coded agent."""

    response: str = Field(description="The agent's deterministic response.")


class AgentState(BaseModel):
    """Internal graph state."""

    message: str
    response: str = ""


async def respond(state: AgentState) -> dict[str, str]:
    """Return a simple response without LLMs, credentials, or external systems."""

    return {
        "response": (
            "Intelligent Loan Processing Agent is ready. "
            f"Received message: {state.message}"
        )
    }


builder = StateGraph(
    AgentState,
    input_schema=AgentInput,
    output_schema=AgentOutput,
)
builder.add_node("respond", respond)
builder.add_edge(START, "respond")
builder.add_edge("respond", END)

graph = builder.compile()
