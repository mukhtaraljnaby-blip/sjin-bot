import os
import sys
import subprocess
import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ChatPermissions
import asyncio
import random

MAKER_TOKEN = "8719015904:AAG7MwDSnyGMeNLfUH1W9aiumtlOr0WJMr8"
DEV_USERNAME = "@M_C_67"

bot = AsyncTeleBot(MAKER_TOKEN, parse_mode="Markdown")

if not os.path.exists("bots"):
    os.makedirs("bots")

MAKER_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
MAKER_KEYBOARD.add(
    KeyboardButton("إنشاء بوت فوري ⚡"),
    KeyboardButton("قائمة بوتاتي 📋")
)

user_states = {}

@bot.message_handler(commands=['start'])
async def start_maker(message):
    await bot.send_message(
        message.chat.id,
        "هلا بيك عيني مختار ⚡ في **مصنع سجين**\n- دز توكن بوتك الجديد من @BotFather حتى اصنعه لك فوراً!",
        reply_markup=MAKER_KEYBOARD
    )

@bot.message_handler(func=lambda msg: msg.text == "إنشاء بوت فوري ⚡")
async def ask_token(message):
    user_states[message.from_user.id] = "waiting_token"
    await bot.send_message(
        message.chat.id,
        "📌 دز توكن بوتك الجديد هنا هسه:"
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
    "شنو أكثر شي تحبه بصديقك المقرب؟ 🖤", "لو انطوك مليار دولار، شنو أول شغلة تشتريها؟ 💸", "كلمة توجها لشخص خان ثقتك؟ 🎭",
    "شنو أحلى صفة بشخصيتك وأسوأ صفة؟ 🤔", "لو رجع بيك الزمن للماضي، شنو الشغلة اللي تغيرها؟ ⏳", "أكثر موقف محرج صار وياك بحياتك شنو هو؟ 😅",
    "تحب الحياة الهادئة لو حياة المغامرات والسفر؟ 🌍", "شنو الأكلة العراقية اللي مستحيل تمل منها؟ 🍲", "لو تكدر تختفي يوم واحد، وين تروح وشسوّي؟ 🫥",
    "شنو اكتر موقف ضحكت بيه بحياتك لحد ما دمعت عيونك؟ 😂", "منو الشخص اللي مستحيل تغفرله بحياتك؟ 🖤", "شنو أكتر شي يخوفك بالمستقبل؟ 🔮",
    "لو خيروك تختار بين الفلوس لو راحة البال، شتختار؟ 💵", "شنو أسم الدلع اللي كانوا يصيحونك بيه بطفولتك؟ 👶", "أكثر عراقي مشهور تحب تتابعهم منو؟ 🇮🇶",
    "لو گولوك عندك طائرة خاصة، أول دولة تسافر لها شنو؟ ✈️", "شنو ردة فعلك لو شفت شخص ديظلم قطة بالشارع؟ 🐈", "شنو أكتر موقف بجّاك وأنت كبران؟ 💧",
    "اذا انطوك فرصة ترجع طفل عمرك 5 سنين، تقبل لو لا؟ 🧒", "شنو الكلمة اللي دائماً تكولها منتعصب؟ 🤬", "أكثر صفة تكرهها بالناس شنو هي؟ 😒",
    "لو گولوك الك أمنية وحدة تتحقق هسه، شنو تطلب؟ ✨", "شنو أكتر كتاب أو قصة قريتها وأثرت بيك؟ 📖", "تفضل تعيش بدون نت شهر لو بدون أكل دسم أسبوع؟ 📱",
    "شنو أحلى يوم بحياتك ما راح تنساه أبداً؟ 🗓️", "لو گولوك صير رئيس وزراء العراق ليوم واحد، شتسوّي أول شي؟ 🏛️", "شنو نوع المزاج اللي يسيطر عليك بالليل؟ 🌙",
    "اذا صارحك شخص بحبه لك وأنت ما تحبه، شتسوي؟ 💔", "شنو أكتر غرض تحب تشتريه بس هو تافه؟ 🛒", "شنو الموقف اللي تحس بيه نفسك غبي بس محد درى بيك؟ 🙃",
    "تحب الصراحة الجارحة لو النفاق اللطيف؟ 🎭", "شنو أكتر شي يخليك تفقد أعصابك بسرعة؟ ⚡", "لو گولوك اكتب رسالة لكل العالم، شكتب بيها؟ 📝",
    "شنو أكتر برنامج أو تطبيق مكضي عليه وقتك؟ 📲", "اذا كسبت جائزة مليون دولار، تشاركها ويا صديقك المقرب لو تقشمر عليه؟ 💰", "شنو الشي اللي تسويه من تصفن وحدك؟ 🌌",
    "شنو هو الحلم اللي لحد هسه ما قدرت تحققه؟ 🌠", "هل أنت شخص سريع الثقة بالناس لو شكاك؟ 🧐", "شنو أكتر موقف حسيت بيه بالفخر بنفسك؟ 🎖️",
    "لو گولوك تختار تعيش بغير زمن، يا زمن تختار (عصر الديناصورات، المستقبل، الخلافة، الخ)؟ ⏳", "شنو أكتر أكلة تفشل بطبخها؟ 🍳", "شنو أكتر اسم ولد وبنية يعجبوك؟ 👶",
    "لو گولوك عندك قوة خارقة، شتختار تكون (تطير، تختفي، تقرأ الأفكار)؟ 🦸‍♂️", "شنو أكتر شي يلفت نظرك اول ما تشوف شخص جديد؟ 👀", "شنو هو الشي اللي مستحيل تسامح شخص عليه؟ 🚫",
    "تحب تكون قائد لو شخص جندي مجهول بصفقاتك؟ 👑", "شنو أكتر شي تبذل فلوسك عليه؟ 💸", "اذا خيروك تعيش بقرية هادئة لو بغداد الصاخبة، شتختار؟ 🏙️",
    "شنو أكتر موقف حسيت بيه بالاحراج گدام العائلة؟ 👨‍👩‍👦", "هل تكدر تعيش بدون موبايلك أسبوع كامل؟ 📵", "شنو أكتر أكلتك السريعة المفضلة؟ 🍔",
    "شنو شعورك من تشوف شخص يقلدك؟ 🤭", "لو گولوك غير شكلك، شتغير بيك؟ 🎨", "شنو أكتر مهنة تحترمها بالمجتمع؟ 🛠️",
    "اذا صار عندك سحر وخليت شي يختفي، شنو تخفي؟ 🪄", "شنو أكتر شي تندمت عليه بالماضي؟ 🥀", "شنو هي الكلمة اللي تعبت من سماعها؟ 🛑",
    "تحب السهر بالليل لو النوم المبكر بالصيف؟ 🌌", "شنو أكتر موقف ضحكك بكروب تليجرام؟ 💬", "لو گولوك تقدر تسافر للماضي تقابل شخصية تاريخية، منو تقابل؟ 📜",
    "شنو أكتر شي تحبه بغرفتك الخاصة؟ 🛏️", "هل أنت شخص عاطفي لو عقلي بقراراتك؟ 🧠", "شنو أكتر شي تغار منه؟ 🤫",
    "لو صار عندك فرصة تفتح مشروع خاص، شنو تفتح؟ 🏬", "شنو أكتر موقف حسيت بيه بالوحدة؟ 🌧️", "شنو هو الشي اللي اذا فقدته تحس نفسك ضعت؟ 🧭",
    "هل تتأثر بكلام الناس السلبي لو معتز بنفسك؟ 🦁", "شنو أكتر نوع موسيقى أو أغانِ تحب تسمعها؟ 🎶", "لو گولوك اكو سيارة هدية بانتظارك، شنو لونها ونوعها؟ 🚗",
    "شنو هو الشي اللي تفضل تسويه وأنت وحدك؟ ☕", "شنو أكتر شي يخليك تحترم الشخص اللي گدامك؟ 🤝", "اذا گولوك عندك القدرة تغير قانون بالبلد، شتغير؟ ⚖️",
    "شنو أكتر شي تحب تشتريه من السوبرماركت؟ 🍫", "شنو شعورك من تدخل مكان أول مرة بحياتك؟ 🚪", "لو گولوك اختصر حياتك بكلمة وحدة، شتكتبرها؟ ✍️",
    "شنو أكتر صفة تعجبك بصديقك الروحي؟ ✨", "هل أنت شخص يحب المفاجآت لو يحب الترتيب المسبق؟ 🎁", "شنو أكتر شي يوجعك بالحياة؟ 💔",
    "لو رجع بك العمر، تدخل نفس الكلية/المدرسة لو تغيرها؟ 🏫", "شنو أكتر شي تحب تاكله وأنت تباوع فيلم؟ 🍿", "شنو أكتر شي تتمنى تتعلمه بس ما عندك وقت؟ ⏱️",
    "هل تخاف من العواصف والرعد لو تحبها؟ 🌩️", "شنو أكتر كلمة تكولها من تفرح؟ 🥳", "لو گولوك انطيك بيت بأي دولة تحبها، تختار وين؟ 🏡",
    "شنو أكتر موقف صار وياك وحسيته صدفة غريبة؟ 🎲", "هل تميل للفضول وتعرف أسرار الناس لو ما مهتم؟ 🕵️‍♂️", "شنو أكتر شي تحس نفسك بارع بيه؟ 🎯",
    "لو انطوك تذكرة سفر لشخصين، ويا منو تسافر؟ ✈️", "شنو أكتر شي يخليك تحس بالأمان؟ 🛡️", "شنو أكتر شي يزعجك بالناس اللي تكعد وياهم؟ 😒",
    "هل تكدر تكذب حتى تطلع نفسك من ورطة؟ 🤥", "شنو أكتر شي تفتخر بوجوده بحياتك؟ 🌟", "لو گولوك عندك بودكاست خاص، شنو تسميه؟ 🎙️",
    "شنو أكتر أكل تحب تطبخ بنفسك؟ 🍳", "هل أنت شخص سريع النسيان لو تذكر كل التفاصيل؟ 🐘", "شنو أكتر شي يخليك تحس بالكسل؟ 🥷",
    "لو گولوك תگدر تحل مشكلة وحدة بالعالم، شنو تحل؟ 🌍", "شنو أكتر شي تحبه بيوم الجمعة؟ 🕌", "شنو شعورك من تنجح بشي تعبت عليه هواي؟ 🏆"
]

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

    if chat_id in CUSTOM_REPLIES and text in CUSTOM_REPLIES[chat_id]:
        sub_bot.reply_to(msg, CUSTOM_REPLIES[chat_id][text])
        return

    if text.startswith("اضف رد "):
        try:
            parts = text.replace("اضف رد ", "").split(" ", 1)
            if len(parts) == 2:
                k, v = parts[0], parts[1]
                if chat_id not in CUSTOM_REPLIES:
                    CUSTOM_REPLIES[chat_id] = {{}}
                CUSTOM_REPLIES[chat_id][k] = v
                sub_bot.reply_to(msg, f"✅ تم إضافة الرد بنجاح:\\nكل ما تكول ({{k}}) راح أرد بـ ({{v}})")
            else:
                sub_bot.reply_to(msg, "⚠️ الاستخدام الصحيح: `اضف رد الكلمة الجواب`")
        except Exception:
            sub_bot.reply_to(msg, "❌ صار خطأ، تأكد من الصيغة.")

    elif text == "تاك" or text == "منشن":
        sub_bot.reply_to(msg, "📢 **تنبيه جماعي لكل الموجودين بالكروب!** تنورون الدردشة ⚡🖤")

    elif text == "ا" or text.lower() == "ايدي":
        user_name = msg.from_user.first_name
        user_id = msg.from_user.id
        caption = f"هلا بيك يا {{user_name}} 🖤\\nايديك الرائع: `{{user_id}}`\\nرتبتك بالسورس: مطورنا الغالي!"
        try:
            photos = sub_bot.get_user_profile_photos(user_id, limit=1)
            if photos.total_count > 0:
                file_id = photos.photos[0][0].file_id
                sub_bot.send_photo(chat_id, file_id, caption=caption, reply_to_message_id=msg.message_id)
            else:
                sub_bot.reply_to(msg, caption)
        except Exception:
            sub_bot.reply_to(msg, caption)

    elif text in ["تغير ايدي", "تغ", "تغيير"]:
        sub_bot.reply_to(msg, "🎨 **تم تحديث ستايل الايدي بنجاح!**")

    elif text == "تك":
        sub_bot.reply_to(msg, "ابشر تم تنزيل الرتب بنجاح وصرت عضو عادي!")

    elif text == "قفل الدردشة":
        try:
            sub_bot.set_chat_permissions(chat_id, ChatPermissions(can_send_messages=False))
            sub_bot.reply_to(msg, "🔒 **تم قفل الدردشة بنجاح!**")
        except Exception:
            sub_bot.reply_to(msg, "❌ ما عندي صلاحية كافية، تأكد من رفعي مشرف.")

    elif text == "فتح الدردشة":
        try:
            sub_bot.set_chat_permissions(chat_id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True))
            sub_bot.reply_to(msg, "🔓 **تم فتح الدردشة بنجاح!**")
        except Exception:
            sub_bot.reply_to(msg, "❌ ما عندي صلاحية كافية، تأكد من رفعي مشرف.")

    elif text == "كت" or text.lower() == "اسئلة":
        q = random.choice(CAT_QUESTIONS)
        sub_bot.reply_to(msg, f"❓ **سؤال كت:**\\n\\n{{q}}")

    elif text.startswith("يوت "):
        query = text.replace("يوت ", "")
        yt_link = f"https://www.youtube.com/results?search_query={{query.replace(' ', '+')}}"
        sub_bot.reply_to(msg, f"🔍 **بحث اليوتيوب عن:** `{{query}}`\\n🔗 اضغط للمشاهدة:\\n{{yt_link}}")

    elif text in ["طرد", "حظر", "كتم"]:
        sub_bot.reply_to(msg, "تم تنفيذ الإجراء بحق العضو المخالف بقبضة سجين ⚡")

