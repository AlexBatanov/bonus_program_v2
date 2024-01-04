from aiogram import F, Router
from aiogram.types import Message
from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from db.models import Employee
from utils.crud import create_obj
from utils.update_data import update_data_user
from utils.user_valid import is_valid_data_user
from keyboards import kb
from utils.states import UserForm
from db.async_engine import async_session


user_router = Router()


@user_router.callback_query(F.data == "add_user")
async def input_employee_name(callback: types.CallbackQuery, state: FSMContext):
    """Объявляем состояние и запрашиваем имя и фамилию продавца"""
    await callback.message.answer(
        "Введи имя и фамилию продовца через пробел\n"
        "Пример: Иван Иванов",)
    await state.set_state(UserForm.name)


@user_router.message(UserForm.name)
async def set_name(message: Message, state: FSMContext):
    """Сохраняем имя и предлагаем ввести telegram_id"""
    await state.update_data(name=message.text)
    await state.set_state(UserForm.telegram_id)
    await message.answer(
        "Введи телеграм_id сотрудника, только цифры"
    )


@user_router.message(UserForm.telegram_id)
async def set_telegram_id(message: Message, state: FSMContext):
    """Сохраняем id в форму и справшиваем делать админом или нет"""
    await state.update_data(telegram_id=message.text)
    await state.set_state(UserForm.is_admin)
    await message.answer(
        "Сделать администратором?",
        reply_markup=kb.is_admin()
    )


@user_router.callback_query(F.data == "is_admin_true")
async def set_employee_admin(callback: types.CallbackQuery, state: FSMContext):
    """Устанавливаем админом"""
    await state.set_state(UserForm.is_admin)
    await state.update_data(is_admin=True)
    await callback.answer()
    await output_data_employee(callback, state)


@user_router.callback_query(F.data == "is_admin_false")
async def output_data_employee(callback: types.CallbackQuery, state: FSMContext):
    """Выводим введенные данные и предлогаем сохранить"""
    data = await state.get_data()
    message_error = await is_valid_data_user(data)
    if message_error:
        await callback.message.answer(
            f'{message_error}\n нажми на команду /start что бы продолжить работу')
        return
    await callback.message.answer(
        f"{data.get('name')}\n"
        f"Телеграм_id: {data.get('telegram_id')}\n"
        f"Администратор: {'Да' if data.get('is_admin') else 'Нет'}",
        reply_markup=kb.save_user()
    )
    await callback.answer()


@user_router.callback_query(F.data == "save_user")
async def save_employee(callback: types.CallbackQuery, state: FSMContext):
    """Выводим введенные данные и предлогаем сохранить"""
    data = update_data_user(await state.get_data())
    user = Employee(**data)
    await create_obj(async_session, user)
    await state.clear()
    await callback.answer()
    await callback.message.answer("Сотрудник добавлен 👍",
                                #   reply_markup=repeat()
                                  )
