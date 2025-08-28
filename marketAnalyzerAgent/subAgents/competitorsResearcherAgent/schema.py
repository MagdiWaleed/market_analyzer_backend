from langgraph.graph.message import add_messages
from typing import Annotated, List, TypedDict
from pydantic import BaseModel, Field
from ..inhancerAgent.schema import MarketIntent



class CompetitorCompany(BaseModel):
    name: str = Field(description="The name of the competitive company.")

class CompetitorCompanyList(BaseModel):
    competitorCompanies:List[CompetitorCompany] = Field(description="List of all the competitive companies names.") 


class AgentState(TypedDict):
    messages:Annotated[List,add_messages]
    competitorCompanies: List[CompetitorCompany] | None
    marketIntent: MarketIntent





    