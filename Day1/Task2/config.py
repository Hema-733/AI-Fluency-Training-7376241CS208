import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "groq")
MODEL = os.getenv("MODEL", "llama-3.1-8b-instant")

if PROVIDER == "groq":
    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )
else:
    raise ValueError("Unsupported provider")

print("Provider:", PROVIDER)
print("Model:", MODEL)