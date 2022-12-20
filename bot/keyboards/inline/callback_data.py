from aiogram.utils.callback_data import CallbackData


event_type_data = CallbackData("event_type", "type_code", "page_number")
tag_data = CallbackData("event_tag", "type_code", "page_number")
event_list_data = CallbackData("event_list", "page_number")
mailing_type_data = CallbackData("mailing_type", "type")
mailing_status_data = CallbackData("mailing_status", "status")
action_button_data = CallbackData("action", "type")
