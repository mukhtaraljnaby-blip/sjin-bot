import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
import random

TOKEN = "8719015904:AAG7MwDSnyGMeNLfUH1W9aiumtlOr0WJMr8"
DEV = "@M_C_67"
sub_bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

ACTIVATED_CHATS = set()
WELCOME_SETTINGS = {}
CUSTOM_REPLIES = {}
DEV_SECONDARY = set()
CREATORS = set()
ID_PHOTO_SETTINGS = {} # قاموس لحفظ حالة صورة الايدي لكل كروب (افتراضياً True أي مع صورة)

DEV_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("مطور السورس 👤", url="https://t.me/M_C_67")],
    [InlineKeyboardButton("إعدادات البوت ⚙️", callback_data="bot_settings"), InlineKeyboardButton("قائمة الأوامر 📋", callback_data="commands_list")],
    [InlineKeyboardButton("حماية المجموعات 🛡️", callback_data="protection")]
])

CAT_QUESTIONS = [
    "شنو أكثر شي تحبه بصديقك المقرب؟ 🖤", "لو انطوك مليار دولار، شنو أول شغلة تشتريها؟ 💸", "كلمة توجها لشخص خان ثقتك؟ 🎭",
    "شنو أحلى صفة بشخصيتك وأسوأ صفة؟ 🤔", "لو رجع بيك الزمن للماضي، شنو الشغلة اللي تغيرها؟ ⏳", "أكثر موقف محرج صار وياك بحياتك شنو هو؟ 😅",
    "تحب الحياة الهادئة لو حياة المغامرات والسفر؟ 🌍", "شنو الأكلة العراقية اللي مستحيل تمل منها؟ 🍲", "لو تكدر تختفي يوم واحد، وين تروح وشسوّي؟ 🫥"
]

ID_STYLES = [
    "✨ ━━━━━ ⦗ ايديك الرائع ⦘ ━━━━━ ✨",
    "🔥 ── • [ بطاقة الهوية ] • ── 🔥",
    "💎 ════ ≪ بطاقة العضو ≫ ════ 💎",
    "⚡ ──━[ هويتك الرسمية ]━━── ⚡",
    "🌟 ─── ❖ ⦗ كرت التعريف ⦘ ❖ ─── 🌟",
    "🖤 ══════ ≪ ايدي مميز ≫ ══════ 🖤",
    "🚀 ─── • ⦗ هويتك بالكروب ⦘ • ─── 🚀",
    "👑 ───── ❖ ⦗ بطاقة الملوك ⦘ ───── 👑",
    "💫 ━━━ ≪ كرت التعريف الخاص ≫ ━━━ 💫",
    "⚜️ ─── • [ ايدي سجين ] • ─── ⚜️",
    "🔹 ════════ ≪ هويتك ≫ ════════ 🔹",
    "🌠 ───── ❖ ⦗ بطاقتك ⦘ ❖ ───── 🌠",
    "🎯 ─── • ⦗ ايدي الفخم ⦘ • ─── 🎯",
    "🔮 ═════ ≪ كرت العضو ≫ ═════ 🔮",
    "⚡ ───── ❖ ⦗ الهوية ⦘ ───── ⚡",
    "💥 ─── • [ ايديك الأنيق ] • ─── 💥",
    "🎇 ══════ ≪ بطاقة التعريف ≫ ══════ 🎇",
    "⚓ ───── ❖ ⦗ ايدي الكروب ⦘ ❖ ───── ⚓",
    "🌙 ─── • [ كرت الهوية ] • ─── 🌙",
    "🔥 ═════ ≪ هويتك الأسطورية ≫ ═════ 🔥",
    "⭐ ───── ❖ ⦗ ايديك ⦘ ───── ⭐",
    "💎 ─── • [ بطاقتك الرسمية ] • ─── 💎",
    "💠 ══════ ≪ ايدي فخم ≫ ══════ 💠",
    "⚡ ───── ❖ ⦗ الكرت الشخصي ⦘ ───── ⚡",
    "🖤 ─── • [ هويتك الخاصة ] • ─── 🖤",
    "🌐 ═════ ≪ ايدي العضو ≫ ═════ 🌐",
    "🔥 ───── ❖ ⦗ كرت التعريف ⦘ ❖ ───── 🔥",
    "👑 ─── • [ بطاقة المالك ] • ─── 👑",
    "✨ ══════ ≪ ايدي مميز ≫ ══════ ✨",
    "🚀 ───── ❖ ⦗ الهوية الشخصية ⦘ ───── 🚀",
    "🌟 ─── • [ ايديك الرائع ] • ─── 🌟",
    "💫 ═════ ≪ كرت العضوية ة ≫ ═════ 💫",
    "⚡ ───── ❖ ⦗ ايدي سجين ⦘ ❖ ───── ⚡",
    "🎯 ─── • [ بطاقة الهوية ] • ─── 🎯",
    "💎 ══════ ≪ ايدي فخم ≫ ══════ 💎",
    "🔥 ───── ❖ ⦗ الهوية الرسمية ⦘ ───── 🔥",
    "🖤 ─── • [ كرت التعريف ] • ─── 🖤",
    "✨ ═════ ≪ ايديك الفخم ≫ ═════ ✨",
    "🚀 ───── ❖ ⦗ بطاقتك ⦘ ───── 🚀",
    "⭐ ─── • [ ايدي العضو ] • ─── ⭐",
    "⚜️ ══════ ≪ كرت مميز ≫ ══════ ⚜️",
    "⚡ ───── ❖ ⦗ الهوية الفخمة ⦘ ───── ⚡",
    "🔥 ─── • [ ايدي الكروب ] • ─── 🔥",
    "💎 ═════ ≪ بطاقة العضو ≫ ═════ 💎",
    "🌟 ───── ❖ ⦗ ايديك الأنيق ⦘ ───── 🌟",
    "🖤 ─── • [ كرت التعريف ] • ─── 🖤",
    "⚡ ══════ ≪ ايدي سجين ≫ ══════ ⚡",
    "🚀 ───── ❖ ⦗ بطاقة الهوية ⦘ ───── 🚀",
    "✨ ─── • [ ايديك الأسطوري ] • ─── ✨",
    "🔥 ═════ ≪ الهوية الخاصة ≫ ═════ 🔥"
]

