import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from app.handlers import router
from app.config import TOKEN
from app.database.portfolio import init_models

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

async def main():
    load_dotenv()
    
    await init_models()
    
    dp=Dispatcher()
    bot = Bot(token=TOKEN)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    dp.include_router(router)
    await dp.start_polling(bot)
    
async def startup(dispatcher: Dispatcher):
    print("Bot is starting...")
async def shutdown(dispatcher: Dispatcher):
    print("Bot is stopping...")


if __name__ == '__main__':
    try:
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted by user")