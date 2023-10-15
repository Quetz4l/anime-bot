from aiogram.dispatcher.filters.state import StatesGroup, State

class Questions(StatesGroup):
    how_many_series_user_watch = State()
