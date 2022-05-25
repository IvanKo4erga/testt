# Телеграм-бот v.002 - бот создаёт меню, присылает собачку, и анекдот

import telebot  # pyTelegramBotAPI	4.3.1
from telebot import types
import requests
import bs4
from menuBot import Menu
from random import randint

bot = telebot.TeleBot('5275596119:AAEuhyVOFr2yD6x6pUtVqqk3sn5FiZA3Is0')  # Создаем экземпляр бота

m_main = Menu("Меню", buttons=["Табы", "Аккорды", "Помощь"])
m_tabs = Menu("Табы", buttons=["Начинающий", "Восходящий", "Маэстро", "Рандом", "Меню"], parent=m_main)
m_tabs_easy = Menu("Начинающий", buttons=[""], parent=m_tabs)  # action=""
m_tabs_mid = Menu("Восходящий", buttons=[""], parent=m_tabs)
m_tabs_hard = Menu("Маэстро", buttons=[""], parent=m_tabs)
m_tabs_random = Menu("Рандом", buttons=[""], parent=m_tabs)

m_accords = Menu("Аккорды", buttons=["Новинки", "Популярные", "Меню"], parent=m_main)
m_accords_pop = Menu("Популярные", buttons=[""], parent=m_main)
m_accords_new = Menu("Новинки", buttons=[""], parent=m_main)

# m_tuner = Menu("Тюнер", buttons=[""], parent=m_main)

m_help = Menu("Помощь", buttons=[""], parent=m_main)


# -----------------------------------------------------------------------
# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(message):
    # chat_id = message.chat.id

    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    bot.send_message(message.chat.id, 'Привет, давай начинать!', reply_markup=m_main.markup)

    # bot.send_message(chat_id,
    #                 text="Привет, {0.first_name}! Я бот для гитаростов".format(
    #                     message.from_user), reply_markup=markup)


# -----------------------------------------------------------------------
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    ms_text = message.text
    if ms_text == 'Начинающий':
        ms_text = get_tabs('Ученик')

    elif ms_text == 'Восходящий':
        ms_text = get_tabs('Новичок')

    elif ms_text == 'Виртуоз':
        ms_text = get_tabs('Виртуоз')

    elif ms_text == 'Маэстро':
        ms_text = get_tabs('Бывалый')

    elif ms_text == 'Рандом':
        ms_text = get_tabs_random()

    elif ms_text == 'Популярные':
        ms_text = get_accords('https://amdm.ru/akkordi/popular/all/')

    elif ms_text == 'Новинки':
        ms_text = get_accords('https://amdm.ru/akkordi/')

    elif ms_text == "Помощь" or ms_text == "/help":
        bot.send_message(message.chat.id, "Автор: Каргин Даниил")
        key1 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="Напишите автору", url="https://t.me/ivankocherga")
        key1.add(btn1)
        img = open('1мд19_Каргин_Даниил.jpg', 'rb')
        bot.send_photo(message.chat.id, img, reply_markup=key1)

    bot.send_message(message.chat.id, text=ms_text, reply_markup=m_main.getMenu(message.text).markup,
                     parse_mode='Markdown')
    # bot.send_message(message.chat.id, '[StackOverflow на русском](https://ru.stackoverflow.com/)',
    #                 parse_mode='Markdown')
    # if ms_text == 'Табы':
    #     m_tabs = Menu("Табы", buttons=["Начинающий", "Восходящий", "Маэстро", "Рандом"], parent=m_main)
    #     bot.send_message(chat_id, text="Табы", reply_markup=m_tabs.markup)

    # if ms_text == "Главное меню" or ms_text == "👋 Главное меню" or ms_text == "Вернуться в главное меню":  # ..........
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btn1 = types.KeyboardButton("Развлечения")
    #     btn2 = types.KeyboardButton("WEB-камера")
    #     btn3 = types.KeyboardButton("Управление")
    #     back = types.KeyboardButton("Помощь")
    #     markup.add(btn1, btn2, btn3, back)
    #     bot.send_message(chat_id, text="Вы в главном меню", reply_markup=markup)

    # elif ms_text == "Развлечения":  # ..................................................................................
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btn1 = types.KeyboardButton("Прислать собаку")
    #     btn2 = types.KeyboardButton("Прислать анекдот")
    #     btn3 = types.KeyboardButton("Что посмотреть")
    #     back = types.KeyboardButton("Вернуться в главное меню")
    #     markup.add(btn1, btn2, btn3, back)
    #     bot.send_message(chat_id, text="Развлечения", reply_markup=markup)

    # if ms_text == "/dog" or ms_text == "Прислать собаку":  # .........................................................
    #     contents = requests.get('https://random.dog/woof.json').json()
    #     urlDog = contents['url']
    #     bot.send_photo(chat_id, photo=urlDog, caption='На собачку!')
    #
    # elif ms_text == "Прислать анекдот":  # .............................................................................
    #     bot.send_message(chat_id, text=get_anekdot())
    #
    # elif ms_text == "Что посмотреть":  # .............................................................................
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btn1 = types.KeyboardButton("Аниме")
    #     btn2 = types.KeyboardButton("Фильмы")
    #     btn3 = types.KeyboardButton("Сериалы")
    #     back = types.KeyboardButton("Вернуться в главное меню")
    #     markup.add(btn1, btn2, btn3, back)
    #     bot.send_message(chat_id, text="Что посмотреть", reply_markup=markup)
    #
    # elif ms_text == "Аниме":
    #     bot.send_message(chat_id, text=get_anime())
    #
    # elif ms_text == "Фильмы":
    #     bot.send_message(chat_id, text=get_films())
    #
    # elif ms_text == "Сериалы":
    #     bot.send_message(chat_id, text=get_series())
    #
    # elif ms_text == "WEB-камера":
    #     bot.send_message(chat_id, text="еще не готово...")
    #
    # elif ms_text == "Управление":  # ...................................................................................
    #     bot.send_message(chat_id, text="еще не готово...")
    #

    #
    # else:  # ...........................................................................................................
    #     bot.send_message(chat_id, text="Я тебя слышу!!! Ваше сообщение: " + ms_text)


