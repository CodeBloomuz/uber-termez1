# UBER TERMEZ - Bot O'rnatish Qo'llanmasi

## Fayllar:
- klient_bot.py  → Mijozlar uchun bot
- usta_bot.py    → Ustalar uchun bot
- ustalar.json   → Ustalar ma'lumotlari (avtomatik to'ldiriladi)
- requirements.txt

---

## 1-QADAM: Telegram ID ingizni aniqlang

@userinfobot ga yozing → u sizga ID yuboradi
Bu ID ni klient_bot.py va usta_bot.py dagi ADMIN_ID ga qo'ying

---

## 2-QADAM: Railway.app da ishga tushirish (BEPUL)

1. https://railway.app ga kiring
2. GitHub bilan ro'yxatdan o'ting
3. "New Project" → "Deploy from GitHub repo"
4. Fayllarni yuklang
5. Ikkita service yarating:
   - Biri: python klient_bot.py
   - Ikkinchisi: python usta_bot.py

---

## 3-QADAM: Admin ID ni o'zgartirish

klient_bot.py va usta_bot.py fayllarida:
    ADMIN_ID = 123456789
Bu qatorni o'zingizning Telegram ID ga o'zgartiring!

---

## Bot qanday ishlaydi:

### Klient boti (@UberTermezBot):
1. Mijoz /start bosadi
2. Xizmat tanlaydi
3. 5 ta usta ko'rinadi
4. Qo'ng'iroq qiladi

### Usta boti (@UberTermezUstaBot):
1. Usta /start bosadi
2. Ro'yxatdan o'tadi (ism, tel, xizmat)
3. Sizga (adminga) ariza keladi
4. Siz tasdiqlaysiz → Usta klient botda ko'rinadi

---

## Admin buyruqlari (usta botda):
/ustalar → Barcha ustalar ro'yxati
