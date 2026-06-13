import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

TOKEN = "YOUR_BOT_TOKEN"
ADMIN_ID = 123456789  # Твій Telegram ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📦 Замовити")],
        [KeyboardButton(text="💰 Продати")]
    ],
    resize_keyboard=True
)

class OrderState(StatesGroup):
    waiting_for_order = State()

class SellState(StatesGroup):
    waiting_for_sell = State()

@dp.message(CommandStart())
async def start(message: Message):
    text = """
🏝 SEA SHOP

Вітаємо в SEA SHOP!

Ми — новий магазин на ринку цифрових товарів, який робить ставку на чесність, швидкість та індивідуальний підхід до кожного клієнта.

🎮 Працюємо виключно з:
• Standoff 2
• Brawl Stars
• Clash Royale

Оберіть потрібну дію нижче.
"""
    await message.answer(text, reply_markup=keyboard)

@dp.message(F.text == "📦 Замовити")
async def order(message: Message, state: FSMContext):
    await state.set_state(OrderState.waiting_for_order)

    await message.answer(
        "📦 Для оформлення замовлення надішліть одним повідомленням:\n\n"
        "1. Товар:\n"
        "2. ID товару:\n"
        "3. Кількість:\n"
        "4. Ваш Telegram (@username):"
    )

@dp.message(OrderState.waiting_for_order)
async def get_order(message: Message, state: FSMContext):
    await bot.send_message(
        ADMIN_ID,
        f"📦 НОВЕ ЗАМОВЛЕННЯ\n\n"
        f"Від: @{message.from_user.username}\n"
        f"ID: {message.from_user.id}\n\n"
        f"{message.text}"
    )

    await message.answer(
        "✅ Вашу заявку передано оператору.\n\n"
        "⏳ Час відповіді: від 10 хвилин до 3 годин.\n"
        "📩 Відповідь надійде в особисті повідомлення Telegram.\n\n"
        "Дякуємо за звернення до SEA SHOP!"
    )

    await state.clear()

@dp.message(F.text == "💰 Продати")
async def sell(message: Message, state: FSMContext):
    await state.set_state(SellState.waiting_for_sell)

    await message.answer(
        "💰 Для продажу товару надішліть одним повідомленням:\n\n"
        "1. Ваша пропозиція (акаунт/валюта):\n"
        "2. Гра:\n"
        "3. Кількість:\n"
        "4. Ціна:"
    )

@dp.message(SellState.waiting_for_sell)
async def get_sell(message: Message, state: FSMContext):
    await bot.send_message(
        ADMIN_ID,
        f"💰 НОВА ПРОПОЗИЦІЯ НА ПРОДАЖ\n\n"
        f"Від: @{message.from_user.username}\n"
        f"ID: {message.from_user.id}\n\n"
        f"{message.text}"
    )

    await message.answer(
        "✅ Вашу пропозицію передано оператору.\n\n"
        "⏳ Час відповіді: від 10 хвилин до 3 годин.\n"
        "📩 Відповідь надійде в особисті повідомлення Telegram.\n\n"
        "Дякуємо за співпрацю з SEA SHOP!"
    )

    await state.clear()

async def main():
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())
