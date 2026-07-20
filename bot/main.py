import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.handlers import get_handlers_router
from bot.misc.env import EnvKeys

async def start_bot():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    bot = Bot(token=EnvKeys.TOKEN)
    dp = Dispatcher()
    
    dp.include_router(get_handlers_router())
    
    logging.info("🚀 Bot custom logic initialized successfully!")
    await dp.start_polling(bot)