from pathlib import Path
import os
from dotenv import load_dotenv

ROOT_DIR=Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")

LLM_API_KEY=os.getenv("LLM_API_KEY","")
LLM_BASE_URL=os.getenv("LLM_BASE_URL","https://api.deepseek.com")
LLM_MODEL=os.getenv("LLM_MODEL","deepseek-v4-flash")
MAX_RESEARCH_STEPS=int(os.getenv("MAX_RESEARCH_STEPS","12"))
MAX_CRITIC_ROUNDS=int(os.getenv("MAX_CRITIC_ROUNDS","2"))

SEARCH_API_KEY = os.getenv("SEARCH_API_KEY", "")
SEARCH_PROVIDER = os.getenv("SEARCH_PROVIDER", "tavily")
USE_MCP = os.getenv("USE_MCP", "0").strip() in ("1", "true", "True", "yes")