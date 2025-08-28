from langgraph.graph import START, END, StateGraph
from .schema import AgentState,CompetitorCompanyList
from langchain_google_genai  import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode, tools_condition
from ..tools.searchTool import getSearchTool
from dotenv import load_dotenv

load_dotenv()

def getCompetitorResearcherAgent():

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    search = getSearchTool()
    tools = [search]

    llm_with_tools = llm.bind_tools(tools)
    llm_with_structured_output = llm.with_structured_output(CompetitorCompanyList)

    def competitivesFinder(state:AgentState)->AgentState:
        """An agent can find all competitors companies in a given market.""" 
        sys_prompt = f"""
        You are a market analyzer Agent, your task is to find a list of competitors companies in {state['marketIntent'].marketType} market, the domanating companies.
        select from 5 to 10 at most companies don't increase than that number and foucs on the dominatings companies.
        {state['marketIntent'].marketType} market is: {state['marketIntent'].description}
        Tools:
            - search: To search the internet about anything you don't know.
        Instructions:
            - Use Think-> Act-> Observe patter and use the tools only 2->4 times until you reach your goal.
            - Always search in KSA regions.
            - YOU MUST FINDS AND LIST ALL THE COMPANIES IN THAT market.
        output:
            - List of Companies names. in this format:
                1 - Company Name: 'The name of the competitive company'                
                2 - Company Name: 'The name of the competitive company'
                ...
                until n company.
                    
        """
        messages = state['messages']
        response = llm_with_tools.invoke([SystemMessage(sys_prompt)]+messages+[SystemMessage("Don't forget to follow the above instructions")])
        messages.append(response)
        state['messages'] = messages

        return state

    def outputParser(state:AgentState)->AgentState:
        message = state['messages'][-1].content
        response = llm_with_structured_output.invoke(message)
        state['competitorCompanies'] = response
        return state
    
    graph = StateGraph(AgentState)
    graph.add_node("competitivesFinder", competitivesFinder)
    graph.add_node("tools",ToolNode(tools)) 
    graph.add_node("outputParser",outputParser)

    graph.add_edge(START,"competitivesFinder")
    graph.add_conditional_edges(
        "competitivesFinder",
        tools_condition,
            {
            "tools":"tools",
                END:"outputParser"
                })
    graph.add_edge("tools","competitivesFinder")
    graph.add_edge("outputParser",END)


    agent  = graph.compile()
    # agent.get_graph().draw_mermaid_png(
    #     output_file_path="graph.png"
    # )
    return agent
    
        






