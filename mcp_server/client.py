import asyncio
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

http_url = "http://localhost:8000/mcp"

# Option 1: Inferred transport (default for HTTP URLs)
client_inferred = Client(http_url)

# Option 2: Explicit transport (e.g., to add custom headers)
# headers = {"Authorization": "Bearer mytoken"}
transport_explicit = StreamableHttpTransport(url=http_url)
client_explicit = Client(transport_explicit)

async def use_streamable_http_client(client):
    async with client:
        tools = await client.list_tools()
        print(f"Connected via Streamable HTTP, found tools: {tools}")

# asyncio.run(use_streamable_http_client(client_inferred))
asyncio.run(use_streamable_http_client(client_explicit))