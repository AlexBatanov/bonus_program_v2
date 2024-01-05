from aiogram.utils.keyboard import InlineKeyboardBuilder


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

def sale_buyer():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Провести продажу", callback_data="saly"
    )
    builder.button(
        text="Обращение по гарантии", callback_data="warranty"
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