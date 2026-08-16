from tavily import TavilyClient
from deep_research.config import SEARCH_API_KEY

cilent=TavilyClient(api_key=SEARCH_API_KEY)
response=cilent.search("Whar is Model Context Protocol MCP?")
print(response)