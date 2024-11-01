import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_CONFIG = {
    "GEM_API_KEY": os.getenv("GEM_API_KEY")
}
