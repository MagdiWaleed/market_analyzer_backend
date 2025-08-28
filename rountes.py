
from flask import request
from langchain_core.messages import HumanMessage
from marketAnalyzerAgent.agent import getMarketAnalyzerAgent
from tools.tools import toMap
import json

def registerRoutes(app):
    marketResearcherAgent = getMarketAnalyzerAgent()


    @app.route("/analyze",methods = ["POST"])
    def analyze():
        data = request.get_json()
        message = data['message']
        result = marketResearcherAgent.invoke({"messages":[HumanMessage(message)]})
        data = {"data":toMap(result)}
        return  json.dumps(data), 200
    


    @app.route("/")
    def main():
        return {"message":"hi"}