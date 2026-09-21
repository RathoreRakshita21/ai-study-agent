import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
)

print("Sending a test request to Groq...")
response = llm.invoke("Say hello in one sentence.")
print("SUCCESS:", response.content)