from Instruction.TgBot import TgBot
from importlib.metadata import entry_points
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler)
from Model.Enum import TgCallBackType, TgCommand, Language as langE, LanguageList as ll
from Service.UserService import UserService
from Model.Language import LANG
from Model.Keyboard import Keyboard_CMin, Keyboard_Hour, Keyboard_SubWR_Confirm
from Model.DTO import SubWeatherReport

CHOOSE_LOC, CHOOSE_TIME_HOUR, CHOOSE_TIME_MINUTE, CONFIRM = range(4)

class NewWRSub():
    def __init__(self) -> None:
        pass
    
    def newSub(self, update, context):
        user = update.message.from_user
        userLang = UserService().getTgUserLang(user.id)
        lang = LANG(userLang)

        sub = SubWeatherReport()
        sub.TgID = user.id
        context.user_data['sub_wr_data'] = sub

        update.message.reply_text(lang.l(ll.SUB_WR_CHO_LOC))
        return CHOOSE_LOC
    
    def chooseLoc(self, update, context):
        user = update.message.from_user
        userLang = UserService().getTgUserLang(user.id)
        lang = LANG(userLang)

        context.user_data['sub_wr_data'].Location = update.message.location
        
        replyMarkup = Keyboard_Hour().get()
        update.message.reply_text(lang.l(ll.SUB_WR_CHO_TIME_Hour), reply_markup=replyMarkup)
        return CHOOSE_TIME_HOUR
    
    def chooseTimeHour(self, update, context):
        bot = TgBot().get_bot()
        user = update.callback_query.from_user
        userLang = UserService().getTgUserLang(user.id)
        lang = LANG(userLang)

        hour = update.callback_query.data.split(f"{TgCallBackType.SUB_WR_SETH.value}_")[1]
        context.user_data['sub_wr_data'].TimeHour = hour
        
        replyMarkup = Keyboard_CMin().get()
        hourToShow = str(hour).zfill(2)
        bot.edit_message_text(
            text=(lang.l(ll.SUB_WR_CHO_TIME_MINUTE) % (hourToShow)),
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
        context.user_data['sub_wr_data'].TimeMinute = minute

        replyMarkup = Keyboard_SubWR_Confirm(userLang).get()
        hourToShow = str(context.user_data['sub_wr_data'].TimeHour).zfill(2)
        minuteToShow = str(minute).zfill(2)
        timeToShow = f"{hourToShow} : {minuteToShow}"
        bot.edit_message_text(
            text=(lang.l(ll.SUB_WR_CHO_CONFIRM) % (timeToShow)),
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
        userLang = UserService().getTgUserLang(user.id)
        lang = LANG(userLang)

        UserService().upsertTgUser(user)

        hourToShow = str(context.user_data['sub_wr_data'].TimeHour).zfill(2)
        minuteToShow = str(context.user_data['sub_wr_data'].TimeMinute).zfill(2)
        timeToShow = f"{hourToShow} : {minuteToShow}"
        bot.edit_message_text(
            text = (lang.l(ll.SUB_WR_SET) % (timeToShow)),
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            parse_mode= 'Markdown'
        )
        return ConversationHandler.END

    def cancel(self, update, context):
        user = update.message.from_user
        userLang = UserService().getTgUserLang(user.id)
        lang = LANG(userLang)
        
        update.message.reply_text(lang.l(ll.SUB_WR_CANCEL))
        return ConversationHandler.END
    
    def getHandler(self):
        handler = ConversationHandler(
            entry_points=[CommandHandler(TgCommand.SUBWEATHER.value, self.newSub)],
            states={
                CHOOSE_LOC: [MessageHandler(Filters.location & ~Filters.command, self.chooseLoc)],
                CHOOSE_TIME_HOUR: [CallbackQueryHandler(self.chooseTimeHour, pattern=f"^{TgCallBackType.SUB_WR_SETH.value}_")],
                CHOOSE_TIME_MINUTE: [CallbackQueryHandler(self.chooseTimeMinute, pattern=f"^{TgCallBackType.SUB_WR_SETM.value}_")],
                CONFIRM: [CallbackQueryHandler(self.confirm, pattern=f"^{TgCallBackType.SUB_WR_CONFIRM.value}")]
            },
            fallbacks=[CommandHandler(TgCommand.CANCEL.value, self.cancel), CallbackQueryHandler(self.cancel, pattern=f"^{TgCallBackType.SUB_WR_CANCEL.value}")],
            conversation_timeout=60
        )
        return handler