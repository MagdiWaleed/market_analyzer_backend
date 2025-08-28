from langgraph.graph import START, END, StateGraph
from .schema import AgentState,CompetitorCompanyList
from langchain_google_genai  import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage,HumanMessage
from langgraph.prebuilt import ToolNode, tools_condition
from .subAgents.inhancerAgent.agent import getInhancerAgent
from .subAgents.competitorsResearcherAgent.agent import getCompetitorResearcherAgent
from .subAgents.companyAnalyzer.agent import getCompanyAnalyzerAgent
from .subAgents.solutionFinderAgent.agent import getSolutionFinderAgent
from tqdm import tqdm

from dotenv import load_dotenv

load_dotenv()

def getMarketAnalyzerAgent():

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    inhancerAgent = getInhancerAgent()
    competitorResearcherAgent = getCompetitorResearcherAgent()
    companyAnalyzerAgent = getCompanyAnalyzerAgent()
    solutionFinderAgent =  getSolutionFinderAgent()





    def inhancerNode(state:AgentState)->AgentState:
        """An inhancer agent who is responsible of inhancing the user message and identifying which market the user is asking about."""
        messages = state['messages']
        response = inhancerAgent.invoke({"messages":messages})
        state['marketIntent'] = response['market']
        print("Finished Inhancing")
        return state

    
    def competitivesFinder(state:AgentState)->AgentState:
        result = competitorResearcherAgent.invoke(state)
        state['competitorCompanies'] = result['competitorCompanies']
        print("Finished Finding Compititors")
        return state
    
    def companyAnalyzer(state:AgentState)->AgentState:

        state['companiesDetails'] = []
        state['companiesNames'] = []

        for companyName in tqdm(state["competitorCompanies"].competitorCompanies):

            result = companyAnalyzerAgent.invoke(
                {
                    "companyName":companyName,
                    "marketIntent":state['marketIntent'],
                    "messages":[HumanMessage(state['marketIntent'].inhancedUserMessage)]
                }
            )
            state['companiesDetails'].append(result['companyDetails'])
            state['companiesNames'].append(result['companyName'])
        print("Finished Analyzing The Compititors")
        return state
    
    def solutionFinder(state:AgentState)->AgentState:
        messages = [HumanMessage(state['marketIntent'].inhancedUserMessage)]
        state['messages'] = messages
        result = solutionFinderAgent.invoke(state)
        state['finalAnswer'] = result['finalAnswer']
        state['messages'] = result['messages']
        print("Finished")
        return state
    
    graph = StateGraph(AgentState)
    graph.add_node("inhancerNode",inhancerNode)
    graph.add_node("competitivesFinder", competitivesFinder)
    graph.add_node("companyAnalyzer",companyAnalyzer)
    graph.add_node("solutionFinder",solutionFinder)

    graph.add_edge(START,"inhancerNode")
    graph.add_edge("inhancerNode","competitivesFinder")
    graph.add_edge("competitivesFinder","companyAnalyzer")
    graph.add_edge("companyAnalyzer", "solutionFinder")
    graph.add_edge("solutionFinder", END)

    agent  = graph.compile()
    # agent.get_graph().draw_mermaid_png(
    #     output_file_path="CompleteGraph.png"
    # )
    return agent
    
        






