import os
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_aws import ChatBedrockConverse
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

async def call_agent(user_input):
    model = ChatBedrockConverse(
        model="us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    )

    async with MultiServerMCPClient(
        {
            "weather": {
                "url": os.environ['MCP_SERVER_ENDPOINT'],
                "transport": "sse",
            }
        }
    ) as client:
        # Create the agent with tools
        agent = create_react_agent(model, client.get_tools())
        
        # Simple invocation without callbacks
        response = await agent.ainvoke({"messages": user_input})

        return response
        
if __name__ == "__main__":
    user_input = input("Enter your input: ")
    response = asyncio.run(call_agent(user_input))

    for message in response["messages"]:
        print(message.content)
