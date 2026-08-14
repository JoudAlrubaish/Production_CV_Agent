from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from agent.prompts import SYSTEM_PROMPT
from agent.tools import TOOL_SCHEMAS, ToolError, execute_tool_call_json

load_dotenv()


def build_client() -> OpenAI:
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise RuntimeError("LLM_API_KEY is missing. Add it to your .env file.")

    base_url = os.getenv("LLM_BASE_URL") or None
    return OpenAI(api_key=api_key, base_url=base_url)


def run_agent(
    user_message: str,
    *,
    client: OpenAI | None = None,
    model: str | None = None,
    max_tool_rounds: int = 5,
) -> str:
    """Run an OpenAI-compatible tool-calling agent grounded in FastAPI tools."""
    client = client or build_client()
    model = model or os.getenv("LLM_MODEL", "gpt-4o-mini")

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    for _ in range(max_tool_rounds):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
            temperature=0,
        )

        message = response.choices[0].message
        messages.append(message.model_dump(exclude_none=True))

        if not message.tool_calls:
            return message.content or ""

        for tool_call in message.tool_calls:
            try:
                tool_result = execute_tool_call_json(
                    tool_call.function.name,
                    tool_call.function.arguments,
                )
            except ToolError as exc:
                tool_result = f'{{"error": "{str(exc)}"}}'

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                }
            )

    return "The request required too many tool-calling rounds and was stopped safely."


def main() -> None:
    print("Production CV Agent is ready. Type 'exit' to stop.")
    print("Example: What model is currently deployed?")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue

        try:
            answer = run_agent(user_input)
            print(f"Agent: {answer}")
        except Exception as exc:
            print(f"Agent error: {exc}")


if __name__ == "__main__":
    main()