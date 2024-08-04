# Set env var OPENAI_API_KEY or load from a .env file:
import dotenv
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

chat = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
