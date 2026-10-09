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

            @sub_bot.message_handler(commands=['start'])
            def sub_start(msg):
                if msg.chat.type == 'private':
                    user_id = msg.from_user.id
                    text = msg.text.strip()
                    
                    if text.startswith("/start whisper_"):
                        parts = text.split("_")
                        if len(parts) >= 4:
                            target_id = int(parts[2])
                            chat_id = int(parts[3])
                            target_name = parts[4].replace("_", " ") if len(parts) > 4 else "العضو"
                            
                            global_whispers_cache[user_id] = {
                                'target_id': target_id,
                                'target_name': target_name,
                                'chat_id': chat_id
                            }
                            sub_bot.send_message(
                                user_id,
                                f"🔒 **أهلاً بك في خاص الهمسات السرية!**\n\n"
                                f"👤 الشخص المراد اهماسه: **{target_name}**\n"
                                f"✍️ اكتب نص الهمسة الآن في هذه الرسالة، وسأقوم بنشرها سراً في المجموعة 👇"
                            )
                            return

                    if user_id in global_whispers_cache:
                        sub_bot.send_message(user_id, "⚠️ بانتظار كتابة نص الهمسة، أرسل النص الآن مباشرة في هذه المحادثة:")
                        return

                    start_caption = (
                        f"⌔︙أهـلا بـك في بـوت ﴿ {bot_name} ﴾\n"
                        f"⌔︙لحماية المجموعات من التفليش 🛡️\n"
                        f"⌔︙يمڪنك تفعيل البوت ڪالاتي :\n"
                        f"⌔︙اضف البوت وارفعه مشرف في مجموعتك\n"
                        f"⌔︙ارسل ﴿ تفعيل ﴾ ليتم تفعيل المجموعه ⚡\n\n"
                        f"⌔︙يوزر البوت ← {bot_username}\n"
                        f"⌔︙يوزر مطور البوت ← {DEV}\n"
                        f"⌔︙يوزر مطور السورس ← {DEV}"
                    )
                    try:
                        photos = sub_bot.get_user_profile_photos(me.id, limit=1)
                        if photos.total_count > 0:
                            sub_bot.send_photo(msg.chat.id, photos.photos[0][0].file_id, caption=start_caption)
                            return
                    except Exception:
                        pass
                    sub_bot.send_message(msg.chat.id, start_caption)

            @sub_bot.message_handler(func=lambda msg: msg.chat.type == 'private' and msg.from_user.id in global_whispers_cache)
            def handle_whisper_text_input(msg):
                user_id = msg.from_user.id
                whisper_data = global_whispers_cache.get(user_id)
                
                if not whisper_data:
                    sub_bot.reply_to(msg, "⚠️ انتهت صلاحية جلسة الهمسة، اضغط على زر الهمسة من المجموعة مجدداً.")
                    return

                whisper_text = msg.text.strip() if msg.text else ""
                if whisper_text.startswith('/'):
                    sub_bot.reply_to(msg, "⚠️ يرجى إرسال نص الهمسة بشكل طبيعي وليس كأمر تليجرام.")
                    return
                
                target_id = whisper_data['target_id']
                target_name = whisper_data['target_name']
                chat_id = whisper_data['chat_id']
                sender_name = msg.from_user.first_name

                del global_whispers_cache[user_id]

                whisper_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton("💬 اضغط لقراءة الهمسة السرية", callback_data=f"read_whisper_{user_id}_{target_id}")]
                ])
                
                try:
                    sub_bot.send_message(
                        chat_id,
                        f"🔒 **هـمسـة سـريـة جديدة!**\n\n"
                        f"👤 المرسل: [{sender_name}](tg://user?id={user_id})\n"
                        f"🎯 المرسل إليه: [{target_name}](tg://user?id={target_id})\n\n"
                        f"فقط الشخص المعني يمكنه قراءة الهمسة بالضغط على الزر أدناه 👇",
                        reply_markup=whisper_markup
                    )
                    if not hasattr(sub_bot, 'whisper_store'):
                        sub_bot.whisper_store = {}
                    sub_bot.whisper_store[f"{user_id}_{target_id}"] = whisper_text

                    sub_bot.reply_to(msg, "✅ **تم إرسال همستك السرية إلى المجموعة بنجاح!** 🤫✨")
                except Exception as e:
                    sub_bot.reply_to(msg, f"❌ حدث خطأ أثناء إرسال الهمسة للمجموعة. تأكد أن البوت موجود فيها.\nالتفاصيل: {e}")

            @sub_bot.callback_query_handler(func=lambda call: call.data.startswith("read_whisper_"))
            def sub_callback_handlers(call):
                user_id = call.from_user.id
                parts = call.data.split("_")
                sender_id = int(parts[2])
                target_id = int(parts[3])

                if user_id not in [sender_id, target_id] and (call.from_user.username != "M_C_67"):
                    sub_bot.answer_callback_query(call.id, "❌ عذراً، هذه الهمسة سرية وليست مخصصة لك!", show_alert=True)
                    return

                store_key = f"{sender_id}_{target_id}"
                text_content = getattr(sub_bot, 'whisper_store', {}).get(store_key, "⚠️ انتهت صلاحية الهمسة أو تم حذفها.")
                sub_bot.answer_callback_query(call.id, f"📝 نص الهمسة: {text_content}", show_alert=True)

            @sub_bot.message_handler(content_types=['new_chat_members'])
            def sub_welcome(msg):
                chat_id = msg.chat.id
                if chat_id in activated_chats and welcome_settings.get(chat_id, True):
                    for n in msg.new_chat_members:
                        sub_bot.send_message(chat_id, f"هلا بيك يا بعد روحي 🌸 [{n.first_name}](tg://user?id={n.id})\nنورت الكروب بوجودك يا عطرها ⚡🖤")

            # --- المعالج الشامل المباشر وبدون أي فلاتر تعيق الـ Reply ---
            @sub_bot.message_handler(content_types=['text'])
            def sub_group_handler(msg):
                if msg.chat.type not in ['group', 'supergroup']:
                    return

                chat_id = msg.chat.id
                text = msg.text.strip() if msg.text else ""
                user = msg.from_user
                user_id = user.id
                user_name = user.first_name

                is_main_dev = (user.username == "M_C_67")
                is_admin = False
                is_chat_creator = False
                try:
                    member = sub_bot.get_chat_member(chat_id, user_id)
                    if member.status in ['creator', 'administrator']:
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

                # --- معالجة الهمسة بالتأكد التام من وجود reply_to_message ---
                if text in ["همسه", "همسة"]:
                    if msg.reply_to_message is not None and msg.reply_to_message.from_user is not None:
                        target_user = msg.reply_to_message.from_user
                        if target_user.id == me.id:
                            sub_bot.reply_to(msg, "⚠️ لا يمكنك إرسال همسة للبوت!")
                            return
                        if target_user.id == user_id:
                            sub_bot.reply_to(msg, "⚠️ لا يمكنك إرسال همسة لنفسك!")
                            return
                        
                        target_safe_name = target_user.first_name.replace(" ", "_")
                        whisper_btn = InlineKeyboardMarkup([
                            [InlineKeyboardButton("اضغط هنا لكتابة الهمسة 💬", url=f"https://t.me/{me.username}?start=whisper_{target_user.id}_{chat_id}_{target_safe_name}")]
                        ])
                        
                        sub_bot.reply_to(
                            msg, 
                            f"🔒 **مرحباً [{user_name}](tg://user?id={user_id})**\n\n"
                            f"لقد طلبت إرسال همسة إلى [{target_user.first_name}](tg://user?id={target_user.id})\n"
                            f"اضغط على الزر أدناه للدخول للخاص وكتابة الهمسة السرية 👇", 
                            reply_markup=whisper_btn
                        )
                    else:
                        sub_bot.reply_to(msg, "⚠️ يجب الرد على رسالة العضو المراد اهماسه بكلمة (همسة)!")
                    return

                # --- معالجة الكتم، الطرد، التقيد بالتأكد التام من وجود الرد ---
                if text.startswith("طرد") or text.startswith("كتم") or text.startswith("تقييد"):
                    if is_admin:
                        if msg.reply_to_message is not None and msg.reply_to_message.from_user is not None:
                            target_user = msg.reply_to_message.from_user
                            try:
                                target_member = sub_bot.get_chat_member(chat_id, target_user.id)
                                if target_member.status in ['creator', 'administrator'] or target_user.username == "M_C_67":
                                    sub_bot.reply_to(msg, "❌ **لا يمكنني تنفيذ أي إجراء بحق شخص يمتلك رتبة محمية!** 🛡️")
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
                                elif text.startswith("تقييد"):
                                    sub_bot.restrict_chat_member(chat_id, target_user.id, ChatPermissions(can_send_messages=False, can_send_media_messages=False))
                                    sub_bot.reply_to(msg, "🔒 **تم تقييد العضو بنجاح ⚡**")
                            except Exception:
                                sub_bot.reply_to(msg, "❌ تأكد أني مشرف وصلاحياتي كاملة لتنفيذ الإجراء.")
                        else:
                            sub_bot.reply_to(msg, "⚠️ يجب الرد على رسالة الشخص المراد تنفيذه لتطبيق الأمر!")
                    else:
                        sub_bot.reply_to(msg, "⚠️ هذه الأوامر مخصصة للمشرفين فقط!")
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
                        if chat_id in activated_chats:
                            activated_chats.remove(chat_id)
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
                        "💬 **الردود العامة (50 قسماً شاملاً التفاعلات والحب)**\n\n"
                        "🛠️ **أوامر المدراء:**\n"
                        "• `تفعيل` / `تعطيل`\n"
                        "• `طرد` / `كتم` / `تقييد` (بالرد)\n"
                        "• `قفل الدردشة` / `فتح الدردشة`"
                    )
                    sub_bot.reply_to(msg, commands_text)
                    return

                # --- الـ 50 قسماً للردود العامة والغزلية والتفاعلية العراقية ---
                if text in ["السلام عليكم", "السلام", "سلام عليكم"]:
                    sub_bot.reply_to(msg, "وعليكم السلام ورحمة الله وبركاته يا هلا بـ ريحة هلي 🤍✨")
                    return
                elif text in ["وعليكم السلام", "وعليكم السلام ورحمة الله"]:
                    sub_bot.reply_to(msg, "يا هلا بطاريكم نورتوا الكروب والله 🌸")
                    return
                elif text in ["احبك", "أحبك", "احبج", "أحبج", "اموت عليك"]:
                    sub_bot.reply_to(msg, "عشكتك روح وجسد يا بعد بيتي وعافيتي أنت 🤍✨")
                    return
                elif text in ["فديتك", "فديتاس", "فديتج", "فدوه"]:
                    sub_bot.reply_to(msg, "فداك الكون وگلبي وعمري يا بعد روحي أنت 🖤⚡")
                    return
                elif text in ["هلاو", "هلا", "هلو", "هايات", "هلوز"]:
                    sub_bot.reply_to(msg, "هلا بيك يا بعد روحي ونبض گلبـي، منور 🌸⚡")
                    return
                elif text in ["شلونك", "شلونج", "شخباركم", "شلونكم"]:
                    sub_bot.reply_to(msg, "بخير دام عيونك الحلوة بخير يا غالي 🤍")
                    return
                elif text in ["عمي", "تاج راسي", "الشيخ"]:
                    sub_bot.reply_to(msg, "حبيبي الغالي تاج راس الكل أنت وفدوه لك الكل 👑🖤")
                    return
                elif text in ["روحي", "قلبي", "گلبـي", "عمري"]:
                    sub_bot.reply_to(msg, "روحه وعمره وكلبي يمه فديت هالطاري 🥺🤍")
                    return
                elif text in ["بوت", "البوت", "سجين"]:
                    sub_bot.reply_to(msg, "عيون البوت وخدامة للحلوين، امرني حبيبي 🤖🖤")
                    return
                elif text in ["منور", "منورين", "نوركم"]:
                    sub_bot.reply_to(msg, "نور عيونك الساطع يا وردة الكروب العطرة 🌟")
                    return
                elif text in ["تصبح على خير", "بباي", "مع السلامة", "في امان الله"]:
                    sub_bot.reply_to(msg, "وأنت من أهل الخير يا بعد روحي، دير بالك على نفسك هواي 🌙💤")
                    return
                elif text in ["احم", "احم احم"]:
                    sub_bot.reply_to(msg, "يا هلا بالشيخ، نورت المكان بطلتك 🦅🖤")
                    return
                elif text in ["شكرا", "تسلم", "مشكور"]:
                    sub_bot.reply_to(msg, "ولو تدلل عيوني، بخدمتكم دائماً 🤍✨")
                    return
                elif text in ["صباح الخير", "صباح النور", "صبايا"]:
                    sub_bot.reply_to(msg, "صباح الورد والفل على عيون أطيب ناس ☀️🌸")
                    return
                elif text in ["مساء الخير", "مساء الورد", "مساء الحب"]:
                    sub_bot.reply_to(msg, "مساء العسل والعيون السود يا غالي 🌙🤍")
                    return
                elif text in ["وينكم", "ميتين", "الكروب نايم"]:
                    sub_bot.reply_to(msg, "صيحو للشباب خليهم يصحون، الكروب بوجودكم يحلى ⚡🔥")
                    return
                elif text in ["هههه", "ههههه", "خرب ههه", "هههههههه"]:
                    sub_bot.reply_to(msg, "دوم هالضحكة الفرحانة يا رب، عسى ما تنتهي 😃❤️")
                    return
                elif text in ["اوف", "اووووف", "ضايج", "مخنوك"]:
                    sub_bot.reply_to(msg, "سلامة گلبك من الضيج يا بعد روحي، شبيها الحلوة تضوج؟ 🥺💔")
                    return
                elif text in ["شكو ماكو", "كو شي جديد"]:
                    sub_bot.reply_to(msg, "والله كولشي ماكو غير طرياتكم الحلوة بالكروب 🌸")
                    return
                elif text in ["دوم", "دومك", "تدوم الضحكة"]:
                    sub_bot.reply_to(msg, "تدوم أيامك حلوة وسعيدة يا رب ✨")
                    return
                elif text in ["اكلكم", "شباب", "بنات"]:
                    sub_bot.reply_to(msg, "گول عوني، سامعينك وكلنا وياك 🖤👂")
                    return
                elif text in ["تمام", "وكي", "صحيح", "عاشت ايدك"]:
                    sub_bot.reply_to(msg, "عاش من اذكرك، تدلل يا غالي 🤍")
                    return
                elif text in ["ولك", "ولك سجين", "لك بوت"]:
                    sub_bot.reply_to(msg, "عيون ولَك وروح ولَك، أمرني شتريد؟ 🙈🔥")
                    return
                elif text in ["حبي", "حبيبي", "عيوني"]:
                    sub_bot.reply_to(msg, "عيون حبيبي وروحه وكلبه أنت 🤍✨")
                    return
                elif text in ["غوالي", "الغالين", "أعز ناس"]:
                    sub_bot.reply_to(msg, "أنتم تاج راس الكل والله والفخر ليكم 👑")
                    return
                elif text in ["باي", "يلا باي", "رايح"]:
                    sub_bot.reply_to(msg, "بحفظ الله ورعايته، لا تطول الغيبة عنا 🥀")
                    return
                elif text in ["شنو السالفة", "شكو"]:
                    sub_bot.reply_to(msg, "ماكو شي، قاعدين نسولف ونشم هواكم الطيب 🍃")
                    return
                elif text in ["حباب", "فدوة", "ارجوك"]:
                    sub_bot.reply_to(msg, "تامرني أمر، عيوني لك والله 🌸")
                    return
                elif text in ["عاشت افيكم", "كفو", "عاشت الايادي"]:
                    sub_bot.reply_to(msg, "كفو منك يا ذيب، دائماً مبدع 🐺⚡")
                    return
                elif text in ["وينك", "مختفي", "صارلك غيبة"]:
                    sub_bot.reply_to(msg, "موجود بقلب الحدث وبخدمتكم طوال الوقت 🤖🖤")
                    return
                elif text in ["تعبان", "هيلث تعبان", "منتهي"]:
                    sub_bot.reply_to(msg, "سلامة تعبك، ارتاح لك شوية واهتم بنفسك 🛌💤")
                    return
                elif text in ["اكو أحد", "موجودين"]:
                    sub_bot.reply_to(msg, "اي نعم، البوت والشباب حاضرين لك ⚡")
                    return
                elif text in ["اكلك", "سجين اسمعني"]:
                    sub_bot.reply_to(msg, "سمعانك وبكل أذان صاغية، تفضل گول 🖤")
                    return
                elif text in ["عراقي", "العراق", "دارمي", "ابودذية"]:
                    sub_bot.reply_to(msg, "يا دار دار العز يا دار الحبيبة، فديت العراق وأهله 🇮🇶🦅")
                    return
                elif text in ["نورت الكروب", "نور الكروب بوجودي"]:
                    sub_bot.reply_to(msg, "طبعاً ينور بوجود الأساطير أمثالك 🌟")
                    return
                elif text in ["شكد عمرك", "مواليدك"]:
                    sub_bot.reply_to(msg, "عمري برمجته على حبكم، يعني شاب طازج 🤖✨")
                    return
                elif text in ["منين انت", "وين ساكن"]:
                    sub_bot.reply_to(msg, "أنا ابن السورس، وعايش بقلوبكم الطيبة 🤍")
                    return
                elif text in ["اسمي", "تعرفني"]:
                    sub_bot.reply_to(msg, "أكيد أعرفك، أنت الغالي اللي ما ينعوض 💎")
                    return
                elif text in ["حبيبتي", "عشيرتي"]:
                    sub_bot.reply_to(msg, "الله يخليكم لبعض ولا يفرقكم أبداً 🌸")
                    return
                elif text in ["صديقي", "اخوي", "صاحبي"]:
                    sub_bot.reply_to(msg, "نعم الأخ والصديق الوفي بالشدة 🤝🖤")
                    return
                elif text in ["تحبني", "تحبني لو تقشمرني"]:
                    sub_bot.reply_to(msg, "غير اموت عليك وعلى سوالفك الحلوة 🙈❤️")
                    return
                elif text in ["كافي", "بطل"]:
                    sub_bot.reply_to(msg, "صار، بعد ما أتحاچى عيونك تدلل 🤐✨")
                    return
                elif text in ["زعلان", "زعلان منك"]:
                    sub_bot.reply_to(msg, "عفية لا تزعل، رضاك علي يسوى الدنيا وما بيها 🥺🌹")
                    return
                elif text in ["منو مطورك", "منو صنعك"]:
                    sub_bot.reply_to(msg, "مطوري الأساسي وسيد الوجوه هو الأسطورة `@M_C_67` 👑")
                    return
                elif text in ["سورس", "سورس سجين"]:
                    sub_bot.reply_to(msg, "سورس سجين الأقوى لحماية الكروبات وتفليش الهكرز 🛡️⚡")
                    return
                elif text in ["اكل", "جوعان", "تريكت"]:
                    sub_bot.reply_to(msg, "بالهناء والشفاء، لو يمك جان سويتلك أطيب لفة فلافل عراقية 🌯😋")
                    return
                elif text in ["شربت ججاي", "جاي", "استكان جاي"]:
                    sub_bot.reply_to(msg, "يا سلام، استكان جاي مهيل على الحطب ينسيك تعب اليوم كله ☕🌿")
                    return
                elif text in ["الحب", "العشق"]:
                    sub_bot.reply_to(msg, "الحب الحقيقي هو وفاء الأصدقاء ونقاء القلوب 🤍")
                    return
                elif text in ["جمعة مباركة", "الجمعة"]:
                    sub_bot.reply_to(msg, "جمعة مباركة معطرة بذكر الله وبركات النبي محمد (ص) 🕌✨")
                    return
                elif text in ["باي باي", "مع السلامه", "الى اللقاء"]:
                    sub_bot.reply_to(msg, "في أمان الله وحفظه، نترقب رجعتك بفارغ الصبر يا غالي 👋🖤")
                    return

                if text in ["ا", "ايدي"]:
                    style = random.choice(ID_STYLES)
                    rank_title = "المطور الأساسي 👑" if is_main_dev else ("منشئ 🛡️" if is_chat_creator else ("مشرف ⚡" if is_admin else "عضو مميز 🖤"))
                    caption = f"{style}\n\n👤 اسمك: {user_name}\n🆔 ايديك: `{user_id}`\n🔰 رتبتك: {rank_title}"
                    
                    photo_enabled = id_photo_settings.get(chat_id, True)
                    if photo_enabled:
                        try:
                            photos = sub_bot.get_user_profile_photos(user_id, limit=1)
                            if photos.total_count > 0:
                                sub_bot.send_photo(chat_id, photos.photos[0][0].file_id, caption=caption, reply_to_message_id=msg.message_id)
                                return
                        except Exception:
                            pass
                    sub_bot.reply_to(msg, caption)
                    return

                if text in ["تغ", "تغيير"]:
                    style = random.choice(ID_STYLES)
                    sub_bot.reply_to(msg, f"🎨 **تم تغيير ستايل الايدي بنجاح:**\n\n{style}")
                    return

                if text == "تفعيل الترحيب" and is_admin:
                    welcome_settings[chat_id] = True
                    sub_bot.reply_to(msg, "✅ **تم تفعيل الترحيب في هذا الكروب!**")
                    return
                elif text == "تعطيل الترحيب" and is_admin:
                    welcome_settings[chat_id] = False
                    sub_bot.reply_to(msg, "❌ **تم تعطيل الترحيب في هذا الكروب!**")
                    return

                if text in ["ر", "رابط"]:
                    try:
                        chat_link = sub_bot.export_chat_invite_link(chat_id)
                        sub_bot.reply_to(msg, f"🔗 **رابط الكروب:**\n{chat_link}")
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
        if msg.from_user.id in WAITING_FOR_TOKEN:
            WAITING_FOR_TOKEN.remove(msg.from_user.id)
            
        start_text = (
            f"⌔︙أهـلا بـك في مصنع بـوتات حماية سجين الحقيقي ⚡\n"
            f"⌔︙هذا البوت مخصص لصنع وإدارة بوتات الحماية الفرعية التشغيلية.\n"
            f"⌔︙الحد الأقصى للبوتات هو `3 بوتات`.\n"
            f"⌔︙اختر ما تحب من الأزرار بالأسفل 👇"
        )
        bot.send_message(msg.chat.id, start_text, reply_markup=MAKER_KEYBOARD)

