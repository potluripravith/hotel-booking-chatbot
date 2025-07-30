import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

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