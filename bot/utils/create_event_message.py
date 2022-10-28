def create_event_messsage(event_data) -> str:
    message = ""
    message += (f"<b>{event_data['title']}</b>\n\n")
    message += (event_data["description"] +  "\n\n")
    message += f"Адрес мероприятия: {event_data['address']}\n\n"
    message += event_data["url"]

    return message
