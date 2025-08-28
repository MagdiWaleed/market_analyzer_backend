from marketAnalyzerAgent.schema import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from .schema import AgentState, Solution, FinishedStatus
from dotenv import load_dotenv
from ..tools.searchTool import getSearchTool

def getSolutionFinderAgent():
    load_dotenv()

    llm = ChatGoogleGenerativeAI(model= "gemini-2.5-flash",temperature =0)
    llm_with_structured_output = llm.with_structured_output(Solution)
    llm_with_finished_status = llm.with_structured_output(FinishedStatus)

    search = getSearchTool()
    tools = [search]


    def main (state:AgentState)->AgentState:
        """Agent responsible of identifying what is the gap in the market and provide recommendations for solutions."""
        data  = []
        for i in range(len(state['competitorCompanies'].competitorCompanies)):
            company = state['competitorCompanies'].competitorCompanies[i]
            details = state['companiesDetails'][i]
            data.append(f"Company Name: {company}\nProducts: {details.products}\nOverall Advantages: {details.overall_advantages}\nOverall Weaknesses: {details.overal_weaknesses}\n")
        
        sys_prompt = f"""
        You are a helpful agent that analysis a products advantages and weaknesses to identifying the gap in {state['marketIntent'].marketType} and provide solutinos for them.

        Companyes and their Products are: {
            data
        }
        Your task is to analyze the above data and identify the gap in the market based on the weaknesses of the competitors products, then provide some recommendations for solutions that can fill that gap.
        The Market Type is: {state['marketIntent'].marketType}
        Tools:
            - search: Usefull tool for searching the internet.
        Instructions:
            - Use Think-> Act-> Observe patter and use the tools only 2->4 times until you reach your goal.
            - Search about anything you don't know to accuratlly know, to have better results.
            - Always search in KSA regions.
        Output:
                Define the gap in the market based on the weaknesses of the competitors products, then provide some recommendations for solutions that can fill that gap.
                Gaps in the Market:
                Recommendations for Solutions:
                """
        
        messages = state['messages']
        result = llm.invoke([SystemMessage(sys_prompt)]+ messages +[SystemMessage("Follow the above instructions.")])
        messages.append(result)
        state["messages"] = messages
        return state
    

    def outputParser(state:AgentState):
        message = state["messages"][-1]
        result = llm_with_structured_output.invoke(message.content)
        state["finalAnswer"]= result
        return state

    
    
    graph = StateGraph(AgentState)
    graph.add_node("main",main)
    graph.add_node("tools",ToolNode(tools))
    graph.add_node("outputParser",outputParser)

    graph.add_edge(START,"main")
    graph.add_conditional_edges(
        "main",
        tools_condition,
            {
            "tools":"tools",
            END:"outputParser",
                }
                )
    graph.add_edge("tools","main")
    graph.add_edge("outputParser",END)


    agent  = graph.compile()
    # agent.get_graph().draw_mermaid_png(
    #     output_file_path="SolutionFinderGraph.png"
    # )
    return agent
    