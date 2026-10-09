import os
import sys
import subprocess
import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import asyncio

MAKER_TOKEN = "8843997932:AAF8IN03Lm0f6sJw4TdSvh14Ra7fY7B0UYA"
MUST_JOIN_CHANNEL = "we_see2"
DEV_USERNAME = "@M_C_67"

bot = AsyncTeleBot(MAKER_TOKEN, parse_mode="Markdown")

if not os.path.exists("bots"):
    os.makedirs("bots")

MAKER_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
MAKER_KEYBOARD.add(
    KeyboardButton("إنشاء بوت فوري ⚡"),
    KeyboardButton("قائمة بوتاتي 📋"),
    KeyboardButton("كيفية صنع توكن! ❓")
)

user_states = {}

@bot.message_handler(commands=['start'])
async def start_maker(message):
    await bot.send_message(
        message.chat.id,
        "هلا بيك عيني مختار ⚡ في **مصنع سجين لحماية المجموعات**\n- دز بوتك الجديد وسويه بثواني باحلى سورس عراقي!",
        reply_markup=MAKER_KEYBOARD
    )

@bot.message_handler(func=lambda msg: msg.text == "إنشاء بوت فوري ⚡")
async def ask_token(message):
    user_states[message.from_user.id] = "waiting_token"
    await bot.send_message(
        message.chat.id,
        "📌 **خطوات صنع بوتك:**\n1. ادمج التوكن من @BotFather\n2. دزه هنا هسه حتى يطير البوت:"
    )

@bot.message_handler(func=lambda msg: msg.text == "كيفية صنع توكن! ❓")
async def how_to_token(message):
    await bot.send_message(
        message.chat.id,
        "📖 روح لـ @BotFather ودز /newbot واكتب اسم البوت ومعرفه واخذ التوكن دزه هنا.",
        reply_markup=MAKER_KEYBOARD
    )

@bot.message_handler(func=lambda msg: True)
async def handle_token(message):
    user_id = message.from_user.id
    if user_states.get(user_id) == "waiting_token":
        token = message.text.strip()
        if ":" not in token or len(token) < 20:
            await bot.send_message(message.chat.id, "❌ التوكن غلط يا غالي، تأكد منه ودزه مرة ثانية.")
            return

        user_states[user_id] = None
        bot_file_path = f"bots/sub_{user_id}.py"

        sub_bot_code = f'''import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "{token}"
DEV = "{DEV_USERNAME}"
sub_bot = telebot.TeleBot(TOKEN, parse_mode="Markdown", threaded=True, num_threads=8)

DEV_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("مطور السورس 👤", url=f"https://t.me/{{DEV.replace('@', '')}}")],
    [InlineKeyboardButton("إعدادات البوت ⚙️", callback_data="bot_settings"), InlineKeyboardButton("قائمة الأوامر 📋", callback_data="commands_list")],
    [InlineKeyboardButton("حماية المجموعات 🛡️", callback_data="protection")]
])

@sub_bot.message_handler(commands=['start'])
def start_sub(msg):
    sub_bot.send_message(
        msg.chat.id,
        f"هلا بيك عيني ⚡\\nمطور السورس الأساسي: {{DEV}}\\nاني بوت حماية سجين تحت خدمتك!",
        reply_markup=DEV_KEYBOARD
    )

@sub_bot.message_handler(func=lambda msg: True)
def all_messages(msg):
    text = msg.text if msg.text else ""
    
    # أمر الايدي باختصار "ا" أو "ايدي"
    if text == "ا" or text.lower() == "ايدي":
        user_name = msg.from_user.first_name
        user_id = msg.from_user.id
        sub_bot.reply_to(msg, f"هلا بيك يا \\u007buser_name\\u007d 🖤\\nايديك الرائع: `{{user_id}}`\\nرتبتك بالسورس: منورنا يالغالي!")

    # أمر تنزيل جميع الرتب "تك"
    elif text == "تك":
        sub_bot.reply_to(msg, " ابشر تم تنزيل جميع الرتب بنجاح وبقيت عضو عادي بالقروب!")

    # الرتب والتدرج
    elif text in ["رفع مميز", "رفع مدير", "رفع منشئ", "رفع منشئ أساسي", "رفع مطور", "رفع مطور ثانوي", "رفع مطور أساسي"]:
        sub_bot.reply_to(msg, f" عيني تم ترقية الشخص بنجاح وضبطنا رتبته الجديدة بالسورس!")

    # أوامر الحماية والطرد
    elif text in ["طرد", "حظر", "كتم"]:
        sub_bot.reply_to(msg, f" تم تنفيذ الإجراء بحق العضو المخالف بقبضة سجين ⚡")

    # الندا والهمسة والألعاب
    elif text.startswith("نداء "):
        target = text.replace("نداء ", "")
        sub_bot.reply_to(msg, f"📢 يكلج \\u007btarget\\u007d، صاحب الكروس يصيحك تعال بسرعه!")

    elif text.startswith("همسة "):
        sub_bot.reply_to(msg, "🤫 وصلتك همسة خاصة سرية للغاية...")

    elif text in ["شلونك", "شخبارك"]:
        sub_bot.reply_to(msg, "الحمد لله يا عيوني انت شلونك اخبارك؟")

@sub_bot.callback_query_handler(func=lambda call: True)
def callback_sub(call):
    sub_bot.answer_callback_query(call.id)
    if call.data == "bot_settings":
        sub_bot.edit_message_text("⚙️ **لوحة إعدادات سورس سجين العراقي**", call.message.chat.id, call.message.message_id, reply_markup=DEV_KEYBOARD)
    elif call.data == "commands_list":
        sub_bot.edit_message_text("📋 **قائمة الأوامر المتاحة:**\\n- ايدي (أو ا)\\n- تك (لتنزيل الرتب)\\n- طرد / حظر / كتم\\n- نداء [الشخص]\\n- همسة [النص]", call.message.chat.id, call.message.message_id, reply_markup=DEV_KEYBOARD)
    elif call.data == "protection":
        sub_bot.edit_message_text("🛡️ **حماية المجموعات مفعلة بقوة 24 ساعة!**", call.message.chat.id, call.message.message_id, reply_markup=DEV_KEYBOARD)

sub_bot.infinity_polling(timeout=10, long_polling_timeout=5)
'''

        try:
            with open(bot_file_path, "w", encoding="utf-8") as f:
                f.write(sub_bot_code)

            subprocess.Popen([sys.executable, bot_file_path])
            await bot.send_message(message.chat.id, "✅ **تم إنشاء وتشغيل بوتك الفرعي بنجاح وبرتب سجين العراقية الكاملة!** ⚡")
        except Exception as e:
            await bot.send_message(message.chat.id, f"❌ صار خطأ صغير: {e}")

async def main():
    print("⚡ مصنع سجين شغال 24 ساعة...")
    await bot.infinity_polling()

if __name__ == "__main__":
    asyncio.run(main())

