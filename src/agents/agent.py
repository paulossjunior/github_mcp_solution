from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from src.tools.repository.github_milestones_tool import GitHubMilestoneTool
from tools.repository.github_issue_tool import GitHubIssueTool
from tools.repository.generate_report_tool import GenerateReportTool
from tools.repository.list_all_milestones_and_issues_tool import ListAllMilestonesAndIssuesTool
from tools.repository.generate_developer_report_tool import  GenerateDevelopersReportTool
from tools.project.github_projects_tool import GitHubProjectsV2Tool
from tools.project.list_projects_cards_milestones_tool import ListProjectsCardsMilestonesTool
from tools.project.generate_projects_report_tool import GenerateProjectsReportTool
import os
from dotenv import load_dotenv


load_dotenv()

class GitHubAgent():
    def __init__(self):
        

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        tools = [
            GitHubMilestoneTool(),
            GitHubIssueTool(),
            GenerateReportTool(),
            ListAllMilestonesAndIssuesTool(),
            GenerateDevelopersReportTool(),
            GitHubProjectsV2Tool(),
            ListProjectsCardsMilestonesTool(),
            GenerateProjectsReportTool()
        ]


        self.agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            memory=memory,
            verbose=True,
            return_direct=True
        )
    def run(self, input:str):
        return self.agent.run(input)