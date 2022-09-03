import imp
from Instruction.TgBot import TgBot
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler)
from Instruction.Singleton import Singleton
import logging

from Service.WeatherSubService import WeatherSubService
from .CaiyunService import CaiyunService
from Model.Enum import Setting, TgCommand, skycon, TgCallBackType, LanguageList as ll
from pymongo import MongoClient
from sqlite_utils import Database
from Model.PO import User
from Model.Keyboard import Keyboards
from Service.UserService import UserService
from Model.Language import LANG
from Conversation.NewWeatherReportSub import NewWRSub
from Model.DTO import Location
from Model.Keyboard import Keyboards

@Singleton
class TgBotService():
    def __init__(self) -> None:
        self.tgBot = TgBot()
        bot = TgBot().get_bot()
        self.dispatcher = self.tgBot.get_dispatcher()
        self.dispatcher.add_handler(CommandHandler(TgCommand.START.value, self.start))
        self.dispatcher.add_handler(CommandHandler(TgCommand.CHECKRAIN.value, self.checkRain))
        self.dispatcher.add_handler(CommandHandler(TgCommand.MYSUBS.value, self.listsubs))
        self.dispatcher.add_handler(NewWRSub().getHandler())

        self.dispatcher.add_handler(MessageHandler(Filters.location, self.location))
        self.dispatcher.add_handler(MessageHandler(Filters.animation, self.recvSticker))
        self.dispatcher.add_handler(MessageHandler(Filters.document, self.recvSticker))

        self.dispatcher.add_handler(CallbackQueryHandler(self.moreWeatherDetail, pattern=f"^{TgCallBackType.OPT_WR_START.value}"))

        self.dispatcher.add_handler(CallbackQueryHandler(self.listsubs, pattern=f"{TgCallBackType.LIST_SUBS.value}"))
        self.dispatcher.add_handler(CallbackQueryHandler(self.managesub, pattern=f"^{TgCallBackType.SUB_WR_DETAIL.value}"))
        self.dispatcher.add_handler(CallbackQueryHandler(self.delsub, pattern=f"(^{TgCallBackType.SUB_WR_DELETE.value})|(^{TgCallBackType.SUB_WR_DEL_CONFIRM.value})"))
        self.dispatcher.add_handler(CallbackQueryHandler(self.managesub, pattern=f"^{TgCallBackType.SUB_WR_DEL_CANCEL.value}"))

    def start(self, update, context):
        logging.info("Receive user start command %s" % (update))
        user = update.message.from_user
        userLang = UserService().getTgUserLang(user.id)
        lang = LANG(userLang)
        update.message.reply_text(lang.l(ll.WELCOME) % (user.first_name))

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
        # replyMarkup = WRKeyboard(loc, lang).get()
        msg.edit_text(resultMsg)

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

    def listsubs(self, update, context):
        if(None != update.message):
            user = update.message.from_user
            u = UserService().getUserByTgID(user.id)
            userLang = u.Language
            lang = LANG(userLang)
            if(None == u.id):
                update.message.reply_text(lang.l(ll.NO_SUB))
                return
            
            subButtons = Keyboards().getSubsKB(u)
            if(len(subButtons["inline_keyboard"]) < 1):
                update.message.reply_text(lang.l(ll.NO_SUB))
                return
            
            update.message.reply_text(lang.l(ll.HAS_SUBS), reply_markup=subButtons)
        
        if(None != update.callback_query):
            rpl = update.callback_query.message
            user = update.callback_query.from_user
            u = UserService().getUserByTgID(user.id)
            userLang = u.Language
            lang = LANG(userLang)
            if(None == u.id):
                bot.edit_message_text(
                    text = (lang.l(ll.NO_SUB)),
                    chat_id=rpl.chat_id,
                    message_id=rpl.message_id,
                    parse_mode= 'Markdown'
                )
                return
            
            subButtons = Keyboards().getSubsKB(u)
            if(len(subButtons["inline_keyboard"]) < 1):
                bot.edit_message_text(
                    text = (lang.l(ll.NO_SUB)),
                    chat_id=rpl.chat_id,
                    message_id=rpl.message_id,
                    parse_mode= 'Markdown'
                )
                return
        
            bot = TgBot().get_bot()
            bot.edit_message_text(
                text = (lang.l(ll.HAS_SUBS)),
                chat_id=rpl.chat_id,
                message_id=rpl.message_id,
                reply_markup=subButtons,
                parse_mode= 'Markdown'
            )

    def managesub(self, update, context):
        query = update.callback_query
        rpl = query.message
        user = update.callback_query.from_user
        u = UserService().getUserByTgID(user.id)
        userLang = u.Language
        lang = LANG(userLang)
        bot = TgBot().get_bot()
        subid = query.data.split('_')[2]
        sub = WeatherSubService().getByID(subid)
        if(None == sub.id):
            subButtons = Keyboards().getSubsKB(u)
            if(len(subButtons["inline_keyboard"]) < 1):
                bot.edit_message_text(
                    text = (lang.l(ll.NO_SUB)),
                    chat_id=rpl.chat_id,
                    message_id=rpl.message_id,
                    parse_mode= 'Markdown'
                )
                return
            bot.edit_message_text(
                text = (lang.l(ll.HAS_SUBS)),
                chat_id=rpl.chat_id,
                message_id=rpl.message_id,
                reply_markup=subButtons,
                parse_mode= 'Markdown'
            )
            return
        bot.edit_message_text(
            text = (lang.l(ll.SUB_DETAIL) % (sub.Name, sub.Longitude, sub.Latitude, sub.IsSub, sub.ReportTime, sub.IsSubAlert)),
            chat_id=rpl.chat_id,
            message_id=rpl.message_id,
            reply_markup=Keyboards().getSubManKB(userLang, subid),
            parse_mode= 'Markdown'
        )

    def delsub(self, update, context):
        query = update.callback_query
        rpl = query.message
        user = update.callback_query.from_user
        u = UserService().getUserByTgID(user.id)
        userLang = u.Language
        lang = LANG(userLang)
        bot = TgBot().get_bot()
        subid = query.data.split('_')[2]
        
        if(TgCallBackType.SUB_WR_DEL_CONFIRM.value in query.data):
            WeatherSubService().delByID(subid)

            subButtons = Keyboards().getSubsKB(u)
            if(len(subButtons["inline_keyboard"]) < 1):
                bot.edit_message_text(
                    text = (lang.l(ll.NO_SUB)),
                    chat_id=rpl.chat_id,
                    message_id=rpl.message_id,
                    parse_mode= 'Markdown'
                )
                return
        
            bot = TgBot().get_bot()
            bot.edit_message_text(
                text = (lang.l(ll.HAS_SUBS)),
                chat_id=rpl.chat_id,
                message_id=rpl.message_id,
                reply_markup=subButtons,
                parse_mode= 'Markdown'
            )
            return
        
        bot.edit_message_text(
            text = (lang.l(ll.DEL_SUB)),
            chat_id=rpl.chat_id,
            message_id=rpl.message_id,
            reply_markup=Keyboards().getDelSubKB(userLang, subid),
            parse_mode= 'Markdown'
        )