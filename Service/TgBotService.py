from Instruction.TgBot import TgBot
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler)
from Instruction.Singleton import Singleton
import logging
from .CaiyunService import CaiyunService
from Model.Enum import Setting, TgCommand, skycon, TgCallBackType, LanguageList as ll
from pymongo import MongoClient
from sqlite_utils import Database
from Model.PO import User
from Model.Keyboard import WRKeyboard
from Service.UserService import UserService
from Model.Language import LANG
from Conversation.NewWeatherReportSub import NewWRSub
from Model.DTO import Location

@Singleton
class TgBotService():
    def __init__(self) -> None:
        self.tgBot = TgBot()
        bot = TgBot().get_bot()
        self.dispatcher = self.tgBot.get_dispatcher()
        self.dispatcher.add_handler(CommandHandler(TgCommand.START.value, self.start))
        self.dispatcher.add_handler(CommandHandler(TgCommand.CHECKRAIN.value, self.checkRain))
        self.dispatcher.add_handler(NewWRSub().getHandler())

        self.dispatcher.add_handler(MessageHandler(Filters.location, self.location))
        self.dispatcher.add_handler(MessageHandler(Filters.animation, self.recvSticker))
        self.dispatcher.add_handler(MessageHandler(Filters.document, self.recvSticker))

        self.dispatcher.add_handler(CallbackQueryHandler(self.moreWeatherDetail, pattern=f"^{TgCallBackType.OPT_WR_START.value}"))

    def start(self, update, context):
        self.upsertUser(update.message.from_user)
        logging.info("Receive user start command %s" % (update))
        user = update.message.from_user
        update.message.reply_text('Hi %s nice to see you' % (user.first_name))

    def location(self, update, context):
        logging.info("Receive user location %s" % (update))
        user = update.message.from_user
        userLang = UserService().getTgUserLang(user.id)
        lang = LANG(userLang)
        msg = update.message.reply_text(lang.l(ll.MSG_GOT_LOC) % (user.first_name))

        cy = CaiyunService()
        location = update.message.location
        loc = Location(location.longitude, location.latitude)
        result = cy.check_by_location(loc)
        resultMsg = cy.getReportMsg(result, userLang)

        messageId = update.message.message_id
        loc = str([loc.latitude, loc.longitude])
        replyMarkup = WRKeyboard(loc, lang).get()
        msg.edit_text(resultMsg, reply_markup=replyMarkup)

    def moreWeatherDetail(self, update, context):
        print(update)
        pass

    def unknown(self, update, context):
        logging.info("Unknown command %s" % (update)) 

    def checkRain(self, update, context):
        update.message.reply_text('This function is not yet done')
        pass

    def recvSticker(self, update, context):
        with open(f"custom/{update.message.document.file_name}", 'wb') as f:
            context.bot.get_file(update.message.document).download(out=f)
        print(update)