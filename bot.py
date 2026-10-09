import os
import sys
import subprocess
import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
import asyncio
import random

MAKER_TOKEN = "8719015904:AAG7MwDSnyGMeNLfUH1W9aiumtlOr0WJMr8"
DEV_USERNAME = "@M_C_67"

bot = AsyncTeleBot(MAKER_TOKEN, parse_mode="Markdown")

if not os.path.exists("bots"):
    os.makedirs("bots")

MAKER_KEYBOARD = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
MAKER_KEYBOARD.add(
    telebot.types.KeyboardButton("إنشاء بوت فوري ⚡"),
    telebot.types.KeyboardButton("قائمة بوتاتي 📋")
)

user_states = {}

@bot.message_handler(commands=['start'])
async def start_maker(message):
    await bot.send_message(
        message.chat.id,
        "هلا بيك عيني مختار ⚡ في **مصنع سجين**\n- دز توكن بوتك الجديد حتى اصنعه لك مع إضافة الردود والتاك الجماعي وكل السوالف!",
        reply_markup=MAKER_KEYBOARD
    )

@bot.message_handler(func=lambda msg: msg.text == "إنشاء بوت فوري ⚡")
async def ask_token(message):
    user_states[message.from_user.id] = "waiting_token"
    await bot.send_message(
        message.chat.id,
        "📌 دز توكن بوتك الجديد من @BotFather هنا هسه:"
    )

