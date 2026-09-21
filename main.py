"""Главный модуль Telegram-бота-переводчика.

Содержит обработчики /start, перевод и историю. В код добавлены
комментарии и базовая обработка ошибок для надёжности.
"""

from dotenv import load_dotenv
from telebot import TeleBot, types
import os
import logging
import keyboards as kb
from googletrans import Translator, LANGCODES
import database as db




load_dotenv()

# Базовая конфигурация логирования — при необходимости расширьте
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    logging.critical("TOKEN not found in environment. Create a .env file with TOKEN=<your token>")
    raise RuntimeError("TOKEN not found in environment")

bot = TeleBot(token=TOKEN)
translator = Translator()

# @bot.message_handler(commands=['start', 'help'])
# def start(message: types.Message):
#     chat_id = message.chat.id
#     first_name = message.from_user.first_name
#     if message.text == '/help':
#         bot.send_message(chat_id, 'commands:  /help to get commands or /start to start bot')
#     else:
#         bot.send_message(chat_id, f'Привет, {first_name}')
# # @bot.message_handler(commands=['help'])
# # def help(message: types.Message):
# #     chat_id = message.chat.id
# #     bot.send_message(chat_id, 'commands:  /help to get commands or /start to start bot')
# @bot.message_handler(content_types=['text'])
# def answer(message: types.Message):
#     chat_id = message.chat.id
#     bot.send_message(chat_id, message.text)
@bot.message_handler(commands=['start'])
def start(message: types.Message):
    """Обработчик команды /start: регистрирует пользователя и показывает клавиатуру."""
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    try:
        db.add_user(first_name, chat_id)
    except Exception as e:
        logging.exception("Не удалось добавить пользователя в БД: %s", e)
    bot.send_message(chat_id, 'Выберите действие снизу', reply_markup=kb.start_kb())


@bot.message_handler(func=lambda msg: msg.text == 'Start')
def start_translation(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Выберите язык с которого хотите перевести',
                     reply_markup=kb.land_menu())
    bot.register_next_step_handler(message, get_lang_from)


def get_lang_from(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id,'Выберите язык на который вы хотите сделать перевод',
                     reply_markup=kb.land_menu())
    bot.register_next_step_handler(message, get_lang_to, message.text)


def get_lang_to(message: types.Message, lang_from):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Напишите слово или текст для перевода',
                     reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, translate, lang_from, message.text)

def translate(message: types.Message, lang_from, lang_to):
    """Выполнить перевод и сохранить результат в БД. Обрабатывает ошибки и неверный выбор языка."""
    chat_id = message.chat.id

    try:
        _from = LANGCODES[lang_from.lower()]
        _to = LANGCODES[lang_to.lower()]
    except Exception:
        # Неизвестный язык (возможно, текст кнопки отличается)
        bot.send_message(chat_id, 'Неизвестный язык. Пожалуйста, повторите выбор.')
        start(message)
        return

    try:
        translator_text = translator.translate(message.text, dest=_to, src=_from).text
    except Exception as e:
        logging.exception('Ошибка при переводе: %s', e)
        bot.send_message(chat_id, 'Не удалось выполнить перевод. Попробуйте позже.')
        start(message)
        return

    bot.send_message(chat_id, translator_text)
    try:
        saved = db.add_trans(_from, _to, original_text=message.text, translated_text=translator_text, chat_id=chat_id)
        if not saved:
            logging.warning('add_trans вернул False — пользователь может отсутствовать в БД')
    except Exception as e:
        logging.exception('Не удалось сохранить перевод в БД: %s', e)
    start(message)

@bot.message_handler(func=lambda msg: msg.text == 'History')
def start_history(message: types.Message):
    """Отправить историю переводов пользователя (если есть)."""
    chat_id = message.chat.id
    try:
        hist = db.add_hist(chat_id)
    except Exception as e:
        logging.exception('Не удалось получить историю из БД: %s', e)
        bot.send_message(chat_id, 'Не удалось получить историю. Попробуйте позже.')
        return

    if not hist:
        bot.send_message(chat_id, 'У вас нету истории')
        return

    for history in hist:
        # history expected format: (id, lang_from, lang_to, original_text, translated_text, user_id)
        bot.send_message(chat_id, f"Ваша история: Языки == {history[1]} --> {history[2]}, исходное слово ({history[3]}) --> результат ({history[4]})")



bot.polling(none_stop=True)