from config import admins
from utils import printts


## Helper functions

def tlg_user_is_admin(bot, user_id, chat_id):
    '''Check if the specified user is an Administrator of a group given by IDs'''
    if user_id in admins: return True
    try:
        group_admins = bot.get_chat_administrators(chat_id)
    except:
        return None
    for admin in group_admins:
        if user_id == admin.user.id:
            return True
    return False


def tlg_delete_msg(bot, chat_id, msg_id):
    '''Try to remove a telegram message'''
    return_code = 0
    if msg_id is not None:
        try:
            bot.delete_message(chat_id, msg_id)
            return_code = 1
        except Exception as e:
            printts("[{}] {}".format(chat_id, str(e)))
            # Message is already deleted
            if str(e) == "Message to delete not found":
                return_code = -1
            # The bot has no privileges to delete messages
            elif str(e) == "Message can't be deleted":
                return_code = -2
    return return_code


def tlg_ban_user(bot, chat_id, user_id):
    '''Telegram Ban a user of an specified chat'''
    return_code = 0
    try:
        user_data = bot.getChatMember(chat_id, user_id)
        if (user_data['status'] != "left") and (user_data['status'] != "kicked"):
            bot.kickChatMember(chat_id, user_id)
            return_code = 1
        else:
            return_code = -1
    except Exception as e:
        printts("[{}] {}".format(chat_id, str(e)))
        if str(e) == "Not enough rights to restrict/unrestrict chat member":
            return_code = -2
        elif str(e) == "User is an administrator of the chat":
            return_code = -3
    return return_code


def tlg_kick_user(bot, chat_id, user_id):
    '''Telegram Kick (no ban) a user of an specified chat'''
    return_code = 0
    try:
        user_data = bot.getChatMember(chat_id, user_id)
        if (user_data['status'] != "left") and (user_data['status'] != "kicked"):
            bot.kickChatMember(chat_id, user_id)
            bot.unbanChatMember(chat_id, user_id)
            return_code = 1
        else:
            return_code = -1
    except Exception as e:
        printts("[{}] {}".format(chat_id, str(e)))
        if str(e) == "Not enough rights to restrict/unrestrict chat member":
            return_code = -2
        elif str(e) == "User is an administrator of the chat":
            return_code = -3
    return return_code


def tlg_check_chat_type(bot, chat_id_or_alias):
    '''Telegram check if a chat exists and what type it is (user, group, channel).'''
    chat_type = None
    # Check if it is a group or channel
    try:
        get_chat = bot.getChat(chat_id_or_alias)
        chat_type = getattr(get_chat, "type", None)
    except Exception as e:
        if str(e) != "Chat not found":
            printts("[{}] {}".format(chat_id_or_alias, str(e)))
    return chat_type
