import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Test API Key
api_key = os.getenv("SARVAM_API_KEY")
print(
    "API Key Loaded Successfully!"
    if api_key
    else "API Key Missing in .env file"
)

# Test function/import from transcriber
from core.transcriber import transcribe_all

print("Imports working fine!")