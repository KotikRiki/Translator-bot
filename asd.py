from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import os
import json
import pandas as pd
from google.cloud import translate_v2 #наш переводчик
from telegram import *
from requests import *

# MessageHandler - respond any mess'e
print('We work')
# снизу мы создаём окружение разработки, тут же и наш ключ в JSON, котоырй мы читаем 'r'
# указывая дерикторию
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\Dima\PycharmProjects\alert-tiger-332214-0ab7b0ceb1c0.json'

translate_client = translate_v2.Client()  # создаём класс, чтобы свободно пользоваться
LANGUAGES = {
'af': 'afrikaans',
'sq': 'albanian',
'am': 'amharic',
'ar': 'arabic',
'hy': 'armenian',
'az': 'azerbaijani',
'eu': 'basque',
'be': 'belarusian',
'bn': 'bengali',
'bs': 'bosnian',
'bg': 'bulgarian',
'ca': 'catalan',
'ceb': 'cebuano',
'ny': 'chichewa',
'zh-cn': 'chinese (simplified)',
'zh-tw': 'chinese (traditional)',
'co': 'corsican',
'hr': 'croatian',
'cs': 'czech',
'da': 'danish',
'nl': 'dutch',
'en': 'english',
'eo': 'esperanto',
'et': 'estonian',
'tl': 'filipino',
'fi': 'finnish',
'fr': 'french',
'fy': 'frisian',
'gl': 'galician',
'ka': 'georgian',
'de': 'german',
'el': 'greek',
'gu': 'gujarati',
'ht': 'haitian creole',
'ha': 'hausa',
'haw': 'hawaiian',
'iw': 'hebrew',
'hi': 'hindi',
'hmn': 'hmong',
'hu': 'hungarian',
'is': 'icelandic',
'ig': 'igbo',
'id': 'indonesian',
'ga': 'irish',
'it': 'italian',
'ja': 'japanese',
'jw': 'javanese',
'kn': 'kannada',
'kk': 'kazakh',
'km': 'khmer',
'ko': 'korean',
'ku': 'kurdish (kurmanji)',
'ky': 'kyrgyz',
'lo': 'lao',
'la': 'latin',
'lv': 'latvian',
'lt': 'lithuanian',
'lb': 'luxembourgish',
'mk': 'macedonian',
'mg': 'malagasy',
'ms': 'malay',
'ml': 'malayalam',
'mt': 'maltese',
'mi': 'maori',
'mr': 'marathi',
'mn': 'mongolian',
'my': 'myanmar (burmese)',
'ne': 'nepali',
'no': 'norwegian',
'ps': 'pashto',
'fa': 'persian',
'pl': 'polish',
'pt': 'portuguese',
'pa': 'punjabi',
'ro': 'romanian',
'ru': 'russian',
'sm': 'samoan',
'gd': 'scots gaelic',
'sr': 'serbian',
'st': 'sesotho',
'sn': 'shona',
'sd': 'sindhi',
'si': 'sinhala',
'sk': 'slovak',
'sl': 'slovenian',
'so': 'somali',
'es': 'spanish',
'su': 'sundanese',
'sw': 'swahili',
'sv': 'swedish',
'tg': 'tajik',
'ta': 'tamil',
'te': 'telugu',
'th': 'thai',
'tr': 'turkish',
'uk': 'ukrainian',
'ur': 'urdu',
'uz': 'uzbek',
'vi': 'vietnamese',
'cy': 'welsh',
'xh': 'xhosa',
'yi': 'yiddish',
'yo': 'yoruba',
'zu': 'zulu',
'fil': 'Filipino',
'he': 'Hebrew'
}

# ----------------Buttons in the chat-----------------------------
def build_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None):  # creating of our buttons inline
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]  # yfcnhjqrf vty.
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


# ------------------LIST-------------------------------------------
def list_languages(update, conext):  # список языков
    chat = update.effective_chat
    LANGUAGES_TEXT = "**Languages**\n"
    for language in LANGUAGES:
        LANGUAGES_TEXT += f"\n`{LANGUAGES[language].capitalize()}` -> `{language}`"
    conext.bot.send_message(chat_id=chat.id, text=LANGUAGES_TEXT)  # попытаться через нумпай, уже импортировал.
        # тут нужно вывести лишь {'name'} языка



