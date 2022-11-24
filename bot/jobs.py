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
                    event_message = "<b>Новое мероприятие!</b>\n" + event_message
                    need_to_send = False
                    try:
                        if user_preferences["mailing_type"] == "all":
                            need_to_send = True
                        else:
                            user_events_codes = user_preferences["events_types"]
                            user_tags_codes = user_preferences["tags"]
                            event_code = new_event.type_of_event.type_code
                            tags_codes = map(lambda x: x.type_code, new_event.tags)
                            matched_by_tag = \
                                any(item in user_tags_codes for item in tags_codes)
                            matched_by_event_code = event_code in user_events_codes
                            if len(user_events_codes) != 0 and len(user_tags_codes) != 0:
                                if matched_by_tag and matched_by_event_code:
                                    need_to_send = True
                            elif len(user_events_codes) != 0 and matched_by_event_code:
                                need_to_send = True
                            elif len(user_tags_codes) != 0 and matched_by_tag:
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
