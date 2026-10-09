import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
import random

TOKEN = "8719015904:AAG7MwDSnyGMeNLfUH1W9aiumtlOr0WJMr8"
DEV = "@M_C_67"
bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

USER_BOTS = {}            
WAITING_FOR_TOKEN = set() 
ACTIVATED_CHATS = set()   
WELCOME_SETTINGS = {}     
DEV_SECONDARY = set()     
CREATORS = set()          
ID_PHOTO_SETTINGS = {}    

MAKER_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("صنع بوت فرعي جديد 🤖", callback_data="create_bot")],
    [InlineKeyboardButton("قائمة بوتاتي 📋", callback_data="my_bots"), InlineKeyboardButton("تفعيل بوت VIP 💎", url="https://t.me/M_C_67")],
    [InlineKeyboardButton("مطور المصنع 👤", url="https://t.me/M_C_67")]
])

# أكثر من 100 سؤال كت مرتبة لعيونك
CAT_QUESTIONS = [
    "شنو أكثر شي تحبه بصديقك المقرب؟ 🖤", "لو انطوك مليار دولار، شنو أول شغلة تشتريها؟ 💸", "كلمة توجها لشخص خان ثقتك؟ 🎭",
    "شنو أحلى صفة بشخصيتك وأسوأ صفة؟ 🤔", "لو رجع بيك الزمن للماضي، شنو الشغلة اللي تغيرها؟ ⏳", "أكثر موقف محرج صار وياك بحياتك شنو هو؟ 😅",
    "تحب الحياة الهادئة لو حياة المغامرات والسفر؟ 🌍", "شنو الأكلة العراقية اللي مستحيل تمل منها؟ 🍲", "لو تكدر تختفي يوم واحد، وين تروح وشسوّي؟ 🫥",
    "شنو اكتر اسم تحب تسميه بالمستقبل؟ 👶", "لو خيروك تعيش بلا إنترنت أو بلا أصدقاء، شتختار؟ 📵", "شنو أكتر موقف ضحكك لدرجة البجي بحياتك؟ 😂",
    "شخص تعتبره قدوتك بالحياة وليش؟ 🌟", "شنو ردت فعلك لو شخص عيط بوجهك بدون سبب؟ 😡", "لو كولشي متوفر عندك، وين تتمنى تعيش؟ 🏡",
    "شنو أكتر صفة تكرهها بالناس؟ 😒", "إذا انطوك فرصة ترجع لليوم الصبح، شنو تغير بي؟ 🌅", "شنو أكتر شي يخوفك بالمستقبل؟ 🔮",
    "شنو هوايتك السرية اللي ما حد يعرفها؟ 🤫", "لو صار عندك مصنع بوتات، شنو أول شي تسويه؟ 🤖", "كلمة تعتذر بيها لنفسك، شنو تكولها؟ 🥀",
    "شنو أكتر طبخة تعرف تسويها؟ 🍳", "لو كالوا لك عندك أمنية وحدة وتتحقق، شنو تطلب؟ 🌠", "شكد نسبة العصبية بحياتك من 10؟ ⚡",
    "اذا جان عندك القدرة تقرأ أفكار الناس، تقرأها لو تخاف؟ 🧠", "شنو أكتر شي يخليك تفقد أعصابك بسرعة؟ 🔥", "تحب تعترف بغلطك لو تكابر؟ 🎭",
    "شنو أحلى هدية اجتك بحياتك؟ 🎁", "لو كالوا لك بدّل اسمك، شنو تختار؟ 🏷️", "أكتر مكان ترتاح من تقعد بي لوحدك؟ 🌊",
    "شنو رد فعلك من تشوف شخص يبجي؟ 🥺", "تثق بالبسهولة لو تحتاج وقت؟ ⏳", "شنو أكتر كتاب أو قصة أثرت بيك؟ 📚",
    "إذا كالو لك سافر لدولة وحدة وممنوع ترجع، وين تروح؟ ✈️", "شنو أكتر كلمة تكولها بحياتك اليومية؟ 🗣️", "أحلى مرحلة عمرية عشتها بحياتك؟ 🧸",
    "شنو أكتر مقلب صاير بيك وانقهرت منه؟ 🤡", "تحب الشتا لو الصيف وليش؟ 🌧️", "شنو رأيك بالحب من أول نظرة؟ 💘",
    "أكتر كلمة تفرحك من تسمعها؟ 🌸", "لو صرت ممثل مشهور، شنو الدور اللي تتمناه؟ 🎬", "شنو أكتر شي تندمت عليه لأن ما سويته؟ 💨",
    "شخص مستحيل تنسى موقفه وياك بالشدة؟ 🤝", "شنو أكتر شي يزعجك بالناس المزاجية؟ 🌀", "اذا انطوك فرصة تنام شهر كامل وتكعد، توافق؟ 🛌",
    "شنو أكتر شي تفتخر بي سويته بحياتك؟ 🎖️", "هل أنت شخص غيور بطبيعتك؟ 🖤", "شنو رد فعلك لو شخص انتقدك قدام الناس؟ 🛑",
    "لو انطوك طاقة خفية، شتختار (طيران، اختفاء، قراءة أفكار)؟ 🦸‍♂️", "شنو أكتر أكلة تكرهها بحياتك؟ 🤢", "شنو أكتر موقف حسيت بيه بالامتنان؟ 🙏",
    "هل تكدر تكعد الصبح ببدون منبه؟ ⏰", "شنو أكتر شي يلفت انتباهك بالشخص أول ما تشوفه؟ 👀", "اذا صار عندك مليون متابع، شنو تقدم محتوى؟ 📱",
    "شنو أكتر موقف حسيت بيه بالظلم؟ ⚖️", "تحب الأكل الحار لو البارد؟ 🌶️", "شنو أكتر شي تخاف تخسره بحياتك؟ 💔",
    "إذا جان عندك قناة تليجرام، شنو تسميها؟ 📢", "شنو أكتر شي يخليك تبتسم بدون سبب؟ 😊", "هل أنت شخص صريح لدرجة الجرح؟ 🗡️",
    "شنو أكتر وقت تحس بي نفسك منتج ونشط؟ 🔋", "شنو أكتر شي تعبت عليه بحياتك ونلت بسببه نتيجة حلوة؟ 🏆", "إذا كالوا لك اكتب رسالة لكل شخص خانك، شتكتب؟ ✉️",
    "شنو أكتر شيء يلغي تعبك ونفسيتك التعبة؟ 🎧", "شنو العادة السيئة اللي تتمنى تخلص منها؟ 🚬", "إذا جان بيدك تغير قانون بالدولة، شتغير؟ 🏛️",
    "شنو أكتر شي تحبه بغرفتك؟ 🛏️", "شنو نوع الموسيقى أو الأناشيد اللي تفضلها؟ 🎵", "لو صار عندك المقدرة تسافر للماضي، أي سنة تختار؟ 🕰️",
    "شنو أكتر موقف خلاك تحس بالكبر والمسؤولية؟ 🧠", "هل تؤمن بالحظ لو بالتعب والسعي؟ 🎯", "شنو أكتر صفة تعجبك بالمحيطين بيك؟ 💎",
    "إذا انطوك فرصة تكون بطل قصة خيالية، تختار تكون منو؟ 🦸", "شنو أكتر شي يخليك تثق بشخص غريب؟ 🤝", "شنو شعورك أول ما تفتح عيونك الصبح؟ 🌅",
    "شنو أكتر شي يضوجك من شخص يتأخر عليك بموعد؟ ⌛", "لو خيروك بين العزلة واللمة، شتختار؟ 🌌", "شنو أكتر شي تتابعه بيوتيوب؟ 📺",
    "شنو أكتر اكله تفضلها بالليل؟ 🍕", "إذا جان بيدك تلغي شغلة وحدة من العالم، شتلغي؟ 🗑️", "شنو أكتر شي تحب تسويه من تكون ضايج؟ 🚶‍♂️",
    "شنو أكتر موقف خلاك تضحك على نفسك؟ 😂", "هل أنت شخص يتأثر بالانتقادات لو تخليه ورا ضهرك؟ 🛡️", "شنو أمنيتك لهل السنة؟ 🎄",
    "شنو أكتر شي تلاحظه بشخصية المقابل؟ 🔍", "إذا انطوك فرصة تغير شكلك، شنو تغير؟ ✨", "شنو أكتر اسم دلع تحب يصيحونك بي؟ 🗣️",
    "هل تحب تسوي مقالب بالناس؟ 🎭", "شنو أكتر شي يخليك تفقد الأمل وترجع تعتمده؟ 🔄", "شنو أكتر صفة توارثتها من أهلك؟ 🧬",
    "لو كالو لك تكدر تطير لساعة وحدة، وين تطير؟ 🦅", "شنو أكتر شي يخليك تحس بالأمان؟ 🏡", "هل تكدر تقاوم النوم والسهر؟ 🌙",
    "شنو أكتر كلمة تقال الك وتفرحك؟ 💌", "اذا انطوك كتاب حياتك وتقرأ صفحة النهاية، تقراها لو تخاف؟ 📖", "شنو رأيك بالناس اللي تحكي من ورا ضهرك؟ 🗣️",
    "شنو أكتر موقف حسيت بيه بالفخر؟ 🦅", "ختاماً، كلمة توجها لنفسك اليوم؟ 🖤"
]

