import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import config
from utils import printts
from events import *
from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler


def main():
    '''Main Function'''
    printts("Bot starting...")
    updater = Updater(config.token, use_context=False)
    updater.dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, msg_new_user))
    updater.dispatcher.add_handler(CallbackQueryHandler(button_verify_clicked))
    updater.start_polling(clean=True, allowed_updates=[])
    printts("Bot started.", bot=updater.bot)


if __name__ == "__main__":
    main()
