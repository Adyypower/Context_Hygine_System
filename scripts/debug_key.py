import os
from dotenv import load_dotenv
from pathlib import Path
# import google.generativeai as genai # Commented out

# Explicitly load .env
env_path = Path(__file__).parent.parent / ".env"
print(f"Loading .env from: {env_path}")
load_dotenv(dotenv_path=env_path, override=True)

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("ERROR: GOOGLE_API_KEY not found in environment.")
    exit(1)

print(f"API Key found: '{api_key[:5]}...{api_key[-5:]}' (Length: {len(api_key)})")
print(f"Repr: {repr(api_key)}")

