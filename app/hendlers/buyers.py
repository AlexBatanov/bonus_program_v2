from datetime import datetime, timedelta, date

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from hendlers.start import check_buyer
from keyboards import kb
from utils.update_data import update_buyer, update_data_cheque
from utils.validators import is_valid_data_cheque_buyer, is_valid_number
from utils.states import BuyerForm, ChangeForm, ChequeForm, WarrantyForm
from utils.crud import create_obj, get_obj, get_obj_relation, update_obj
from db.async_engine import async_session
from db.models import Buyer, Cheque, Employee



buyer_router = Router()

# Регистрация клиента
@buyer_router.message(BuyerForm.name)
async def buyer_name(message: Message, state: FSMContext):
    """Устанавлием имя и записываем в бд клиента"""
    await state.update_data(name=message.text)
    data = await state.get_data()
    obj = Buyer(number=data.get('number'), name=data.get('name'))
    await create_obj(async_session, obj)
    await message.answer(
        'Клиент создан \U0001F919\n',
        reply_markup=kb.sale_buyer(data.get('is_admin'))
    )


# Блок проведения продажи
@buyer_router.callback_query(F.data == "saly")
async def input_films(callback: CallbackQuery, state: FSMContext):
    """Устанавливаем состояние пленок для чека"""
    await callback.message.answer('Введи пленки которые установил')
    await state.set_state(ChequeForm.films)
    await callback.answer()


@buyer_router.message(ChequeForm.films)
async def input_amount(message: Message, state: FSMContext):
    """Устанавливем состояние для суммы чека"""
    await state.update_data(films=message.text)
    await message.answer('Введи сумму покупки, только цифры')
    await state.set_state(ChequeForm.amount)


@buyer_router.message(ChequeForm.amount)
async def input_bonus(message: Message, state: FSMContext):
    """Устанавливем состояние для бонусов"""
    await state.update_data(amount=message.text)
    data = await state.get_data()
    buyer = await get_obj(async_session, Buyer, 'number', data.get('number'))
    await state.update_data(buyer=buyer.id)
    if buyer.bonus_points > 0:
        await message.answer(
            f'Введи количество бонусов для списания, доступно: {buyer.bonus_points}'
        )
        await state.set_state(BuyerForm.bonus_points)
    else:
        # await state.update_data(bonus_points=message.text)
        await chek_data(message, state, points=False)
        


@buyer_router.message(BuyerForm.bonus_points)
async def chek_data(message: Message, state: FSMContext, points=True):
    """Проверяем данные из состояний"""
    if not points:
        await state.update_data(bonus_points='0')
    else:
        await state.update_data(bonus_points=message.text)
    await state.update_data(employee=message.from_user.id)
    data = await state.get_data()
    error_message = await is_valid_data_cheque_buyer(data)
    if error_message:
        await message.answer(error_message)
        await state.clear()
        return

    await message.answer(
        f'Установленные пленки: {data.get("films")}\n'
        f'Сумма чека: {data.get("amount")}\n'
        f'Списано баллов: {data.get("bonus_points")}\n\n'
        f'К оплате: {int(data.get("amount")) - int(data.get("bonus_points"))}',
        reply_markup=kb.save_sale()
    )


@buyer_router.callback_query(F.data == "save_saly")
async def save_saly(callback: CallbackQuery, state: FSMContext):
    """Обновляем данные и сохраняем в бд"""
    data = await state.get_data()
    cheque = Cheque(**update_data_cheque(data))
    buyer = await update_buyer(async_session, data)
    await create_obj(async_session, cheque)
    await update_obj(async_session, buyer)
    await callback.message.answer(
        'Продажа проведена \U0001F919\n'
        'Для продолжения работы нажми кнопку "Начать продажу"\U0001F446'
    )
    await callback.answer()
    await state.clear()


# Блок проведения гарантии
@buyer_router.callback_query(F.data == "warranty")
async def start_warranty(callback: CallbackQuery, state: FSMContext):
    """Начало диалога обращения по гарантии"""
    data = await state.get_data()
    buyer = await get_obj_relation(
        async_session, Buyer, 'number', data.get('number'), 'cheques'
    )
    min_date = datetime.now() - timedelta(days=60)
    cheques = [cheque for cheque in buyer.cheques if cheque.date >= min_date]
    await state.update_data(cheques=cheques)

    message = (
        'Здесь отображаются все чеки клиента за последние два месяца\n'
        'Выбери номер нужного чека\n\n'
    )
    if not cheques:
        await callback.message.answer(
            'Нет чеков удовлетворяющих условию гарантии\n'
            'прошло более 2ух месяцев c момента покупки'
        )
        await callback.answer()
        await state.clear()
        return

    for indx, cheque in enumerate(cheques, start=1):
        employee = await get_obj(async_session, Employee, 'telegram_id', cheque.employee)
        warranty_employees = []

        if len(cheque.warranty_employee) != 0:
            warranty_employees = await get_obj(
                async_session, Employee, 'telegram_id', cheque.warranty_employee
            )

        message += (
            f'№: {indx}\n'
            f'Дата покупки: {cheque.date}\n'
            f'Установленные пленки: {cheque.films}\n'
            f'Продавец: {employee.first_name} {employee.last_name}\n'
            f'Сумма чека: {cheque.amount}\n\n'
        )

        if warranty_employees:
            message += (
                'Было обращаение по гарантии, провел:\n'
                f'{"  ".join(warranty_employees)}'
            )
    await callback.message.answer(message, reply_markup=kb.numder_cheques(len(cheques)))
    await callback.answer()


