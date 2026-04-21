import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "llama-3.1-8b-instant"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"