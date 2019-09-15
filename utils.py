from base64 import b64encode, b64decode
from datetime import datetime
from telegram import Chat, User, Bot
from pprint import pprint
from config import log_chatid

def PrintChat(chat : Chat):
    return f"\"{chat.title}\" ({chat.id})"

def PrintUser(user : User):
    return f"\"{user.first_name} {user.last_name}\" @{user.username} ({user.id})"

def PrintUserOnly(user : User):
    joined_user_name = add_lrm(user.full_name)
    if len(joined_user_name) > 35: joined_user_name = joined_user_name[0:35]
    return joined_user_name

Chat.__str__ = PrintChat
User.__str__ = PrintUser
User.short = PrintUserOnly

def printts(to_print = "", timestamp = True, prettyprint = False, chat : Chat = None, bot : Bot = None):
    '''printts with timestamp.'''
    print_without_ts = False
    if (not timestamp): print_without_ts = True
    else:
        if isinstance(to_print, str):
            to_print = to_print.replace("\r", "\n")
            if to_print == "": print_without_ts = True
            elif (" " in to_print) and (len(set(to_print)) == 1): print_without_ts = True
            elif ("\n" in to_print) and (len(set(to_print)) == 1): print_without_ts = True
            else:
                num_eol = -1
                for character in to_print:
                    if character == '\n':
                        print("")
                        num_eol = num_eol + 1
                    else: break
                if num_eol != -1: to_print = to_print[num_eol+1:]
    prefix = ""
    if not print_without_ts: prefix = datetime.utcnow().strftime("[%Y-%m-%d %H:%M:%S] ")
    if chat != None: prefix += f"{chat} "
    print_func = pprint if prettyprint else print
    print_func(f"{prefix}{to_print}")
    if log_chatid != 0 and bot != None:
        print(log_chatid, bot.id)
        bot.sendMessage(log_chatid, to_print, disable_notification=True)

def is_int(s):
    '''Check if the string is an integer number'''
    try:
        int(s)
        return True
    except ValueError:
        return False


def add_lrm(str_to_modify):
    '''Add a Left to Right Mark (LRM) at provided string start'''
    barray = bytearray(b"\xe2\x80\x8e")
    str_to_modify = str_to_modify.encode("utf-8")
    for b in str_to_modify:
        barray.append(b)
    str_to_modify = barray.decode("utf-8")
    return str_to_modify

def encode(input : str):
    return b64encode(bytes(str(input), "utf-8")).decode("utf-8", "ignore")
def decode(input : str):
    return b64decode(input).decode("utf-8", "ignore")