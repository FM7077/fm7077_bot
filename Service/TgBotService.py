from Instruction.TgBot import TgBot
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler)
from Instruction.Singlton import Singleton
import logging
from .CaiyunService import CaiyunService
from Model.Enum import Setting, skycon, TgCallBackType
from pymongo import MongoClient
from sqlite_utils import Database
from Model.PO import User
from Model.Keyboard import WRKeyboard

@Singleton
class TgBotService():
    def __init__(self) -> None:
        self.tgBot = TgBot()
        bot = TgBot().get_bot()
        dispatcher = self.tgBot.get_dispatcher()
        dispatcher.add_handler(CommandHandler('start', self.start))
        dispatcher.add_handler(CommandHandler('checkRain', self.checkRain))
        dispatcher.add_handler(CommandHandler('subWeather', self.checkRain))

        dispatcher.add_handler(MessageHandler(Filters.location, self.location))
        dispatcher.add_handler(MessageHandler(Filters.animation, self.recvSticker))
        dispatcher.add_handler(MessageHandler(Filters.document, self.recvSticker))

        dispatcher.add_handler(CallbackQueryHandler(self.moreWeatherDetail, pattern=f"^{TgCallBackType.OPT_WR_START.value}"))

    def start(self, update, context):
        self.upsertUser(update.message.from_user)
        logging.info("Receive user start command %s" % (update))
        user = update.message.from_user
        update.message.reply_text('Hi %s nice to see you' % (user.first_name))

    def location(self, update, context):
        self.upsertUser(update.message.from_user)
        logging.info("Receive user location %s" % (update))
        user = update.message.from_user
        msg = update.message.reply_text('Hi %s, got your location, now I will check weather report for you' % (user.first_name))

        cy = CaiyunService()
        location = update.message.location
        result = cy.check_by_location(update.message.location)
        resultMsg = cy.getReportMsg(result)

        messageId = update.message.message_id
        loc = str([location.latitude, location.longitude])
        replyMarkup = WRKeyboard(loc).get()
        msg.edit_text(resultMsg, reply_markup=replyMarkup)
    def moreWeatherDetail(self, update, context):
        print(update)
        pass

    def unknown(self, update, context):
        logging.info("Unknown command %s" % (update)) 

    def checkRain(self, update, context):
        self.upsertUser(update.message.from_user)
        update.message.reply_text('This function is not yet finish')
        pass

    def recvSticker(self, update, context):
        self.upsertUser(update.message.from_user)
        with open(f"custom/{update.message.document.file_name}", 'wb') as f:
            context.bot.get_file(update.message.document).download(out=f)
        print(update)

    def upsertUser(self, user):
        db = Database(Setting.DBName.value)
        table = db[Setting.DBTableUser.value]
        u = User()
        u.TgFirstName = user.first_name
        u.TgID = user.id
        u.TgName = user.username
        udict = u.__dict__
        del udict["id"]
        if(len(table.columns) == 0): # what the fuck is this feature, sqlite?
            table.insert(udict, hash_id="id")
        else:
            oldUser = list(table.rows_where(f"TgID = {user.id}"))
            if(len(oldUser) == 0):
                table.insert(udict, hash_id="id")
            else:
                udict = {k: v for k, v in udict.items() if v}
                table.update(oldUser[0]["id"], udict)

    def subWeather(self, update, context):
        pass