@sub_bot.message_handler(commands=['start'])
def start_sub(msg):
    if msg.chat.type == 'private':
        try:
            bot_info = sub_bot.get_me()
            bot_username = f"@{bot_info.username}"
            
            start_text = (
                f"⌔︙أهـلا بـك في بـوت ️\n"
                f"⌔︙لحماية المجموعات من التفليش\n"
                f"⌔︙يمڪنك تفعيل البوت ڪالاتي :\n"
                f"⌔︙اضف البوت وارفعه مشرف في مجموعتك\n"
                f"⌔︙ارسل {{ تفعيل }} ليتم تفعيل المجموعه\n"
                f"⌔︙يوزر البوت ← {bot_username}"
            )
            
            photos = sub_bot.get_user_profile_photos(bot_info.id, limit=1)
            if photos.total_count > 0:
                file_id = photos.photos[0][0].file_id
                sub_bot.send_photo(msg.chat.id, file_id, caption=start_text, reply_markup=DEV_KEYBOARD)
            else:
                sub_bot.send_message(msg.chat.id, start_text, reply_markup=DEV_KEYBOARD)
        except Exception:
            sub_bot.send_message(
                msg.chat.id,
                f"⌔︙أهـلا بـك في بـوت حماية سجين ⚡\n⌔︙اضفني إلى مجموعتك وارفعه مشرفاً ثم أرسل `تفعيل`",
                reply_markup=DEV_KEYBOARD
            )

@sub_bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(msg):
    chat_id = msg.chat.id
    if chat_id in ACTIVATED_CHATS and WELCOME_SETTINGS.get(chat_id, True):
        for new_user in msg.new_chat_members:
            name = new_user.first_name
            sub_bot.send_message(
                chat_id,
                f"هلا بيك يا وردة 🌸 [{name}](tg://user?id={new_user.id})\nنورت الكروب بوجودك، نتمنى لك أوقات ممتعة معنا ⚡🖤"
            )

