import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
models = client.models.list()

print("Available models for your key:")
for m in models.data:
    print("-", m.id)