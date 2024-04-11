# import logging  # Почитай об этом попозже (уровни и т.д.)
import os
from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import (
    Updater, Filters,
    MessageHandler, CommandHandler,
    CallbackContext, ConversationHandler
    )
from telegram.utils.request import Request


import messages


NAME, SURNAME, AGE = range(3)

USER_INFO = {
    'name': None,     # это потом нужно заменить:
    'surname': None,  # либо будем брать из контекста
    'age': None       # либо из БД
}


def get_surname(update: Update, context: CallbackContext):
    """Вторая функция, запрос фамилии."""

    chat = update.effective_chat
    user_name = update.message.text
    USER_INFO['name'] = user_name
    second_message_text = messages.SURNAME_MESSAGE.format(
        name=USER_INFO['name']
    )
    context.bot.send_message(chat_id=chat.id, text=second_message_text)
    return SURNAME


def get_age(update: Update, context: CallbackContext):
    """Третья функция, запрос возраста."""

    chat = update.effective_chat
    user_surname = update.message.text
    USER_INFO['surname'] = user_surname
    second_message_text = messages.AGE_MESSAGE.format(
        name=USER_INFO['name'],
        surname=USER_INFO['surname']
    )
    context.bot.send_message(chat_id=chat.id, text=second_message_text)
    return AGE


def return_info_msg(update: Update, context: CallbackContext):
    """Финальная функция для вывода информации о пользователе."""

    chat = update.effective_chat
    age = update.message.text
    USER_INFO['age'] = age
    info_message = messages.INFO_MESSAGE.format(
        name=USER_INFO['name'],
        surname=USER_INFO['surname'],
        age=USER_INFO['age'],
        id=update.message.chat.id
    )
    context.bot.send_message(chat_id=chat.id, text=info_message)
    return ConversationHandler.END


def say_hi(update: Update, context: CallbackContext):
    """Первая функция, запрос имени."""

    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=messages.NAME_MESSAGE)
    return NAME


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Отмена. Для начала с нуля нажмите /start')
    return ConversationHandler.END


if __name__ == '__main__':

    load_dotenv()
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    request = Request(con_pool_size=8)
    bot = Bot(token=TELEGRAM_TOKEN, request=request)
    updater = Updater(bot=bot)

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', say_hi)
        ],
        states={
            NAME: [
                MessageHandler(
                    Filters.text,
                    get_surname,
                    pass_user_data=True
                )
            ],
            SURNAME: [
                MessageHandler(
                    Filters.text,
                    get_age,
                    pass_user_data=True
                )
            ],
            AGE: [
                MessageHandler(
                    Filters.text,
                    return_info_msg,
                    pass_user_data=True
                )
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    updater.dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
