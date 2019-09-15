from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from functions import tlg_user_is_admin
from utils import printts, encode, decode


def msg_new_user(bot, update):
    '''New member join the group event handler'''
    # Ignore if message comes from a channel
    msg = getattr(update, "message", None)
    if msg.chat.type == "channel": return
    for joined_user in update.message.new_chat_members:
        if bot.id == joined_user.id: return
        printts(" ")
        printts("New join detected: {}".format(joined_user), chat=msg.chat, bot=bot)
        if tlg_user_is_admin(bot, joined_user.id, update.message.chat_id):
            printts("User is an administrator. Skipping the captcha process.", chat=msg.chat, bot=bot)
            continue
        if joined_user.is_bot:
            printts("User is a Bot. Skipping the captcha process.", chat=msg.chat, bot=bot)
            continue
        bot.restrict_chat_member(msg.chat.id, joined_user.id, can_send_messages=False)
        btn_cb_text = f"ag.newusr:requestVerify[{encode(joined_user.id)}]"
        keyboard = [
            [
                InlineKeyboardButton(
                    "Click here to prove you're a human.",
                    callback_data=btn_cb_text
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        printts("Sending captcha message: {}".format(btn_cb_text), chat=msg.chat, bot=bot)
        msg_text = f"Welcome @{joined_user.username}.\nPlease click on the button below to talk here!"
        bot.send_message(chat_id=msg.chat.id, text=msg_text, reply_markup=reply_markup)


def button_verify_clicked(bot, update):
    '''Button pressed handler'''
    if not update.callback_query.data.startswith("ag.newusr:requestVerify["): return
    user_verify_id = update.callback_query.data.replace("ag.newusr:requestVerify[", "").replace("]", "")
    user_verify_id = int(decode(user_verify_id))
    member_clicked = bot.get_chat_member(update.callback_query.message.chat_id, update.callback_query.from_user.id)
    member_verify = bot.get_chat_member(update.callback_query.message.chat_id, user_verify_id)
    user_clicked_is_admin = tlg_user_is_admin(bot, update.callback_query.from_user.id,
                                              update.callback_query.message.chat_id)
    printts("{} started verification for {}".format(member_clicked.user, member_verify.user),
            chat=update.callback_query.message.chat, bot=bot)
    if user_clicked_is_admin:
        update.callback_query.answer(f"{member_verify.user} can now chat in {update.callback_query.message.chat}",
                                     alert=True)
    elif user_verify_id != update.callback_query.from_user.id:
        update.callback_query.answer("This verification was not meant for you!", alert=True)
        return
    elif member_verify.can_send_messages:
        return
    bot.restrict_chat_member(update.callback_query.message.chat.id, user_verify_id, can_send_messages=True)
    update.callback_query.message.delete()
    printts("Finished verification of {}".format(member_verify.user), chat=update.callback_query.message.chat, bot=bot)
    update.callback_query.answer(f"You can now chat in {update.callback_query.message.chat.title}", alert=True)