def get_tabs(a):
    array_tabs = []
    tabs_text = ''
    req_tabs = requests.get('https://guitarmaestro.ru/free-tabs-library/')
    soup = bs4.BeautifulSoup(req_tabs.text, 'html.parser')
    result_find = soup.select('.column-2')
    level_find = soup.select('.column-3')
    link_find = soup.select('td ~ .column-5 > a')
    for l in range(1, len(result_find) - 2):
        if level_find[l + 1].getText().strip() == a:
            array_tabs.append(f'[{result_find[l + 1].getText().strip()}] ({link_find[l]["href"]})')

    for i in range(len(array_tabs)):
        tabs_text = tabs_text + '\n' + array_tabs[i]
    return tabs_text


def get_tabs_random():
    req_tabs = requests.get('https://guitarmaestro.ru/free-tabs-library/')
    soup = bs4.BeautifulSoup(req_tabs.text, 'html.parser')
    result_find = soup.select('.column-2')
    link_find = soup.select('td ~ .column-5 > a')
    print(link_find)
    print(result_find)
    l = randint(1, 50)
    return f'[{result_find[l + 1].getText().strip()}] ({link_find[l]["href"]})'


def get_accords(a):
    array_tabs = []
    tabs_text = ''
    req_tabs = requests.get(a)
    soup = bs4.BeautifulSoup(req_tabs.text, 'html.parser')
    result_find = soup.select('td ~ .artist_name > a')
    print(result_find)
    for l in range(2, len(result_find) - 6, 2):
        array_tabs.append(f'{result_find[l].getText().strip()} - {result_find[l + 1].getText().strip()} ({result_find[l + 1]["href"][2:]})')

    for i in range(len(array_tabs)):
        tabs_text = tabs_text + '\n' + array_tabs[i]
    return tabs_text


def get_tuner():
    return


# def get_anime():
#     array_anim = []
#     anim_text = ''
#     req_anim = requests.get('https://www.kinonews.ru/top100-anime/')
#     soup = bs4.BeautifulSoup(req_anim.text, 'html.parser')
#     result_find = soup.select('.bigtext')
#     for res in result_find:
#         array_anim.append(res.getText().strip())
#     for i in range(51):
#         anim_text = anim_text + '\n' + array_anim[i]
#     return anim_text
#
#
# def get_films():
#     array_film = []
#     film_text = ''
#     req_film = requests.get('https://www.kinonews.ru/top100/')
#     soup = bs4.BeautifulSoup(req_film.text, 'html.parser')
#     result_find = soup.select('.bigtext')
#     for res in result_find:
#         array_film.append(res.getText().strip())
#     for i in range(51):
#         film_text = film_text + '\n' + array_film[i]
#     return film_text
#
#
# def get_series():
#     array_series = []
#     series_text = ''
#     req_series = requests.get('https://www.kinonews.ru/serial_top100/')
#     soup = bs4.BeautifulSoup(req_series.text, 'html.parser')
#     result_find = soup.select('.bigtext')
#     for res in result_find:
#         array_series.append(res.getText().strip())
#     for i in range(51):
#         series_text = series_text + '\n' + array_series[i]
#     return series_text


# -----------------------------------------------------------------------
bot.polling(none_stop=True, interval=0)  # Запускаем бота

print()
