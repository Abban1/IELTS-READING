from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# List all models your key can access
models = client.models.list()

for m in models:
    # Print the model name and its metadata (supports generation or chat)
    print("Model Name:", m.name)
    if hasattr(m, "capabilities"):
        print("Capabilities:", m.capabilities)
    print("---")
