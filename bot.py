import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import config
import os

updater = Updater(token=config.get_token(), use_context=True)

dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="The Lord of Cinder welcomes you!")


def chat_id(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=update.message.chat_id)


def ls(update, context):
    stream = os.popen('dir')
    output = stream.read()
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=f"```{output}```",
                             parse_mode="markdown")


# Security response
def block(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=f"You have no power here! `{update.message.chat_id}`",
                             parse_mode="markdown")


# Security handler
block_handler = MessageHandler(~ Filters.chat(int(config.get_chat_id())), block)
dispatcher.add_handler(block_handler)

start_handler = CommandHandler('start', start)
chat_id_handler = CommandHandler('chatid', chat_id)
ls_handler = CommandHandler('ls', ls)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(chat_id_handler)
dispatcher.add_handler(ls_handler)

updater.start_polling()
updater.idle()
