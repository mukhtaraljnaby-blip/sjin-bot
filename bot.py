import os
import time
import random
import threading
import tempfile
import shutil
from pathlib import Path
from urllib.parse import quote_plus

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions, ReplyKeyboardRemove

# Railway: أضف BOT_TOKEN من Variables ولا تضع التوكن داخل GitHub.
TOKEN = os.getenv("BOT_TOKEN", "").strip()
DEV_USERNAME = "M_C_67"
DEV_LINK = "https://t.me/M_C_67"
MAX_BOTS = 3
RANKS = ["عضو", "مميز", "مدير", "ادمن", "منشئ", "منشئ أساسي", "مطور", "مطور ثانوي", "مطور أساسي"]
RANK_ALIASES = {"مم": "مميز", "م": "مميز", "مد": "مدير", "اد": "ادمن", "أدمن": "ادمن", "من": "منشئ", "اس": "منشئ أساسي", "أس": "منشئ أساسي", "مط": "مطور", "ثانوي": "مطور ثانوي", "اساسي": "مطور أساسي", "أساسي": "مطور أساسي"}

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
            rename_sessions = {}       # user_id -> {step, old}
            command_aliases = {}       # chat_id -> {new_name: old_name}
            sticker_locks = {}
            gif_locks = {}

            def is_dev(user):
                return bool(user and user.username and user.username.lower() == DEV_USERNAME.lower())

            def replied_user(message):
                reply = getattr(message, "reply_to_message", None)
                return getattr(reply, "from_user", None) if reply else None

            def rank_of(chat_id, user):
                if is_dev(user):
                    return "مطور أساسي"
                try:
                    member = sb.get_chat_member(chat_id, user.id)
                    if member.status == "creator":
                        return "مطور أساسي"
                    if member.status == "administrator":
                        return "مدير"
                except Exception:
                    pass
                return ranks.get(chat_id, {}).get(user.id, "عضو")

            def rank_level(rank):
                try:
                    return RANKS.index(rank)
                except ValueError:
                    return 0

            def can_manage(chat_id, actor, target):
                ar, tr = rank_of(chat_id, actor), rank_of(chat_id, target)
                return ar == "مطور أساسي" or rank_level(ar) > rank_level(tr)

            def admin(chat_id, user):
                return rank_level(rank_of(chat_id, user)) >= rank_level("مدير")

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

            @sb.callback_query_handler(func=lambda c: c.data.startswith("rankhelp:"))
            def rank_help(call):
                key = call.data.split(":", 1)[1]
                if key.isdigit() and 0 <= int(key) < len(RANKS):
                    rank = RANKS[int(key)]
                    level = rank_level(rank)
                    text_help = (f"🔰 <b>رتبة {rank}</b>\n" +
                                 ("• الأوامر العامة للأعضاء\n" if level == 0 else "• أوامر الرتب الأدنى بحسب الصلاحيات\n") +
                                 ("• إدارة الرتب الأدنى\n" if level >= rank_level("مدير") else "") +
                                 ("• جميع الصلاحيات وإدارة كل الرتب\n" if rank == "مطور أساسي" else "") +
                                 "• الصلاحيات الفعلية تعتمد على صلاحيات البوت ومشرفيته في تيليگرام.")
                elif key == "admin":
                    text_help = "🛡️ أوامر الإدارة: طرد، حظر، كتم، تقييد، إنذار، تثبيت، القوائم والمسح، قفل وفتح الحماية. متاحة للمدير فما فوق."
                else:
                    text_help = "👥 أوامر الأعضاء: ايدي، رابط، همسة بالرد، كت، يوت + اسم الأغنية، وأوامر الترفيه والردود العامة."
                try: sb.answer_callback_query(call.id)
                except Exception: pass
                try: sb.send_message(call.message.chat.id, text_help)
                except Exception: pass

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
                sb.answer_callback_query(call.id, text[:180] + ("…" if len(text) > 180 else ""), show_alert=True)

            @sb.message_handler(content_types=["sticker", "animation"])
            def filter_stickers_and_gifs(msg):
                cid = msg.chat.id
                if msg.chat.type not in ("group", "supergroup") or cid not in activated:
                    return
                try:
                    if msg.content_type == "sticker" and sticker_locks.get(cid, False):
                        sb.delete_message(cid, msg.message_id)
                    elif msg.content_type == "animation" and gif_locks.get(cid, False):
                        sb.delete_message(cid, msg.message_id)
                except Exception:
                    pass

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

                # خطوات إعادة تسمية أمر: المدير فما فوق فقط، والتغيير خاص بهذه المجموعة.
                if uid in rename_sessions:
                    session = rename_sessions[uid]
                    if not admin(cid, user):
                        rename_sessions.pop(uid, None)
                        sb.reply_to(msg, "⚠️ تعديل الأوامر للرتبة مدير فما فوق.")
                        return
                    if session["step"] == "old":
                        old_name = text.strip()
                        known = set(["تفعيل", "تعطيل", "الأوامر", "ايدي", "ا", "تغ", "تغيير", "رابط", "ر", "همسة", "تفعيل الترحيب", "تعطيل الترحيب", "رفع مميز", "مم", "م", "تنزيل مميز", "المميزين", "المكتومين", "المطرودين", "المحظورين", "المقيدين", "مسح المكتومين", "مسح المطرودين", "مسح المحظورين", "مسح المقيدين", "مسح المميزين", "قفل الدردشة", "فتح الدردشة", "قفل الروابط", "فتح الروابط", "قفل الصور", "فتح الصور", "قفل الفيديو", "فتح الفيديو", "قفل الملفات", "فتح الملفات", "قفل التكرار", "فتح التكرار", "قفل التوجيه", "فتح التوجيه", "قفل الملصقات", "فتح الملصقات", "قفل المتحركات", "فتح المتحركات", "تعديل أمر", "طرد", "حظر", "إلغاء حظر", "كتم", "إلغاء كتم", "تقييد", "إلغاء تقييد", "رفع القيود", "إنذار", "تثبيت", "إلغاء التثبيت", "كت", "يوت", "جمالي", "الحب", "الكره", "الرجولة", "الأنوثة", "اقتباس", "شعر", "قرآن"])
                        # نقبل فقط أمراً معروفاً أو اسماً سبق تخصيصه.
                        all_names = known | set(command_aliases.get(cid, {}).keys())
                        if old_name not in all_names:
                            sb.reply_to(msg, "❌ هذا الأمر مو موجود. أرسل الاسم مثل ما تستخدمه بالضبط، أو اكتب إلغاء.")
                            if old_name.lower() == "إلغاء": rename_sessions.pop(uid, None)
                            return
                        session.update({"step": "new", "old": command_aliases.get(cid, {}).get(old_name, old_name)})
                        sb.reply_to(msg, "✏️ هسه أرسل الاسم الجديد للأمر.")
                        return
                    new_name = text.strip()
                    if new_name in ("إلغاء", "الغاء"):
                        rename_sessions.pop(uid, None)
                        sb.reply_to(msg, "تم إلغاء تعديل الأمر.")
                        return
                    if not new_name or len(new_name) > 40 or " " in new_name or new_name.startswith("/"):
                        sb.reply_to(msg, "❌ الاسم الجديد لازم يكون كلمة واحدة، بدون /، وبحد أقصى 40 حرفاً.")
                        return
                    old_name = session["old"]
                    aliases = command_aliases.setdefault(cid, {})
                    if new_name in aliases or new_name in ("تعديل", "تعديل أمر", "إلغاء"):
                        sb.reply_to(msg, "❌ الاسم مستخدم بالفعل، اختار اسم ثاني.")
                        return
                    aliases[new_name] = old_name
                    rename_sessions.pop(uid, None)
                    sb.reply_to(msg, f"✅ صار الأمر <b>{new_name}</b> ينفّذ وظيفة <b>{old_name}</b> بهذه المجموعة.")
                    return

                # إذا كتب الاسم البديل، نفّذ نفس الأمر الأصلي، حتى لو تبعته وسائط مثل اسم أغنية.
                aliases_now = command_aliases.get(cid, {})
                for alias_name in sorted(aliases_now, key=len, reverse=True):
                    if text == alias_name or text.startswith(alias_name + " "):
                        text = aliases_now[alias_name] + text[len(alias_name):]
                        break
                parts = text.split()

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
                    markup = InlineKeyboardMarkup(row_width=2)
                    for rank_name in RANKS:
                        markup.add(InlineKeyboardButton("صلاحيات " + rank_name, callback_data="rankhelp:" + str(RANKS.index(rank_name))))
                    markup.add(InlineKeyboardButton("أوامر الإدارة", callback_data="rankhelp:admin"), InlineKeyboardButton("أوامر الأعضاء", callback_data="rankhelp:member"))
                    sb.reply_to(msg, "📋 <b>قائمة أوامر سجين</b>\nاختار رتبة حتى تشوف صلاحياتها.\n\nالرتب الأعلى تقدر تدير الرتب الأدنى، والمطور الأساسي أعلى رتبة.", reply_markup=markup)
                    return

                if text == "تعديل أمر":
                    if not admin(cid, user):
                        sb.reply_to(msg, "⚠️ هذا الأمر للرتبة مدير فما فوق.")
                        return
                    rename_sessions[uid] = {"step": "old"}
                    sb.reply_to(msg, "✏️ أرسل اسم الأمر الموجود الذي تريد تغييره، أو اكتب إلغاء.")
                    return

                if text in ("قفل الملصقات", "فتح الملصقات", "قفل المتحركات", "فتح المتحركات"):
                    if not admin(cid, user):
                        sb.reply_to(msg, "⚠️ هذا الأمر للرتبة مدير فما فوق.")
                        return
                    if "الملصقات" in text:
                        sticker_locks[cid] = text.startswith("قفل")
                        feature = "الملصقات"
                        enabled = sticker_locks[cid]
                    else:
                        gif_locks[cid] = text.startswith("قفل")
                        feature = "المتحركات"
                        enabled = gif_locks[cid]
                    sb.reply_to(msg, f"✅ تم {'قفل' if enabled else 'فتح'} {feature}.")
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
                rank_cmds = ("رفع مميز", "مم", "م", "تنزيل مميز", "رفع مدير", "رفع مد", "رفع ادمن", "رفع أدمن", "رفع اد", "رفع منشئ", "رفع من", "رفع منشئ أساسي", "رفع اس", "رفع أس", "رفع مطور", "رفع مط", "رفع مطور ثانوي", "رفع ثانوي", "رفع مطور أساسي", "رفع اساسي", "رفع أساسي", "تنزيل مدير", "تنزيل مد", "تنزيل ادمن", "تنزيل أدمن", "تنزيل اد", "تنزيل منشئ", "تنزيل من", "تنزيل منشئ أساسي", "تنزيل اس", "تنزيل أس", "تنزيل مطور", "تنزيل مط", "تنزيل مطور ثانوي", "تنزيل ثانوي", "تنزيل مطور أساسي", "تنزيل اساسي", "تنزيل أساسي", "تك")
                matched_rank = next((x for x in sorted(rank_cmds, key=len, reverse=True) if text == x), None)
                if matched_rank:
                    target = replied_user(msg)
                    if not target:
                        sb.reply_to(msg, "⚠️ رد على رسالة العضو ثم أرسل الأمر.")
                        return
                    if target.id == uid or is_dev(target):
                        sb.reply_to(msg, "⚠️ لا يمكن تغيير رتبة هذا العضو.")
                        return
                    if not can_manage(cid, user, target):
                        sb.reply_to(msg, "⚠️ لازم رتبتك أعلى من رتبة العضو، والمطور الأساسي يقدر يدير كل الرتب.")
                        return
                    if matched_rank == "تك":
                        ranks.setdefault(cid, {}).pop(target.id, None)
                        sb.reply_to(msg, f"✅ تم تنزيل {target.first_name} إلى رتبة عضو.")
                        return
                    removing = matched_rank.startswith("تنزيل")
                    if matched_rank in ("مم", "م", "رفع مميز", "تنزيل مميز"):
                        desired = "مميز"
                    else:
                        name = matched_rank.replace("رفع ", "").replace("تنزيل ", "")
                        desired = RANK_ALIASES.get(name, name)
                    if desired not in RANKS:
                        sb.reply_to(msg, "❌ رتبة غير معروفة.")
                        return
                    if removing:
                        ranks.setdefault(cid, {}).pop(target.id, None)
                        sb.reply_to(msg, f"✅ تم تنزيل {target.first_name} إلى رتبة عضو.")
                    else:
                        ranks.setdefault(cid, {})[target.id] = desired
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
                    "قفل التوجيه": ("forward", True), "فتح التوجيه": ("forward", False),
                    "قفل الملصقات": ("stickers", True), "فتح الملصقات": ("stickers", False),
                    "قفل المتحركات": ("gifs", True), "فتح المتحركات": ("gifs", False)
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
                    if not query:
                        sb.reply_to(msg, "🎵 اكتب اسم الأغنية بعد يوت، مثال: يوت Faded")
                        return
                    status = sb.reply_to(msg, f"🔎 دا أبحث عن الصوت: <b>{query}</b>، انتظر شوي…")
                    workdir = None
                    try:
                        import yt_dlp
                        workdir = tempfile.mkdtemp(prefix="sijin_audio_")
                        outtmpl = os.path.join(workdir, "audio.%(ext)s")
                        opts = {"format": "bestaudio/best", "noplaylist": True, "default_search": "ytsearch1", "outtmpl": outtmpl,
                                "quiet": True, "no_warnings": True, "extract_flat": False,
                                "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
                                "max_filesize": 48 * 1024 * 1024}
                        with yt_dlp.YoutubeDL(opts) as ydl:
                            ydl.download(["ytsearch1:" + query])
                        audio_path = next((os.path.join(workdir, f) for f in os.listdir(workdir) if f.lower().endswith((".mp3", ".m4a", ".opus", ".webm", ".ogg"))), None)
                        if not audio_path:
                            raise RuntimeError("لم يتم العثور على ملف صوت")
                        with open(audio_path, "rb") as audio:
                            sb.send_audio(cid, audio, title=query, reply_to_message_id=msg.message_id, timeout=120)
                        try: sb.delete_message(cid, status.message_id)
                        except Exception: pass
                    except Exception:
                        sb.reply_to(msg, "❌ ما كدرت أجيب الصوت هالمرة. تأكد من تثبيت yt-dlp وFFmpeg وأن الأغنية متاحة، وجرب اسم أغنية ثاني.")
                    finally:
                        if workdir:
                            shutil.rmtree(workdir, ignore_errors=True)
                    return
                general_replies = {
                    "السلام عليكم": ["وعليكم السلام ورحمة الله وبركاته 🌷", "هلا وعليكم السلام، نورتوا 🤍"],
                    "سلام عليكم": ["وعليكم السلام ورحمة الله وبركاته 🌹"], "هلا": ["هلا وغلا بيك 🌸", "يا هلا نورت المكان"], "هلو": ["هلوات، شلونك؟ 😄"],
                    "صباح الخير": ["صباح النور والسرور ☀️", "صباح الورد والياسمين 🌷"], "مساء الخير": ["مساء النور والراحة 🌙", "مساء الورد"],
                    "شلونك": ["الحمدلله بخير، إنت شلونك؟ 🤍", "تمام دامك بخير، شخبارك؟"], "شخبارك": ["كلشي تمام الحمدلله، إنت شلونك؟"],
                    "الحمدلله": ["دوم الحمد والشكر لله 🤲", "يدوم عليك الخير والعافية"], "شكرا": ["ولو، بالخدمة 🌷", "تدلل ما سوينا شي"], "شكراً": ["ولو، بالخدمة 🌷", "تدلل ما سوينا شي"],
                    "عاشت ايدك": ["الله يعافيك ويسلمك 🤍", "تسلم، هذا من ذوقك"], "عاشت إيدك": ["الله يعافيك ويسلمك 🤍"], "اسف": ["حصل خير، لا تشيل هم 🌿"], "آسف": ["حصل خير، ولا يهمك 🤍"],
                    "سامحني": ["مسامحك، تصير بأحسن العوائل 🌷"], "مبروك": ["ألف ألف مبروك، تستاهل كل خير 🎉"], "الف مبروك": ["ألف مبروك وعقبال الأفراح دوم 🎊"],
                    "الله يوفقك": ["وياك يا رب ويفتحها بوجهك 🤲"], "امين": ["آمين يا رب العالمين 🤲"], "آمين": ["آمين وياك يا رب"], "الله يخليك": ["ويخليك لأحبابك يا رب 🤍"],
                    "هههه": ["دوم هالضحكة 😂", "ضحكتك بالدنيا كلها"], "😂": ["دوم الضحكة 😂"], "ملل": ["غيّر جو شوي، سولف ويانه أو اسمع شي تحبه 😄"], "طفشان": ["تعال نغيّر الجو، تريد سؤال لو نكتة؟ 😄"],
                    "فرحان": ["تدوم فرحتك يا رب، الله يزيدك أفراح 🌟"], "زعلان": ["إن شاء الله تنفرج، إذا تحب احچي شبيك وأنا أسمعك 🤍"], "معصب": ["هدي بالك وخذ نفس، لا تخلي لحظة عصبية تضايقك 🌿"], "معقولة": ["إي والله؟ شنو السالفة؟ 😯"],
                    "اي": ["تمام حبيبي 🤝"], "إي": ["تمام حبيبي 🤝"], "لا": ["براحتك، رأيك محترم 🌷"], "شلون": ["تقصد شنو بالضبط؟ وضّحلي وأساعدك 😄"], "شنو": ["تفضل، شنو سؤالك؟ 👀"],
                    "اسمك": ["آني بوت سجين 🤖"], "كم عمرك": ["آني بوت، ما عندي عمر مثل البشر 😄"], "وينك": ["موجود هنانا وياكم 🤖"], "الساعة": ["شوف ساعة جهازك حتى تحصل الوقت المحلي الدقيق ⏰"],
                    "ساعدني": ["أكيد، گلي شنو تحتاج وإن شاء الله أساعدك 🤝"], "ما فهمت": ["ولا يهمك، وضّحلي أي جزء وأشرحه بطريقة أبسط 🌷"], "كفو": ["كفوك الطيب والأصيل 👑", "كفو منك ومن أصلك"],
                    "حبيبي": ["حبيب قلبي، تدلل 🤍", "عيوني إنت"], "عيني": ["عيونك الحلوة 🌹", "تدلل عيني"], "وردة": ["إنت الورد كله 🌹"], "مبدع": ["الإبداع من ذوقك والله ✨"],
                    "احبك": ["محبة واحترام إلك، الله يسعدك 🤍"], "أحبك": ["محبة واحترام إلك، الله يسعدك 🤍"], "اشتقتلك": ["الله يديم الود بينكم ويجمعكم على خير 🤍"], "اكرهك": ["براحتك، أتمنى لك الخير على كل حال 🌿"],
                    "استفزاز": ["خلّينا نحچي بهدوء ونحترم بعض 🤝"], "غبي": ["خلّينا نخلي كلامنا ألطف حتى تبقى السالفة حلوة 🌿"], "تسلم": ["الله يسلمك ويحفظك 🌷"], "فدوة": ["فداك الطيب، تدلل 🤍"],
                    "حياك": ["الله يحييك ويبقيك 🌹"], "نورت": ["بنورك يا طيب ✨"], "منور": ["نورك سابق 🌟"], "يا هلا": ["هلا بيك أكثر، نورتنا 🌸"], "مع السلامة": ["الله وياك ويحفظك، نشوفك على خير 👋"],
                    "تصبح على خير": ["وإنت من أهل الخير والأحلام الحلوة 🌙"], "تصبحون على خير": ["وإنتوا من أهل الخير 🌙"], "كفو والله": ["كفوك الطيب يا أصيل 👑"], "حبي": ["تدلل يا طيب 🤍"], "الغالي": ["الغالي إنت والله 🌹"],
                }
                if text in general_replies:
                    sb.reply_to(msg, random.choice(general_replies[text]))
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
        # Remove any old persistent reply keyboard saved in the Telegram chat.
        bot.send_message(msg.chat.id, "تم تحديث القائمة وإزالة الأزرار السفلية القديمة.",
                         reply_markup=ReplyKeyboardRemove())
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
