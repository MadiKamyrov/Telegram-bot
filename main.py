# -*- coding: utf-8 -*-
import telebot
import json
import requests
from db import feedback_collection
from telebot import types

bot = telebot.TeleBot('5901618580:AAGaBkjDds36ZuTpfKL20hb0TbH474U14Ro')
API_URL = "http://127.0.0.1:8000/student/{}"
EVENTS_URL = 'http://127.0.0.1:8000/events'
FAQS_API = 'http://127.0.0.1:8000/faqs'
user_ids = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = get_main_menu()
    if message.chat.id not in user_ids:
        user_ids[message.chat.id] = ''
    bot.reply_to(message, "Добро пожаловать! Я ваш ассистент. Пожалуйста, введите свой студенческий билет:",
                 reply_markup=keyboard)
    bot.register_next_step_handler(message, process_user_id)


def process_user_id(message):
    user_id = message.text
    user_ids[message.chat.id] = user_id
    bot.reply_to(message, f"Ваш студенческий билет: {user_id}")


@bot.message_handler(func=lambda message: message.text == 'Расписание')
def send_schedule(message):
    if message.chat.id not in user_ids:
        bot.reply_to(message, "Пожалуйста, введите свой студенческий билет:")
        bot.register_next_step_handler(message, process_user_id)
    else:
        user_id = user_ids[message.chat.id]
        response = requests.get(API_URL.format(user_id))
        student_data = response.json()
        if "error" in student_data:
            bot.reply_to(message, "К сожалению, не удалось найти информацию о студенте.")
        else:
            schedule_data = student_data['user'].get('schedule')
            if not schedule_data:
                bot.reply_to(message, "К сожалению, расписание не найдено.")
            else:
                schedule_text = f"Расписание на следующую неделю:\n\n"
                for day, lessons in schedule_data.items():
                    schedule_text += f"{day}:\n"
                    for lesson in lessons:
                        schedule_text += f"{lesson['предмет']} {lesson['время']}\n"
                    schedule_text += "\n"
                bot.reply_to(message, schedule_text)


@bot.message_handler(func=lambda message: message.text == 'Оценки')
def get_grades(message):
    if message.chat.id not in user_ids:
        bot.reply_to(message, "Пожалуйста, введите свой студенческий билет:")
        bot.register_next_step_handler(message, process_user_id)
    else:
        user_id = user_ids[message.chat.id]
        response = requests.get(API_URL.format(user_id))
        student_data = response.json()
        if "error" in student_data:
            bot.reply_to(message, "К сожалению, не удалось найти информацию о студенте.")
        else:
            grades_text = "Ваши текущие оценки:\n\n"
            for subject, grade in student_data['user']['grades'].items():
                grades_text += f"{subject}: {grade} баллов\n"
            grades_text += "\n"
            bot.reply_to(message, grades_text)

@bot.message_handler(func=lambda message: message.text == 'Экзамены')
def send_exams(message):
    if message.chat.id not in user_ids:
        bot.reply_to(message, "Пожалуйста, введите свой студенческий билет:")
        bot.register_next_step_handler(message, process_user_id)
    else:
        user_id = user_ids[message.chat.id]
        response = requests.get(API_URL.format(user_id))
        student_data = response.json()
        if "error" in student_data:
            bot.reply_to(message, "К сожалению, не удалось найти информацию о студенте.")
        else:
            exams = student_data["user"]["exams"]
            if exams:
                exams_text = 'Экзамены:\n\n'
                for exam in exams:
                    exams_text += f"{exam}\n"
                bot.reply_to(message, exams_text)


@bot.message_handler(func=lambda message: message.text == 'FAQs')
def faq_command(message):
    faqs = get_faqs_from_api()
    if faqs:
        questions = [faq['question'] for faq in faqs]
        keyboard = create_faq_keyboard(questions)
        bot.reply_to(message, "Пожалуйста, выберите вопрос:", reply_markup=keyboard)
    else:
        bot.reply_to(message, "Извините, в настоящее время вопросы недоступны. Попробуйте позже.")