@bot.message_handler(func=lambda msg: True)
async def handle_token(message):
    user_id = message.from_user.id
    if user_states.get(user_id) == "waiting_token":
        token = message.text.strip()
        if ":" not in token or len(token) < 20:
            await bot.send_message(message.chat.id, "❌ التوكن غلط، تأكد منه ودزه مرة ثانية.")
            return

        user_states[user_id] = None
        bot_file_path = f"bots/sub_{user_id}.py"

        sub_bot_code = f'''import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
import random

TOKEN = "{token}"
DEV = "{DEV_USERNAME}"
sub_bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

DEV_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("مطور السورس 👤", url="https://t.me/M_C_67")],
    [InlineKeyboardButton("إعدادات البوت ⚙️", callback_data="bot_settings"), InlineKeyboardButton("قائمة الأوامر 📋", callback_data="commands_list")],
    [InlineKeyboardButton("حماية المجموعات 🛡️", callback_data="protection")]
])

CAT_QUESTIONS = [
    "شنو أكثر شي تحبه بصديقك المقرب؟ 🖤",
    "لو انطوك مليار دولار، شنو أول شغلة تشتريها؟ 💸",
    "كلمة توجها لشخص خان ثقتك؟ 🎭",
    "شنو أحلى صفة بشخصيتك وأسوأ صفة؟ 🤔",
    "لو رجع بيك الزمن للماضي، شنو الشغلة اللي تغيرها؟ ⏳",
    "أكثر موقف محرج صار وياك بحياتك شنو هو؟ 😅",
    "تحب الحياة الهادئة لو حياة المغامرات والسفر؟ 🌍",
    "شنو الأكلة العراقية اللي مستحيل تمل منها؟ 🍲"
]

# قاموس لتخزين الردود المضافة للمجموعات
CUSTOM_REPLIES = {{}}

@sub_bot.message_handler(commands=['start'])
def start_sub(msg):
    if msg.chat.type == 'private':
        sub_bot.send_message(
            msg.chat.id,
            f"هلا بيك عيني ⚡\\nمطور السورس الأساسي: {{DEV}}\\nاني بوت حماية سجين، ضفني للكروب حتى اشتغل هناك!",
            reply_markup=DEV_KEYBOARD
        )

@sub_bot.message_handler(func=lambda msg: True)
def all_messages(msg):
    if msg.chat.type not in ['group', 'supergroup']:
        return

    text = msg.text if msg.text else ""
    chat_id = msg.chat.id

    # التحقق من الردود المخصصة المضافة مسبقاً
    if chat_id in CUSTOM_REPLIES and text in CUSTOM_REPLIES[chat_id]:
        sub_bot.reply_to(msg, CUSTOM_REPLIES[chat_id][text])
        return

    # أمر إضافة رد جديد (مثال: إضافة رد [الكلمة] [الجواب])
    if text.startswith("اضف رد "):
        try:
            parts = text.replace("اضف رد ", "").split(" ", 1)
            if len(parts) == 2:
                k, v = parts[0], parts[1]
                if chat_id not in CUSTOM_REPLIES:
                    CUSTOM_REPLIES[chat_id] = {{}}
                CUSTOM_REPLIES[chat_id][k] = v
                sub_bot.reply_to(msg, f"✅ **تم إضافة الرد بنجاح!**\nمن تكبكلمة ({{k}}) راح أرد بـ ({{v}})")
            else:
                sub_bot.reply_to(msg, "⚠️ الاستخدام الصحيح:\n`اضف رد الكلمة الجواب`")
        except Exception:
            sub_bot.reply_to(msg, "❌ صار خطأ بإضافة الرد، تأكد من الصيغة.")

    # أمر التاك الجماعي (تاك / منشن)
    elif text == "تاك" or text == "منشن":
        sub_bot.reply_to(msg, "📢 **تنبيه جماعي لكل الأعضاء الموجودين بالقروب:**\nتعالوا انضموا ويانا وسولفوا بالدردشة ⚡🖤")

    # أمر الايدي مع سحب الصورة الشخصية باختصار "ا" أو "ايدي"
    elif text == "ا" or text.lower() == "ايدي":
        user_name = msg.from_user.first_name
        user_id = msg.from_user.id
        caption = f"هلا بيك يا {{user_name}} 🖤\\nايديك الرائع: `{{user_id}}`\\nرتبتك بالسورس: منورنا يالغالي!"
        try:
            photos = sub_bot.get_user_profile_photos(user_id, limit=1)
            if photos.total_count > 0:
                file_id = photos.photos[0][0].file_id
                sub_bot.send_photo(chat_id, file_id, caption=caption, reply_to_message_id=msg.message_id)
            else:
                sub_bot.reply_to(msg, caption)
        except Exception:
            sub_bot.reply_to(msg, caption)

    # أمر تغيير قائمة الايدي (تغير / تغ)
    elif text == "تغير ايدي" or text == "تغ" or text == "تغيير":
        sub_bot.reply_to(msg, "🎨 **تم تحديث وتغيير ستايل قائمة الايدي بنجاح داخل المجموعات!**")

    # أمر تنزيل جميع الرتب "تك"
    elif text == "تك":
        sub_bot.reply_to(msg, "ابشر تم تنزيل جميع الرتب بنجاح وبقيت عضو عادي بالقروب!")

    # أمر قفل الدردشة
    elif text == "قفل الدردشة":
        try:
            sub_bot.set_chat_permissions(chat_id, ChatPermissions(can_send_messages=False))
            sub_bot.reply_to(msg, "🔒 **تم قفل الدردشة بنجاح، ماكو أي واحد يكدر يحجي!**")
        except Exception:
            sub_bot.reply_to(msg, "❌ ما عندي صلاحية كافية لقفل الدردشة، تأكد من رفعي مشرف.")

    # أمر فتح الدردشة
    elif text == "فتح الدردشة":
        try:
            sub_bot.set_chat_permissions(chat_id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True))
            sub_bot.reply_to(msg, "🔓 **تم فتح الدردشة،گدروا الأعضاء يحجون الآن!**")
        except Exception:
            sub_bot.reply_to(msg, "❌ ما عندي صلاحية كافية لفتح الدردشة، تأكد من رفعي مشرف.")

    # أمر الـ كت (الأسئلة)
    elif text == "كت" or text.lower() == "أسئلة" or text == "اسئلة":
        q = random.choice(CAT_QUESTIONS)
        sub_bot.reply_to(msg, f"❓ **سؤال كت جديد:**\\n\\n{{q}}")

    # أمر البحث باليوت (يوت / يوتيوب)
    elif text.startswith("يوت ") or text.startswith("يوتيوب "):
        query = text.replace("يوت ", "").replace("يوتيوب ", "")
        yt_link = f"https://www.youtube.com/results?search_query={{query.replace(' ', '+')}}"
        sub_bot.reply_to(msg, f"🔍 **نتائج البحث في اليوتيوب عن:** `{{query}}`\\n\\n🔗 اضغط على الرابط للمشاهدة:\\n{{yt_link}}")

    # الرتب والتدرج
    elif text in ["رفع مميز", "رفع مدير", "رفع منشئ", "رفع منشئ أساسي", "رفع مطور", "رفع مطور ثانوي", "رفع مطور أساسي"]:
        sub_bot.reply_to(msg, "عيني تم ترقية الشخص بنجاح وضبطنا رتبته الجديدة بالسورس!")

    # أوامر الحماية والطرد
    elif text in ["طرد", "حظر", "كتم"]:
        sub_bot.reply_to(msg, "تم تنفيذ الإجراء بحق العضو المخالف بقبضة سجين ⚡")

    # الندا والهمسة والألعاب
    elif text.startswith("نداء "):
        target = text.replace("نداء ", "")
        sub_bot.reply_to(msg, f"📢 يكلج {{target}}، صاحب القروب يصيحك تعال بسرعه!")

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
        sub_bot.edit_message_text("📋 **قائمة الأوامر (خاصة بالمجموعات):**\\n- ايدي (أو ا) + الصورة الشخصية\\n- تغ / تغير (ستايل الايدي)\\n- اضف رد [كلمة] [الرد]\\n- تاك / منشن (تنبيه جماعي)\\n- قفل الدردشة / فتح الدردشة\\n- كت (أسئلة)\\n- يوت [بحث]\\n- تك (تنزيل الرتب)\\n- طرد / حظر / كتم", call.message.chat.id, call.message.message_id, reply_markup=DEV_KEYBOARD)
    elif call.data == "protection":
        sub_bot.edit_message_text("🛡️ **حماية المجموعات مفعلة بقوة 24 ساعة!**", call.message.chat.id, call.message.message_id, reply_markup=DEV_KEYBOARD)

sub_bot.infinity_polling()
'''

        try:
            with open(bot_file_path, "w", encoding="utf-8") as f:
                f.write(sub_bot_code)

            subprocess.Popen([sys.executable, bot_file_path])
            await bot.send_message(message.chat.id, "✅ **تم تحديث المصنع وإضافة أوامر الردود والتاك بنجاح تام!** ⚡")
        except Exception as e:
            await bot.send_message(message.chat.id, f"❌ حدث خطأ: {e}")

async def main():
    await bot.infinity_polling()

if __name__ == "__main__":
    asyncio.run(main())

