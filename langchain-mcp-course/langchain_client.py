import asyncio
import os

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)



async def main():
    print("Starting the application...")
    client = MultiServerMCPClient({
    "math": {
        "command": "python",
        "args": [os.getenv("MATH_SERVER_LOCATION")],
        "transport": "stdio"
    },
    "weather": {
        "url": "http://localhost:8000/sse",
        "transport": "sse",
        }
    })
    tools = await client.get_tools()
    agent = create_react_agent(llm, tools)
    result = await agent.ainvoke({"messages": [HumanMessage(content="What is 54 + 2 * 3?")]})
    print(result['messages'][-1].content)
     
if __name__ == "__main__":
    asyncio.run(main())