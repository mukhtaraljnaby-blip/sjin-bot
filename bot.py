import os
import time
import random
import threading
from urllib.parse import quote_plus

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions

# Railway: أضف BOT_TOKEN من Variables ولا تضع التوكن داخل GitHub.
TOKEN = os.getenv("BOT_TOKEN", "").strip()
DEV_USERNAME = "M_C_67"
DEV_LINK = "https://t.me/M_C_67"
MAX_BOTS = 3

if not TOKEN:
    raise RuntimeError("أضف BOT_TOKEN في Railway → Variables")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
USER_BOTS = {}
WAITING_FOR_TOKEN = set()
RUNNING_SUB_BOTS = {}

MAKER_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("صنع بوت فرعي جديد 🤖", callback_data="create_bot")],
    [InlineKeyboardButton("قائمة بوتاتي 📋", callback_data="my_bots"),
     InlineKeyboardButton("تفعيل VIP 💎", url=DEV_LINK)],
    [InlineKeyboardButton("مطور المصنع 👤", url=DEV_LINK)]
])

QUESTIONS = [
    "شنو أكثر شي تحبه بصديقك المقرب؟ 🖤",
    "لو انطوك مليار دولار، شنو أول شغلة تشتريها؟ 💸",
    "كلمة توجها لشخص خان ثقتك؟ 🎭",
    "شنو أحلى صفة بشخصيتك وأسوأ صفة؟ 🤔",
    "لو رجع بيك الزمن للماضي، شنو الشغلة اللي تغيرها؟ ⏳",
    "شنو الأكلة العراقية اللي مستحيل تمل منها؟ 🍲",
    "تحب الحياة الهادئة لو المغامرات والسفر؟ 🌍",
    "لو عندك أمنية وحدة وتتحقق، شنو تطلب؟ 🌠",
    "شنو أكثر شي يخليك تبتسم بدون سبب؟ 😊",
    "شنو أكثر صفة تكرهها بالناس؟ 😒"
]
ID_STYLES = [
    "✨ ━━━━━ ⦗ ايديك الرائع ⦘ ━━━━━ ✨",
    "🔥 ── • [ بطاقة الهوية ] • ── 🔥",
    "💎 ════ ≪ بطاقة العضو ≫ ════ 💎",
    "⚡ ──━[ هويتك الرسمية ]━━── ⚡",
    "🌟 ─── ❖ ⦗ كرت التعريف ⦘ ─── 🌟",
    "👑 ───── ❖ ⦗ بطاقة الملوك ⦘ ───── 👑"
]

