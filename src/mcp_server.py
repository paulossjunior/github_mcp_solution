from fastapi import FastAPI, Request
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from tools.github_repository_tool import GitHubRepositoryTool
from tools.github_issue_tool import GitHubIssueTool
from tools.markdown_generator_tool import MarkdownGeneratorTool
from tools.generate_report_tool import GenerateReportTool
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

tools = [
    GitHubRepositoryTool(),
    GitHubIssueTool(),
    GenerateReportTool()  
]


agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

@app.post("/v1/mcp")
async def mcp_query(request: Request):
    data = await request.json()
    user_input = data.get("input")

    if not user_input:
        return {"error": "No input provided."}

    output = agent.run({"input": user_input})
    return {"response": output}
