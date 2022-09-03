from Instruction.TgBot import TgBot
from importlib.metadata import entry_points
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler)
from Model.Enum import Setting, TgCallBackType, TgCommand, Language as langE, LanguageList as ll
from Service.UserService import UserService
from Service.WeatherSubService import WeatherSubService
from Model.Language import LANG
from Model.Keyboard import Keyboards
from Model.PO import WeatherSub

CHOOSE_LOC, SET_NAME, CHOOSE_TIME_HOUR, CHOOSE_TIME_MINUTE, CONFIRM = range(5)

class NewWRSub():
    def __init__(self) -> None:
        pass
    
    def newSub(self, update, context):
        user = update.message.from_user
        u = UserService().getUserByTgID(user.id)
        userLang = u.Language
        lang = LANG(userLang)

        if WeatherSubService().isReachLimit(u.id):
            update.message.reply_text((lang.l(ll.SUB_WR_REACH_LIMIT) % (Setting.MaxSubLimit)))
            return ConversationHandler.END

        sub = WeatherSub()
        sub.IsSub = True
        sub.IsSubAlert = True
        context.user_data['sub_wr_data'] = sub

        update.message.reply_text(lang.l(ll.SUB_WR_CHO_LOC) % (lang.l(ll.SUB_WR_ACT_SUB)))
        return CHOOSE_LOC
    
    def updateSub(self, update, context):
        bot = TgBot().get_bot()
        user = update.callback_query.from_user
        userLang = UserService().getTgUserLang(user.id)
        lang = LANG(userLang)
        subid = update.callback_query.data.split(f"{TgCallBackType.SUB_WR_EDIT.value}_")[1]
        sub = WeatherSubService().getByID(subid)
        context.user_data['sub_wr_data'] = sub
        
        bot.edit_message_text(
            text=(lang.l(ll.SUB_WR_CHO_LOC) % (lang.l(ll.SUB_WR_ACT_UPDATE), f"*{sub.Name}*")),
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            parse_mode= 'Markdown'
        )
        return CHOOSE_LOC
    
    def chooseLoc(self, update, context):
        user = update.message.from_user
        userLang = UserService().getTgUserLang(user.id)
        lang = LANG(userLang)

        context.user_data['sub_wr_data'].Longitude = update.message.location.longitude
        context.user_data['sub_wr_data'].Latitude = update.message.location.latitude
        
        update.message.reply_text(lang.l(ll.SUB_WR_SET_NAME))
        return SET_NAME
    
    def setName(self, update, context):
        user = update.message.from_user
        userLang = UserService().getTgUserLang(user.id)
        lang = LANG(userLang)

        name = update.message.text
        if(not name or name.isspace()):
            update.message.reply_text(lang.l(ll.SUB_WR_EMP_NAME))
            return SET_NAME
        context.user_data['sub_wr_data'].Name = name
        
        replyMarkup = Keyboards().get24HKB()
        update.message.reply_text(lang.l(ll.SUB_WR_CHO_TIME_Hour), reply_markup=replyMarkup)
        return CHOOSE_TIME_HOUR
    
    def chooseTimeHour(self, update, context):
        bot = TgBot().get_bot()
        user = update.callback_query.from_user
        userLang = UserService().getTgUserLang(user.id)
        lang = LANG(userLang)

        hour = update.callback_query.data.split(f"{TgCallBackType.SUB_WR_SETH.value}_")[1]
        context.user_data['sub_wr_data'].ReportTime = hour
        
        replyMarkup = Keyboards().getCMin()
        bot.edit_message_text(
            text=(lang.l(ll.SUB_WR_CHO_TIME_MINUTE) % (hour)),
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            reply_markup=replyMarkup,
            parse_mode= 'Markdown'
        )
        bot.answer_callback_query(update.callback_query.id, text='')
        return CHOOSE_TIME_MINUTE

    def chooseTimeMinute(self, update, context):
        bot = TgBot().get_bot()
        user = update.callback_query.from_user
        userLang = UserService().getTgUserLang(user.id)
        lang = LANG(userLang)
        
        minute = update.callback_query.data.split(f"{TgCallBackType.SUB_WR_SETM.value}_")[1]
        context.user_data['sub_wr_data'].ReportTime += f":{minute}"

        replyMarkup = Keyboards().getSubWRKB(userLang)
        bot.edit_message_text(
            text=(lang.l(ll.SUB_WR_CHO_CONFIRM) % (context.user_data['sub_wr_data'].ReportTime)),
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            reply_markup=replyMarkup,
            parse_mode= 'Markdown'
        )
        bot.answer_callback_query(update.callback_query.id, text='')
        return CONFIRM

    def confirm(self, update, context):
        bot = TgBot().get_bot()
        user = update.callback_query.from_user
        user.lang = langE.ENG.name
        user.chatid = update.callback_query.message.chat_id
        u = UserService().getUserByTgID(user.id)
        userLang = u.Language
        lang = LANG(userLang)

        userId = UserService().upsertTgUser(user)
        subMsg = context.user_data['sub_wr_data']
        subMsg.UserID = userId

        if None != subMsg.id:
            WeatherSubService().update(subMsg)
        else:
            WeatherSubService().upsertByTgID(subMsg)
        name = subMsg.Name
        timeToShow = subMsg.ReportTime
        bot.edit_message_text(
            text = (lang.l(ll.SUB_WR_SET) % (name, timeToShow)),
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            parse_mode= 'Markdown'
        )
        return ConversationHandler.END

    def cancel(self, update, context):
        user = None
        rpl = None
        if(None != update.message):
            user = update.message.from_user
            rpl = update.message
            userLang = UserService().getTgUserLang(user.id)
            lang = LANG(userLang)

            update.message.reply_text(lang.l(ll.SUB_WR_CANCEL))
            
        if(None != update.callback_query):
            user = update.callback_query.from_user
            rpl = update.callback_query.message
            userLang = UserService().getTgUserLang(user.id)
            lang = LANG(userLang)
        
            bot = TgBot().get_bot()
            bot.edit_message_text(
                text = (lang.l(ll.SUB_WR_CANCEL)),
                chat_id=rpl.chat_id,
                message_id=rpl.message_id,
                parse_mode= 'Markdown'
            )

        return ConversationHandler.END
    
    def IsInvalidInput(self, update, context):
        user = update.message.from_user
        userLang = UserService().getTgUserLang(user.id)
        lang = LANG(userLang)

        update.message.reply_text(lang.l(ll.SUB_WR_UNKNOWN_MSG))
    
    def getHandler(self):
        handler = ConversationHandler(
            entry_points=[CommandHandler(TgCommand.SUBWEATHER.value, self.newSub), CallbackQueryHandler(self.updateSub, pattern=f"{TgCallBackType.SUB_WR_EDIT.value}")],
            states={
                CHOOSE_LOC: [MessageHandler(Filters.location & ~Filters.command, self.chooseLoc), MessageHandler(Filters.all & ~Filters.command, self.IsInvalidInput)],
                SET_NAME: [MessageHandler(Filters.text, self.setName), MessageHandler(Filters.all & ~Filters.command, self.IsInvalidInput)],
                CHOOSE_TIME_HOUR: [CallbackQueryHandler(self.chooseTimeHour, pattern=f"^{TgCallBackType.SUB_WR_SETH.value}_"), MessageHandler(Filters.all & ~Filters.command, self.IsInvalidInput)],
                CHOOSE_TIME_MINUTE: [CallbackQueryHandler(self.chooseTimeMinute, pattern=f"^{TgCallBackType.SUB_WR_SETM.value}_"), MessageHandler(Filters.all & ~Filters.command, self.IsInvalidInput)],
                CONFIRM: [CallbackQueryHandler(self.confirm, pattern=f"^{TgCallBackType.SUB_WR_CONFIRM.value}"), MessageHandler(Filters.all & ~Filters.command, self.IsInvalidInput)],
            },
            fallbacks=[CommandHandler(TgCommand.CANCEL.value, self.cancel), CallbackQueryHandler(self.cancel, pattern=f"^{TgCallBackType.SUB_WR_CANCEL.value}")],
            conversation_timeout=60
        )
        return handler