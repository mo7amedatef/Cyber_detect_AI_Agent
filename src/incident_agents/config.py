import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# using llama-3.3-70b for its advanced reasoning capabilities
llm = ChatGroq(
    temperature=0, 
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)