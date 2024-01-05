from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from keyboards import kb
from db.models import BonusPoint, Employee, Buyer
from db.async_engine import async_session
from utils.crud import get_obj, create_obj
from utils.states import BuyerForm


start_router = Router()


@start_router.startup()
async def on_startup():
    """
    Проверяет наличие объекта бонус в бд,
    если нет, то создает.
    
    используется при запуске бота
    """
    obj = await get_obj(async_session, BonusPoint, 'name', 'bonus_pointer')
    if not obj:
        obj = BonusPoint(name='bonus_pointer')
        await create_obj(async_session, obj)
        print("Бонусы добавлены")


# @start_router.callback_query(F.data == "cancel")
@start_router.message(CommandStart())
async def start(message: Message | CallbackQuery, state: FSMContext):
    """Начало работы бота"""

    employee_id = message.from_user.id
    obj = await get_obj(async_session, Employee, 'telegram_id', employee_id)
    if True:
    # if obj and obj.is_admin:
        # 
        await message.answer(
            "Введи номер клиента в формате: 89271112233",
            reply_markup=kb.add_user()
        )
    elif obj and not obj.is_banned:
        # await state.set_state(BuyerForm.number)
        await message.answer(
            "Введи номер клиента в формате: 89271112233",
        )
    else:
        await message.answer(
            "Для работы с ботом отправь администратору\n"
            f"свой id <code><b>{employee_id}</b></code>",
            parse_mode=ParseMode.HTML
        )
    await state.set_state(BuyerForm.number)

@start_router.message(F.text.regexp(r"\d{11}"))
@start_router.message(BuyerForm.number, F.text.regexp(r"\d{11}"))
async def check_buyer(message: Message, state: FSMContext):
    """
    Проверяем существование покупателя
    Если нет, то переходим к диалогу создания
    иначе открываем диалог работы с клиентом
    """
    await state.update_data(number=message.text)

    obj = await get_obj(async_session, Buyer, 'number', message.text)
    if obj:
        await message.answer(
            f"Имя: {obj.name}\n"
            f"Доступно бонусов: {obj.bonus_points}\n"
            f"Количество установок: {obj.count_aplications}\n",
            reply_markup=kb.sale_buyer()
        )
    else:
        await state.update_data(number=int(message.text))
        await message.answer('Введи имя клиента')
        await state.set_state(BuyerForm.name)

