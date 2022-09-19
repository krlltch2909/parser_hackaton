import requests
from datetime import datetime
from main.models import Event, EventTypeClissifier, StatusOfEvent


# Получаем хакатоны
def get_events():
    response = requests.get('https://leadersofdigital.ru/api/v1/site_get_all/0')
    data = response.json()
    raw_events = data['event']
    events = []
    print(raw_events)
    # for raw_event in raw_events:
    #     event = Event.objects.create()
    #     event.title = raw_event['name']
    #     event.description = raw_event['description']
    #     raw_event_start_date = event['timeline_steps'][0]['start']
    #     event.start_date = datetime.fromisoformat(raw_event_start_date)
    #     raw_event_end_date = event['timeline_steps'][len(event['timeline_steps'])-1]['start']
    #     event.end_date = datetime.fromisoformat(raw_event_end_date)
    #     event.url = f'https://leadersofdigital.ru/event/{event["event_id"]}'
    #     event.type_of_event = EventTypeClissifier.objects.get(id=2) # hackaton
    #     event.status_of_event = StatusOfEvent.objects.get(id=3) # unavailable
    #     events.append(event)
    return events
    
if __name__ == '__main__':
    print(get_events())