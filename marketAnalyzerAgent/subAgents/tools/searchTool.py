# from langchain_community.tools import DuckDuckGoSearchRun
# from langchain.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
# def getSearchTool():
#     wrapper = DuckDuckGoSearchAPIWrapper(region="xa-en",  max_results=4)
#     search = DuckDuckGoSearchRun(output_format="list", api_wrapper=wrapper)
#     return search

def getSearchTool():
    tool = TavilySearchResults(
    max_results=10,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True
)
    return tool