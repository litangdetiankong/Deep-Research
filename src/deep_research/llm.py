from __future__ import annotations

from openai import OpenAI

from deep_research.config import LLM_API_KEY,LLM_BASE_URL,LLM_MODEL

def get_client()->OpenAI:
    return OpenAI(api_key=LLM_API_KEY,base_url=LLM_BASE_URL)

def chat(messages:list[dict],temperature:float=0.2)->str:
    client=get_client()
    resp=client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        temperature=temperature,
    )
    return resp.choices[0].message.content or ""
