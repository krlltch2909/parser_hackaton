import os
from motor.motor_asyncio import AsyncIOMotorClient


client = AsyncIOMotorClient(os.getenv("DB_CONNECTION_STRING"))
db = client.get_database("bot_db")
user_preferences_collection = db.get_collection("user_preferences")
