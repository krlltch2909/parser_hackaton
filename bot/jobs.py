import aiogram
import asyncio
import logging
import os
from loader import bot
from database import user_preferences_collection
from utils.parser_api import get_updates
from utils.create_event_message import create_event_messsage
from models.User import User


CRAWLING_INTERVAL = os.getenv("API_CRAWLING_INTERVAL")
CRAWLING_INTERVAL = int(CRAWLING_INTERVAL) if CRAWLING_INTERVAL is not None else 30
logger = logging.getLogger(f"root.{__name__}")


async def send_new_events():
    while True:  
        new_events = await get_updates()
        logger.info(f"{len(new_events)} new events received")
        
        async for user_preferences in user_preferences_collection.find({}):
            user = User.parse_obj(user_preferences)
            
            if user.agreed_to_mailing():   
                for new_event in new_events:  
                    event_message = create_event_messsage(new_event)
                    event_message = "<b>Новое мероприятие!</b>\n" + event_message
                    try:
                        if user.agreed_to_accept_event(new_event):
                            await bot.send_message(user.id, 
                                                   event_message, 
                                                   parse_mode="HTML",
                                                   disable_web_page_preview=True)
                            
                    except aiogram.utils.exceptions.BotBlocked:
                        await user.delete()
                        break
        await asyncio.sleep(CRAWLING_INTERVAL)    
