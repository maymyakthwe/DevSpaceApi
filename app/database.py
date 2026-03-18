from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

client = AsyncIOMotorClient(MONGO_URL)

db = client["mydatabase"]

projects_collection = db["projects"]
user_collection = db["users"]
profile_collection = db["profile"]
