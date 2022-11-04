from aiogram.dispatcher.filters.state import StatesGroup, State


class MailingPreferencesStatesGroup(StatesGroup):
    mailing_type = State()
    mailing_status = State()
