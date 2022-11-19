import os
import sys
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient


DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")
DATABASE_NAME = os.getenv("DATABASE_NAME")

if DB_CONNECTION_STRING is None or DATABASE_NAME is None:
    sys.exit("Incorrect database connection parameters")

sync_client = MongoClient(DB_CONNECTION_STRING)
sync_db = sync_client[DATABASE_NAME]
sync_user_preferences_collection = sync_db["user_preferences"] 
client = AsyncIOMotorClient(DB_CONNECTION_STRING)
db = client.get_database(DATABASE_NAME)
user_preferences_collection = db.get_collection("user_preferences")
