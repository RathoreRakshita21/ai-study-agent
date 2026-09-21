from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

import os 
import time
from tenacity import retry, wait_exponential, stop_after_attempt

def get_llm():
    return ChatGroq(
        model="openai/gpt-oss-20b",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3,
        max_retries=0,
    )

@retry(
    wait=wait_exponential(multiplier=2, min=4, max=60),
    stop=stop_after_attempt(5)
)
def safe_invoke(chain, input_data):
    time.sleep(1.1)  # stay under the 1 request/second limit
    return chain.invoke(input_data)

def split_transcript(transcript: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 3000,
        chunk_overlap = 200
    )

    return splitter.split_text(transcript)

def summarize(transcript : str) -> str:
    llm = get_llm()

    map_prompt = ChatPromptTemplate.from_messages(
        [
        ("system", "Summarize this portion of a video transcript concisely."),
        ("human", "{text}"),
    ]
    )

    map_chain = map_prompt | llm | StrOutputParser()

    chunks = split_transcript(transcript)

    chunk_summaries = []
    for chunk in chunks:
        chunk_summaries.append(safe_invoke(map_chain, {"text": chunk}))
        time.sleep(1)

    combined = "\n\n".join(chunk_summaries)

    combined_prompt = ChatPromptTemplate.from_messages(
        [
        (
            "system",
            "You are an expert video summarizer. Combine these partial summaries "
            "into one final professional video summary in bullet points.",
        ),
        ("human", "{text}"),
    ]
    )

    combined_chain = (
        RunnablePassthrough() | RunnableLambda(lambda x:{"text":x}) | combined_prompt | llm | StrOutputParser()
    )

    return safe_invoke(combined_chain, combined)

def generate_title(transcript : str) -> str:
    llm = get_llm()

    

    title_chain = (
        RunnablePassthrough() | RunnableLambda(lambda x:{"text":x}) | 
        ChatPromptTemplate.from_messages([
             (
                "system",
                "Based on the meeting transcript, generate a short professional video title "
                "(max 8 words). Only return the title, nothing else.",
            ),
            ("human", "{text}"),
        ])
        | llm
        |StrOutputParser()
    )

    return safe_invoke(title_chain, transcript[:2000])



