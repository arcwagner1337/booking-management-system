from aiogram import Router

from app.bot.routes.admin.filters.admin_access import AdminAccessFilter

from .handlers import get_admin_handlers_router


def create_admin_router() -> Router:
    router: Router = Router()
    router.include_router(get_admin_handlers_router())
    router.message.filter(AdminAccessFilter())
    router.callback_query.filter(AdminAccessFilter())

    return router