ID_STYLES = [
    "✨ ━━━━━ ⦗ ايديك الرائع ⦘ ━━━━━ ✨", "🔥 ── • [ بطاقة الهوية ] • ── 🔥", "💎 ════ ≪ بطاقة العضو ≫ ════ 💎",
    "⚡ ──━[ هويتك الرسمية ]━━── ⚡", "🌟 ─── ❖ ⦗ كرت التعريف ⦘ ❖ ─── 🌟", "🖤 ══════ ≪ ايدي مميز ≫ ══════ 🖤",
    "🚀 ─── • ⦗ هويتك بالكروب ⦘ • ─── 🚀", "👑 ───── ❖ ⦗ بطاقة الملوك ⦘ ───── 👑", "💫 ━━━ ≪ كرت التعريف الخاص ≫ ━━━ 💫",
    "⚜️ ─── • [ ايدي سجين ] • ─── ⚜️", "🔹 ════════ ≪ هويتك ≫ ════════ 🔹", "🌠 ───── ❖ ⦗ بطاقتك ⦘ ───── 🌠",
    "🎯 ─── • ⦗ ايدي الفخم ⦘ • ─── 🎯", "🔮 ═════ ≪ كرت العضو ≫ ═════ 🔮", "⚡ ───── ❖ ⦗ الهوية ⦘ ───── ⚡",
    "💥 ─── • [ ايديك الأنيق ] • ─── 💥", "🎇 ══════ ≪ بطاقة التعريف ≫ ══════ 🎇", "⚓ ───── ❖ ⦗ ايدي الكروب ⦘ ───── ⚓",
    "🌙 ─── • [ كرت الهوية ] • ─── 🌙", "🔥 ═════ ≪ هويتك الأسطورية ≫ ═════ 🔥"
]

