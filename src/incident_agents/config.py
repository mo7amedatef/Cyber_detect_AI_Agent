import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise RuntimeError(
        "Missing GROQ_API_KEY. Create a .env file from .env.example and set GROQ_API_KEY."
    )

# using llama-3.3-70b for its advanced reasoning capabilities
llm = ChatGroq(
    temperature=0, 
    model_name="llama-3.3-70b-versatile",
    groq_api_key=groq_api_key
)
