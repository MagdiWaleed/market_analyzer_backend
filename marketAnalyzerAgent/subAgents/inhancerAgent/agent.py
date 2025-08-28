from marketAnalyzerAgent.schema import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from ..tools.searchTool import getSearchTool
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from .schema import AgentState, MarketIntent
from dotenv import load_dotenv

def getInhancerAgent():
    load_dotenv()

    llm = ChatGoogleGenerativeAI(model= "gemini-2.5-flash",temperature =0)

    search = getSearchTool()
    tools = [search]

    llm_with_tool = llm.bind_tools(tools)
    llm_with_structured_output = llm.with_structured_output(MarketIntent)
    


    def main (state:AgentState)->AgentState:
        """Agent responsible of identifying what the user really intense, And identifying which market is meaning"""
        sys_prompt = """
        You are a helpful agent that analysis user input and identifying which market he/she is asking for eg.(online shoping like Amazon, Noon) or eg. (food delivary like Talabat, Marsool) etc...
        your task is identifying which market the user diser to outsmart his/her competitors in it.
        
        Tools:
            - search: Usefull tool for searching the internet.
        Instructions:
            - Use Think-> Act-> Observe patter and use the tools only 2->4 times until you reach your goal.
            - Search about anything you don't know to accuratlly specifing which market the user is asking for, to have better results.
            - Always search in KSA regions.
            - The name of the market must be searchable which means it's actual market with a lot of competitors there, And that market has a lot of product ion it. 
        Output:
            Identifying what is the market the user targeting and is exactlly the product he/she want to creaete, and description about that market, in this format:
            Market:
            Product:
            desciription:
            Recommendation Of How The User Message Should be:
        """
        messages = state['messages']
        result = llm_with_tool.invoke([SystemMessage(sys_prompt)]+messages+[SystemMessage("Follow the above instructions.")])
        
        messages.append(result)
        state["messages"] = messages

        return state
    
    def outputParser(state:AgentState):
        message = state["messages"][-1]
        result = llm_with_structured_output.invoke(message.content)
        state["market"]= result
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
                END:"outputParser"
                })
    graph.add_edge("tools","main")
    graph.add_edge("outputParser",END)


    agent  = graph.compile()
    # agent.get_graph().draw_mermaid_png(
    #     output_file_path="graph.png"
    # )
    return agent
    