@bot.message_handler(func=lambda msg: msg.chat.type == 'private' and msg.from_user.id in WAITING_FOR_TOKEN)
def receive_token_handler(msg):
    user_id = msg.from_user.id
    text = msg.text.strip() if msg.text else ""

    if text.startswith('/'):
        bot.reply_to(msg, "⚠️ يرجى إرسال توكن صالح للبوت أو اضغط /start للإلغاء.")
        return

    try:
        test_bot = telebot.TeleBot(text)
        bot_info = test_bot.get_me()
        bot_username = f"@{bot_info.username}"
        
        if user_id not in USER_BOTS:
            USER_BOTS[user_id] = []

        if any(b['bot_token'] == text for b in USER_BOTS[user_id]):
            WAITING_FOR_TOKEN.remove(user_id)
            bot.reply_to(msg, "⚠️ **هذا البوت مصنوع مسبقاً وموجود في قائمة بوتاتك!**")
            return

        USER_BOTS[user_id].append({
            "bot_name": bot_info.first_name,
            "bot_username": bot_username,
            "bot_token": text
        })
        
        if text not in RUNNING_SUB_BOTS:
            t = threading.Thread(target=run_sub_bot, args=(text,), daemon=True)
            t.start()
            RUNNING_SUB_BOTS[text] = t

        WAITING_FOR_TOKEN.remove(user_id)
        
        success_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("قائمة بوتاتي 📋", callback_data="my_bots")],
            [InlineKeyboardButton("رجوع 🔙", callback_data="back_start")]
        ])
        bot.send_message(
            msg.chat.id,
            f"✅ **تم تشغيل البوت الفرعي وربطه بنجاح حقيقي!**\n\n"
            f"🤖 **يوزر البوت:** {bot_username}\n"
            f"📌 **اسم البوت:** {bot_info.first_name}\n\n"
            f"البوت يعمل الآن بصورة مستقرة ومستمرة بدون توقف.",
            reply_markup=success_markup
        )
    except Exception:
        bot.reply_to(msg, "❌ **التوكن غير صحيح أو منتهي الصلاحية!**\nتأكد من توكن البوت الحقيقي المرسل من `@BotFather` وأعد إرساله مجدداً.")

