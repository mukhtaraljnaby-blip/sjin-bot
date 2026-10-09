import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
import random
import threading
import time

TOKEN = "8719015904:AAG7MwDSnyGMeNLfUH1W9aiumtlOr0WJMr8"
DEV = "@M_C_67"
bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

USER_BOTS = {}
WAITING_FOR_TOKEN = set()
RUNNING_SUB_BOTS = {}

MAKER_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("صنع بوت فرعي جديد 🤖", callback_data="create_bot")],
    [InlineKeyboardButton("قائمة بوتاتي 📋", callback_data="my_bots"), InlineKeyboardButton("تفعيل بوت VIP 💎", url="https://t.me/M_C_67")],
    [InlineKeyboardButton("مطور المصنع 👤", url="https://t.me/M_C_67")]
])

CAT_QUESTIONS = [
    "شنو أكثر شي تحبه بصديقك المقرب؟ 🖤", "لو انطوك مليار دولار، شنو أول شغلة تشتريها؟ 💸", "كلمة توجها لشخص خان ثقتك؟ 🎭",
    "شنو أحلى صفة بشخصيتك وأسوأ صفة؟ 🤔", "لو رجع بيك الزمن للماضي، شنو الشغلة اللي تغيرها؟ ⏳", "أكثر موقف محرج صار وياك بحياتك شنو هو؟ 😅",
    "تحب الحياة الهادئة لو حياة المغامرات والسفر؟ 🌍", "شنو الأكلة العراقية اللي مستحيل تمل منها؟ 🍲", "لو تكدر تختفي يوم واحد، وين تروح وشسوّي؟ 🫥",
    "شنو أكتر اسم تحب تسميه بالمستقبل؟ 👶", "لو خيروك تعيش بلا إنترنت أو بلا أصدقاء، شتختار؟ 📵", "شنو أكتر موقف ضحكك لدرجة البجي بحياتك؟ 😂",
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
    "⚡ ──━[ هويتك الرسمية ]━━── ⚡", "🌟 ─── ❖ ⦗ كرت التعريف ⦘ ─── 🌟", "🖤 ══════ ≪ ايدي مميز ≫ ══════ 🖤",
    "🚀 ─── • ⦗ هويتك بالكروب ⦘ • ─── 🚀", "👑 ───── ❖ ⦗ بطاقة الملوك ⦘ ───── 👑", "💫 ━━━ ≪ كرت التعريف الخاص ≫ ━━━ 💫",
    "⚜️ ─── • [ ايدي سجين ] • ─── ⚜️", "🔹 ════════ ≪ هويتك ≫ ════════ 🔹", "🌠 ───── ❖ ⦗ بطاقتك ⦘ ───── 🌠",
    "🎯 ─── • ⦗ ايدي الفخم ⦘ • ─── 🎯", "🔮 ═════ ≪ كرت العضو ≫ ═════ 🔮", "⚡ ───── ❖ ⦗ الهوية ⦘ ───── ⚡",
    "💥 ─── • [ ايديك الأنيق ] • ─── 💥", "🎇 ══════ ≪ بطاقة التعريف ≫ ══════ 🎇", "⚓ ───── ❖ ⦗ ايدي الكروب ⦘ ⚓",
    "🌙 ─── • [ كرت الهوية ] • ─── 🌙", "🔥 ═════ ≪ هويتك الأسطورية ≫ ═════ 🔥"
]

