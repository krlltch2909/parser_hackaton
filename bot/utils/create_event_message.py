import os
from datetime import datetime
from models.Event import Event


MAX_ROW_LENGTH = os.getenv("EVENTS_ROW_MAX_LENGTH")
MAX_ROW_LENGTH = int(MAX_ROW_LENGTH) if MAX_ROW_LENGTH else 25 


def create_event_messsage(event: Event) -> str:
    """
    Функция создает текст сообщения на основании переданного мероприятия
    """
    message = ""
    message += f"<b>{__format_title(event.title, ' ')}</b>\n\n"
    if event.address is not None:
        message += f"<i>Место проведения:</i> {event.address}\n"
    if event.start_date is not None and event.end_date is not None:
        start_datetime = datetime.fromisoformat(event.start_date)
        end_datetime = datetime.fromisoformat(event.end_date)
        message += (f"<i>Даты проведения:</i> {start_datetime.strftime('%d.%m.%Y')}" \
            f" - {end_datetime.strftime('%d.%m.%Y')}" + "\n")
    if event.registration_deadline is not None:
        registration_datetime = datetime.fromisoformat(event.registration_deadline)
        message += f"<i>Окончание регистрации:</i> {registration_datetime.strftime('%d.%m.%Y')}\n"
    if event.is_free is not None:
        if event.is_free:
            message += "<i>Стоимость участия:</i> Бесплатно\n"
        else:
            message += "<i>Стоимость участия:</i> Платно\n"
    message += f"<i>Тип мероприятия: </i>{event.type_of_event.description}\n"
    for event_tag in event.tags:
        message += f"#{event_tag.description} \n"
    message += "\n"
    message += f"<a href=\"{event.url}\">Подробнее</a>\n"
    return message


def __format_title(title: str, words_separator: str) -> str:
    title_parts = title.split(words_separator)
    result_title_parts = []
    current_row = ""
    
    for part in title_parts:
        current_row += part + " "
        
        if len(current_row) >= MAX_ROW_LENGTH:
            result_title_parts.append(current_row)
            current_row = ""
    
    if len(current_row) != 0:
        result_title_parts.append(current_row)
    
    return "\n".join(result_title_parts)
