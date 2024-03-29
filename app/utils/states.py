from aiogram.filters.state import StatesGroup, State


class BuyerForm(StatesGroup):
    number = State()
    name = State()
    bonus_points = State()


class ChequeForm(StatesGroup):
    amount = State()
    films = State()
    buyers = State()
    employee = State()


class UserForm(StatesGroup):
    telegram_id = State()
    name = State()
    is_admin = State()

class WarrantyForm(StatesGroup):
    cheque = State()
    films = State()

class ChangeUserForm(StatesGroup):
    tg_id = State()


class ChangeForm(StatesGroup):
    number = State()
    bonus = State()


class BonusForm(StatesGroup):
    percent = State()


class DateForm(StatesGroup):
    date = State()