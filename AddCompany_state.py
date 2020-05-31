from aiogram.dispatcher.filters.state import StatesGroup, State


# Class for take list companies which user enter after he enter command 'addcompany'
class AddCompany(StatesGroup):
    Q1 = State()

