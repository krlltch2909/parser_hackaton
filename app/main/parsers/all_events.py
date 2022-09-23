import requests


def get_all_events():
    response = requests.get("https://all-events.ru/events/calendar/theme-is-informatsionnye_tekhnologii")
    print(response.content)
