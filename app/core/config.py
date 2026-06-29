from pydantic_settings import BaseSettings
import os 
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    #openai_api_key: str
    model_name: str = os.getenv("OllAMA_MODEL_NAME")

settings = Settings()