from openai import OpenAI  # Import the client class
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"  # Correct parameter name
)

response = client.chat.completions.create(  # Use client instance
    model="deepseek/deepseek-chat-v3-0324:free",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a joke about robots."}
    ]
)

print(response.choices[0].message.content)