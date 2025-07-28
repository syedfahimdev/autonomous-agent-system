import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Application Settings
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

# Database Settings
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "./data/faiss_index")
MEMORY_PATH = os.getenv("MEMORY_PATH", "./data/memory")

# n8n Integration
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

# Check if required API key is set
if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY not found in environment variables.")
    print("Please set your OpenAI API key to use CrewAI.")
    print("You can set it as an environment variable or in a .env file.")

# Create data directories if they don't exist
os.makedirs("./data", exist_ok=True)
os.makedirs("./data/memory", exist_ok=True)
os.makedirs("./data/reports", exist_ok=True) 