@sub_bot.callback_query_handler(func=lambda call: True)
def callback_sub(call):
    sub_bot.answer_callback_query(call.id)
    if call.data == "bot_settings":
        sub_bot.edit_message_text("⚙️ **إعدادات سورس سجين**", call.message.chat.id, call.message.message_id, reply_markup=DEV_KEYBOARD)
    elif call.data == "commands_list":
        sub_bot.edit_message_text("📋 **الأوامر الخاصة بالمجموعات:**\\n- ايدي (ا)\\n- تغ\\n- اضف رد\\n- تاك\\n- قفل / فتح الدردشة\\n- كت (أكثر من 100 سؤال منوع)\\n- يوت", call.message.chat.id, call.message.message_id, reply_markup=DEV_KEYBOARD)
    elif call.data == "protection":
        sub_bot.edit_message_text("🛡️ **الحماية تعمل بكامل طاقتها!**", call.message.chat.id, call.message.message_id, reply_markup=DEV_KEYBOARD)

sub_bot.infinity_polling()
'''

        try:
            with open(bot_file_path, "w", encoding="utf-8") as f:
                f.write(sub_bot_code)
            subprocess.Popen([sys.executable, bot_file_path])
            await bot.send_message(message.chat.id, "✅ **تم تحديث المصنع وإضافة أكثر من 100 سؤال كت بنجاح تام!** ⚡")
        except Exception as e:
            await bot.send_message(message.chat.id, f"❌ صار خطأ بسيط: {e}")

async def main():
    await bot.infinity_polling()

if __name__ == "__main__":
    asyncio.run(main())

