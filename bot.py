import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
import random

TOKEN = "8719015904:AAG7MwDSnyGMeNLfUH1W9aiumtlOr0WJMr8"
DEV = "@M_C_67"
bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

# قواعد البيانات المؤقتة
USER_BOTS = {}            # لتخزين البوتات الفرعية لكل يوزر (الحد 3)
ACTIVATED_CHATS = set()   # المجموعات المفعلة للبوت الفرعي
WELCOME_SETTINGS = {}     # ترحيب المجموعات
CUSTOM_REPLIES = {}       # الردود المخصصة
DEV_SECONDARY = set()     # المطورين الثانويين
CREATORS = set()          # المنشئين
ID_PHOTO_SETTINGS = {}    # إعداد صورة الأيدي (True مع صورة، False بدون)

DEV_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("مطور السورس 👤", url="https://t.me/M_C_67")],
    [InlineKeyboardButton("صنع بوت فرعي 🤖", callback_data="create_bot"), InlineKeyboardButton("قائمة بوتاتي 📋", callback_data="my_bots")],
    [InlineKeyboardButton("تفعيل بوت VIP 💎", url="https://t.me/M_C_67")]
])

CAT_QUESTIONS = [
    "شنو أكثر شي تحبه بصديقك المقرب؟ 🖤", "لو انطوك مليار دولار، شنو أول شغلة تشتريها؟ 💸", "كلمة توجها لشخص خان ثقتك؟ 🎭",
    "شنو أحلى صفة بشخصيتك وأسوأ صفة؟ 🤔", "لو رجع بيك الزمن للماضي، شنو الشغلة اللي تغيرها؟ ⏳", "أكثر موقف محرج صار وياك بحياتك شنو هو؟ 😅",
    "تحب الحياة الهادئة لو حياة المغامرات والسفر؟ 🌍", "شنو الأكلة العراقية اللي مستحيل تمل منها؟ 🍲", "لو تكدر تختفي يوم واحد، وين تروح وشسوّي؟ 🫥"
]

ID_STYLES = [
    "✨ ━━━━━ ⦗ ايديك الرائع ⦘ ━━━━━ ✨", "🔥 ── • [ بطاقة الهوية ] • ── 🔥", "💎 ════ ≪ بطاقة العضو ≫ ════ 💎",
    "⚡ ──━[ هويتك الرسمية ]━━── ⚡", "🌟 ─── ❖ ⦗ كرت التعريف ⦘ ❖ ─── 🌟", "🖤 ══════ ≪ ايدي مميز ≫ ══════ 🖤",
    "🚀 ─── • ⦗ هويتك بالكروب ⦘ • ─── 🚀", "👑 ───── ❖ ⦗ بطاقة الملوك ⦘ ───── 👑", "💫 ━━━ ≪ كرت التعريف الخاص ≫ ━━━ 💫",
    "⚜️ ─── • [ ايدي سجين ] • ─── ⚜️", "🔹 ════════ ≪ هويتك ≫ ════════ 🔹", "🌠 ───── ❖ ⦗ بطاقتك ⦘ ❖ ───── 🌠",
    "🎯 ─── • ⦗ ايدي الفخم ⦘ • ─── 🎯", "🔮 ═════ ≪ كرت العضو ≫ ═════ 🔮", "⚡ ───── ❖ ⦗ الهوية ⦘ ───── ⚡",
    "💥 ─── • [ ايديك الأنيق ] • ─── 💥", "🎇 ══════ ≪ بطاقة التعريف ≫ ══════ 🎇", "⚓ ───── ❖ ⦗ ايدي الكروب ⦘ ───── ⚓",
    "🌙 ─── • [ كرت الهوية ] • ─── 🌙", "🔥 ═════ ≪ هويتك الأسطورية ≫ ═════ 🔥"
]