@bot.message_handler(func=lambda message: message.text in [faq['question'] for faq in get_faqs_from_api()])
def faq_message(message):
    question = message.text
    faq = get_faq_by_question(question)
    if faq:
        answer = faq['answer']
        bot.reply_to(message, answer, reply_markup=get_faq_keyboard())
    else:
        bot.reply_to(message, "Извините, ответ на данный вопрос недоступен. Попробуйте выбрать другой вопрос.")


def create_faq_keyboard(questions):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for question in questions:
        keyboard.add(types.KeyboardButton(question))
    keyboard.add(types.KeyboardButton('Вернуться в главное меню'))
    return keyboard


def get_faq_keyboard():
    faqs = get_faqs_from_api()
    questions = [faq['question'] for faq in faqs]
    return create_faq_keyboard(questions)


def get_faqs_from_api():
    try:
        response = requests.get(FAQS_API)
        if response.status_code == 200:
            faqs = json.loads(response.text)['faqs']
            return faqs
        else:
            return []
    except requests.exceptions.RequestException:
        return []


def get_faq_by_question(question):
    faqs = get_faqs_from_api()
    for faq in faqs:
        if faq['question'] == question:
            return faq
    return None


@bot.message_handler(func=lambda message: message.text == 'Вернуться в главное меню')
def back_to_main_menu(message):
    bot.reply_to(message, 'Вы в главном меню!', reply_markup=get_main_menu())


@bot.message_handler(func=lambda message: message.text == 'Оставить отзыв')
def message_handler(message):
    if message.text == 'Оставить отзыв':
        bot.send_message(message.from_user.id, 'Введите вашу корпоративную почту:',
                         reply_markup=create_cancel_keyboard())
        bot.register_next_step_handler(message, email_handler)
    else:
        bot.send_message(message.from_user.id, 'Используйте кнопки в меню.', reply_markup=get_main_menu())


def save_feedback(email, feedback):
    feedback_collection.insert_one({'email': email, 'feedback': feedback})
    return 'Спасибо за ваш отзыв!'


def create_cancel_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    back_button = types.KeyboardButton('Назад')
    keyboard.add(back_button)
    return keyboard


def email_handler(message):
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Вы вернулись в главное меню!', reply_markup=get_main_menu())
        return
    email = message.text
    if '@' not in email:
        bot.send_message(message.from_user.id, 'Некорректный email, попробуйте еще раз.',
                         reply_markup=create_cancel_keyboard())
        bot.register_next_step_handler(message, email_handler)
        return
    bot.send_message(message.from_user.id, 'Напишите ваш отзыв:', reply_markup=create_cancel_keyboard())
    bot.register_next_step_handler(message, feedback_handler, email)


def feedback_handler(message, email):
    if message.text == 'Назад':
        bot.send_message(message.from_user.id, 'Вы вернулись к вводу email!', reply_markup=create_cancel_keyboard())
        bot.register_next_step_handler(message, email_handler)
        return
    save_feedback(email, message.text)
    bot.send_message(message.from_user.id, 'Спасибо за ваш отзыв!', reply_markup=get_main_menu())
    bot.send_message(message.from_user.id, 'Вы снова в главном меню!')


def get_exam_subjects():
    response = requests.get(API_URL.format('items'))
    subjects = response.json()['users']['items']
    return subjects


