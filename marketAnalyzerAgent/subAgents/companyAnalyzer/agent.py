from marketAnalyzerAgent.schema import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from .schema import AgentState, Company
from dotenv import load_dotenv
from ..tools.searchTool import getSearchTool

def getCompanyAnalyzerAgent():
    load_dotenv()

    llm = ChatGoogleGenerativeAI(model= "gemini-2.5-flash",temperature =0)

    search = getSearchTool()
    tools = [search]

    llm_with_structured_output = llm.with_structured_output(Company)


    def main (state:AgentState)->AgentState:
        """Agent responsible of identifying relative company's products with there advantages and weaknesses."""
        sys_prompt = f"""
        You are a helpful agent that analysis a Company based on specific market to Identify and listing all the relevant products that the user wants to outsmart them, in that company.
        Then identifying what is the advantages of each product and its weaknesses.

        The Company is: {state['companyName']}
        The Market Type is: {state['marketIntent'].marketType}
        The Market Description is: {state['marketIntent'].description}
        The Product is: {state['marketIntent'].product}
        
        Tools:
            - search: Usefull tool for searching the internet.
        Instructions:
            - Use Think-> Act-> Observe patter and use the tools only 2->4 times until you reach your goal.
            - Search about anything you don't know to accuratlly know what related products that the company offers, to have better results.
            - Always search in KSA regions.
        Output:
            - A list of all the related product that company offers, with there advantages and weaknesses in this format:
                1 Product Name:
                    Advantage:
                    Weaknesses:
                2 Product Name:
                    Advantage:
                    Weaknesses:
                ...
                Until n Product
            - After that give us conclusion about what is the overall advantage of the company and its weaknesses in that market.
                Overall Advantage:
                Overall Weaknesses:
                """
        
        messages = state['messages']
        result = llm.invoke([SystemMessage(sys_prompt)]+ messages +[SystemMessage("Follow the above instructions.")])
        messages.append(result)
        state["messages"] = messages
        return state
    
    def outputParser(state:AgentState):
        message = state["messages"][-1]
        result = llm_with_structured_output.invoke(message.content)
        state["companyDetails"]= result
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
    #     output_file_path="CompanyAnalyzerGraph.png"
    # )
    return agent
    