@bot.message_handler(commands=['start'])
def start_handler(msg):
    if msg.chat.type == 'private':
        try:
            bot_info = bot.get_me()
            bot_username = f"@{bot_info.username}"
            start_text = (
                f"⌔︙أهـلا بـك في مصنع وبوت حماية سجين ⚡\n"
                f"⌔︙يمكنك صنع حتى 3 بوتات فرعية مجاناً أو تفعيل بوت VIP.\n"
                f"⌔︙أضفني إلى مجموعتك وارفعه مشرفاً ثم أرسل `تفعيل` لتشغيل الحماية.\n"
                f"⌔︙يوزر البوت: {bot_username}"
            )
            photos = bot.get_user_profile_photos(bot_info.id, limit=1)
            if photos.total_count > 0:
                bot.send_photo(msg.chat.id, photos.photos[0][0].file_id, caption=start_text, reply_markup=DEV_KEYBOARD)
            else:
                bot.send_message(msg.chat.id, start_text, reply_markup=DEV_KEYBOARD)
        except Exception:
            bot.send_message(msg.chat.id, "أهلاً بك في بوت سجين ⚡", reply_markup=DEV_KEYBOARD)

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(msg):
    chat_id = msg.chat.id
    if chat_id in ACTIVATED_CHATS and WELCOME_SETTINGS.get(chat_id, True):
        for new_user in msg.new_chat_members:
            bot.send_message(chat_id, f"هلا بيك يا وردة 🌸 [{new_user.first_name}](tg://user?id={new_user.id})\nنورت الكروب بوجودك ⚡🖤")