@buyer_router.callback_query(F.data.startswith('number'))
async def input_films_warranty(callback: CallbackQuery, state: FSMContext):
    """Выбирается объект чека и запрашиваются типы пленок"""
    index_cheque = int(callback.data.split('_')[1])
    data = await state.get_data()
    cheque = data.get('cheques')[index_cheque]
    await state.update_data(cheque=cheque)
    await state.update_data(films=cheque.films)
    await callback.message.answer(
        f'Установленные пленки: {cheque.films}\n'
        'Нажми "пропустить" если тип пленки не изменился, иначе напиши новую(ые)',
        reply_markup=kb.skip_films()
    )
    await state.set_state(WarrantyForm.films)
    await callback.answer()


@buyer_router.message(WarrantyForm.films)
async def set_films_warranty(message: Message, state: FSMContext):
    """Обновляем пленки в чеке и завершаем диалог с гарантией"""
    employee = await get_obj(async_session, Employee, 'telegram_id', int(data.get('tg_id')))
    data = await state.get_data()
    cheque = data.get('cheque')
    cheque.films = message.text
    name = f'{employee.first_name} {employee.last_name}'
    cheque.warranty_employee.append({name: date.today()})
    await update_obj(async_session, cheque)
    await message.answer('Данные обновлены и проведены')
    await state.clear()


@buyer_router.callback_query(F.data == 'skip_films')
async def cancel_warranty(callback: CallbackQuery, state: FSMContext):
    """Чистим состояние и завершаем диалог с гарантией"""
    employee = await get_obj(async_session, Employee, 'telegram_id', int(data.get('tg_id')))
    data = await state.get_data()
    cheque = data.get('cheque')
    name = f'{employee.first_name} {employee.last_name}'
    cheque.warranty_employee.append({name: date.today()})
    await update_obj(async_session, cheque)
    await callback.message.answer('Работа с гарантией завершена')
    await callback.answer()
    await state.clear()


# Блок изменения данных клиента
@buyer_router.callback_query(F.data == 'change_buyer')
async def satrt_change_data_buyer(callback: CallbackQuery, state: FSMContext):
    """Чистим состояние и завершаем диалог с гарантией"""
    await callback.message.answer(
        'Что меняем?',
        reply_markup=kb.change_buyer()
    )
    await callback.answer()


@buyer_router.callback_query(F.data == 'change_number')
async def request_new_number(callback: CallbackQuery, state: FSMContext):
    """Запрашиваем новый номер"""
    await state.set_state(ChangeForm.number)
    await callback.message.answer('Напиши новый номер')
    await callback.answer()


@buyer_router.message(ChangeForm.number)
async def set_number_buyer(message: Message, state: FSMContext):
    """Чекаем номер и сохранянем изменения если с номером ок"""

    err_message = await is_valid_number(message.text)

    if err_message:
        await message.answer(err_message)
        await state.clear()
        return

    data = await state.get_data()
    buyer = data.get('buyer')
    buyer.number = message.text
    await update_obj(async_session, buyer)
    await message.answer('Номер изменен')
    await state.clear()


@buyer_router.callback_query(F.data == 'change_bonus')
async def request_new_bonus(callback: CallbackQuery, state: FSMContext):
    """Запрашиваем новое количество бонусов"""
    await state.set_state(ChangeForm.bonus)
    await callback.message.answer('Сколько бонусов делаем, можно от 0 до ...')
    await callback.answer()


@buyer_router.message(ChangeForm.bonus)
async def set_number_buyer(message: Message, state: FSMContext):
    """Проверяем на валидность баллы и сохранянем изменения если ок"""

    if not message.text.isdigit():
        await message.answer('Пишем только цифры')
        await state.clear()
        return

    data = await state.get_data()
    buyer = data.get('buyer')
    buyer.bonus_points = int(message.text)
    await update_obj(async_session, buyer)
    await message.answer('Баллы обновлены')
    await state.clear()