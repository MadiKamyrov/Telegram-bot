import pymongo
import telebot
from telebot import types

bot = telebot.TeleBot('5901618580:AAGaBkjDds36ZuTpfKL20hb0TbH474U14Ro')

client = pymongo.MongoClient('mongodb+srv://madiayzhalby:kanada19@cluster0.zodb7u9.mongodb.net/test')
db = client['students_db']
feedback_collection = db['feedback']


def save_feedback(email, feedback):
    feedback_collection.insert_one({'email': email, 'feedback': feedback})
    return 'Спасибо за ваш отзыв!'


def send_feedback(message, email):
    feedback_text = message.text
    save_feedback(email, feedback_text)
    bot.send_message(message.from_user.id, "Благодарим за ваш отзыв! Он поможет нам сделать наш университет еще лучше.", reply_markup=get_main_menu())


def email_handler(message):
    email = message.text
    if '@' not in email:
        bot.send_message(message.from_user.id, 'Некорректный email, попробуйте еще раз.', reply_markup=create_cancel_keyboard())
        bot.register_next_step_handler(message, email_handler)
        return
    bot.send_message(message.from_user.id, 'Напишите ваш отзыв:', reply_markup=create_cancel_keyboard())
    bot.register_next_step_handler(message, send_feedback, email)


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    if message.text == 'Оставить отзыв':
        bot.send_message(message.from_user.id, 'Введите ваш email:', reply_markup=create_cancel_keyboard())
        bot.register_next_step_handler(message, email_handler)
    else:
        bot.send_message(message.from_user.id, 'Используйте кнопки в меню.', reply_markup=get_main_menu())

def create_cancel_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    back_button = types.KeyboardButton('Назад')
    keyboard.add(back_button)
    return keyboard

def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('/start'))
    markup.add(types.KeyboardButton('Расписание'))
    markup.add(types.KeyboardButton('Экзамены'))
    markup.add(types.KeyboardButton('Оценки'))
    markup.add(types.KeyboardButton('FAQs'))
    markup.add(types.KeyboardButton('Оставить отзыв'))
    markup.add(types.KeyboardButton('Подготовка к экзамену'))

    return markup
