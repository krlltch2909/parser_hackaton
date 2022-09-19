import requests
from main.models import *

def get_events():
    response = requests.get('https://hacks-ai.ru/api/v2/hackathons/cards')
