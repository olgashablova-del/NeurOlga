
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")
WEBAPP_HOST = os.getenv("WEBAPP_HOST")
WEBAPP_PORT = int(os.getenv("WEBAPP_PORT"))

WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    channel_button = types.InlineKeyboardButton(text="Перейти в канал", url="https://t.me/neurograf_OlgaS")
    check_button = types.InlineKeyboardButton(text="Я подписался", callback_data="check")
    keyboard.add(channel_button)
    keyboard.add(check_button)
    await message.answer(
        "Привет! Я Ольга, инструктор нейрографики.\n"
        "Чтобы получить подарок — подпишись на канал и возвращайся.\n",
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: c.data == 'check')
async def process_check(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    newbie = types.InlineKeyboardButton(text="Я новичок", callback_data="newbie")
    pro = types.InlineKeyboardButton(text="Я уже знаком", callback_data="pro")
    keyboard.add(newbie)
    keyboard.add(pro)
    await bot.send_message(
        callback_query.from_user.id,
        "Ты новичок в нейрографике?\nВыбери вариант:",
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: c.data == 'newbie')
async def process_newbie(callback_query: types.CallbackQuery):
    await bot.send_message(
        callback_query.from_user.id,
        "✨ Вот твой подарок — мастер-класс для новичков:\n"
        "https://t.me/+jiDGsehELho0ODhi\n"
        "Пусть вдохновляет тебя!"
    )

@dp.callback_query_handler(lambda c: c.data == 'pro')
async def process_pro(callback_query: types.CallbackQuery):
    await bot.send_message(
        callback_query.from_user.id,
        "✨ Вот твой подарок — мастер-класс для тех, кто уже знаком с нейрографикой:\n"
        "https://t.me/+KDUotZWKuCllNjAy\n"
        "Используй с удовольствием!"
    )

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
