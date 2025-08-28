from langchain_core.messages import BaseMessage
from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages
from ..inhancerAgent.schema import MarketIntent
from ..competitorsResearcherAgent.schema import CompetitorCompanyList
from ..companyAnalyzer.schema import Company
from pydantic import BaseModel, Field

class FinishedStatus(BaseModel):
    status: str = Field(description="The status of the agent whether it is finished or not. It can be either 'finished' or 'not finished'.")

class Solution(BaseModel):
    gapInMarket: List[str] = Field(description="Extracted List of Gaps from the text.")
    recommendations: List[str] = Field(description="Extracted List of Recommendations from the text.")

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    marketIntent: MarketIntent
    competitorCompanies: CompetitorCompanyList
    companiesDetails: List[Company]
    finalAnswer: Annotated[Solution,None,"The final solution that the agent has found based on the analysis of the competitors."]
