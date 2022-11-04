from datetime import datetime
from utils.parser_api import get_events_types, get_tags


# В проекте будет асинхронным
async def create_event_messsage(event_data: dict) -> str:
    message = ""
    message += f"<b>{event_data['title']}</b>\n\n"
    message += f"<i>Место проведения:</i> {event_data['address']}\n\n"
    if event_data["start_date"] is not None and event_data["end_date"] is not None:
        start_datetime = datetime.fromisoformat(event_data["start_date"])
        end_datetime = datetime.fromisoformat(event_data["end_date"])
        message += (f"<i>Даты проведения:</i> {start_datetime.strftime('%d.%m.%Y')}" \
            f" - {end_datetime.strftime('%d.%m.%Y')}" + "\n\n")
    if event_data["registration_deadline"] is not None:
        registration_datetime = datetime.fromisoformat(event_data["registration_deadline"])
        message += f"<i>Окончание регистрации:</i> {registration_datetime.strftime('%d.%m.%Y')}\n\n"
    if event_data["is_free"] is not None:
        if event_data["is_free"]:
            message += "<i>Стоимость участия:</i> Бесплатно\n\n"
        else:
            message += "<i>Стоимость участия:</i> Платно\n\n"
    events_types = await get_events_types()
    for event_type in events_types:
        if event_type.type_code == event_data["type_of_event"]:
            message += f"<i>Тип мероприятия: </i>{event_type.description}\n\n"
    events_tags = await get_tags()
    for event_tag in events_tags:
        if event_tag.type_code in event_data["tags"]:
            message += f"#{event_tag.description}  "
    message += "\n\n"
    message += f"<a href=\"{event_data['url']}\">Подробнее</a>\n"
    return message
