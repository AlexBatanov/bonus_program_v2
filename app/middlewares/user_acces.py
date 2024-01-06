from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.enums import ParseMode

from utils.crud import get_obj
from db.async_engine import async_session
from db.models import Employee

class AccesBot(BaseMiddleware):
    """Проверяем наличие сотрудника и имеет ли он доступ"""
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:

        user_id = data.get('event_from_user').id
        employee = await get_obj(async_session, Employee, 'telegram_id', user_id)
        if False:
        # if not employee or employee.is_banned:
            await event.answer(
                'Нет доступа!\n'
                "Для работы с ботом отправь администратору\n"
                f"свой id <code><b>{user_id}</b></code>",
                parse_mode=ParseMode.HTML
            )
            return

        data['is_admin'] = False #employee.is_admin     
        return await handler(event, data)