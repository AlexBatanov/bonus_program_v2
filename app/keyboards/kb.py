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
    builder.button(
        text="Отменить", callback_data="cancel"
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
            types.KeyboardButton(text="Добавить сотрудника"),
            types.KeyboardButton(text="Заблокировать/разблокировать сотрудника"),
        ],
        [
            types.KeyboardButton(text="Статистика"),
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
            types.KeyboardButton(text="Отмена"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Галя у нас отмена"
    )
    return keyboard