from aiogram import F, Router
from aiogram.types import Message
from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from db.models import Employee
from utils.crud import create_obj, get_obj, update_obj
from utils.update_data import update_data_user
from utils.validators import is_valid_data_user, is_valid_tg_id
from keyboards import kb
from utils.states import BannedForm, UserForm
from db.async_engine import async_session


user_router = Router()


# Начало блока регистрации сотрудника
@user_router.message(F.text.lower() == "добавить сотрудника")
async def input_employee_name(message: types.Message, state: FSMContext):
    """Объявляем состояние и запрашиваем имя и фамилию продавца"""
    await message.answer(
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
    await callback.message.answer(
        "Сотрудник добавлен 👍"
    )


# Начало блока блокировки\разблокировки сотрудника
@user_router.message(F.text.lower() == 'заблокировать/разблокировать сотрудника')
async def start_banned_user(message: Message, state: FSMContext):
    """Запрашиваем телеграмм_id сотрудника для блокировки/разблокировки"""
    await state.set_state(BannedForm.tg_id)
    await message.answer(
        "Введи телеграм_id сотрудника, только цифры"
    )


@user_router.message(BannedForm.tg_id)
async def banned_user(message: Message, state: FSMContext):
    """Валедируем tg_id, чекаем сотрудника"""
    err_message = is_valid_tg_id(message.text)
    if err_message:
        await message.answer(err_message)
        return
    employee = await get_obj(async_session, Employee, 'telegram_id', message.text)
    if not employee:
        await message.answer('Сотрудника с таким id нет')
        return
    await state.update_data(employee=employee)
    if employee.is_banned:
        await message.answer(
            f'Сотрудник: {employee.first_name} {employee.last_name}',
            reply_markup=kb.unlock()
        )
    else:
        await message.answer(
            f'Сотрудник: {employee.first_name} {employee.last_name}',
            reply_markup=kb.block()
        )


@user_router.callback_query(F.data == "block")
async def save_block_user(callback: types.CallbackQuery, state: FSMContext):
    """Баннем сотрудника и сохраняем"""
    await block_unlock(callback, state, True)


@user_router.callback_query(F.data == "unlock")
async def save_block_user(callback: types.CallbackQuery, state: FSMContext):
    """Разбаниваем сотрудника и сохраняем"""
    await block_unlock(callback, state, False)


async def block_unlock(callback: types.CallbackQuery, state: FSMContext, is_banned: bool):
    """Блокировка/разблокировка сотрудника"""
    data = await state.get_data()
    employee = data.get('employee')
    employee.is_banned = is_banned
    await update_obj(async_session, employee)
    await state.clear()
    await callback.answer()
    if is_banned:
        await callback.message.answer(
            "Сотрудник заблокирован",
        )
    else:
        await callback.message.answer(
            "Сотрудник разаблокирован",
        )
