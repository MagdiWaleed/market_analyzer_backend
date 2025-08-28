from langgraph.graph.message import add_messages
from typing import Annotated, List, TypedDict
from pydantic import BaseModel, Field
from .subAgents.inhancerAgent.schema import MarketIntent
from .subAgents.competitorsResearcherAgent.schema import CompetitorCompanyList
from .subAgents.companyAnalyzer.schema import Company
from .subAgents.solutionFinderAgent.schema import Solution

class AgentState(TypedDict):
    messages:Annotated[List,[],"The list of messages that the agent has exchanged so far."]
    marketIntent: MarketIntent | None
    competitorCompanies: CompetitorCompanyList | None
    companiesDetails: List[Company] | None
    companiesNames: List[str] | None
    finalAnswer: Solution | None





    