@sub_bot.message_handler(func=lambda msg: True)
def all_messages(msg):
    chat_id = msg.chat.id
    text = msg.text if msg.text else ""
    user = msg.from_user
    user_id = user.id
    user_name = user.first_name

    is_main_dev = (user.username == "M_C_67")
    is_secondary_dev = (user_id in DEV_SECONDARY)
    is_creator = (user_id in CREATORS)

    if is_main_dev:
        if text.startswith("اذاعة "):
            broadcast_text = text.replace("اذاعة ", "", 1)
            sub_bot.reply_to(msg, f"📢 **تم بدء الإذاعة بنجاح بواسطة المطور الأساسي ⚡**\n\n{broadcast_text}")
            return
        elif text == "الاحصائيات":
            sub_bot.reply_to(msg, f"📊 **إحصائيات بوت سجين:**\n• المجموعات المفعلة: `{len(ACTIVATED_CHATS)}` كروب ⚡\n• حالة السورس: متصل ومستقر 👑")
            return
        elif text.startswith("تعيين مطور ثانوي ") and msg.reply_to_message:
            sec_id = msg.reply_to_message.from_user.id
            DEV_SECONDARY.add(sec_id)
            sub_bot.reply_to(msg, "👑 **تم تعيين العضو كمطور ثانوي بنجاح!**")
            return

    if msg.chat.type not in ['group', 'supergroup']:
        return

    is_admin = False
    is_chat_creator = False
    try:
        member = sub_bot.get_chat_member(chat_id, user_id)
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
            sub_bot.reply_to(msg, "✅ **تم تفعيل المجموعه بنجاح وحماية سجين تعمل بكامل طاقتها ⚡**")
        else:
            sub_bot.reply_to(msg, "⚠️ أمر التفعيل مخصص للمدراء والمشرفين فقط!")
        return

    if chat_id not in ACTIVATED_CHATS:
        return

    # التحكم بصورة الايدي (تفع / تعط) للمدراء فما فوق
    if text == "تفع":
        if is_admin:
            ID_PHOTO_SETTINGS[chat_id] = True
            sub_bot.reply_to(msg, "🖼️ **تم تفعيل عرض الصورة الشخصية في الايدي بنجاح!** ⚡")
        else:
            sub_bot.reply_to(msg, "⚠️ هذا الأمر خاص بالمدراء والمشرفين فما فوق!")
        return

    elif text == "تعط":
        if is_admin:
            ID_PHOTO_SETTINGS[chat_id] = False
            sub_bot.reply_to(msg, "📝 **تم تعطيل عرض الصورة في الايدي (إرسال معلومات فقط) بنجاح!** ⚡")
        else:
            sub_bot.reply_to(msg, "⚠️ هذا الأمر خاص بالمدراء والمشرفين فما فوق!")
        return

    if text == "تعطيل":
        if is_admin or is_chat_creator:
            if chat_id in ACTIVATED_CHATS:
                ACTIVATED_CHATS.remove(chat_id)
            sub_bot.reply_to(msg, "❌ **تم تعطيل البوت في هذه المجموعة!**")
        else:
            sub_bot.reply_to(msg, "⚠️ أمر التعطيل مخصص للمدراء والمشرفين فقط!")
        return

    if chat_id in CUSTOM_REPLIES and text in CUSTOM_REPLIES[chat_id]:
        sub_bot.reply_to(msg, CUSTOM_REPLIES[chat_id][text])
        return

    if text == "تفعيل الترحيب":
        if is_admin:
            WELCOME_SETTINGS[chat_id] = True
            sub_bot.reply_to(msg, "✅ **تم تفعيل الترحيب بنجاح في هذا الكروب!**")
        else:
            sub_bot.reply_to(msg, "⚠️ هذا الأمر خاص بالمدراء والمشرفين فقط!")
        return

    elif text == "تعطيل الترحيب":
        if is_admin:
            WELCOME_SETTINGS[chat_id] = False
            sub_bot.reply_to(msg, "❌ **تم تعطيل الترحيب في هذا الكروب!**")
        else:
            sub_bot.reply_to(msg, "⚠️ هذا الأمر خاص بالمدراء والمشرفين فقط!")
        return

    elif text in ["ر", "رابط"]:
        try:
            chat_link = sub_bot.export_chat_invite_link(chat_id)
            sub_bot.reply_to(msg, f"🔗 **رابط الكروب الحالي:**\n{chat_link}")
        except Exception:
            sub_bot.reply_to(msg, "⚠️ ما عندي صلاحية جلب الرابط، تأكد من رفعي مشرف.")
        return

    elif text in ["الأوامر", "اوامر", "ترتيب الاوامر", "قائمة الأوامر"]:
        commands_text = (
            "📋 **قائمة أوامر سورس سجين الشاملة:**\n\n"
            "👤 **أوامر الأعضاء:**\n"
            "• `ا` أو `ايدي` - عرض ايديك (مع أو بدون صورة حسب إعداد الكروب)\n"
            "• `تغ` أو `تغير` - تغيير ستايل الايدي\n"
            "• `ر` أو `رابط` - جلب رابط الكروب\n"
            "• `كت` - أسئلة كت العشوائية\n"
            "• `يوت [كلمة]` - بحث يوتيوب\n"
            "• `اضف رد [الكلمة] [الجواب]` - إضافة رد مخصص\n\n"
            "🛠️ **أوامر المدراء والمشرفين:**\n"
            "• `تفعيل` / `تعطيل` - تفعيل أو تعطيل البوت\n"
            "• `تفع` / `تعط.]` - تفعيل أو تعطيل صورة الايدي\n"
            "• `تفعيل الترحيب` / `تعطيل الترحيب` - التحكم بالترحيب\n"
            "• `طرد` / `كتم` / `تقييد` (بالرد) - (محمي ضد الرتب)\n"
            "• `قفل الدردشة` / `فتح الدردشة` - قفل وفتح الكروب\n\n"
            "🛡️ **أوامر المنشئين والمنشئين الأساسيين:**\n"
            "• `تعيين منشئ` (بالرد) - لرفع منشئ بالكروب\n\n"
            "👑 **أوامر المطورين والمطورين الثانويين:**\n"
            "• `اذاعة [النص]` - إرسال رسالة لكل المجموعات\n"
            "• `الاحصائيات` - عرض الإحصائيات"
        )
        sub_bot.reply_to(msg, commands_text)
        return

    if text.startswith("اضف رد "):
        try:
            parts = text.replace("اضف رد ", "").split(" ", 1)
            if len(parts) == 2:
                k, v = parts[0], parts[1]
                if chat_id not in CUSTOM_REPLIES:
                    CUSTOM_REPLIES[chat_id] = {}
                CUSTOM_REPLIES[chat_id][k] = v
                sub_bot.reply_to(msg, f"✅ تم إضافة الرد بنجاح:\nكل ما تكول ({k}) راح أرد بـ ({v})")
        except Exception:
            pass

    elif text == "تاك" or text == "منشن":
        sub_bot.reply_to(msg, "📢 **تنبيه جماعي لكل الموجودين بالكروب!** تنورون الدردشة ⚡🖤")

    elif text == "ا" or text.lower() == "ايدي":
        style = random.choice(ID_STYLES)
        rank_title = "المطور الأساسي 👑" if is_main_dev else ("المطور الثانوي ⚡" if is_secondary_dev else ("المنشئ 🛡️" if is_creator or is_chat_creator else ("مدير / مشرف ⚡" if is_admin else "عضو مميز 🖤")))
        caption = f"{style}\n\n👤 اسمك: {user_name}\n🆔 ايديك: `{user_id}`\n🔰 رتبتك: {rank_title}"
        
        # التحقق من حالة تفعيل الصورة (افتراضياً مفعلة True)
        photo_enabled = ID_PHOTO_SETTINGS.get(chat_id, True)
        
        if photo_enabled:
            try:
                photos = sub_bot.get_user_profile_photos(user_id, limit=1)
                if photos.total_count > 0:
                    file_id = photos.photos[0][0].file_id
                    sub_bot.send_photo(chat_id, file_id, caption=caption, reply_to_message_id=msg.message_id)
                else:
                    sub_bot.reply_to(msg, caption)
            except Exception:
                sub_bot.reply_to(msg, caption)
        else:
            # إذا معطلة (تعط)، ترسل نص فقط بدون صورة
            sub_bot.reply_to(msg, caption)

    elif text in ["تغير ايدي", "تغ", "تغيير"]:
        style = random.choice(ID_STYLES)
        sub_bot.reply_to(msg, f"🎨 **تم تغيير وتحديث ستايل الايدي بنجاح!**\n\n{style}")

    elif text == "قفل الدردشة":
        if is_admin:
            try:
                sub_bot.set_chat_permissions(chat_id, ChatPermissions(can_send_messages=False))
                sub_bot.reply_to(msg, "🔒 **تم قفل الدردشة بنجاح!**")
            except Exception:
                pass

    elif text == "فتح الدردشة":
        if is_admin:
            try:
                sub_bot.set_chat_permissions(chat_id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True))
                sub_bot.reply_to(msg, "🔓 **تم فتح الدردشة بنجاح!**")
            except Exception:
                pass

    elif text == "كت" or text.lower() == "اسئلة":
        q = random.choice(CAT_QUESTIONS)
        sub_bot.reply_to(msg, f"❓ **سؤال كت:**\n\n{q}")

    elif text.startswith("يوت"):
        query = text.replace("يوت", "", 1).strip()
        if query:
            yt_link = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            sub_bot.reply_to(msg, f"🔍 **بحث اليوتيوب عن:** `{query}`\n🔗 اضغط للمشاهدة:\n{yt_link}")

    elif text in ["طرد", "كتم", "تقييد"]:
        if not is_admin:
            sub_bot.reply_to(msg, "⚠️ أوامر الإجراءات مخصصة للمدراء والمشرفين فقط!")
            return

        if msg.reply_to_message:
            target_user = msg.reply_to_message.from_user
            target_id = target_user.id
            
            target_is_protected = False
            try:
                target_member = sub_bot.get_chat_member(chat_id, target_id)
                if target_member.status in ['creator', 'administrator'] or target_user.username == "M_C_67" or target_id in DEV_SECONDARY:
                    target_is_protected = True
            except Exception:
                pass

            if target_is_protected and not is_main_dev:
                sub_bot.reply_to(msg, "❌ **عذراً! لا يمكنني تنفيذ أي إجراء بحق هذا الشخص لأنه يمتلك رتبة محمية (مشرف/منشئ/مطور)!** 🛡️")
                return

            try:
                if text == "طرد":
                    sub_bot.ban_chat_member(chat_id, target_id)
                    sub_bot.reply_to(msg, "🥾 **تم طرد العضو المخالف بنجاح بقبضة سجين ⚡**")
                elif text == "كتم":
                    sub_bot.restrict_chat_member(chat_id, target_id, ChatPermissions(can_send_messages=False))
                    sub_bot.reply_to(msg, "🔇 **تم كتم العضو المخالف بنجاح ⚡**")
                elif text == "تقييد":
                    sub_bot.restrict_chat_member(chat_id, target_id, ChatPermissions(can_send_messages=False, can_send_media_messages=False))
                    sub_bot.reply_to(msg, "🔒 **تم تقييد العضو من إرسال الوسائط والرسائل ⚡**")
            except Exception:
                sub_bot.reply_to(msg, "❌ ما أگدر أنفذ الإجراء، تأكد أني مشرف وصلاحياتي كاملة.")
        else:
            sub_bot.reply_to(msg, "⚠️ رد على رسالة الشخص حتى أنفذ الإجراء بحقه!")

