from aiogram.dispatcher.filters.state import StatesGroup, State


class EventStatesGroup(StatesGroup):
    field = State()
