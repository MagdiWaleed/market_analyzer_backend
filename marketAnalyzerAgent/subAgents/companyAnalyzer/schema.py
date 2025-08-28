from pydantic import BaseModel, Field
from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages
from ..inhancerAgent.schema import MarketIntent


class Product(BaseModel):
    name: str = Field(description="Name of the product.")
    advantages: str = Field(description="The advantages of this product.")
    weaknesses: str = Field(description="What is the weaknesses of this product.")

class Company(BaseModel):
    products: List[Product] = Field(description="List of products with their data.")
    overall_advantages: str = Field(description="Overall advantage of the whole company in that Market.")
    overal_weaknesses: str = Field(description="Overall weaknesses of the whole company in that Market.")


class AgentState(TypedDict):
    messages: List
    companyName: str
    companyDetails: Annotated[Company,"competitor company details."]
    marketIntent: MarketIntent
