import telebot


class shopping_list:
    def __init__(self):
        self.products = []
        self.keyboard_markup = telebot.types.ReplyKeyboardMarkup()
        item1 = telebot.types.KeyboardButton("Добавить продукт")
        item2 = telebot.types.KeyboardButton("Удалить продукт")
        item3 = telebot.types.KeyboardButton("Очистить список")
        self.keyboard_markup.row(item1, item2)
        self.keyboard_markup.row(item3)
        self.commands_list = ["Добавить продукт", "Удалить продукт", "Очистить список"]

    def clear(self):
        self.products.clear()
        return True

    def remove_item(self, n):
        if len(self.products) >= n:
            return self.products.pop(n - 1)
        return False

    def get_remove_item_keyboard(self):
        keyboard = telebot.types.ReplyKeyboardMarkup()
        now = []
        for i in range(len(self.products)):
            if len(now) < 3:
                now.append(str(i + 1))
            else:
                keyboard.row(*now)
                now = []
        return keyboard

    def add_item(self, item):
        self.products.append(item)
        return True

    def get_shopping_list(self):
        if len(self.products) > 0:
            numed_products = [str(i + 1) + "." + self.products[i]
                              for i in range(len(self.products))]
            text = "Вот ваш список покупок:\n"
            text += "\n".join(numed_products)
            return text
        return "Список покупок пуст!"

    def __len__(self):
        return len(self.products)


FLAGS = {"new_product": False,
         "remove_product": False}
SHOPPING_LIST = shopping_list()
SHOPPING_LIST.add_item("Молоко")
SHOPPING_LIST.add_item("Яйца")
COMMANDS = {("Список покупок, Список, список, список покупок"): shopping_list}
TOKEN = ''
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Всем привет, на связи Dimasik!\nЯ бот созданный крутейшим Димасиком на земле,"
                                      " специально для чата лучшей семьи."
                                      "На данный момент я умею следующее:"
                                      "1) Составлять и хранить список покупок"
                                      "Для подробной информации о командах пишите /help")


@bot.message_handler(commands=['help'])
def start_command(message):
    bot.send_message(message.chat.id, "1)Димасик, список покупок - выводит список покупок и предлагает его модифицировать\n"
                                      "Пока всё)")


@bot.message_handler(func=lambda message: message.text[:9] == "Димасик, ")
def dimasik_command(message):
    text = message.text[9:]
    if text in ("Список покупок, Список, список, список покупок"):
        bot.send_message(message.chat.id, SHOPPING_LIST.get_shopping_list(), reply_markup=SHOPPING_LIST.keyboard_markup)
    else:
        bot.send_message(message.chat.id, "Команда не распознана")


@bot.message_handler(func=lambda message: message.text in SHOPPING_LIST.commands_list)
def shopping_list_command(message):
    if message.text == SHOPPING_LIST.commands_list[0]:
        bot.send_message(message.chat.id, "Введите продукт:")
        FLAGS["new_product"] = True
    elif message.text == SHOPPING_LIST.commands_list[1]:
        bot.send_message(message.chat.id, "Введите номер продукта:",
                         reply_markup=SHOPPING_LIST.get_remove_item_keyboard())
        FLAGS["remove_product"] = True
    elif message.text == SHOPPING_LIST.commands_list[2]:
        SHOPPING_LIST.clear()
        bot.send_message(message.chat.id, "Список очищен")


@bot.message_handler(content_types=["text"])
def text_answers(message):
    if FLAGS["new_product"]:
        SHOPPING_LIST.add_item(message.text)
        bot.send_message(message.chat.id, "Продукт {} успешно добавлен в список покупок!".format(message.text))
        FLAGS["new_product"] = False
    elif FLAGS["remove_product"]:
        FLAGS["remove_product"] = False
        if message.text.isnumeric():
            item_num = int(message.text)
            if 0 < item_num <= len(SHOPPING_LIST):
                SHOPPING_LIST.remove_item(item_num)
                bot.send_message(message.chat.id, "Продукт №{} успешно удален из списка покупок!".format(message.text))
            else:
                bot.send_message(message.chat.id, "Неподходящий номер")


bot.polling()
