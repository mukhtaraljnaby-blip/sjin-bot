import os
import sys
import subprocess
import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import asyncio

MAKER_TOKEN = "8843997932:AAF8IN03Lm0f6sJw4TdSvh14Ra7fY7B0UYA"
MUST_JOIN_CHANNEL = "we_see2"

bot = AsyncTeleBot(MAKER_TOKEN, parse_mode="Markdown")

if not os.path.exists("bots"):
    os.makedirs("bots")

MAKER_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
MAKER_KEYBOARD.add(
    KeyboardButton("إنشاء بوت فوري ⚡"),
    KeyboardButton("قائمة بوتاتي 📋"),
    KeyboardButton("شراء بوت 💎"),
    KeyboardButton("كيفية صنع توكن! ❓")
)

user_states = {}

@bot.message_handler(commands=['start'])
async def start_maker(message):
    await bot.send_message(
        message.chat.id,
        "- : أهلاً بك عزيزي في **مصنع سجين لحماية المجموعات** ⚡\n- : يمكنك إنشاء بوت حماية خاص بك مجاناً وبأعلى سرعة.",
        reply_markup=MAKER_KEYBOARD
    )

@bot.message_handler(func=lambda msg: msg.text == "إنشاء بوت فوري ⚡")
async def ask_token(message):
    user_states[message.from_user.id] = "waiting_token"
    await bot.send_message(
        message.chat.id,
        "📌 **لإنشاء بوتك الجديد:**\n1. اذهب إلى بوت @BotFather واستخرج توكن جديد.\n2. أرسل التوكن هنا الآن:"
    )

@bot.message_handler(func=lambda msg: msg.text == "كيفية صنع توكن! ❓")
async def how_to_token(message):
    await bot.send_message(
        message.chat.id,
        "📖 **طريقة استخراج التوكن:**\n1. ادخل لبوت @BotFather\n2. أرسل الأمر /newbot\n3. اكتب اسم البوت ثم معرف البوت (ينتهي بـ bot).\n4. انسخ كود الـ API Token وأرسله هنا."
    )

@bot.message_handler(func=lambda msg: True)
async def handle_token(message):
    user_id = message.from_user.id
    if user_states.get(user_id) == "waiting_token":
        token = message.text.strip()
        if ":" not in token or len(token) < 20:
            await bot.send_message(message.chat.id, "❌ **التوكن غير صحيح!** أعد المحاولة إرساله من جديد.")
            return

        user_states[user_id] = None
        bot_file_path = f"bots/sub_{user_id}.py"

        sub_bot_code = f'''import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "{token}"
MUST_JOIN = "{MUST_JOIN_CHANNEL}"
sub_bot = telebot.TeleBot(TOKEN, parse_mode="Markdown", threaded=True, num_threads=8)

DEV_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("المطور الأساسي 👤", url="https://t.me/M_C_67")],
    [InlineKeyboardButton("إعدادات الأساسي", callback_data="admin_settings")],
    [InlineKeyboardButton("إعدادات البوت", callback_data="bot_settings"), InlineKeyboardButton("أوامر الإذاعة", callback_data="broadcast")],
    [InlineKeyboardButton("إعدادات الهمسة", callback_data="whisper_settings"), InlineKeyboardButton("الأوامر العامة", callback_data="general_cmd")]
])

@sub_bot.message_handler(commands=['start'])
def start_sub(msg):
    sub_bot.send_message(msg.chat.id, "- : أهلاً بك في سورس سجين ⚡", reply_markup=DEV_KEYBOARD)

@sub_bot.message_handler(func=lambda msg: True)
def msg_sub(msg):
    text = msg.text
    if text == "الاوامر":
        sub_bot.send_message(msg.chat.id, "- : أوامر سورس سجين ⚡", reply_markup=DEV_KEYBOARD)
    elif text in ["أحبك", "هلا", "السلام عليكم", "شلونك"]:
        res = {{"أحبك": "أموت عليك", "هلا": "هلا بالعمرر", "السلام عليكم": "نورت حبيبي", "شلونك": "وف عمري"}}
        sub_bot.send_message(msg.chat.id, res[text])

@sub_bot.callback_query_handler(func=lambda call: True)
def cb_sub(call):
    sub_bot.answer_callback_query(call.id)
    if call.call_data == "admin_settings":
        sub_bot.edit_message_text("⚙️ **إعدادات الأساسي - سورس سجين ⚡**", call.message.chat.id, call.message.message_id, reply_markup=DEV_KEYBOARD)

sub_bot.infinity_polling(timeout=10, long_polling_timeout=5)
'''

        try:
            with open(bot_file_path, "w", encoding="utf-8") as f:
                f.write(sub_bot_code)

            subprocess.Popen([sys.executable, bot_file_path])
            await bot.send_message(message.chat.id, "✅ **تم إنشاء وتشغيل بوتك بنجاح وسرعة عالية!** ⚡")
        except Exception as e:
            await bot.send_message(message.chat.id, f"❌ حدث خطأ أثناء تشغيل البوت: {e}")

async def main():
    print("⚡ مصنع سجين شغال الآن بنجاح...")
    await bot.infinity_polling()

if __name__ == "__main__":
    asyncio.run(main())