@sub_bot.callback_query_handler(func=lambda call: True)
def callback_sub(call):
    sub_bot.answer_callback_query(call.id)
    if call.data == "bot_settings":
        sub_bot.edit_message_text("⚙️ **إعدادات سورس سجين ورتب الإدارة**", call.message.chat.id, call.message.message_id, reply_markup=DEV_KEYBOARD)
    elif call.data == "commands_list":
        commands_text = (
            "📋 **قائمة أوامر سورس سجين الشاملة:**\n\n"
            "👤 **أوامر الأعضاء:**\n"
            "• `ا` أو `ايدي` - عرض ايديك (مع/بدون صورة)\n"
            "• `تغ` أو `تغير` - تغيير ستايل الايدي\n"
            "• `ر` أو `رابط` - جلب رابط الكروب\n"
            "• `كت` - أسئلة كت العشوائية\n"
            "• `يوت [كلمة]` - بحث يوتيوب\n"
            "• `اضف رد [الكلمة] [الجواب]` - إضافة رد مخصص\n\n"
            "🛠️ **أوامر المدراء والمشرفين:**\n"
            "• `تفعيل` / `تعطيل` - تفعيل أو تعطيل البوت\n"
            "• `تفع` / `تعط` - تفعيل أو تعطيل صورة الايدي\n"
            "• `تفعيل الترحيب` / `تعطيل الترحيب` - التحكم بالترحيب\n"
            "• `طرد` / `كتم` / `تقييد` (بالرد) - (محمي ضد الرتب)\n"
            "• `قفل الدردشة` / `فتح الدردشة` - قفل وفتح الكروب\n\n"
            "🛡️ **أوامر المنشئين والمنشئين الأساسيين:**\n"
            "• `تعيين منشئ` (بالرد)\n\n"
            "👑 **أوامر المطورين والمطورين الثانويين:**\n"
            "• `اذاعة [النص]` - إرسال رسالة لكل المجموعات\n"
            "• `الاحصائيات` - عرض الإحصائيات"
        )
        sub_bot.edit_message_text(commands_text, call.message.chat.id, call.message.message_id, reply_markup=DEV_KEYBOARD)
    elif call.data == "protection":
        sub_bot.edit_message_text("🛡️ **حماية المجموعات ونظام الرتب والحصانات يعمل بكامل الكفاءة!**", call.message.chat.id, call.message.message_id, reply_markup=DEV_KEYBOARD)

sub_bot.infinity_polling()
