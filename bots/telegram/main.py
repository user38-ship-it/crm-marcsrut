import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "changeme")


async def start_handler(message: Message) -> None:
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мої рейси"), KeyboardButton(text="Старт")],
            [KeyboardButton(text="Немає місць"), KeyboardButton(text="Фініш")],
        ],
        resize_keyboard=True,
    )
    await message.answer(
        "👋 Вітаємо у Booking CRM! Оберіть дію у меню.", reply_markup=menu
    )


async def menu_handler(message: Message) -> None:
    await message.answer(f"Функція '{message.text}' поки у розробці.")


def build_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.message.register(start_handler, CommandStart())
    dp.message.register(menu_handler, F.text.in_({"Мої рейси", "Старт", "Немає місць", "Фініш"}))
    return dp


async def main() -> None:
    if TELEGRAM_TOKEN == "changeme":
        raise RuntimeError("TELEGRAM_TOKEN is not configured")

    bot = Bot(token=TELEGRAM_TOKEN)
    dp = build_dispatcher()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