@bot.message_handler(commands=['start'])
def start_handler(msg):
    if msg.chat.type == 'private':
        if msg.from_user.id in WAITING_FOR_TOKEN:
            WAITING_FOR_TOKEN.remove(msg.from_user.id)
            
        start_text = (
            f"⌔︙أهـلا بـك في مصنع بـوتات حماية سجين ⚡\n"
            f"⌔︙هذا البوت مخصص لصنع وإدارة بوتات الحماية الفرعية الخاصة بك.\n"
            f"⌔︙الحد الأقصى للبوتات المجانية هو `3 بوتات` فقط.\n"
            f"⌔︙اختر ما تحب من الأزرار بالأسفل للبدء 👇"
        )
        bot.send_message(msg.chat.id, start_text, reply_markup=MAKER_KEYBOARD)

@bot.message_handler(func=lambda msg: msg.chat.type == 'private')
def private_messages_handler(msg):
    user_id = msg.from_user.id
    text = msg.text if msg.text else ""

    if user_id in WAITING_FOR_TOKEN:
        if text.startswith('/'):
            bot.reply_to(msg, "⚠️ يرجى إرسال توكن صالح للبوت أو اضغط /start للإلغاء.")
            return

        try:
            test_bot = telebot.TeleBot(text.strip())
            bot_info = test_bot.get_me()
            bot_username = f"@{bot_info.username}"
            
            if user_id not in USER_BOTS:
                USER_BOTS[user_id] = []

            USER_BOTS[user_id].append({
                "bot_name": bot_info.first_name,
                "bot_username": bot_username,
                "bot_token": text.strip()
            })
            
            WAITING_FOR_TOKEN.remove(user_id)
            
            success_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("قائمة بوتاتي 📋", callback_data="my_bots")],
                [InlineKeyboardButton("رجوع 🔙", callback_data="back_start")]
            ])
            bot.send_message(
                msg.chat.id,
                f"✅ **تم صنع وربط البوت الفرعي بنجاح!**\n\n"
                f"🤖 **يوزر البوت:** {bot_username}\n"
                f"📌 **اسم البوت:** {bot_info.first_name}\n\n"
                f"الإصدار مضاف الآن داخل قائمة بوتاتك.",
                reply_markup=success_markup
            )
        except Exception:
            bot.reply_to(msg, "❌ **التوكن غير صحيح أو منتهي الصلاحية!**\nتأكد من توكن البوت المرسل من `@BotFather` وأعد إرساله مجدداً.")
        return

    is_main_dev = (msg.from_user.username == "M_C_67")
    if is_main_dev:
        if text.startswith("اذاعة "):
            broadcast_text = text.replace("اذاعة ", "", 1)
            bot.reply_to(msg, f"📢 **تم بدء الإذاعة بنجاح ⚡**\n\n{broadcast_text}")
            return
        elif text == "الاحصائيات":
            bot.reply_to(msg, f"📊 **إحصائيات السورس:**\n• المجموعات المفعلة: `{len(ACTIVATED_CHATS)}` كروب ⚡")
            return

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(msg):
    chat_id = msg.chat.id
    if chat_id in ACTIVATED_CHATS and WELCOME_SETTINGS.get(chat_id, True):
        for new_user in msg.new_chat_members:
            bot.send_message(chat_id, f"هلا بيك يا وردة 🌸 [{new_user.first_name}](tg://user?id={new_user.id})\nنورت الكروب بوجودك ⚡🖤")

