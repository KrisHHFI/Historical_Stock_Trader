import sys
import os
from openai import OpenAI

def ask_copilot_for_strategy() -> str:
    token = os.environ.get("GITHUB_TOKEN")
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=token,
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": "Name one popular quantitative trading strategy with the words separated by \"_\". Reply with only the strategy name, nothing else.",
            }
        ],
        max_tokens=32,
    )
    return (response.choices[0].message.content or "").strip()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "start":
        print(ask_copilot_for_strategy())
