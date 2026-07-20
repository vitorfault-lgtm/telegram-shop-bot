from aiogram import Router
from bot.handlers.user import router as user_router

def get_handlers_router() -> Router:
    router = Router()
    router.include_router(user_router)
    return router