# Телеграм-бот v.002 - бот создаёт меню, присылает собачку, и анекдот

import telebot  # pyTelegramBotAPI	4.3.1
from telebot import types
import requests
import bs4
from menuBot import Menu
from random import randint
import secret

bot = telebot.TeleBot(secret.TELEGRAM_TOKEN)  # Создаем экземпляр бота

m_main = Menu("Меню", buttons=["Табы", "Аккорды", "Помощь"])
m_tabs = Menu("Табы", buttons=["Начинающий", "Восходящий", "Маэстро", "Рандом", "Меню"], parent=m_main)
m_tabs_easy = Menu("Начинающий", buttons=[""], parent=m_tabs)  # action=""
m_tabs_mid = Menu("Восходящий", buttons=[""], parent=m_tabs)
m_tabs_hard = Menu("Маэстро", buttons=[""], parent=m_tabs)
m_tabs_random = Menu("Рандом", buttons=[""], parent=m_tabs)

m_accords = Menu("Аккорды", buttons=["Новинки", "Популярные", "Меню"], parent=m_main)
m_accords_pop = Menu("Популярные", buttons=[""], parent=m_main)
m_accords_new = Menu("Новинки", buttons=[""], parent=m_main)

m_help = Menu("Помощь", buttons=[""], parent=m_main)


# -----------------------------------------------------------------------
# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Привет, давай начинать!', reply_markup=m_main.markup)


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
    l = randint(1, 50)
    return f'[{result_find[l + 1].getText().strip()}] ({link_find[l]["href"]})'


def get_accords(a):
    array_tabs = []
    tabs_text = ''
    req_tabs = requests.get(a)
    soup = bs4.BeautifulSoup(req_tabs.text, 'html.parser')
    result_find = soup.select('td ~ .artist_name > a')
    for l in range(2, len(result_find) - 6, 2):
        array_tabs.append(
            f'{result_find[l].getText().strip()} - {result_find[l + 1].getText().strip()} ({result_find[l + 1]["href"][2:]})')

    for i in range(len(array_tabs)):
        tabs_text = tabs_text + '\n' + array_tabs[i]
    return tabs_text


bot.polling(none_stop=True, interval=0)

print()
