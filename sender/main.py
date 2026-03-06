import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TELEGRAM_BOT_TOKEN
from handlers import commands, messages

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def main():
    """Основная функция для запуска бота"""
    
    # Создаем бота и диспетчер
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Регистрируем роутеры
    dp.include_router(commands.router)
    dp.include_router(messages.router)
    
    # Запускаем бота
    logger.info("Бот запущен и готов к работе!")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