def run_sub_bot(token):
    """كل بوت فرعي يعمل بعامل منفصل. بيانات الرتب والقوائم في الذاكرة مؤقتة."""
    while True:
        try:
            sb = telebot.TeleBot(token, parse_mode="HTML")
            me = sb.get_me()
            activated = set()
            welcomes = {}
            id_photo = {}
            ranks = {}       # chat_id -> {user_id: rank}
            muted = {}       # سجل عمليات البوت الحالية، وليس كشفاً كاملاً من تيليجرام
            banned = {}
            kicked = {}
            restricted = {}
            warnings = {}
            whisper_sessions = {}
            whisper_store = {}
            settings = {}

            def is_dev(user):
                return bool(user and user.username and user.username.lower() == DEV_USERNAME.lower())

            def replied_user(message):
                reply = getattr(message, "reply_to_message", None)
                return getattr(reply, "from_user", None) if reply else None

            def rank_of(chat_id, user):
                if is_dev(user):
                    return "المطور الأساسي"
                try:
                    member = sb.get_chat_member(chat_id, user.id)
                    if member.status == "creator":
                        return "مالك"
                    if member.status == "administrator":
                        return "مدير"
                except Exception:
                    pass
                return ranks.get(chat_id, {}).get(user.id, "عضو")

            def admin(chat_id, user):
                return rank_of(chat_id, user) in ("المطور الأساسي", "مالك", "مدير")

            def target_user(message, parts):
                target = replied_user(message)
                if target:
                    return target
                if len(parts) > 1 and parts[1].isdigit():
                    try:
                        return sb.get_chat_member(message.chat.id, int(parts[1])).user
                    except Exception:
                        return None
                return None

            def get_ids(store, chat_id):
                ids = sorted(store.get(chat_id, set()))
                if not ids:
                    return "القائمة فارغة حالياً."
                lines = []
                for uid in ids[:80]:
                    try:
                        name = sb.get_chat_member(chat_id, uid).user.first_name
                    except Exception:
                        name = "عضو"
                    lines.append(f"• {name} — <code>{uid}</code>")
                if len(ids) > 80:
                    lines.append(f"… وبقية {len(ids)-80} عضواً.")
                return "\n".join(lines)

            @sb.message_handler(commands=["start"])
            def start_sub(msg):
                if msg.chat.type != "private":
                    return
                uid = msg.from_user.id
                raw = (msg.text or "").strip()
                if raw.startswith("/start whisper_"):
                    payload = raw[len("/start whisper_"):]
                    try:
                        target_s, chat_s, name = payload.split("_", 2)
                        whisper_sessions[uid] = {
                            "target": int(target_s), "chat": int(chat_s), "name": name.replace("_", " ")
                        }
                        sb.send_message(uid, "🔒 أرسل نص الهمسة الآن برسالة جديدة.")
                    except Exception:
                        sb.send_message(uid, "⚠️ رابط الهمسة غير صالح؛ ارجع للمجموعة وجرّب من جديد.")
                    return
                sb.send_message(
                    msg.chat.id,
                    f"أهلاً بك في بوت {me.first_name} 🤖\n"
                    "أضفني للمجموعة وارفعني مشرفاً ثم أرسل: تفعيل\n\n"
                    f"يوزر البوت: @{me.username}\nمطور المصنع: {DEV_LINK}"
                )

            @sb.message_handler(
                func=lambda m: m.chat.type == "private" and m.from_user and m.from_user.id in whisper_sessions,
                content_types=["text"]
            )
            def whisper_input(msg):
                uid = msg.from_user.id
                data = whisper_sessions.get(uid)
                body = (msg.text or "").strip()
                if not data or not body or body.startswith("/"):
                    sb.reply_to(msg, "أرسل نص الهمسة مباشرة.")
                    return
                key = f"{uid}:{data['target']}:{data['chat']}"
                whisper_store[key] = body
                markup = InlineKeyboardMarkup([[
                    InlineKeyboardButton("💬 قراءة الهمسة السرية",
                        callback_data=f"readwhisper:{uid}:{data['target']}:{data['chat']}")
                ]])
                try:
                    sb.send_message(
                        data["chat"],
                        f"🔒 همسة من <a href='tg://user?id={uid}'>مرسل</a> "
                        f"إلى <a href='tg://user?id={data['target']}'>{data['name']}</a>.",
                        reply_markup=markup
                    )
                    sb.reply_to(msg, "✅ تم إرسال الهمسة.")
                except Exception:
                    sb.reply_to(msg, "❌ تعذر إرسال الهمسة؛ تأكد أن البوت موجود بالمجموعة.")
                whisper_sessions.pop(uid, None)

            @sb.callback_query_handler(func=lambda c: c.data.startswith("readwhisper:"))
            def read_whisper(call):
                try:
                    _, sender_s, target_s, chat_s = call.data.split(":")
                    sender, target, chat_id = int(sender_s), int(target_s), int(chat_s)
                except Exception:
                    sb.answer_callback_query(call.id, "همسة غير صالحة.", show_alert=True)
                    return
                if call.from_user.id not in (sender, target) and not is_dev(call.from_user):
                    sb.answer_callback_query(call.id, "هذه الهمسة ليست مخصصة لك.", show_alert=True)
                    return
                text = whisper_store.get(f"{sender}:{target}:{chat_id}", "انتهت صلاحية الهمسة.")
                sb.answer_callback_query(call.id, text[:190], show_alert=True)

            @sb.message_handler(content_types=["new_chat_members"])
            def welcome(msg):
                cid = msg.chat.id
                if cid in activated and welcomes.get(cid, True):
                    for member in msg.new_chat_members:
                        sb.send_message(cid, f"هلا بيك يا <a href='tg://user?id={member.id}'>{member.first_name}</a> 🌸 نورت المجموعة.")

            @sb.message_handler(content_types=["text"])
            def group_commands(msg):
                if msg.chat.type not in ("group", "supergroup") or not msg.from_user:
                    return
                cid, user = msg.chat.id, msg.from_user
                uid = user.id
                text = (msg.text or "").strip()
                parts = text.split()
                is_admin = admin(cid, user)

                if text == "تفعيل":
                    if is_admin:
                        activated.add(cid)
                        sb.reply_to(msg, "✅ تم تفعيل المجموعة.")
                    else:
                        sb.reply_to(msg, "⚠️ التفعيل للمالك والمدراء فقط.")
                    return
                if text == "تعطيل":
                    if is_admin:
                        activated.discard(cid)
                        sb.reply_to(msg, "⛔ تم تعطيل البوت في المجموعة.")
                    return
                if cid not in activated:
                    return

                if text in ("الأوامر", "اوامر", "قائمة الأوامر", "ترتيب الاوامر"):
                    sb.reply_to(msg,
                        "📋 <b>أوامر سجين</b>\n\n"
                        "🛡️ <b>الحماية:</b>\nقفل الدردشة / فتح الدردشة\n"
                        "قفل الروابط / فتح الروابط\nقفل الصور / فتح الصور\n"
                        "قفل الفيديو / فتح الفيديو\nقفل الملفات / فتح الملفات\n"
                        "قفل التكرار / فتح التكرار\nقفل التوجيه / فتح التوجيه\n"
                        "تفعيل الترحيب / تعطيل الترحيب\n\n"
                        "👑 <b>الرتب:</b>\nرفع مميز أو مم أو م (بالرد)\nتنزيل مميز (بالرد)\n"
                        "رفع مشرف / تنزيل مشرف (بالرد)\nرفع مدير / تنزيل مدير (بالرد)\n\n"
                        "🔨 <b>الإدارة:</b>\nطرد / حظر / إلغاء حظر / كتم / إلغاء كتم\n"
                        "تقييد / إلغاء تقييد / رفع القيود / إنذار (بالرد أو الآيدي)\n"
                        "تثبيت / إلغاء التثبيت\n\n"
                        "🧹 <b>القوائم والمسح:</b>\nالمميزين / المكتومين / المطرودين / المحظورين / المقيدين\n"
                        "مسح المكتومين / مسح المطرودين / مسح المحظورين / مسح المقيدين / مسح المميزين\n\n"
                        "🎮 <b>الأعضاء:</b>\nايدي أو ا / تغيير أو تغ / رابط أو ر / همسة (بالرد)\nكت / يوت [كلمة] / جمالي / الحب / الكره / الرجولة / الأنوثة / اقتباس / شعر / قرآن")
                    return

                if text in ("ايدي", "ا", "آيدي", "آيدي العضو"):
                    r = rank_of(cid, user)
                    caption = f"{random.choice(ID_STYLES)}\n\n👤 الاسم: {user.first_name}\n🆔 الآيدي: <code>{uid}</code>\n🔰 الرتبة: {r}"
                    if id_photo.get(cid, True):
                        try:
                            photos = sb.get_user_profile_photos(uid, limit=1)
                            if photos.total_count:
                                sb.send_photo(cid, photos.photos[0][0].file_id, caption=caption, reply_to_message_id=msg.message_id)
                                return
                        except Exception:
                            pass
                    sb.reply_to(msg, caption)
                    return

                if text in ("تغ", "تغيير", "تغير"):
                    sb.reply_to(msg, f"🎨 تم تغيير ستايل الآيدي:\n{random.choice(ID_STYLES)}")
                    return

                if text in ("رابط", "ر"):
                    try:
                        sb.reply_to(msg, f"🔗 رابط المجموعة:\n{sb.export_chat_invite_link(cid)}")
                    except Exception:
                        sb.reply_to(msg, "⚠️ ارفع البوت مشرفاً مع صلاحية دعوة المستخدمين.")
                    return

                if text in ("همسة", "همسه"):
                    target = replied_user(msg)
                    if not target:
                        sb.reply_to(msg, "⚠️ استخدم الأمر بالرد على رسالة العضو.")
                        return
                    if target.id in (uid, me.id):
                        sb.reply_to(msg, "⚠️ لا يمكنك إرسال همسة لنفسك أو للبوت.")
                        return
                    name = target.first_name.replace(" ", "_")
                    markup = InlineKeyboardMarkup([[
                        InlineKeyboardButton("اكتب الهمسة 💬", url=f"https://t.me/{me.username}?start=whisper_{target.id}_{cid}_{name}")
                    ]])
                    sb.reply_to(msg, "🔒 اضغط الزر لكتابة الهمسة في الخاص.", reply_markup=markup)
                    return

                if text == "تفعيل الترحيب" and is_admin:
                    welcomes[cid] = True
                    sb.reply_to(msg, "✅ تم تفعيل الترحيب.")
                    return
                if text == "تعطيل الترحيب" and is_admin:
                    welcomes[cid] = False
                    sb.reply_to(msg, "⛔ تم تعطيل الترحيب.")
                    return

                # الرتب محلية للبوت ولا ترفع العضو إلى مشرف تيليجرام.
                rank_cmds = ("رفع مميز", "مم", "م", "تنزيل مميز", "رفع مشرف", "تنزيل مشرف", "رفع مدير", "تنزيل مدير")
                if text in rank_cmds:
                    if not is_admin:
                        sb.reply_to(msg, "⚠️ هذا الأمر للمالك والمدراء فقط.")
                        return
                    target = replied_user(msg)
                    if not target:
                        sb.reply_to(msg, "⚠️ رد على رسالة العضو ثم أرسل الأمر.")
                        return
                    if target.id == uid or is_dev(target):
                        sb.reply_to(msg, "⚠️ لا يمكن تغيير رتبة هذا العضو.")
                        return
                    desired = "مميز" if text in ("رفع مميز", "مم", "م", "تنزيل مميز") else ("مشرف" if "مشرف" in text else "مدير")
                    removing = text.startswith("تنزيل")
                    if desired == "مدير" and rank_of(cid, user) not in ("المطور الأساسي", "مالك"):
                        sb.reply_to(msg, "⚠️ رفع المدير للمالك أو المطور فقط.")
                        return
                    ranks.setdefault(cid, {})
                    if removing:
                        ranks[cid].pop(target.id, None)
                        sb.reply_to(msg, f"✅ تم تنزيل رتبة {target.first_name}.")
                    else:
                        ranks[cid][target.id] = desired
                        sb.reply_to(msg, f"✅ تم رفع {target.first_name} إلى رتبة {desired} داخل البوت.")
                    return

                list_map = {
                    "المكتومين": muted, "المطرودين": kicked,
                    "المحظورين": banned, "المقيدين": restricted
                }
                if text == "المميزين":
                    if not is_admin:
                        sb.reply_to(msg, "⚠️ للمدراء فقط.")
                    else:
                        ids = [str(uid2) for uid2, r in ranks.get(cid, {}).items() if r == "مميز"]
                        sb.reply_to(msg, "📋 المميزين:\n" + ("\n".join(f"• <code>{x}</code>" for x in ids) if ids else "القائمة فارغة."))
                    return
                if text in list_map:
                    if not is_admin:
                        sb.reply_to(msg, "⚠️ للمدراء فقط.")
                    else:
                        sb.reply_to(msg, f"📋 {text}:\n{get_ids(list_map[text], cid)}")
                    return

                clear_map = {
                    "مسح المكتومين": muted, "مسح المطرودين": kicked,
                    "مسح المحظورين": banned, "مسح المقيدين": restricted
                }
                if text in clear_map:
                    if not is_admin:
                        sb.reply_to(msg, "⚠️ المسح للمدراء فقط.")
                    else:
                        store = clear_map[text]
                        count = len(store.get(cid, set()))
                        store[cid] = set()
                        sb.reply_to(msg, f"✅ تم مسح سجل {text.replace('مسح ', '')}: {count}.\nهذا يمسح سجل البوت فقط ولا يغيّر حالة تيليجرام.")
                    return
                if text == "مسح المميزين":
                    if not is_admin:
                        sb.reply_to(msg, "⚠️ المسح للمدراء فقط.")
                    else:
                        old = ranks.get(cid, {})
                        count = sum(1 for r in old.values() if r == "مميز")
                        ranks[cid] = {u: r for u, r in old.items() if r != "مميز"}
                        sb.reply_to(msg, f"✅ تم حذف رتبة مميز من {count} عضو.")
                    return

                lock_map = {
                    "قفل الدردشة": ("chat", True), "فتح الدردشة": ("chat", False),
                    "قفل الروابط": ("links", True), "فتح الروابط": ("links", False),
                    "قفل الصور": ("photos", True), "فتح الصور": ("photos", False),
                    "قفل الفيديو": ("videos", True), "فتح الفيديو": ("videos", False),
                    "قفل الملفات": ("documents", True), "فتح الملفات": ("documents", False),
                    "قفل التكرار": ("repeat", True), "فتح التكرار": ("repeat", False),
                    "قفل التوجيه": ("forward", True), "فتح التوجيه": ("forward", False)
                }
                if text in lock_map:
                    if not is_admin:
                        sb.reply_to(msg, "⚠️ هذا الأمر للمدراء فقط.")
                        return
                    feature, enabled = lock_map[text]
                    settings.setdefault(cid, {})[feature] = enabled
                    if feature == "chat":
                        try:
                            sb.set_chat_permissions(cid, ChatPermissions(
                                can_send_messages=not enabled,
                                can_send_photos=not enabled,
                                can_send_videos=not enabled,
                                can_send_documents=not enabled
                            ))
                        except Exception:
                            sb.reply_to(msg, "⚠️ تعذر تعديل صلاحيات المجموعة؛ تحقق من صلاحيات البوت.")
                            return
                    sb.reply_to(msg, f"✅ تم {'قفل' if enabled else 'فتح'} {feature}.")
                    return

                moderation = {
                    "إلغاء تقييد": "unrestrict", "رفع القيود": "unrestrict",
                    "إلغاء حظر": "unban", "إلغاء كتم": "unmute",
                    "تقييد": "restrict", "إنذار": "warn", "طرد": "kick",
                    "حظر": "ban", "كتم": "mute"
                }
                matched = next((name for name in sorted(moderation, key=len, reverse=True)
                                if text == name or text.startswith(name + " ")), None)
                if matched:
                    if not is_admin:
                        sb.reply_to(msg, "⚠️ أوامر الإدارة للمدراء فقط.")
                        return
                    target = target_user(msg, parts)
                    if not target:
                        sb.reply_to(msg, "⚠️ رد على رسالة العضو أو اكتب الآيدي بعد الأمر.")
                        return
                    if target.id == uid or is_dev(target):
                        sb.reply_to(msg, "⚠️ لا يمكن تنفيذ هذا الإجراء على نفسك أو المطور.")
                        return
                    try:
                        tm = sb.get_chat_member(cid, target.id)
                        if tm.status in ("creator", "administrator"):
                            sb.reply_to(msg, "❌ لا يمكن تنفيذ الإجراء على مالك أو مشرف تيليجرام.")
                            return
                    except Exception:
                        pass
                    action = moderation[matched]
                    try:
                        if action == "kick":
                            sb.ban_chat_member(cid, target.id)
                            sb.unban_chat_member(cid, target.id)
                            kicked.setdefault(cid, set()).add(target.id)
                            answer = "🥾 تم طرد العضو."
                        elif action == "ban":
                            sb.ban_chat_member(cid, target.id)
                            banned.setdefault(cid, set()).add(target.id)
                            answer = "⛔ تم حظر العضو."
                        elif action == "unban":
                            sb.unban_chat_member(cid, target.id)
                            banned.setdefault(cid, set()).discard(target.id)
                            answer = "✅ تم إلغاء الحظر."
                        elif action == "mute":
                            sb.restrict_chat_member(cid, target.id, ChatPermissions(can_send_messages=False))
                            muted.setdefault(cid, set()).add(target.id)
                            answer = "🔇 تم كتم العضو."
                        elif action in ("unmute", "unrestrict"):
                            sb.restrict_chat_member(cid, target.id, ChatPermissions(
                                can_send_messages=True, can_send_photos=True, can_send_videos=True,
                                can_send_documents=True, can_send_audios=True, can_send_voice_notes=True,
                                can_send_video_notes=True, can_send_other_messages=True,
                                can_add_web_page_previews=True
                            ))
                            muted.setdefault(cid, set()).discard(target.id)
                            restricted.setdefault(cid, set()).discard(target.id)
                            answer = "🔓 تم رفع القيود عن العضو."
                        elif action == "restrict":
                            sb.restrict_chat_member(cid, target.id, ChatPermissions(
                                can_send_messages=False, can_send_photos=False,
                                can_send_videos=False, can_send_documents=False
                            ))
                            restricted.setdefault(cid, set()).add(target.id)
                            answer = "🔒 تم تقييد العضو."
                        else:
                            key = (cid, target.id)
                            warnings[key] = warnings.get(key, 0) + 1
                            answer = f"⚠️ تم إنذار العضو. عدد الإنذارات: {warnings[key]}"
                        sb.reply_to(msg, answer)
                    except Exception:
                        sb.reply_to(msg, "❌ تعذر تنفيذ الأمر. تأكد أن البوت مشرف ويملك الصلاحيات اللازمة.")
                    return

                if text == "تثبيت" and is_admin and msg.reply_to_message:
                    try:
                        sb.pin_chat_message(cid, msg.reply_to_message.message_id)
                        sb.reply_to(msg, "📌 تم تثبيت الرسالة.")
                    except Exception:
                        sb.reply_to(msg, "⚠️ تعذر التثبيت؛ تحقق من صلاحيات البوت.")
                    return
                if text == "إلغاء التثبيت" and is_admin:
                    try:
                        sb.unpin_all_chat_messages(cid)
                        sb.reply_to(msg, "✅ تم إلغاء تثبيت الرسائل.")
                    except Exception:
                        sb.reply_to(msg, "⚠️ تعذر إلغاء التثبيت.")
                    return

                if text == "كت":
                    sb.reply_to(msg, "❓ سؤال كت:\n\n" + random.choice(QUESTIONS))
                    return
                if text.startswith("يوت"):
                    query = text[3:].strip()
                    if query:
                        sb.reply_to(msg, "🔎 نتائج يوتيوب:\nhttps://www.youtube.com/results?search_query=" + quote_plus(query))
                    return
                fun = {
                    "جمالي": "✨ الجمال الحقيقي بالأخلاق والروح الحلوة.",
                    "الحب": "🤍 الحب احترام وصدق واهتمام.",
                    "الكره": "🌿 لا تخلي الكره ياخذ من راحتك.",
                    "الرجولة": "🦅 الرجولة مواقف وأخلاق ومسؤولية.",
                    "الأنوثة": "🌸 الرقي بالأخلاق والثقة بالنفس.",
                    "اقتباس": "✨ كل يوم فرصة جديدة حتى تصير أفضل.",
                    "شعر": "🌙 للكلمة الحلوة مكان بالقلب.",
                    "قرآن": "🕌 تذكّر أن الطمأنينة بذكر الله."
                }
                if text in fun:
                    sb.reply_to(msg, fun[text])

            sb.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)
        except Exception:
            time.sleep(5)


