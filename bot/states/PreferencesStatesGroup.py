from aiogram.dispatcher.filters.state import StatesGroup, State


class PreferencesStatesGroup(StatesGroup):
    events_types = State()
    tags = State()
