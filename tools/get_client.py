import os
from openai import OpenAI


def get_client() -> OpenAI:
    token = os.environ.get("GITHUB_TOKEN")
    return OpenAI(base_url="https://models.inference.ai.azure.com", api_key=token)
