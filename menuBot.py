from telebot import types


# -----------------------------------------------------------------------
class Menu:
    hash = {}  # тут будем накапливать все созданные экземпляры класса
    cur_menu = None  # тут будет находиться текущий экземпляр класса, текущее меню

    def __init__(self, name, buttons=None, parent=None, action=None):
        self.parent = parent
        self.name = name
        self.buttons = buttons
        self.action = action

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=6)
        markup.add(*buttons)  # Обратите внимание - звёздочка используется для распаковки списка
        self.markup = markup

        self.__class__.hash[name] = self  # в классе содержится словарь, со всеми экземплярами класса, обновим его

    @classmethod
    def getMenu(cls, name):
        menu = cls.hash.get(name)
        if menu != None:
            cls.cur_menu = menu
        return menu


m_main = Menu("Главное меню", buttons=["Табы", "Аккорды", "Тюнер", "Помощь"])

m_tabs = Menu("Табы", buttons=["Начинающий", "Восходящий", "Маэстро", "Рандом"], parent=m_main)
m_tabs_easy = Menu("Начинающий", buttons=[""], parent=m_tabs)  # action=""
m_tabs_mid = Menu("Восходящий", buttons=[""], parent=m_tabs)
m_tabs_hard = Menu("Маэстро", buttons=[""], parent=m_tabs)
m_tabs_random = Menu("Рандом", buttons=[""], parent=m_tabs)

m_accords = Menu("Аккорды", buttons=[""], parent=m_main)

m_tuner = Menu("Тюнер", buttons=[""], parent=m_main)

m_help = Menu("Помощь", buttons=[""], parent=m_main)