@bot.message_handler(commands=["start"])
def start_handler(msg):
    if msg.chat.type == "private":
        WAITING_FOR_TOKEN.discard(msg.from_user.id)
        bot.send_message(msg.chat.id,
            f"أهلاً بك في مصنع بوتات سجين ⚡\nالحد الأقصى: {MAX_BOTS} بوتات.\nاختر من القائمة:",
            reply_markup=MAKER_KEYBOARD)


@bot.message_handler(
    func=lambda m: m.chat.type == "private" and m.from_user and m.from_user.id in WAITING_FOR_TOKEN,
    content_types=["text"]
)
def receive_token(msg):
    uid = msg.from_user.id
    token = (msg.text or "").strip()
    if token.startswith("/"):
        bot.reply_to(msg, "أرسل توكن البوت من BotFather أو /start للإلغاء.")
        return
    try:
        test = telebot.TeleBot(token)
        info = test.get_me()
        items = USER_BOTS.setdefault(uid, [])
        if len(items) >= MAX_BOTS:
            WAITING_FOR_TOKEN.discard(uid)
            bot.reply_to(msg, "وصلت للحد الأقصى من البوتات.")
            return
        if any(x["token"] == token for x in items):
            WAITING_FOR_TOKEN.discard(uid)
            bot.reply_to(msg, "هذا البوت مسجل عندك مسبقاً.")
            return
        items.append({"name": info.first_name, "username": f"@{info.username}", "token": token})
        if token not in RUNNING_SUB_BOTS:
            thread = threading.Thread(target=run_sub_bot, args=(token,), daemon=True)
            thread.start()
            RUNNING_SUB_BOTS[token] = thread
        WAITING_FOR_TOKEN.discard(uid)
        bot.send_message(msg.chat.id,
            f"✅ تم تشغيل البوت الفرعي.\nالاسم: {info.first_name}\nاليوزر: @{info.username}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("قائمة بوتاتي 📋", callback_data="my_bots")],
                [InlineKeyboardButton("رجوع 🔙", callback_data="back_start")]
            ]))
    except Exception:
        bot.reply_to(msg, "❌ التوكن غير صحيح أو لا يمكن الوصول للبوت. تأكد منه من BotFather.")


