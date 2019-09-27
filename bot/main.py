from telegram.ext import Updater, CommandHandler
import logging

from settings import token

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='🏸🏸🏸')

def main():
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()
    print('[log]: started.')

if __name__ == '__main__':
    main()
