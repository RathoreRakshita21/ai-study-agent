#Actionableitems , decision , questions 

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import os 
import time
from tenacity import retry, wait_exponential, stop_after_attempt

def get_llm():
    return ChatGroq(
        model="openai/gpt-oss-20b",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2,
        max_retries=0,
    )
@retry(
    wait=wait_exponential(multiplier=2, min=5, max=60),
    stop=stop_after_attempt(5)
)
def safe_invoke(chain, input_data):
    time.sleep(2)  # pace calls to stay under Groq's tokens-per-minute limit
    return chain.invoke(input_data)


def build_chain(system_prompt : str):
    llm = get_llm()
    return (
        RunnablePassthrough() | RunnableLambda(lambda x : {"text" : x}) |ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human","{text}"),
    ]) | llm |StrOutputParser()
    )

def extract_action_items(transcript:str)->str:
    chain = build_chain(
         "You are an expert video analyst. From the video transcript, "
        "extract all action items. For each provide:\n"
        "- Task description\n"
        "- Owner (who is responsible)\n"
        "- Deadline (if mentioned, else write 'Not specified')\n\n"
        "Format as a numbered list. If none found say 'No action items found.'"
    )

    return safe_invoke(chain, transcript)


def extract_key_decisions(transcript: str) -> str:
    chain = build_chain(
        "You are an expert video analyst. From the video transcript, "
        "extract all key decisions made. Format as a numbered list. "
        "If none found say 'No key decisions found.'"
    )
    return safe_invoke(chain, transcript)


def extract_questions(transcript: str) -> str:
    chain = build_chain(
        "From the video transcript, extract all unresolved questions "
        "or topics needing follow-up. Format as a numbered list. "
        "If none found say 'No open questions found.'"
    )
    return safe_invoke(chain, transcript)