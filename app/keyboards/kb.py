from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def is_admin():
    """Инлайн кнопки сделать админом"""
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Дa", callback_data="is_admin_true"
    )
    builder.button(
        text="Нет", callback_data="is_admin_false"
    )
    builder.adjust(2)
    return builder.as_markup()


def add_user():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Добавить сотрудника", callback_data="add_user"
    )
    builder.adjust(2)
    return builder.as_markup()


def save_user():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Сохранить сотрудника", callback_data="save_user"
    )
    builder.adjust(1)
    return builder.as_markup()


def sale_buyer(is_admin=False):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Провести продажу", callback_data="saly"
    )
    builder.button(
        text="Обращение по гарантии", callback_data="warranty"
    )
    if is_admin:
        builder.button(
            text="Изменить данные клиента", callback_data="change_buyer"
        )
    builder.adjust(1)
    return builder.as_markup()


def change_buyer():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Изменить количество баллов", callback_data="change_bonus"
    )
    builder.button(
        text="Изменить номер", callback_data="change_number"
    )
    builder.adjust(1)
    return builder.as_markup()


def save_sale():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Провести продажу", callback_data="save_saly"
    )
    builder.adjust(2)
    return builder.as_markup()


def numder_cheques(count):
    """Создание кнопок для выбора чека"""
    builder = InlineKeyboardBuilder()
    for i in range(1, count+1):
        builder.button(
            text=str(i), callback_data=f"number_{i-1}"
        )
    builder.adjust(4)
    return builder.as_markup()


def skip_films():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Пропустить", callback_data="skip_films"
    )
    builder.adjust(1)
    return builder.as_markup()


def block():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Заблокировать", callback_data="block"
    )
    builder.adjust(1)
    return builder.as_markup()


def unlock():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Разблокировать", callback_data="unlock"
    )
    builder.adjust(1)
    return builder.as_markup()


def admin_keys():
    kb = [
        [
            types.KeyboardButton(text="Начать продажу"),
        ],
        [
            types.KeyboardButton(text="Добавить сотрудника"),
            types.KeyboardButton(text="Редактировать сотрудника"),
        ],
        [
            types.KeyboardButton(text="Отчеты"),
            types.KeyboardButton(text="Изменить процент начисления"),
        ],
        [
            types.KeyboardButton(text="Отмена"),
        ],

    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Властвуй"
    )
    return keyboard


def cancel():
    kb = [
        [
            types.KeyboardButton(text="Начать продажу"),
        ],
        [
            types.KeyboardButton(text="Отмена"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Галя у нас отмена"
    )
    return keyboard


def mode_selection():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Блокировка/разблокировка", callback_data="unblock"
    )
    builder.button(
        text="В админы/из админов", callback_data="perk"
    )
    builder.adjust(1)
    return builder.as_markup()


def set_admin():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="В админы", callback_data="set_admin"
    )
    builder.adjust(1)
    return builder.as_markup()


def set_not_admin():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Из админов", callback_data="set_not_admin"
    )
    builder.adjust(1)
    return builder.as_markup()


def list_reports():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Список сотрудников", callback_data="list_employees"
    )
    builder.button(
        text="Список клиентов", callback_data="list_buyers"
    )
    builder.button(
        text="Инфа по чекам", callback_data="info_cheques"
    )
    builder.adjust(1)
    return builder.as_markup()


def report_cheques():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Все чеки", callback_data="all_cheques"
    )
    builder.button(
        text="Чеки за день", callback_data="cheques_today"
    )
    builder.button(
        text="Чеки за период", callback_data="cheques_for"
    )
    builder.adjust(1)
    return builder.as_markup()