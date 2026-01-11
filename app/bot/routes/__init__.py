from aiogram import Router

from .echo import get_echo_router


def create_router() -> Router:
    router: Router = Router()

    router.include_router(get_echo_router())
    return router