@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    uid = call.from_user.id
    if call.data.startswith("delete_bot:"):
        try:
            _, owner_s, index_s = call.data.split(":")
            owner, index = int(owner_s), int(index_s)
        except Exception:
            bot.answer_callback_query(call.id, "طلب غير صالح.")
            return
        if owner != uid:
            bot.answer_callback_query(call.id, "هذه القائمة ليست لك.", show_alert=True)
            return
        items = USER_BOTS.get(uid, [])
        if 0 <= index < len(items):
            deleted = items.pop(index)
            bot.answer_callback_query(call.id, "تم حذف السجل.")
            bot.edit_message_text(
                f"تم حذف {deleted['username']} من القائمة. هذا لا يوقف عامله الذي بدأ بالفعل.",
                call.message.chat.id, call.message.message_id,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("قائمة بوتاتي 📋", callback_data="my_bots")],
                    [InlineKeyboardButton("رجوع 🔙", callback_data="back_start")]
                ]))
        return

    bot.answer_callback_query(call.id)
    if call.data == "create_bot":
        if len(USER_BOTS.get(uid, [])) >= MAX_BOTS:
            bot.edit_message_text("وصلت للحد الأقصى (3 بوتات). تواصل مع المطور لتفعيل VIP.",
                call.message.chat.id, call.message.message_id,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("تواصل مع المطور 💎", url=DEV_LINK)],
                    [InlineKeyboardButton("رجوع 🔙", callback_data="back_start")]
                ]))
        else:
            WAITING_FOR_TOKEN.add(uid)
            bot.edit_message_text("أنشئ بوتاً من @BotFather ثم أرسل التوكن هنا.",
                call.message.chat.id, call.message.message_id,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("إلغاء 🔙", callback_data="back_start")]]))
    elif call.data == "my_bots":
        items = USER_BOTS.get(uid, [])
        text = f"📂 بوتاتك ({len(items)}/{MAX_BOTS}):\n\n"
        markup = InlineKeyboardMarkup()
        for i, item in enumerate(items):
            text += f"{i+1}. {item['name']} — {item['username']}\n"
            markup.add(InlineKeyboardButton(f"حذف {item['username']} 🗑️", callback_data=f"delete_bot:{uid}:{i}"))
        if not items:
            text += "ما عندك بوتات مسجلة في هذه الجلسة."
        markup.add(InlineKeyboardButton("رجوع 🔙", callback_data="back_start"))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif call.data == "back_start":
        WAITING_FOR_TOKEN.discard(uid)
        bot.edit_message_text("أهلاً بك في مصنع بوتات سجين ⚡\nاختر من القائمة:",
            call.message.chat.id, call.message.message_id, reply_markup=MAKER_KEYBOARD)


if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)
