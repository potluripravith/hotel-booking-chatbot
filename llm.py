import os
import json

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI1_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
DEFAULT_SYSTEM_PROMPT = "You are a helpful hotel booking assistant."

EXTRACTION_PROMPT = """
You are an assistant that extracts hotel booking information from user queries.

Return a JSON object with these three keys:
- "dates": a list of dates in YYYY-MM-DD format (example: ["2025-08-01", "2025-08-02"])
- "room_type": the room type as a lowercase string ("single", "double", "suite"), or null if not mentioned.
- "room_count": an integer indicating number of rooms requested, or 1 if not mentioned.

Handle relative dates like "tomorrow", "next weekend", "August 5 to 7", etc.
Assume today's date is 2025-07-29 for all relative date calculations.
Correct any spelling errors in room types.
If the number of rooms is not clearly mentioned, default to 1.
Return only the JSON object, no extra explanation.
"""


def call_deepseek(user_message: str, system_prompt: str = "You are a helpful hotel booking assistant.") -> str:
    """
    Sends a message to the DeepSeek model and returns the generated reply.

    Args:
        user_message (str): The message from the user.
        system_prompt (str): The system prompt (default is hotel assistant).

    Returns:
        str: The assistant's reply.
    """
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    return response.choices[0].message.content


def extract_booking_info(user_message: str) -> dict:
    """
    Uses LLM to extract booking dates, room type, and room count from the user message.

    Args:
        user_message (str): The message from the user.

    Returns:
        dict: {"dates": [...], "room_type": ..., "room_count": ...}
    """
    try:
        raw_response = call_deepseek(user_message, EXTRACTION_PROMPT)

        # If it's already a dict (e.g., in tests), skip parsing
        if isinstance(raw_response, dict):
            data = raw_response
        else:
            if raw_response.strip().startswith("```"):
                raw_response = (
                    raw_response.strip()
                    .removeprefix("```json")
                    .removeprefix("```")
                    .removesuffix("```")
                    .strip()
                )
            data = json.loads(raw_response)

        return {
            "dates": data.get("dates", []),
            "room_type": data.get("room_type"),
            "room_count": data.get("room_count")
        }

    except json.JSONDecodeError:
        print(f"[ERROR] Failed to parse LLM response as JSON:\n{raw_response}")
        return {"dates": [], "room_type": None, "room_count": None}
    except Exception as e:
        print(f"[ERROR] Unexpected error in extract_booking_info: {e}")
        return {"dates": [], "room_type": None, "room_count": None}
