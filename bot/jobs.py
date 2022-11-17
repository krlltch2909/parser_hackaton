import os
from loader import timeloop
from datetime import timedelta
from utils.database import sync_user_preferences_collection


@timeloop.job(interval=timedelta(seconds=os.getenv("API_CRAWLING_INTERVAL")))
def send_new_events() -> None:
    users_preferences = sync_user_preferences_collection.find({})
    count = sync_user_preferences_collection.count_documents({})

    for user_preferences in users_preferences:
        pass        
