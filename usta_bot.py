import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F
import asyncio
import json
import os

# =============================================
# SOZLAMALAR
# =============================================
TOKEN = "8101468996:AAEBJ_Do-VoXghO6GDRvlupNs9GtP3gKCp0"  # Usta bot token
ADMIN_ID = 6551375195  # Sizning Telegram ID ingiz

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

logging.basicConfig(level=logging.INFO)

# =============================================
# RO'YXATDAN O'TISH BOSQICHLARI (FSM)
# =============================================
class UstaRoyxat(StatesGroup):
    ism = State()
    telefon = State()
    xizmat = State()
    haqida = State()

# =============================================
# USTALAR FAYLINI BOSHQARISH
# =============================================
FAYL = "ustalar.json"

def ustalar_olish():
    if os.path.exists(FAYL):
        with open(FAYL, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def usta_saqlash(usta: dict):
    ustalar = ustalar_olish()
    ustalar.append(usta)
    with open(FAYL, "w", encoding="utf-8") as f:
        json.dump(ustalar, f, ensure_ascii=False, indent=2)

def usta_tasdiqlash(telegram_id: int, tasdiqlash: bool):
    ustalar = ustalar_olish()
    for u in ustalar:
        if u.get("telegram_id") == telegram_id and not u.get("tasdiqlangan"):
            u["tasdiqlangan"] = tasdiqlash
            break
    with open(FAYL, "w", encoding="utf-8") as f:
        json.dump(ustalar, f, ensure_ascii=False, indent=2)

# =============================================
# /start BUYRUG'I
# =============================================
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👷 <b>UBER TERMEZ — Usta Boti</b>ga xush kelibsiz!\n\n"
        "Bu bot orqali siz platformaga usta sifatida ro'yxatdan o'tishingiz mumkin.\n\n"
        "Ro'yxatdan o'tgach, admin tasdiqlaydi va mijozlar sizni ko'ra boshlaydi! ✅",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👷 Usta sifatida ro'yxatdan o'tish", callback_data="royxat_boshlash")]
        ]),
        parse_mode="HTML"
    )

# =============================================
# RO'YXATDAN O'TISHNI BOSHLASH
# =============================================
@dp.callback_query(F.data == "royxat_boshlash")
async def royxat_boshlash(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UstaRoyxat.ism)
    await callback.message.answer(
        "📝 Ro'yxatdan o'tish boshlandi!\n\n"
        "1️⃣ Ism va Familiyangizni yozing:\n"
        "<i>Misol: Jasur Toshmatov</i>",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove()
    )
    await callback.answer()