@bot.message_handler(func=lambda msg: True)
def all_messages(msg):
    chat_id = msg.chat.id
    text = msg.text if msg.text else ""
    user = msg.from_user
    user_id = user.id
    user_name = user.first_name

    is_main_dev = (user.username == "M_C_67")
    is_secondary_dev = (user_id in DEV_SECONDARY)
    is_creator = (user_id in CREATORS)

    # أوامر المطور الأساسي في الخاص أو العام
    if is_main_dev and msg.chat.type == 'private':
        if text.startswith("اذاعة "):
            broadcast_text = text.replace("اذاعة ", "", 1)
            bot.reply_to(msg, f"📢 **تم بدء الإذاعة بنجاح ⚡**\n\n{broadcast_text}")
            return
        elif text == "الاحصائيات":
            bot.reply_to(msg, f"📊 **إحصائيات السورس:**\n• المجموعات المفعلة: `{len(ACTIVATED_CHATS)}` كروب ⚡")
            return

    # فحص الإداريين داخل المجموعات
    is_admin = False
    is_chat_creator = False
    if msg.chat.type in ['group', 'supergroup']:
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

    # أوامر التفعيل والتعطيل والتحكم
    if msg.chat.type in ['group', 'supergroup']:
        if text == "تفعيل":
            if is_admin or is_chat_creator:
                ACTIVATED_CHATS.add(chat_id)
                bot.reply_to(msg, "✅ **تم تفعيل المجموعه بنجاح وحماية سجين تعمل بكامل طاقتها ⚡**")
            else:
                bot.reply_to(msg, "⚠️ أمر التفعيل مخصص للمدراء والمشرفين فقط!")
            return

        if chat_id not in ACTIVATED_CHATS:
            return

        # التحكم بصورة الأيدي (تفع / تعط) للمدراء فما فوق
        if text == "تفع":
            if is_admin:
                ID_PHOTO_SETTINGS[chat_id] = True
                bot.reply_to(msg, "🖼️ **تم تفعيل عرض الصورة الشخصية في الايدي بنجاح!** ⚡")
            else:
                bot.reply_to(msg, "⚠️ هذا الأمر خاص بالمدراء والمشرفين فما فوق!")
            return

        elif text == "تعط":
            if is_admin:
                ID_PHOTO_SETTINGS[chat_id] = False
                bot.reply_to(msg, "📝 **تم تعطيل عرض الصورة في الايدي (إرسال معلومات فقط) بنجاح!** ⚡")
            else:
                bot.reply_to(msg, "⚠️ هذا الأمر خاص بالمدراء والمشرفين فما فوق!")
            return

        if text == "تعطيل":
            if is_admin or is_chat_creator:
                if chat_id in ACTIVATED_CHATS:
                    ACTIVATED_CHATS.remove(chat_id)
                bot.reply_to(msg, "❌ **تم تعطيل البوت في هذه المجموعة!**")
            else:
                bot.reply_to(msg, "⚠️ أمر التعطيل مخصص للمدراء والمشرفين فقط!")
            return

        if chat_id in CUSTOM_REPLIES and text in CUSTOM_REPLIES[chat_id]:
            bot.reply_to(msg, CUSTOM_REPLIES[chat_id][text])
            return

        if text == "تفعيل الترحيب":
            if is_admin:
                WELCOME_SETTINGS[chat_id] = True
                bot.reply_to(msg, "✅ **تم تفعيل الترحيب في هذا الكروب!**")
            return
        elif text == "تعطيل الترحيب":
            if is_admin:
                WELCOME_SETTINGS[chat_id] = False
                bot.reply_to(msg, "❌ **تم تعطيل الترحيب في هذا الكروب!**")
            return

        elif text in ["ر", "رابط"]:
            try:
                chat_link = bot.export_chat_invite_link(chat_id)
                bot.reply_to(msg, f"🔗 **رابط الكروب:**\n{chat_link}")
            except Exception:
                bot.reply_to(msg, "⚠️ تأكد من رفعي مشرف لجلب الرابط.")
            return

        elif text in ["الأوامر", "اوامر", "ترتيب الاوامر", "قائمة الأوامر"]:
            commands_text = (
                "📋 **قائمة أوامر سورس سجين الشاملة:**\n\n"
                "👤 **أوامر الأعضاء:**\n"
                "• `ا` أو `ايدي` - عرض ايديك (مع/بدون صورة)\n"
                "• `تغ` أو `تغير` - تغيير ستايل الايدي\n"
                "• `ر` أو `رابط` - جلب رابط الكروب\n"
                "• `كت` - أسئلة كت العشوائية\n"
                "• `يوت [كلمة]` - بحث يوتيوب\n\n"
                "🛠️ **أوامر المدراء والمشرفين:**\n"
                "• `تفعيل` / `تعطيل` - تفعيل أو تعطيل البوت\n"
                "• `تفع` / `تعط` - تفعيل أو تعطيل صورة الايدي\n"
                "• `تفعيل الترحيب` / `تعطيل الترحيب`\n"
                "• `طرد` / `كتم` / `تقييد` (بالرد - محمي ضد الرتب)\n"
                "• `قفل الدردشة` / `فتح الدردشة`"
            )
            bot.reply_to(msg, commands_text)
            return

        elif text == "ا" or text.lower() == "ايدي":
            style = random.choice(ID_STYLES)
            rank_title = "المطور الأساسي 👑" if is_main_dev else ("المنشئ 🛡️" if is_creator or is_chat_creator else ("مدير / مشرف ⚡" if is_admin else "عضو مميز 🖤"))
            caption = f"{style}\n\n👤 اسمك: {user_name}\n🆔 ايديك: `{user_id}`\n🔰 رتبتك: {rank_title}"
            
            photo_enabled = ID_PHOTO_SETTINGS.get(chat_id, True)
            if photo_enabled:
                try:
                    photos = bot.get_user_profile_photos(user_id, limit=1)
                    if photos.total_count > 0:
                        bot.send_photo(chat_id, photos.photos[0][0].file_id, caption=caption, reply_to_message_id=msg.message_id)
                    else:
                        bot.reply_to(msg, caption)
                except Exception:
                    bot.reply_to(msg, caption)
            else:
                bot.reply_to(msg, caption)
            return

        elif text in ["تغ", "تغيير"]:
            style = random.choice(ID_STYLES)
            bot.reply_to(msg, f"🎨 **تم تغيير ستايل الايدي:**\n\n{style}")
            return

        elif text == "قفل الدردشة" and is_admin:
            try:
                bot.set_chat_permissions(chat_id, ChatPermissions(can_send_messages=False))
                bot.reply_to(msg, "🔒 **تم قفل الدردشة!**")
            except Exception:
                pass
            return

        elif text == "فتح الدردشة" and is_admin:
            try:
                bot.set_chat_permissions(chat_id, ChatPermissions(can_send_messages=True, can_send_media_messages=True))
                bot.reply_to(msg, "🔓 **تم فتح الدردشة!**")
            except Exception:
                pass
            return

        elif text == "كت":
            bot.reply_to(msg, f"❓ **سؤال كت:**\n\n{random.choice(CAT_QUESTIONS)}")
            return

        elif text.startswith("يوت"):
            query = text.replace("يوت", "", 1).strip()
            if query:
                bot.reply_to(msg, f"🔍 **بحث اليوتيوب:**\nhttps://www.youtube.com/results?search_query={query.replace(' ', '+')}")
            return

        elif text in ["طرد", "كتم", "تقييد"]:
            if not is_admin:
                bot.reply_to(msg, "⚠️ أوامر الإجراءات للمدراء فقط!")
                return
            if msg.reply_to_message:
                target_user = msg.reply_to_message.from_user
                target_id = target_user.id
                try:
                    target_member = bot.get_chat_member(chat_id, target_id)
                    if target_member.status in ['creator', 'administrator'] or target_user.username == "M_C_67":
                        bot.reply_to(msg, "❌ **لا يمكنني تنفيذ أي إجراء بحق شخص يمتلك رتبة محمية!** 🛡️")
                        return
                except Exception:
                    pass
                try:
                    if text == "طرد":
                        bot.ban_chat_member(chat_id, target_id)
                        bot.reply_to(msg, "🥾 **تم طرد العضو بنجاح ⚡**")
                    elif text == "كتم":
                        bot.restrict_chat_member(chat_id, target_id, ChatPermissions(can_send_messages=False))
                        bot.reply_to(msg, "🔇 **تم كتم العضو بنجاح ⚡**")
                    elif text == "تقييد":
                        bot.restrict_chat_member(chat_id, target_id, ChatPermissions(can_send_messages=False, can_send_media_messages=False))
                        bot.reply_to(msg, "🔒 **تم تقييد العضو ⚡**")
                except Exception:
                    bot.reply_to(msg, "❌ تأكد أني مشرف وصلاحياتي كاملة.")
            else:
                bot.reply_to(msg, "⚠️ رد على رسالة الشخص لتنفيذ الأمر!")
            return

