from fastapi import FastAPI, Request
from agents.agent import GitHubAgent # type: ignore

app = FastAPI()

agent = GitHubAgent()

@app.post("/v1/mcp")
async def mcp_query(request: Request):
    data = await request.json()
    user_input = data.get("input")

    if not user_input:
        return {"error": "No input provided."}

    output = agent.run({"input": user_input})
    return {"response": output}