# =============================================
# ISM KIRITISH
# =============================================
@dp.message(UstaRoyxat.ism)
async def ism_kiritish(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)

    # Telefon tugmasi
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Raqamimni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await state.set_state(UstaRoyxat.telefon)
    await message.answer(
        f"✅ Ism: <b>{message.text}</b>\n\n"
        "2️⃣ Telefon raqamingizni yuboring:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

# =============================================
# TELEFON KIRITISH
# =============================================
@dp.message(UstaRoyxat.telefon, F.contact)
async def telefon_kiritish(message: types.Message, state: FSMContext):
    telefon = message.contact.phone_number
    if not telefon.startswith("+"):
        telefon = "+" + telefon
    await state.update_data(telefon=telefon)

    # Xizmat tanlash tugmalari
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

    await state.set_state(UstaRoyxat.xizmat)
    await message.answer(
        f"✅ Telefon: <b>{telefon}</b>\n\n"
        "3️⃣ Qaysi xizmat turisiz?",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.message(UstaRoyxat.telefon)
async def telefon_xato(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Raqamimni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(
        "⚠️ Iltimos, tugmani bosib raqamingizni yuboring:",
        reply_markup=keyboard
    )

# =============================================
# XIZMAT TANLASH
# =============================================
@dp.callback_query(UstaRoyxat.xizmat, F.data.startswith("xizmat:"))
async def xizmat_tanlash(callback: types.CallbackQuery, state: FSMContext):
    xizmat = callback.data.split(":")[1]
    await state.update_data(xizmat=xizmat)

    await state.set_state(UstaRoyxat.haqida)
    await callback.message.answer(
        f"✅ Xizmat: <b>{xizmat}</b>\n\n"
        "4️⃣ O'zingiz haqingizda qisqacha yozing:\n"
        "<i>Misol: 10 yillik tajriba, sifatli ish kafolati bilan</i>",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove()
    )
    await callback.answer()

# =============================================
# HAQIDA KIRITISH VA YAKUNLASH
# =============================================
@dp.message(UstaRoyxat.haqida)
async def haqida_kiritish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    usta = {
        "telegram_id": message.from_user.id,
        "ism": data["ism"],
        "telefon": data["telefon"],
        "xizmat": data["xizmat"],
        "haqida": message.text,
        "reyting": 5.0,
        "sharhlar": 0,
        "tasdiqlangan": False
    }

    usta_saqlash(usta)

    # Ustaga xabar
    await message.answer(
        "✅ <b>Arizangiz qabul qilindi!</b>\n\n"
        f"👷 Ism: {usta['ism']}\n"
        f"📞 Telefon: {usta['telefon']}\n"
        f"🔧 Xizmat: {usta['xizmat']}\n\n"
        "⏳ Admin tasdiqlashini kuting. Odatda 1-2 soat ichida tasdiqlanadi.",
        parse_mode="HTML"
    )

    # Adminga xabar
    admin_matn = (
        f"🆕 <b>Yangi usta arizasi!</b>\n\n"
        f"👷 Ism: {usta['ism']}\n"
        f"📞 Telefon: {usta['telefon']}\n"
        f"🔧 Xizmat: {usta['xizmat']}\n"
        f"📝 Haqida: {usta['haqida']}\n"
        f"🆔 Telegram ID: {usta['telegram_id']}"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"tasdiq:{message.from_user.id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"rad:{message.from_user.id}"),
        ]
    ])

    try:
        await bot.send_message(ADMIN_ID, admin_matn, reply_markup=keyboard, parse_mode="HTML")
    except:
        pass

# =============================================
# ADMIN: TASDIQLASH / RAD ETISH
# =============================================
@dp.callback_query(F.data.startswith("tasdiq:"))
async def tasdiqlash(callback: types.CallbackQuery):
    usta_id = int(callback.data.split(":")[1])
    usta_tasdiqlash(usta_id, True)

    await callback.message.edit_text(
        callback.message.text + "\n\n✅ <b>TASDIQLANDI</b>",
        parse_mode="HTML"
    )

    try:
        await bot.send_message(
            usta_id,
            "🎉 <b>Tabriklaymiz!</b>\n\n"
            "Sizning arizangiz tasdiqlandi!\n"
            "Endi mijozlar sizni <b>UBER TERMEZ</b> botida ko'rishi mumkin. ✅\n\n"
            "Muvaffaqiyatli ish tilaymiz! 💪",
            parse_mode="HTML"
        )
    except:
        pass

    await callback.answer("✅ Usta tasdiqlandi!")

@dp.callback_query(F.data.startswith("rad:"))
async def rad_etish(callback: types.CallbackQuery):
    usta_id = int(callback.data.split(":")[1])
    usta_tasdiqlash(usta_id, False)

    await callback.message.edit_text(
        callback.message.text + "\n\n❌ <b>RAD ETILDI</b>",
        parse_mode="HTML"
    )

    try:
        await bot.send_message(
            usta_id,
            "😔 Afsuski, arizangiz rad etildi.\n\n"
            "Qo'shimcha ma'lumot uchun: @UberTermezAdmin",
            parse_mode="HTML"
        )
    except:
        pass

    await callback.answer("❌ Usta rad etildi!")

# =============================================
# ADMIN: USTALAR RO'YXATI
# =============================================
@dp.message(Command("ustalar"))
async def ustalar_royxati(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    ustalar = ustalar_olish()
    if not ustalar:
        await message.answer("📭 Hozircha usta yo'q.")
        return

    matn = f"👷 <b>Jami ustalar: {len(ustalar)}</b>\n\n"
    for i, u in enumerate(ustalar, 1):
        holat = "✅" if u.get("tasdiqlangan") else "⏳"
        matn += f"{i}. {holat} {u['ism']} — {u['xizmat']} — {u['telefon']}\n"

    await message.answer(matn, parse_mode="HTML")

# =============================================
# BOTNI ISHGA TUSHIRISH
# =============================================
async def main():
    print("✅ UBER TERMEZ Usta boti ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
