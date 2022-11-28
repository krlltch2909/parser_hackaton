from datetime import datetime
from models.Event import Event


def create_event_messsage(event: Event) -> str:
    """
    Функция создает текст на основании переданного мероприятия 
    для отправки пользователю
    """
    message = ""
    message += f"<b>{event.title}</b>\n\n"
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