# ----------------------------------------------------------------------

# -------------------------------CHOOSING-------------------------------------
def choose_language(update, conext):  # выбор языка, в разработке, не включать в тг, ошибка.
    chat = update.effective_chat
    keyboard1 = [
        [
            InlineKeyboardButton('English', callback_data='en'),
            # каждый список, в который встроен код - находитcя вместе, в однйо строке
            InlineKeyboardButton('Russian', callback_data='ru'),
            # разделение таких списков даёт вывод в виде табоицы, что приятно глазу
        ],
        [
            InlineKeyboardButton('Italian', callback_data='it'),
            InlineKeyboardButton('German', callback_data='de'),
            InlineKeyboardButton('Polish', callback_data='pl'),
            InlineKeyboardButton('Spanish', callback_data='es'),

        ],
        [
            InlineKeyboardButton('Greel', callback_data='el'),
            InlineKeyboardButton('Czech', callback_data='cs'),
            InlineKeyboardButton('Latin', callback_data='la'),
            InlineKeyboardButton('Serbian', callback_data='sr'),

        ],
        [
            InlineKeyboardButton('Slovak', callback_data='sk'),
            InlineKeyboardButton('Swedish', callback_data='sw'),
            InlineKeyboardButton('Ukrainian', callback_data='uk'),
            InlineKeyboardButton('Norwegian', callback_data='no'),

        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard1)
    update.message.reply_text('Choose target language:', reply_markup=reply_markup)


# ----------------------------------------------------------------------
# -----------------------------START-------------------------------------
def on_start(update, conext):
    chat = update.effective_chat  # обновление чата в данный момент, поулчение ИД
    # x = '{"/languages":"Languages"}'
    # y = json.loads(x)   #Попытки сделать название команды
    # x1 = '{"/start":"Start"}'
    # y1 = json.loads(x1)
    buttons = [[KeyboardButton("/choose")], [KeyboardButton('/languages')],
               [KeyboardButton('/start')], [KeyboardButton('/help')]]
    conext.bot.send_message(chat_id=chat.id, text='Well... Go on.',
                            reply_markup=ReplyKeyboardMarkup(buttons))
    conext.bot.send_message(chat_id=chat.id, text='If you do not understand something, then click "Help".')

# ----------------------ANSWER-------------------------------------------
def button(update, conext):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    global q  # we make the statement global to the code
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise.
    query.answer()
    query.edit_message_text(text=f"Target: {query.data}")
    q = query.data


# ------------------------TRANSLATOR-----------------------------------------
def on_message(update, conext):
    chat = update.effective_chat
    text = update.message.text  # наш вводимый текст
    target = q  # происходит выбор целевого языка
    try:
        output = translate_client.translate(
            text,
            target_language=target  # перевод текста
        )
        conext.bot.send_message(chat_id=chat.id, text=output['translatedText'])
    except:
        with open('Link.webp', 'rb') as file1:
            conext.bot.send_sticker(chat_id=chat.id, sticker=file1)


# ------------------------HELP-----------------------------------------------
def helpo(update, conext):
    chat = update.effective_chat
    conext.bot.send_message(chat_id=chat.id, text="/languages -> to get the list of all available languages.\
	 /choose -> to get the list of your own choosing. \
	 /start -> to go back to the start. \
	 /help -> to get information that you need. \
	 !!!WARNING!!!\
	 If you have not chosen the language then you must do it,\
	 otherwise it will not work. GitHub: https://github.com/KotikRiki")


# ---------------------OTHERS STUFF-----------------------------------------------

token = '5038609609:AAGocHX386jbCoV0sUXl5Q9g-KQr67-Myvs'  # без токена бот не будет работать
updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher  # диспетчер даёт нам выполнять команды
dispatcher.add_handler(CommandHandler('start', on_start))  # 2nd is func of formatin'
dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(CommandHandler('help', helpo))
dispatcher.add_handler(CommandHandler('languages', list_languages))
dispatcher.add_handler(CommandHandler('choose', choose_language))
dispatcher.add_handler(
    MessageHandler(Filters.all, on_message))  # Под фильтром указал all, работает для любвых сообщений
# Нужно для запуска
updater.start_polling()
# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT
updater.idle()