@bot.message_handler(func=lambda message: message.text == 'Подготовка к экзамену')
def exams_handler(message):
    user_id = user_ids[message.chat.id]
    response = requests.get(API_URL.format(user_id))
    response_json = response.json()
    subjects = response_json['user']['items']

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for subject in subjects:
        markup.add(types.KeyboardButton(subject))
    markup.add(types.KeyboardButton('Вернуться в главное меню'))
    bot.send_message(message.chat.id, 'Выберите предмет:', reply_markup=markup)

    def get_exam_materials(subject, user_id):
        response = requests.get(API_URL.format(user_id))
        student = response.json().get('user')
        materials = student['materials'].get(subject)
        if materials is None:
            return 'Извините, материалы для этого предмета еще не добавлены'

        lectures = materials.get('lectures', [])
        textbooks = materials.get('textbooks', [])
        problems = materials.get('problems', [])

        result_str = f"Материалы по {subject}:\n\n"
        result_str += f"Лекции:\n"
        if lectures:
            for lecture in lectures:
                result_str += f"• {lecture}\n"
        else:
            result_str += "Материалы не найдены\n"

        result_str += f"\nУчебники:\n"
        if textbooks:
            for textbook in textbooks:
                result_str += f"• {textbook}\n"
        else:
            result_str += "Материалы не найдены\n"

        result_str += f"\nЗадачи:\n"
        if problems:
            for problem in problems:
                result_str += f"• {problem}\n"
        else:
            result_str += "Материалы не найдены\n"

        return result_str

    @bot.message_handler(func=lambda message: message.text in subjects)
    def send_exam_materials(message):
        exam_materials_str = get_exam_materials(message.text, user_id)
        try:
            exam_materials = json.loads(exam_materials_str)
        except json.decoder.JSONDecodeError:
            bot.send_message(message.chat.id, exam_materials_str)
            return
        result_str = f"<b>Материалы по {message.text}:</b>\n\n"
        for category, materials in exam_materials.items():
            result_str += f"<b>{category}:</b> {materials}\n"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Вернуться в главное меню'))
        bot.send_message(message.chat.id, result_str, parse_mode='HTML', reply_markup=markup)

    @bot.message_handler(func=lambda message: True)
    def text_handler(message):
        if message.text == 'Вернуться в главное меню':
            bot.send_message(message.from_user.id, 'Вы вернулись в главное меню!', reply_markup=get_main_menu())
        else:
            bot.send_message(message.chat.id,
                             'Извините, я не понимаю вас. Попробуйте еще раз или выберите другую команду.')


@bot.message_handler(func=lambda message: message.text == 'Предстоящие события')
def events_command(message):
    try:
        response = requests.get(EVENTS_URL)
        data = response.json()
        events = [event['question'] for event in data['events']]
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for event in events:
            keyboard.add(types.KeyboardButton(event))
        keyboard.add(types.KeyboardButton('Вернуться в главное меню'))
        bot.reply_to(message, "Выберите предстоящие события:", reply_markup=keyboard)
    except requests.exceptions.RequestException:
        bot.reply_to(message, "Ошибка при получении данных с сервера")


@bot.message_handler(func=lambda message: True)
def events_message(message):
    try:
        response = requests.get(EVENTS_URL)
        data = response.json()
        events = {event['question']: event['answer'] for event in data['events']}
        answer = events.get(message.text)
        if answer:
            bot.reply_to(message, answer, reply_markup=get_events_keyboard())
        else:
            bot.reply_to(message, "Ответ не найден", reply_markup=get_events_keyboard())
    except requests.exceptions.RequestException:
        bot.reply_to(message, "Ошибка при получении данных с сервера")


def get_events_keyboard():
    try:
        response = requests.get(EVENTS_URL)
        data = response.json()
        questions = [event['question'] for event in data['events']]
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for question in questions:
            keyboard.add(types.KeyboardButton(question))
        keyboard.add(types.KeyboardButton('Вернуться в главное меню'))
        return keyboard
    except requests.exceptions.RequestException:
        return None


@bot.message_handler(func=lambda message: message.text == 'Вернуться в главное меню')
def back_to_main_menu(message):
    bot.reply_to(message, 'Вы в главном меню!', reply_markup=get_main_menu())


def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('/start'))
    markup.add(types.KeyboardButton('Расписание'))
    markup.add(types.KeyboardButton('Экзамены'))
    markup.add(types.KeyboardButton('Оценки'))
    markup.add(types.KeyboardButton('FAQs'))
    markup.add(types.KeyboardButton('Оставить отзыв'))
    markup.add(types.KeyboardButton('Подготовка к экзамену'))
    markup.add(types.KeyboardButton('Предстоящие события'))
    return markup


bot.polling(non_stop=True)
