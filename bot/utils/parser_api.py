import aiohttp
import logging
import os
import sys
from loader import token
from aiohttp.client_exceptions import ClientConnectionError
from models import *


logger = logging.getLogger(f"root.{__name__}")
_headers = {
        "Authorization": "Token " + token
}
API_BASE_URL = os.getenv("API_BASE_URL")
if API_BASE_URL is None:
    sys.exit("Incorrect API url")


def api_request_error_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ClientConnectionError:
            logger.error("Can't connect to server")
            return []
    wrapper.__name__ == func.__name__
    return wrapper


@api_request_error_handler
async def get_events_types() -> list[EventType]:
    url = API_BASE_URL + "hackaton/types/"

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=_headers) as response:
            data = await response.json(content_type="application/json")
            events_types = []
            for raw_event_type in data:
                events_types.append(EventType.parse_obj(raw_event_type))
            return events_types
        

@api_request_error_handler
async def get_events() -> list[Event]:
    url = API_BASE_URL + "hackaton/"

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=_headers) as response:
            data = await response.json(content_type="application/json")
            events = []
            for raw_event in data:
                events.append(Event.parse_obj(raw_event))
            return events


@api_request_error_handler
async def get_events_by_preferences(events_types: list[int], tags: list[int]) -> list[Event]:
    url = API_BASE_URL + "hackaton/?"

    for event_type in events_types:
        url += f"type_of_event={event_type}&"

    for tag in tags:
        url += f"tags={tag}&"
    
    url = url[:-1]
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=_headers) as response:
            data = await response.json(content_type="application/json")
            events = []
            for raw_event in data:
                events.append(Event.parse_obj(raw_event))
            return events


@api_request_error_handler
async def get_tags() -> list[EventTag]:
    url = API_BASE_URL + "hackaton/tags/"

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=_headers) as response:
            data = await response.json(content_type="application/json")
            tags = []
            for raw_tag in data:
                tags.append(EventTag.parse_obj(raw_tag))
            return tags


@api_request_error_handler
async def get_updates() -> list[Event]:
    """
    Функция для получения новых мероприятий.
    Используется для рассылки
    """
    url = API_BASE_URL + "hackaton/update/"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=_headers) as response:
            data = await response.json(content_type="application/json")        
            events = []
            for raw_event in data:
                events.append(Event.parse_obj(raw_event))
            return events