def run_sub_bot(token):
    while True:
        try:
            sub_bot = telebot.TeleBot(token, parse_mode="Markdown")
            me = sub_bot.get_me()
            bot_name = me.first_name
            bot_username = f"@{me.username}"

            activated_chats = set()
            welcome_settings = {}
            id_photo_settings = {}
            global_whispers_cache = {}

            def get_reply_target(message):
                """Return replied-to user, or None. Telegram normally supplies reply_to_message."""
                replied = getattr(message, "reply_to_message", None)
                if replied is not None:
                    target = getattr(replied, "from_user", None)
                    if target is not None:
                        return target
                return None

            @sub_bot.message_handler(commands=['start'])
            def sub_start(msg):
                if msg.chat.type != 'private':
                    return
                user_id = msg.from_user.id
                text = (msg.text or "").strip()

                if text.startswith("/start whisper_"):
                    parts = text.split("_", 4)
                    if len(parts) >= 4:
                        try:
                            target_id = int(parts[2])
                            chat_id = int(parts[3].split()[0])
                        except (ValueError, IndexError):
                            sub_bot.send_message(user_id, "⚠️ رابط الهمسة غير صالح. ارجع للمجموعة واضغط زر الهمسة من جديد.")
                            return
                        target_name = parts[4].replace("_", " ") if len(parts) > 4 else "العضو"
                        global_whispers_cache[user_id] = {
                            'target_id': target_id, 'target_name': target_name, 'chat_id': chat_id
                        }
                        sub_bot.send_message(
                            user_id,
                            f"🔒 **أهلاً بك في خاص الهمسات السرية!**\n\n"
                            f"👤 الشخص المراد اهمـاسه: **{target_name}**\n"
                            f"✍️ اكتب نص الهمسة الآن في رسالة جديدة، وسأنشرها في المجموعة 👇"
                        )
                        return

                if user_id in global_whispers_cache:
                    sub_bot.send_message(user_id, "⚠️ أنت بانتظار كتابة نص الهمسة؛ أرسل النص مباشرة هنا.")
                    return

                start_caption = (
                    f"⌔︙أهـلا بـك في بـوت ﴿ {bot_name} ﴾\n"
                    f"⌔︙لحماية المجموعات 🛡️\n"
                    f"⌔︙أضف البوت وارفعه مشرفاً في مجموعتك\n"
                    f"⌔︙أرسل ﴿ تفعيل ﴾ لتفعيل المجموعة ⚡\n\n"
                    f"⌔︙يوزر البوت ← {bot_username}\n"
                    f"⌔︙يوزر المطور ← {DEV}"
                )
                try:
                    photos = sub_bot.get_user_profile_photos(me.id, limit=1)
                    if photos.total_count:
                        sub_bot.send_photo(msg.chat.id, photos.photos[0][0].file_id, caption=start_caption)
                        return
                except Exception:
                    pass
                sub_bot.send_message(msg.chat.id, start_caption)

            @sub_bot.message_handler(func=lambda msg: msg.chat.type == 'private' and msg.from_user and msg.from_user.id in global_whispers_cache, content_types=['text'])
            def handle_whisper_text_input(msg):
                user_id = msg.from_user.id
                whisper_data = global_whispers_cache.get(user_id)
                if not whisper_data:
                    sub_bot.reply_to(msg, "⚠️ انتهت صلاحية جلسة الهمسة؛ اضغط زر الهمسة من المجموعة مجدداً.")
                    return
                whisper_text = (msg.text or "").strip()
                if not whisper_text or whisper_text.startswith('/'):
                    sub_bot.reply_to(msg, "⚠️ أرسل نص الهمسة بشكل طبيعي، وليس كأمر تليجرام.")
                    return

                target_id = whisper_data['target_id']
                target_name = whisper_data['target_name']
                chat_id = whisper_data['chat_id']
                sender_name = msg.from_user.first_name
                whisper_key = f"{user_id}_{target_id}"
                if not hasattr(sub_bot, 'whisper_store'):
                    sub_bot.whisper_store = {}
                sub_bot.whisper_store[whisper_key] = whisper_text
                del global_whispers_cache[user_id]

                markup = InlineKeyboardMarkup([[
                    InlineKeyboardButton("💬 اضغط لقراءة الهمسة السرية", callback_data=f"read_whisper_{user_id}_{target_id}")
                ]])
                try:
                    sub_bot.send_message(
                        chat_id,
                        f"🔒 **همسة سرية جديدة!**\n\n"
                        f"👤 المرسل: [{sender_name}](tg://user?id={user_id})\n"
                        f"🎯 المرسل إليه: [{target_name}](tg://user?id={target_id})\n\n"
                        f"فقط الشخص المعني يمكنه قراءة الهمسة بالضغط على الزر أدناه 👇",
                        reply_markup=markup
                    )
                    sub_bot.reply_to(msg, "✅ **تم إرسال همستك السرية إلى المجموعة بنجاح!** 🤫✨")
                except Exception as e:
                    sub_bot.reply_to(msg, f"❌ تعذر إرسال الهمسة. تأكد أن البوت موجود بالمجموعة.\nالتفاصيل: {e}")

            @sub_bot.callback_query_handler(func=lambda call: call.data.startswith("read_whisper_"))
            def sub_callback_handlers(call):
                try:
                    parts = call.data.split("_")
                    sender_id, target_id = int(parts[2]), int(parts[3])
                except (ValueError, IndexError):
                    sub_bot.answer_callback_query(call.id, "الهمسة غير صالحة.", show_alert=True)
                    return
                if call.from_user.id not in (sender_id, target_id) and call.from_user.username != "M_C_67":
                    sub_bot.answer_callback_query(call.id, "❌ هذه الهمسة سرية وليست مخصصة لك!", show_alert=True)
                    return
                content = getattr(sub_bot, 'whisper_store', {}).get(f"{sender_id}_{target_id}", "⚠️ انتهت صلاحية الهمسة أو حُذفت.")
                sub_bot.answer_callback_query(call.id, f"📝 نص الهمسة: {content}", show_alert=True)

            @sub_bot.message_handler(content_types=['new_chat_members'])
            def sub_welcome(msg):
                chat_id = msg.chat.id
                if chat_id in activated_chats and welcome_settings.get(chat_id, True):
                    for member in msg.new_chat_members:
                        sub_bot.send_message(chat_id, f"هلا بيك يا بعد روحي 🌸 [{member.first_name}](tg://user?id={member.id})\nنورت الكروب بوجودك يا عطرها ⚡🖤")

            @sub_bot.message_handler(content_types=['text'])
            def sub_group_handler(msg):
                if msg.chat.type not in ('group', 'supergroup') or not msg.from_user:
                    return
                chat_id = msg.chat.id
                text = (msg.text or "").strip()
                user = msg.from_user
                user_id = user.id
                user_name = user.first_name
                is_main_dev = user.username == "M_C_67"
                is_admin = False
                is_chat_creator = False
                try:
                    member = sub_bot.get_chat_member(chat_id, user_id)
                    if member.status in ('creator', 'administrator'):
                        is_admin = True
                    if member.status == 'creator':
                        is_chat_creator = True
                except Exception:
                    pass
                if is_main_dev:
                    is_admin = True

                if text == "تفعيل":
                    if is_admin or is_chat_creator:
                        activated_chats.add(chat_id)
                        sub_bot.reply_to(msg, "✅ **تم تفعيل المجموعة بنجاح وحماية سجين تعمل بكامل طاقتها ⚡**")
                    else:
                        sub_bot.reply_to(msg, "⚠️ أمر التفعيل مخصص للمدراء والمشرفين فقط!")
                    return
                if chat_id not in activated_chats:
                    return

                if text in ("همسه", "همسة"):
                    target_user = get_reply_target(msg)
                    if target_user is None:
                        sub_bot.reply_to(msg, "⚠️ ما وصلني الرد على رسالة العضو. جرّب الرد على رسالة العضو الأصلية مباشرة، وإذا استمرت المشكلة أرسل الأمر بصيغة: همسة 123456789 (ايدي العضو).")
                        return
                    if target_user.id in (me.id, user_id):
                        sub_bot.reply_to(msg, "⚠️ لا يمكنك إرسال همسة للبوت أو لنفسك!")
                        return
                    safe_name = target_user.first_name.replace(" ", "_")
                    markup = InlineKeyboardMarkup([[
                        InlineKeyboardButton("اضغط هنا لكتابة الهمسة 💬", url=f"https://t.me/{me.username}?start=whisper_{target_user.id}_{chat_id}_{safe_name}")
                    ]])
                    sub_bot.reply_to(
                        msg,
                        f"🔒 **مرحباً [{user_name}](tg://user?id={user_id})**\n\n"
                        f"لقد طلبت إرسال همسة إلى [{target_user.first_name}](tg://user?id={target_user.id})\n"
                        f"اضغط على الزر أدناه للدخول للخاص وكتابة الهمسة السرية 👇",
                        reply_markup=markup
                    )
                    return

                if text.startswith(("طرد", "كتم", "تقييد")):
                    if not is_admin:
                        sub_bot.reply_to(msg, "⚠️ هذه الأوامر مخصصة للمشرفين فقط!")
                        return
                    target_user = get_reply_target(msg)
                    # Fallback: support command with a numeric Telegram user ID.
                    if target_user is None:
                        pieces = text.split()
                        if len(pieces) > 1 and pieces[1].isdigit():
                            try:
                                target_user = sub_bot.get_chat_member(chat_id, int(pieces[1])).user
                            except Exception:
                                target_user = None
                    if target_user is None:
                        sub_bot.reply_to(msg, "⚠️ ما وصلني الرد على رسالة الشخص. رد مباشرة على رسالته، أو استخدم: طرد 123456789 / كتم 123456789 / تقييد 123456789")
                        return
                    try:
                        target_member = sub_bot.get_chat_member(chat_id, target_user.id)
                        if target_member.status in ('creator', 'administrator') or target_user.username == "M_C_67":
                            sub_bot.reply_to(msg, "❌ **لا يمكن تنفيذ إجراء بحق مشرف أو شخص محمي!** 🛡️")
                            return
                    except Exception:
                        pass
                    try:
                        if text.startswith("طرد"):
                            sub_bot.ban_chat_member(chat_id, target_user.id)
                            sub_bot.reply_to(msg, "🥾 **تم طرد العضو بنجاح ⚡**")
                        elif text.startswith("كتم"):
                            sub_bot.restrict_chat_member(chat_id, target_user.id, ChatPermissions(can_send_messages=False))
                            sub_bot.reply_to(msg, "🔇 **تم كتم العضو بنجاح ⚡**")
                        else:
                            sub_bot.restrict_chat_member(chat_id, target_user.id, ChatPermissions(can_send_messages=False, can_send_media_messages=False))
                            sub_bot.reply_to(msg, "🔒 **تم تقييد العضو بنجاح ⚡**")
                    except Exception as e:
                        sub_bot.reply_to(msg, f"❌ لم أستطع تنفيذ الأمر. تأكد أن البوت مشرف وصلاحياته تسمح بالإجراء.\nالتفاصيل: {e}")
                    return

                if text == "تفع":
                    if is_admin:
                        id_photo_settings[chat_id] = True
                        sub_bot.reply_to(msg, "🖼️ **تم تفعيل عرض الصورة الشخصية في الأيدي بنجاح!** ⚡")
                    return
                elif text == "تعط":
                    if is_admin:
                        id_photo_settings[chat_id] = False
                        sub_bot.reply_to(msg, "📝 **تم تعطيل عرض الصورة في الأيدي بنجاح!** ⚡")
                    return

                if text == "تعطيل":
                    if is_admin or is_chat_creator:
                        activated_chats.discard(chat_id)
                        sub_bot.reply_to(msg, "❌ **تم تعطيل البوت في هذه المجموعة!**")
                    return

                if text in ["الأوامر", "اوامر", "ترتيب الاوامر", "قائمة الأوامر"]:
                    commands_text = (
                        "📋 **قائمة أوامر سورس سجين الشاملة:**\n\n"
                        "👤 **أوامر الأعضاء:**\n"
                        "• `ا` أو `ايدي` - عرض ايديك الفخم\n"
                        "• `تغ` أو `تغير` - تغيير ستايل الايدي\n"
                        "• `ر` أو `رابط` - جلب رابط الكروب\n"
                        "• `همسة` (بالرد على العضو) - إرسال همسة سرية\n"
                        "• `كت` - أسئلة كت ترفيهية\n"
                        "• `يوت [كلمة]` - بحث يوتيوب سريع\n\n"
                        "💬 **الردود العامة**\n\n"
                        "🛠️ **أوامر المدراء:**\n"
                        "• `تفعيل` / `تعطيل`\n"
                        "• `طرد` / `كتم` / `تقييد` (بالرد)\n"
                        "• `قفل الدردشة` / `فتح الدردشة`"
                    )
                    sub_bot.reply_to(msg, commands_text)
                    return

                # الردود العامة الأصلية
                replies = {
                    ("السلام عليكم", "السلام", "سلام عليكم"): "وعليكم السلام ورحمة الله وبركاته يا هلا بـ ريحة هلي 🤍✨",
                    ("وعليكم السلام", "وعليكم السلام ورحمة الله"): "يا هلا بطاريكم نورتوا الكروب والله 🌸",
                    ("احبك", "أحبك", "احبج", "أحبج", "اموت عليك"): "عشكتك روح وجسد يا بعد بيتي وعافيتي أنت 🤍✨",
                    ("فديتك", "فديتاس", "فديتج", "فدوه"): "فداك الكون وگلبي وعمري يا بعد روحي أنت 🖤⚡",
                    ("هلاو", "هلا", "هلو", "هايات", "هلوز"): "هلا بيك يا بعد روحي ونبض گلبـي، منور 🌸⚡",
                    ("شلونك", "شلونج", "شخباركم", "شلونكم"): "بخير دام عيونك الحلوة بخير يا غالي 🤍",
                    ("عمي", "تاج راسي", "الشيخ"): "حبيبي الغالي تاج راس الكل أنت وفدوه لك الكل 👑🖤",
                    ("روحي", "قلبي", "گلبـي", "عمري"): "روحه وعمره وكلبي يمه فديت هالطاري 🥺🤍",
                    ("بوت", "البوت", "سجين"): "عيون البوت وخدامة للحلوين، امرني حبيبي 🤖🖤",
                    ("منور", "منورين", "نوركم"): "نور عيونك الساطع يا وردة الكروب العطرة 🌟",
                    ("تصبح على خير", "بباي", "مع السلامة", "في امان الله"): "وأنت من أهل الخير يا بعد روحي، دير بالك على نفسك هواي 🌙💤",
                    ("احم", "احم احم"): "يا هلا بالشيخ، نورت المكان بطلتك 🦅🖤",
                    ("شكرا", "تسلم", "مشكور"): "ولو تدلل عيوني، بخدمتكم دائماً 🤍✨",
                    ("صباح الخير", "صباح النور", "صبايا"): "صباح الورد والفل على عيون أطيب ناس ☀️🌸",
                    ("مساء الخير", "مساء الورد", "مساء الحب"): "مساء العسل والعيون السود يا غالي 🌙🤍",
                    ("وينكم", "ميتين", "الكروب نايم"): "صيحو للشباب خليهم يصحون، الكروب بوجودكم يحلى ⚡🔥",
                    ("هههه", "ههههه", "خرب ههه", "هههههههه"): "دوم هالضحكة الفرحانة يا رب، عسى ما تنتهي 😃❤️",
                    ("اوف", "اووووف", "ضايج", "مخنوك"): "سلامة گلبك من الضيج يا بعد روحي، شبيها الحلوة تضوج؟ 🥺💔",
                    ("شكو ماكو", "كو شي جديد"): "والله كولشي ماكو غير طرياتكم الحلوة بالكروب 🌸",
                    ("دوم", "دومك", "تدوم الضحكة"): "تدوم أيامك حلوة وسعيدة يا رب ✨",
                    ("اكلكم", "شباب", "بنات"): "گول عوني، سامعينك وكلنا وياك 🖤👂",
                    ("تمام", "وكي", "صحيح", "عاشت ايدك"): "عاش من اذكرك، تدلل يا غالي 🤍",
                    ("ولك", "ولك سجين", "لك بوت"): "عيون ولَك وروح ولَك، أمرني شتريد؟ 🙈🔥",
                    ("حبي", "حبيبي", "عيوني"): "عيون حبيبي وروحه وكلبه أنت 🤍✨",
                    ("غوالي", "الغالين", "أعز ناس"): "أنتم تاج راس الكل والله والفخر ليكم 👑",
                    ("باي", "يلا باي", "رايح"): "بحفظ الله ورعايته، لا تطول الغيبة عنا 🥀",
                    ("شنو السالفة", "شكو"): "ماكو شي، قاعدين نسولف ونشم هواكم الطيب 🍃",
                    ("حباب", "فدوة", "ارجوك"): "تامرني أمر، عيوني لك والله 🌸",
                    ("عاشت افيكم", "كفو", "عاشت الايادي"): "كفو منك يا ذيب، دائماً مبدع 🐺⚡",
                    ("وينك", "مختفي", "صارلك غيبة"): "موجود بقلب الحدث وبخدمتكم طوال الوقت 🤖🖤",
                    ("تعبان", "هيلث تعبان", "منتهي"): "سلامة تعبك، ارتاح لك شوية واهتم بنفسك 🛌💤",
                    ("اكو أحد", "موجودين"): "اي نعم، البوت والشباب حاضرين لك ⚡",
                    ("اكلك", "سجين اسمعني"): "سمعانك وبكل أذان صاغية، تفضل گول 🖤",
                    ("عراقي", "العراق", "دارمي", "ابودذية"): "يا دار دار العز يا دار الحبيبة، فديت العراق وأهله 🇮🇶🦅",
                    ("نورت الكروب", "نور الكروب بوجودي"): "طبعاً ينور بوجود الأساطير أمثالك 🌟",
                    ("شكد عمرك", "مواليدك"): "عمري برمجته على حبكم، يعني شاب طازج 🤖✨",
                    ("منين انت", "وين ساكن"): "أنا ابن السورس، وعايش بقلوبكم الطيبة 🤍",
                    ("اسمي", "تعرفني"): "أكيد أعرفك، أنت الغالي اللي ما ينعوض 💎",
                    ("حبيبتي", "عشيرتي"): "الله يخليكم لبعض ولا يفرقكم أبداً 🌸",
                    ("صديقي", "اخوي", "صاحبي"): "نعم الأخ والصديق الوفي بالشدة 🤝🖤",
                    ("تحبني", "تحبني لو تقشمرني"): "غير اموت عليك وعلى سوالفك الحلوة 🙈❤️",
                    ("كافي", "بطل"): "صار، بعد ما أتحاچى عيونك تدلل 🤐✨",
                    ("زعلان", "زعلان منك"): "عفية لا تزعل، رضاك علي يسوى الدنيا وما بيها 🥺🌹",
                    ("منو مطورك", "منو صنعك"): "مطوري الأساسي وسيد الوجوه هو الأسطورة `@M_C_67` 👑",
                    ("سورس", "سورس سجين"): "سورس سجين الأقوى لحماية الكروبات وتفليش الهكرز 🛡️⚡",
                    ("اكل", "جوعان", "تريكت"): "بالهناء والشفاء، لو يمك جان سويتلك أطيب لفة فلافل عراقية 🌯😋",
                    ("شربت ججاي", "جاي", "استكان جاي"): "يا سلام، استكان جاي مهيل على الحطب ينسيك تعب اليوم كله ☕🌿",
                    ("الحب", "العشق"): "الحب الحقيقي هو وفاء الأصدقاء ونقاء القلوب 🤍",
                    ("جمعة مباركة", "الجمعة"): "جمعة مباركة معطرة بذكر الله وبركات النبي محمد (ص) 🕌✨",
                    ("باي باي", "مع السلامه", "الى اللقاء"): "في أمان الله وحفظه، نترقب رجعتك بفارغ الصبر يا غالي 👋🖤"
                }
                for triggers, response in replies.items():
                    if text in triggers:
                        sub_bot.reply_to(msg, response)
                        return

                if text in ("ا", "ايدي"):
                    style = random.choice(ID_STYLES)
                    rank = "المطور الأساسي 👑" if is_main_dev else ("منشئ 🛡️" if is_chat_creator else ("مشرف ⚡" if is_admin else "عضو مميز 🖤"))
                    caption = f"{style}\n\n👤 اسمك: {user_name}\n🆔 ايديك: `{user_id}`\n🔰 رتبتك: {rank}"
                    if id_photo_settings.get(chat_id, True):
                        try:
                            photos = sub_bot.get_user_profile_photos(user_id, limit=1)
                            if photos.total_count:
                                sub_bot.send_photo(chat_id, photos.photos[0][0].file_id, caption=caption, reply_to_message_id=msg.message_id)
                                return
                        except Exception:
                            pass
                    sub_bot.reply_to(msg, caption)
                    return
                if text in ("تغ", "تغيير"):
                    sub_bot.reply_to(msg, f"🎨 **تم تغيير ستايل الايدي بنجاح:**\n\n{random.choice(ID_STYLES)}")
                    return
                if text == "تفعيل الترحيب" and is_admin:
                    welcome_settings[chat_id] = True
                    sub_bot.reply_to(msg, "✅ **تم تفعيل الترحيب في هذا الكروب!**")
                    return
                if text == "تعطيل الترحيب" and is_admin:
                    welcome_settings[chat_id] = False
                    sub_bot.reply_to(msg, "❌ **تم تعطيل الترحيب في هذا الكروب!**")
                    return
                if text in ("ر", "رابط"):
                    try:
                        link = sub_bot.export_chat_invite_link(chat_id)
                        sub_bot.reply_to(msg, f"🔗 **رابط الكروب:**\n{link}")
                    except Exception:
                        sub_bot.reply_to(msg, "⚠️ تأكد من رفعي مشرف بصلاحية إضافة أعضاء لجلب الرابط.")
                    return
                if text == "قفل الدردشة" and is_admin:
                    try:
                        sub_bot.set_chat_permissions(chat_id, ChatPermissions(can_send_messages=False))
                        sub_bot.reply_to(msg, "🔒 **تم قفل الدردشة بنجاح!**")
                    except Exception:
                        pass
                    return
                if text == "فتح الدردشة" and is_admin:
                    try:
                        sub_bot.set_chat_permissions(chat_id, ChatPermissions(can_send_messages=True, can_send_media_messages=True))
                        sub_bot.reply_to(msg, "🔓 **تم فتح الدردشة بنجاح!**")
                    except Exception:
                        pass
                    return
                if text == "كت":
                    sub_bot.reply_to(msg, f"❓ **سؤال كت:**\n\n{random.choice(CAT_QUESTIONS)}")
                    return
                if text.startswith("يوت"):
                    query = text.replace("يوت", "", 1).strip()
                    if query:
                        sub_bot.reply_to(msg, f"🔍 **نتائج بحث اليوتيوب:**\nhttps://www.youtube.com/results?search_query={query.replace(' ', '+')}")
                    return

            sub_bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
        except Exception:
            time.sleep(5)

