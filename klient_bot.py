import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
import asyncio
import json
import os

# =============================================
# SOZLAMALAR
# =============================================
TOKEN = "8020803338:AAGOesGlRBDLJj8aWCmpdo18WApmRTsxcCY"  # Klient bot token
ADMIN_ID = 6551375195  # Sizning Telegram ID ingiz

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

# =============================================
# USTALAR MA'LUMOTLARI (JSON fayldan o'qiladi)
# =============================================
def get_ustalar(xizmat_turi: str) -> list:
    """Xizmat turiga qarab ustalarni qaytaradi"""
    try:
        with open("ustalar.json", "r", encoding="utf-8") as f:
            all_ustalar = json.load(f)
        # Faqat tasdiqlangan va mos xizmat turini filtrlash
        mos = [u for u in all_ustalar if u.get("xizmat") == xizmat_turi and u.get("tasdiqlangan") == True]
        return mos[:5]  # Max 5 ta
    except:
        return []

# =============================================
# /start BUYRUG'I
# =============================================
@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🚿 Santexnik", callback_data="xizmat:Santexnik"),
            InlineKeyboardButton(text="⚡ Elektrik", callback_data="xizmat:Elektrik"),
        ],
        [
            InlineKeyboardButton(text="🔥 Gaz ustasi", callback_data="xizmat:Gaz ustasi"),
            InlineKeyboardButton(text="🪑 Mebel ustasi", callback_data="xizmat:Mebel ustasi"),
        ],
        [
            InlineKeyboardButton(text="🎨 Oboychi", callback_data="xizmat:Oboychi"),
            InlineKeyboardButton(text="📦 Labo / Yuk", callback_data="xizmat:Labo"),
        ],
        [
            InlineKeyboardButton(text="🛵 Yetkazib berish", callback_data="xizmat:Yetkazib berish"),
        ],
    ])

    await message.answer(
        "👋 <b>UBER TERMEZ</b> botiga xush kelibsiz!\n\n"
        "🏙 Termiz shahri uchun usta va xizmatlar platformasi.\n\n"
        "👇 Qanday xizmat kerak?",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

# =============================================
# XIZMAT TANLANGANDA
# =============================================
@dp.callback_query(F.data.startswith("xizmat:"))
async def xizmat_tanlandi(callback: types.CallbackQuery):
    xizmat = callback.data.split(":")[1]

    await callback.message.answer(
        f"✅ <b>{xizmat}</b> tanlandi!\n\n"
        f"⏳ Termiz shahridagi ustalar qidirilmoqda...",
        parse_mode="HTML"
    )

    ustalar = get_ustalar(xizmat)

    if not ustalar:
        await callback.message.answer(
            f"😔 Hozircha <b>{xizmat}</b> bo'yicha usta topilmadi.\n\n"
            "🔄 Tez orada ustalar qo'shiladi!\n"
            "📞 Murojaat: @UberTermezAdmin",
            parse_mode="HTML"
        )
        await callback.answer()
        return

    await callback.message.answer(
        f"🔍 <b>Termiz shahridagi {xizmat} ustalar:</b>\n"
        f"{'━' * 30}",
        parse_mode="HTML"
    )

    for u in ustalar:
        matn = (
            f"👷 <b>{u['ism']}</b>\n"
            f"📍 Termiz shahri\n"
            f"⭐ {u['reyting']} ({u['sharhlar']} ta sharh)\n"
            f"💰 Narx: Kelishilgan holda\n"
            f"📞 <a href='tel:{u['telefon']}'>{u['telefon']}</a>"
        )

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text=f"📞 {u['ism']} ga qo'ng'iroq",
                url=f"tel:{u['telefon']}"
            )]
        ])

        await callback.message.answer(matn, reply_markup=keyboard, parse_mode="HTML")

    await callback.message.answer(
        "☝️ Yuqoridagi ustalardan biriga qo'ng'iroq qiling.\n\n"
        "🔄 Boshqa xizmat kerakmi?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="bosh_menyu")]
        ])
    )

    await callback.answer()

# =============================================
# BOSH MENYUGA QAYTISH
# =============================================
@dp.callback_query(F.data == "bosh_menyu")
async def bosh_menyu(callback: types.CallbackQuery):
    await start(callback.message)
    await callback.answer()

# =============================================
# BOTNI ISHGA TUSHIRISH
# =============================================
async def main():
    print("✅ UBER TERMEZ Klient boti ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
