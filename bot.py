import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, Message
from config import TOKEN, WEBAPP_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    
    # Клавиатура с кнопкой Mini App
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="💰 Открыть Хисобчи",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "👋 Добро пожаловать в Хисобчи - ваш личный бухгалтер!\n\n"
        "Нажмите кнопку ниже, чтобы открыть приложение и начать отслеживать расходы.",
        reply_markup=keyboard
    )

@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    await message.answer(
        "📖 Справка:\n\n"
        "• Нажмите '💰 Открыть Хисобчи' для открытия приложения\n"
        "• Добавляйте расходы с категориями\n"
        "• Отслеживайте бюджет с прогресс-баром\n"
        "• Все суммы в узбекском сўме (UZS)"
    )

async def main():
    """Основная функция"""
    logger.info("🚀 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())