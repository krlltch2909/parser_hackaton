import os
from loader import timeloop
from datetime import timedelta
from utils.database import sync_user_preferences_collection


ENV_SECONDS = os.getenv("API_CRAWLING_INTERVAL")
ENV_SECONDS = float(ENV_SECONDS) if ENV_SECONDS is not None else 30


@timeloop.job(interval=timedelta(seconds=ENV_SECONDS))
def send_new_events():
    users_preferences = sync_user_preferences_collection.find({})
    for user_preferences in users_preferences:
        print(user_preferences["_id"])
