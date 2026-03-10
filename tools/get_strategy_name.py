from openai import OpenAI
from get_existing_strategy_names import get_existing_strategy_names


def get_strategy_name(client: OpenAI) -> str:
    existing = get_existing_strategy_names()
    exclusion = (
        f" Do NOT suggest any of these already-existing strategies: {', '.join(existing)}."
        if existing else ""
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": (
                    "Name one popular quantitative trading strategy with the words "
                    "separated by \"_\". Reply with only the strategy name, nothing else."
                    + exclusion
                ),
            }
        ],
        max_tokens=32,
    )
    return (response.choices[0].message.content or "").strip()
