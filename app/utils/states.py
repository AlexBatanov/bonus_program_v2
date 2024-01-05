from aiogram.filters.state import StatesGroup, State


class BuyerForm(StatesGroup):
    number = State()
    name = State()
    bonus_points = State()
#     films = State()
#     last_cheque = State()
#     employee = State()

class ChequeForm(StatesGroup):
    amount = State()
    films = State()
    buyers = State()
    employee = State()

# class BuyerUpdateForm(StatesGroup):
#     number = State()
#     name = State()
#     films = State()
#     last_cheque = State()
#     bonus_points = State()
#     last_employee = State()

# class BuyerWarrantyForm(StatesGroup):
#     films = State()
#     number = State()

class UserForm(StatesGroup):
    telegram_id = State()
    name = State()
    is_admin = State()

# class EmployeeBanForm(StatesGroup):
#     telegram_id = State()