from aiogram import Router

from app.bot.routes.bookings import get_bookings_router

from .admin import create_admin_router
from .echo import get_echo_router
from .main_menu import get_main_menu_router
from .ping import get_ping_router


def create_router() -> Router:
    router: Router = Router()
    router.include_router(get_main_menu_router())
    router.include_router(get_bookings_router())
    router.include_router(get_ping_router())
    router.include_router(get_echo_router())
    return router
