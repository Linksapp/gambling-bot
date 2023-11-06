import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import token
import db_manager as db

bot = telebot.TeleBot(token)

def main_menu(message: telebot.types.Message):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('Заказать напиток🍸', callback_data='bar'))
    markup.row(InlineKeyboardButton('Отправить деньги', callback_data='send_cash'))
    bot.send_message(message.chat.id, f'Ваш баланс💰: {db.get_info(message)[3]} \nВыберете действие:', reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    db.create(message)
    bot.send_message(message.chat.id, 'Привет, пожалуйста введи своё имя🥺: ')
    bot.register_next_step_handler(message, user_name)
    #main_menu(message)

def user_name(message: telebot.types.Message):
    name = message.text
    db.addnametodb(message, name)
    bot.send_message(message.chat.id, 'п-пожалуйста введи свою фамлилю🥵: ')
    bot.register_next_step_handler(message, user_surname)

def user_surname(message: telebot.types.Message):
    surname = message.text
    db.addsurnametodb(message, surname)
    bot.send_message(message.chat.id, 'Поздравляю! Ты теперь официальный гость Влада Козлова🤩')
    main_menu(message)

def check_person(message: telebot.types.Message):
    # print(tuple(message.text.split()[1:2]))
    try:
        names = db.get_names(message)
        ind = int(message.text[1:])
        if ind in range(len(names)):
        # if tuple(message.text.split()) in db.get_names(message):
            bot.send_message(message.chat.id, 'Введите сумму, которую хотите отправить! (коммисия 3%)')
            bot.register_next_step_handler(message, send_cash, db.get_chat_id(names[ind-1]))
        else:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, 'Проверьте корректность введённых данных!')
        bot.send_message(message.chat.id, 'Выберете гостя, которому хотите отправить деньги! (коммисия 3%)')
        members = db.get_names(message)
        members_out = ''
        count = 1
        for i in members:
            members_out += f'/{count} {i[0]} {i[1]} \n'
            count += 1
        bot.send_message(message.chat.id, members_out)
        bot.register_next_step_handler(message, check_person)

def send_cash(message: telebot.types.Message, id: int):
    try:
        if db.check_wealth(message) == 1:
            db.withdraw_money(message, id)
            bot.send_message(message.chat.id, 'Деньги отправлены!')
            main_menu(message)
        elif db.check_wealth(message) == -1:
            bot.send_message(message.chat.id, 'На Вашем балансе недостаточно средств!')
            bot.send_message(message.chat.id, 'Введите сумму, которую хотите отправить! (коммисия 3%)')
            bot.register_next_step_handler(message, send_cash, id)
        else: raise Exception
    except:
        bot.send_message(message.chat.id, 'Введенны неверные данные!')
        bot.send_message(message.chat.id, 'Введите сумму, которую хотите отправить! (коммисия 3%)')
        bot.register_next_step_handler(message, send_cash, id)

@bot.callback_query_handler(func=lambda callback: True)
def callback_start(callback: telebot.types.CallbackQuery):
    # print(callback)
    bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.id, reply_markup=None)
    # bot.edit_message_text(text= ,chat_id=callback.message.chat.id, message_id=callback.message.id, reply_markup=)
    # bot.send_message(callback.message.chat.id, 'тест')
    if callback.data == 'send_cash':
        members = db.get_names(callback.message)
        members_out = ''
        count = 1
        for i in members:
            members_out += f'/{count} {i[0]} {i[1]} \n'
            count += 1
        
        bot.send_message(callback.message.chat.id, 'Выберете гостя, которому хотите отправить деньги! (коммисия 3%)')
        bot.send_message(callback.message.chat.id, members_out)
        bot.register_next_step_handler(callback.message, check_person)
    if callback.data == 'bar':
        pass
    if callback.data == 'games':
        pass


bot.polling()