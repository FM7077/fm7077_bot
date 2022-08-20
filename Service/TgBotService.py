from Instruction.TgBot import TgBot
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler)
from Instruction.Singlton import Singleton
import logging
from .CaiyunService import CaiyunService

@Singleton
class TgBotService():
    def __init__(self) -> None:
        self.tgBot = TgBot()
        bot = TgBot().get_bot()
        dispatcher = self.tgBot.get_dispatcher()
        dispatcher.add_handler(CommandHandler('start', self.start))
        dispatcher.add_handler(MessageHandler(Filters.location, self.location))

    def start(self, update, context):
        logging.info("Receive user start command %s" % (update))
        user = update.message.from_user
        update.message.reply_text('Hi %s nice to see you' % (user.first_name))

    def unknown(self, update, context):
        logging.info("Unknown command %s" % (update))

    def location(self, update, context):
        logging.info("Receive user location %s" % (update))
        user = update.message.from_user
        msg = update.message.reply_text('Hi %s, got your location, now I will check weather report for you' % (user.first_name))

        result = CaiyunService().check_by_location(update.message.location)
        msg.edit_text('Here is the weather for you:\ntemperature: %d \nhumidity: %d' % (result['temperature'], result['humidity']))
