from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


class MarketIntent(BaseModel):
    marketType: str = Field(description="For identifying market type.")
    description: str = Field(description="Detialed description about marketType.")
    product: str= Field(description="What is the product exactly the user want to make.")
    inhancedUserMessage: str = Field(description="An enhanced user message that outlines his/her desire to outsmart his/her competitors.")

class AgentState(TypedDict):
    messages:Annotated[List,add_messages]
    market: MarketIntent | None


