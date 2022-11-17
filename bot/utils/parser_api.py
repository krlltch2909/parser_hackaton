import aiohttp
import os
from typing import List
from loader import token
from models.EventType import EventType
from models.EventTag import EventTag


_headers = {
        "Authorization": "Token " + token
    }


async def get_events_types() -> List[EventType]:
    url = os.getenv("API_BASE_URL") + "hackaton/types/"

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=_headers) as response:
            data = await response.json(content_type=None)
            events = []
            for raw_event in data:
                events.append(EventType(raw_event["description"], 
                    raw_event["type_code"]))
            
            return events


async def get_events() -> dict:
    url = os.getenv("API_BASE_URL") + "hackaton/"

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=_headers) as response:
            data = await response.json(content_type=None)
            return data


async def get_events_by_preferences(events_types: List[int], tags: List[int]) -> dict:
    url = os.getenv("API_BASE_URL") + "hackaton/?"

    for event_type in events_types:
        url += f"type_of_event={event_type}&"

    for tag in tags:
        url += f"tags={tag}&"

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=_headers) as response:
            data = await response.json(content_type=None)
            return data


async def get_tags() -> List[EventTag]:
    url = os.getenv("API_BASE_URL") + "hackaton/tags/"

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=_headers) as response:
            data = await response.json(content_type=None)

            tags = []
            for raw_tag in data:
                tags.append(EventTag(raw_tag["description"], 
                    raw_tag["tag_code"]))
            
            return tags