@bot.message_handler(commands=['start'])
def start_handler(msg):
    if msg.chat.type == 'private':
        WAITING_FOR_TOKEN.discard(msg.from_user.id)
        start_text = (
            "⌔︙أهـلا بـك في مصنع بـوتات حماية سجين الحقيقي ⚡\n"
            "⌔︙هذا البوت مخصص لصنع وإدارة بوتات الحماية الفرعية التشغيلية.\n"
            "⌔︙الحد الأقصى للبوتات هو `3 بوتات`.\n"
            "⌔︙اختر ما تحب من الأزرار بالأسفل 👇"
        )
        bot.send_message(msg.chat.id, start_text, reply_markup=MAKER_KEYBOARD)

@bot.message_handler(func=lambda msg: msg.chat.type == 'private' and msg.from_user and msg.from_user.id in WAITING_FOR_TOKEN, content_types=['text'])
def receive_token_handler(msg):
    user_id = msg.from_user.id
    text = (msg.text or "").strip()
    if text.startswith('/'):
        bot.reply_to(msg, "⚠️ يرجى إرسال توكن صالح للبوت أو اضغط /start للإلغاء.")
        return
    try:
        test_bot = telebot.TeleBot(text)
        info = test_bot.get_me()
        username = f"@{info.username}"
        if user_id not in USER_BOTS:
            USER_BOTS[user_id] = []
        if any(item['bot_token'] == text for item in USER_BOTS[user_id]):
            WAITING_FOR_TOKEN.discard(user_id)
            bot.reply_to(msg, "⚠️ **هذا البوت مصنوع مسبقاً وموجود في قائمة بوتاتك!**")
            return
        USER_BOTS[user_id].append({"bot_name": info.first_name, "bot_username": username, "bot_token": text})
        if text not in RUNNING_SUB_BOTS:
            thread = threading.Thread(target=run_sub_bot, args=(text,), daemon=True)
            thread.start()
            RUNNING_SUB_BOTS[text] = thread
        WAITING_FOR_TOKEN.discard(user_id)
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("قائمة بوتاتي 📋", callback_data="my_bots")],
            [InlineKeyboardButton("رجوع 🔙", callback_data="back_start")]
        ])
        bot.send_message(msg.chat.id,
            f"✅ **تم تشغيل البوت الفرعي وربطه بنجاح!**\n\n🤖 **يوزر البوت:** {username}\n📌 **اسم البوت:** {info.first_name}\n\nالبوت يعمل الآن.",
            reply_markup=markup)
    except Exception:
        bot.reply_to(msg, "❌ **التوكن غير صحيح أو منتهي الصلاحية!**\nتأكد من توكن البوت الحقيقي من `@BotFather`.")