@bot.message_handler(func=lambda msg: msg.chat.type in ['group', 'supergroup'])
def group_messages_handler(msg):
    chat_id = msg.chat.id
    text = msg.text if msg.text else ""
    user = msg.from_user
    user_id = user.id
    user_name = user.first_name

    is_main_dev = (user.username == "M_C_67")
    is_secondary_dev = (user_id in DEV_SECONDARY)
    is_creator = (user_id in CREATORS)

    is_admin = False
    is_chat_creator = False
    try:
        member = bot.get_chat_member(chat_id, user_id)
        if member.status == 'creator':
            is_chat_creator = True
            is_admin = True
        elif member.status == 'administrator':
            is_admin = True
    except Exception:
        pass

    if is_main_dev or is_secondary_dev or is_creator:
        is_admin = True

    if text == "تفعيل":
        if is_admin or is_chat_creator:
            ACTIVATED_CHATS.add(chat_id)
            bot.reply_to(msg, "✅ **تم تفعيل المجموعة بنجاح وحماية سجين تعمل بكامل طاقتها ⚡**")
        else:
            bot.reply_to(msg, "⚠️ أمر التفعيل مخصص للمدراء والمشرفين فقط!")
        return

    if chat_id not in ACTIVATED_CHATS:
        return

    if text == "تفع":
        if is_admin:
            ID_PHOTO_SETTINGS[chat_id] = True
            bot.reply_to(msg, "🖼️ **تم تفعيل عرض الصورة الشخصية في الأيدي بنجاح!** ⚡")
        else:
            bot.reply_to(msg, "⚠️ هذا الأمر خاص بالمدراء والمشرفين!")
        return
    elif text == "تعط":
        if is_admin:
            ID_PHOTO_SETTINGS[chat_id] = False
            bot.reply_to(msg, "📝 **تم تعطيل عرض الصورة في الأيدي (إرسال معلومات نصية) بنجاح!** ⚡")
        else:
            bot.reply_to(msg, "⚠️ هذا الأمر خاص بالمدراء والم
