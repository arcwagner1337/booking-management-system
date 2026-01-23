from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from .keyboards import main_menu


def get_admin_handlers_router() -> Router:
    router = Router()

    @router.message(Command(commands=["start", "menu"]))
    async def start_menu(message: Message):
        role = getattr(message, "role", None)

        if role not in ("owner", "admin"):
            await message.answer("⛔ У вас нет доступа")
            return

        if role == "owner":
            header = "👑 Вы вошли как владелец"
        else:
            header = "🛠 Вы вошли как администратор"

        text = f"{header}\n\nДобро пожаловать в админ-панель!\nВыберите действие:"

        await message.answer(
            text=text,
            reply_markup=main_menu(),
        )

    return router