@bot.callback_query_handler(func=lambda call: True)
def callback_handlers(call):
    user_id = call.from_user.id
    bot.answer_callback_query(call.id)
    if call.data == "create_bot":
        if len(USER_BOTS.get(user_id, [])) >= 3:
            markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("تواصل لتفعيل VIP 💎", url="https://t.me/M_C_67")],
                [InlineKeyboardButton("رجوع 🔙", callback_data="back_start")]
            ])
            bot.edit_message_text("❌ **وصلت للحد الأقصى (3 بوتات فرعية)!**\n\n💎 لتفعيل VIP تواصل مع المطور @M_C_67",
                                  call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            WAITING_FOR_TOKEN.add(user_id)
            markup = InlineKeyboardMarkup([[InlineKeyboardButton("إلغاء 🔙", callback_data="back_start")]])
            bot.edit_message_text("⚙️ **خطوات صنع بوت فرعي:**\n\n1️⃣ أنشئ بوتاً من `@BotFather`.\n2️⃣ انسخ التوكن.\n3️⃣ أرسله هنا لتشغيل البوت تلقائياً.",
                                  call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif call.data == "my_bots":
        items = USER_BOTS.get(user_id, [])
        if not items:
            bot.edit_message_text("📂 **قائمة بوتاتك:**\n\n❌ لا يوجد بوتات مصنوعة حالياً!",
                                  call.message.chat.id, call.message.message_id,
                                  reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع 🔙", callback_data="back_start")]]))
        else:
            text = f"📂 **قائمة بوتاتك ({len(items)}/3):**\n\n"
            markup = InlineKeyboardMarkup()
            for index, item in enumerate(items):
                text += f"{index+1}⌯ البوت: `{item['bot_name']}`\n🔗 اليوزر: {item['bot_username']}\n\n"
                markup.add(InlineKeyboardButton(f"حذف {item['bot_username']} 🗑️", callback_data=f"delete_bot_{user_id}_{index}"))
            markup.add(InlineKeyboardButton("رجوع 🔙", callback_data="back_start"))
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif call.data == "back_start":
        WAITING_FOR_TOKEN.discard(user_id)
        bot.edit_message_text("⌔︙أهـلا بـك في مصنع بـوتات حماية سجين الحقيقي ⚡\n⌔︙اختر ما تحب من الأزرار بالأسفل 👇",
                              call.message.chat.id, call.message.message_id, reply_markup=MAKER_KEYBOARD)
    elif call.data.startswith("delete_bot_"):
        try:
            _, _, uid, idx = call.data.split("_")
            uid, idx = int(uid), int(idx)
        except (ValueError, IndexError):
            return
        if uid == user_id and uid in USER_BOTS and 0 <= idx < len(USER_BOTS[uid]):
            deleted = USER_BOTS[uid].pop(idx)
            # تنبيه: حذف السجل لا يوقف polling الجاري فعلياً؛ الإيقاف يحتاج آلية منفصلة.
            bot.edit_message_text(f"✅ **تم حذف البوت ({deleted['bot_username']}) من قائمتك.**",
                                  call.message.chat.id, call.message.message_id,
                                  reply_markup=InlineKeyboardMarkup([
                                      [InlineKeyboardButton("قائمة بوتاتي 📋", callback_data="my_bots")],
                                      [InlineKeyboardButton("رجوع 🔙", callback_data="back_start")]
                                  ]))

bot.infinity_polling()
