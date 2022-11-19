import aiogram
import asyncio
import os
from loader import bot
from utils.database import user_preferences_collection
from utils.parser_api import get_updates
from utils.create_event_message import create_event_messsage


CRAWLING_INTERVAL = os.getenv("API_CRAWLING_INTERVAL")
CRAWLING_INTERVAL = int(CRAWLING_INTERVAL) if CRAWLING_INTERVAL is not None else 30


async def send_new_events():
    while True:  
        new_events = await get_updates()
        async for user_preferences in user_preferences_collection.find({}):
            id = user_preferences["_id"]
            if "mailing_status" in user_preferences and user_preferences["mailing_status"]:             
                for new_event in new_events:  
                    event_message = create_event_messsage(new_event)
                    event_message = "<b>Новое мероприятие!</b>" + event_message
                    need_to_send = False
                    try:
                        if user_preferences["mailing_type"] == "all":
                            need_to_send = True
                        else:
                            event_type_code = new_event.type_of_event.type_code
                            event_tags_codes = map(lambda x: x.type_code, new_event.tags)
                            if event_type_code in user_preferences["events_types"] \
                                or any(item in user_preferences["tags"] for item in event_tags_codes):
                                    need_to_send = True
                        if need_to_send:
                            await bot.send_message(id, 
                                                   event_message, 
                                                   parse_mode="HTML",
                                                   disable_web_page_preview=True)
                            
                    except aiogram.utils.exceptions.BotBlocked:
                        await user_preferences_collection.delete_one({"_id": id})
                        break
        await asyncio.sleep(CRAWLING_INTERVAL)    