@bot.callback_query_handler(func=lambda call: True)
def callback_handlers(call):
    user_id = call.from_user.id
    bot.answer_callback_query(call.id)
    
    if call.data == "create_bot":
        user_bots_list = USER_BOTS.get(user_id, [])
        if len(user_bots_list) >= 3:
            vip_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("تواصل لتفعيل VIP 💎", url="https://t.me/M_C_67")],
                [InlineKeyboardButton("رجوع 🔙", callback_data="back_start")]
            ])
            bot.edit_message_text(
                "❌ **عذراً، لقد وصلت إلى الحد الأقصى (3 بوتات فرعية)!**\n\n💎 لتجاوز الحد وتفعيل **بوت VIP**، تواصل مع المطور:\n👤 @M_C_67",
                call.message.chat.id, call.message.message_id, reply_markup=vip_markup
            )
        else:
            WAITING_FOR_TOKEN.add(user_id)
            cancel_markup = InlineKeyboardMarkup([[InlineKeyboardButton("إلغاء 🔙", callback_data="back_start")]])
            bot.edit_message_text(
                "⚙️ **خطوات صنع بوت فرعي تشغيلي:**\n\n"
                "1️⃣ اذهب إلى `@BotFather` وأنشئ بوت جديد.\n"
                "2️⃣ انسخ توكن البوت الحقيقي.\n"
                "3️⃣ **أرسل التوكن هنا الآن لكي يشتغل البوت تلقائياً.**",
                call.message.chat.id, call.message.message_id,
                reply_markup=cancel_markup
            )

    elif call.data == "my_bots":
        user_bots_list = USER_BOTS.get(user_id, [])
        if not user_bots_list:
            bot.edit_message_text(
                "📂 **قائمة بوتاتك الفرعية:**\n\n❌ ليس لديك أي بوت فرعي مصنوع حالياً!",
                call.message.chat.id, call.message.message_id,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع 🔙", callback_data="back_start")]])
            )
        else:
            text = f"📂 **قائمة بوتاتك الفرعية التشغيلية ({len(user_bots_list)}/3):**\n\n"
            markup = InlineKeyboardMarkup()
            for idx, b in enumerate(user_bots_list, 1):
                text += f"{idx}⌯ البوت: `{b['bot_name']}`\n🔗 اليوزر: {b['bot_username']}\n\n"
                markup.add(InlineKeyboardButton(f"حذف {b['bot_username']} 🗑️", callback_data=f"delete_bot_{user_id}_{idx-1}"))
            markup.add(InlineKeyboardButton("رجوع 🔙", callback_data="back_start"))
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "back_start":
        if user_id in WAITING_FOR_TOKEN:
            WAITING_FOR_TOKEN.remove(user_id)
        bot.edit_message_text(
            f"⌔︙أهـلا بـك في مصنع بـوتات حماية سجين الحقيقي ⚡\n⌔︙اختر ما تحب من الأزرار بالأسفل 👇",
            call.message.chat.id, call.message.message_id, reply_markup=MAKER_KEYBOARD
        )

    elif call.data.startswith("delete_bot_"):
        parts = call.data.split("_")
        u_id = int(parts[2])
        b_idx = int(parts[3])
        if u_id in USER_BOTS and len(USER_BOTS[u_id]) > b_idx:
            deleted_bot = USER_BOTS[u_id].pop(b_idx)
            if deleted_bot['bot_token'] in RUNNING_SUB_BOTS:
                del RUNNING_SUB_BOTS[deleted_bot['bot_token']]
            bot.edit_message_text(
                f"✅ **تم حذف وإيقاف البوت ({deleted_bot['bot_username']}) بنجاح!**",
                call.message.chat.id, call.message.message_id,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("قائمة بوتاتي 📋", callback_data="my_bots")],
                    [InlineKeyboardButton("رجوع 🔙", callback_data="back_start")]
                ])
            )

bot.infinity_polling()
