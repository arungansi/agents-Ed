from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv  

load_dotenv(override=True)
from_email = os.environ.get("FROM_EMAIL")
to_email = os.environ.get("TO_EMAIL")

def get_model():
    GEMINI_BASE_URL = os.environ.get("GEMINI_BASE_URL")
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)
    model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=gemini_client)
    return model
