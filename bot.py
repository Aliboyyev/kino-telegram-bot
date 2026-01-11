import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = "8592239451:AAFe8YiWwYaQdVH3OKbbrI7TwkZEOrIMhNU"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# 🔗 Majburiy obuna kanallari
CHANNELS = [
    "@kino_topuchi",
    "@kinolar_topuchi",
]

# 🎬 Kino bazasi (KOD → KINO)
MOVIES = {
    "1": {
        "title": "Tunda aytilgan qo'rqinchili ertaklar",
        "channel": "@kino_topuchi",
        "post_id": 4
    },
    "2": {
        "title": "12 raund",
        "channel": "@kino_topuchi",
        "post_id": 2
    }
}

# 🔍 Obuna tekshirish
async def check_subscriptions(user_id: int):
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status not in ("member", "administrator", "creator"):
                return False
        except:
            return False
    return True

# 📢 Obuna tugmalari
def subscribe_keyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[])

    for ch in CHANNELS:
        kb.inline_keyboard.append([
            InlineKeyboardButton(
                text="📢 Kanal",
                url=f"https://t.me/{ch.replace('@','')}"
            )
        ])

    kb.inline_keyboard.append([
        InlineKeyboardButton(
            text="✅ Tasdiqlash",
            callback_data="check_sub"
        )
    ])
    return kb

# ▶️ /start
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "✌ Assalomu alaykum!\n\n"
        "🎬 Men kino kod orqali film topib beraman.\n"
        "❗ Davom etish uchun kanallarga obuna bo‘ling:",
        reply_markup=subscribe_keyboard()
    )

# ✅ Obunani tekshirish
@dp.callback_query(lambda c: c.data == "check_sub")
async def check(call: types.CallbackQuery):
    if await check_subscriptions(call.from_user.id):
        await call.message.edit_text(
            "✅ Rahmat!\n🔢 Endi kino kodini yuboring."
        )
    else:
        await call.answer(
            "❌ Avval barcha kanallarga obuna bo‘ling!",
            show_alert=True
        )

# 🎥 Kino kod qabul qilish
@dp.message()
async def get_code(message: types.Message):
    if not await check_subscriptions(message.from_user.id):
        await message.answer(
            "❌ Avval kanallarga obuna bo‘ling!",
            reply_markup=subscribe_keyboard()
        )
        return

    code = message.text.strip()

    if code in MOVIES:
        movie = MOVIES[code]
        link = f"https://t.me/{movie['channel'].replace('@','')}/{movie['post_id']}"

        await message.answer(
            f"🎬 <b>{movie['title']}</b>\n\n"
            f"👉 Tomosha qilish: {link}",
            parse_mode="HTML"
        )
    else:
        await message.answer(
            "❌ Bunday koddagi kino topilmadi.\n"
            "🔢 Iltimos, to‘g‘ri kod yuboring."
        )

# 🚀 Botni ishga tushirish
async def main():
    print("🤖 Bot ishga tushdi")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

