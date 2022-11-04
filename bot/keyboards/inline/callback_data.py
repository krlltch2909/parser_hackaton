from aiogram.utils.callback_data import CallbackData


event_type_data = CallbackData("event_type", "type_code", "button_type")
tag_data = CallbackData("event_tag", "type_code", "button_type")
event_list_data = CallbackData("event_list", "button_type")
mailing_type_data = CallbackData("mailing_type", "type")
mailing_status_data = CallbackData("mailing_status", "status")
