import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import config
import os

updater = Updater(token=config.get_token(), use_context=True)

dispatcher = updater.dispatcher

admins = list(map(int, config.get_chat_id().split(',')))


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='The Lord of Cinder welcomes you!')


def chat_id(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=update.message.chat_id)


def exec_command(update, context):
    stream = os.popen(update.message.text)
    output = stream.read()
    context.bot.send_message(chat_id=update.message.chat_id,
                             reply_to_message_id=update.message.message_id,
                             text=f'```{output}```',
                             parse_mode='markdown')


# Security response
def block(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=f'You have no power here! `{update.message.chat_id}`',
                             parse_mode='markdown')


# Security handler
# This handler MUST be first.
block_handler = MessageHandler(~ Filters.chat(admins), block)
dispatcher.add_handler(block_handler)

command_handler = MessageHandler(Filters.text, exec_command)
dispatcher.add_handler(command_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

chat_id_handler = CommandHandler('chatid', chat_id)
dispatcher.add_handler(chat_id_handler)


updater.start_polling()
updater.idle()
