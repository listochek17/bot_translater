from dotenv import load_dotenv
from telebot import TeleBot, types
import os
import keyboerds as kb
from googletrans import Translator, LANGCODES
import database as db




load_dotenv()

TOKEN = os.getenv('TOKEN')
# print(TOKEN)

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
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    db.add_user(first_name, chat_id)
    bot.send_message(chat_id, 'Выберите действие снизу', reply_markup=kb.start_kb())


@bot.message_handler(func=lambda msg: msg.text == 'Start')
def start_translation(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Выберите язык с которого хотите перевести',
                     reply_markup=kb.land_menu())
    bot.register_next_step_handler(message, get_lang_from)


def get_lang_from(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id,'Выберите языкб на который вы хотите сделать перевод',
                     reply_markup=kb.land_menu())
    bot.register_next_step_handler(message, get_lang_to, message.text)


def get_lang_to(message: types.Message, lang_from):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Напишите слово или текст для перевода',
                     reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, translate, lang_from, message.text)

def translate(message: types.Message, lang_from, lang_to):
    chat_id = message.chat.id

    _from = LANGCODES[lang_from.lower()]
    _to = LANGCODES[lang_to.lower()]
    translator_text = translator.translate(message.text, dest=_to, src=_from).text
    bot.send_message(chat_id, translator_text)
    db.add_trans(_from, _to, original_text=message.text, translated_text=translator_text, chat_id=chat_id)
    start(message)

@bot.message_handler(func=lambda msg: msg.text == 'History')
def start_history(message: types.Message):
    chat_id = message.chat.id
    hist = db.add_hist(chat_id)
    print(hist)
    for history in hist:
        if not hist:
            bot.send_message(chat_id, 'У вас нету истории')
        else:
            print(history)
            bot.send_message(chat_id, f'''
Ваша история: Языки == {history[1]} --> {history[2]},
исходное слово ({history[3]}) --> результат ({history[4]})

''')



bot.polling(none_stop=True)