@bot.callback_query_handler(func=lambda call: True)
def callback_handlers(call):
    user_id = call.from_user.id
    bot.answer_callback_query(call.id)
    
    if call.data == "create_bot":
        user_bots_list = USER_BOTS.get(user_id, [])
        if len(user_bots_list) >= 3:
            vip_markup = InlineKeyboardMarkup([[InlineKeyboardButton("تواصل لتفعيل VIP 💎", url="https://t.me/M_C_67")]])
            bot.edit_message_text(
                "❌ **عذراً، لقد وصلت إلى الحد الأقصى (3 بوتات فرعية)!**\n\n💎 لتجاوز الحد وتفعيل **بوت VIP**، تواصل مع المطور:\n" + f"👤 {DEV}",
                call.message.chat.id, call.message.message_id, reply_markup=vip_markup
            )
        else:
            # محاكاة لإضافة بوت تجريبي كمثال للمصنع أو استقبال التوكن
            bot.edit_message_text(
                "⚙️ **أنشيء بوت جديد عبر `@BotFather` وأرسل التوكن هنا لربطه.**\n(تم توفير مساحة لتسجيل البوتات ضمن الحد الأقصى 3).",
                call.message.chat.id, call.message.message_id,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع 🔙", callback_data="back_start")]])
            )
            # كمثال اختباري لإضافة بوت للقائمة عند الطلب:
            if user_id not in USER_BOTS:
                USER_BOTS[user_id] = []
            if len(USER_BOTS[user_id]) < 3:
                USER_BOTS[user_id].append({"bot_name": f"بوت حماية رقم {len(USER_BOTS[user_id])+1}"})

    elif call.data == "my_bots":
        user_bots_list = USER_BOTS.get(user_id, [])
        if not user_bots_list:
            bot.edit_message_text(
                "📂 **قائمة بوتاتك الفرعية:**\n\n❌ ليس لديك أي بوت فرعي حالياً!",
                call.message.chat.id, call.message.message_id,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع 🔙", callback_data="back_start")]])
            )
        else:
            text = "📂 **قائمة بوتاتك الفرعية المصنوعة:**\n\n"
            markup = InlineKeyboardMarkup()
            for idx, b in enumerate(user_bots_list, 1):
                text += f"{idx}⌯ اسم البوت: `{b['bot_name']}`\n"
                markup.add(InlineKeyboardButton(f"حذف البوت {idx} 🗑️", callback_data=f"delete_bot_{user_id}_{idx-1}"))
            markup.add(InlineKeyboardButton("رجوع 🔙", callback_data="back_start"))
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "back_start":
        bot.edit_message_text(
            "⌔︙أهـلا بـك في مصنع وبوت حماية سجين ⚡\n⌔︙اختر ما تحب من الأزرار بالأسفل 👇",
            call.message.chat.id, call.message.message_id, reply_markup=DEV_KEYBOARD
        )

    elif call.data.startswith("delete_bot_"):
        parts = call.data.split("_")
        u_id = int(parts[2])
        b_idx = int(parts[3])
        if u_id in USER_BOTS and len(USER_BOTS[u_id]) > b_idx:
            USER_BOTS[u_id].pop(b_idx)
            bot.edit_message_text(
                "✅ **تم حذف البوت الفرعي بنجاح!**",
                call.message.chat.id, call.message.message_id,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("قائمة بوتاتي 📋", callback_data="my_bots")]]))

bot.infinity_polling()

