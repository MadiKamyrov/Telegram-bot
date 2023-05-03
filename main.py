# -*- coding: utf-8 -*-
import telebot
from telebot import types
import json

from db import students_collection
from feedback import save_feedback
from exam_prep import *

bot = telebot.TeleBot('5901618580:AAGaBkjDds36ZuTpfKL20hb0TbH474U14Ro')

user_ids = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = get_main_menu()
    if message.chat.id not in user_ids:
        user_ids[message.chat.id] = ''
    bot.reply_to(message, "Добро пожаловать! я ваш ассистент, пожалуйста введите свой стунденческий билет: ",
                 reply_markup=keyboard)
    bot.register_next_step_handler(message, process_user_id)


def process_user_id(message):
    user_id = message.text
    user_ids[message.chat.id] = user_id
    bot.reply_to(message, f"Ваш студенческий билет: {user_id}")


@bot.message_handler(func=lambda message: message.text == 'Расписание')
def send_schedule(message):
    if message.chat.id not in user_ids:
        bot.reply_to(message, "Пожалуйста, введите ваш стундеческий билет:")
        bot.register_next_step_handler(message, process_user_id)
    else:
        user_id = user_ids[message.chat.id]
        student_data = students_collection.find_one({'user_id': int(user_id)})
        if student_data is None:
            bot.reply_to(message, "У вас пока нет расписания.")
        else:
            schedule_text = f"Расписание на следующую неделю:\n\n" \
                            f"Понедельник:\n" \
                            f"{student_data['schedule']['Понедельник'][0]['предмет']} {student_data['schedule']['Понедельник'][0]['время']}\n" \
                            f"{student_data['schedule']['Понедельник'][1]['предмет']} {student_data['schedule']['Понедельник'][1]['время']}\n\n" \
                            f"Вторник:\n" \
                            f"{student_data['schedule']['Вторник'][0]['предмет']} {student_data['schedule']['Вторник'][0]['время']}\n" \
                            f"{student_data['schedule']['Вторник'][1]['предмет']} {student_data['schedule']['Вторник'][1]['время']}\n\n" \
                            f"Среда:\n" \
                            f"{student_data['schedule']['Среда'][0]['предмет']} {student_data['schedule']['Среда'][0]['время']}\n" \
                            f"{student_data['schedule']['Среда'][1]['предмет']} {student_data['schedule']['Среда'][1]['время']}\n\n" \
                            f"Четверг:\n" \
                            f"{student_data['schedule']['Четверг'][0]['предмет']} {student_data['schedule']['Четверг'][0]['время']}\n" \
                            f"{student_data['schedule']['Четверг'][1]['предмет']} {student_data['schedule']['Четверг'][1]['время']}\n\n" \
                            f"Пятница:\n" \
                            f"{student_data['schedule']['Пятница'][0]['предмет']} {student_data['schedule']['Пятница'][0]['время']}\n" \
                            f"{student_data['schedule']['Пятница'][1]['предмет']} {student_data['schedule']['Пятница'][1]['время']}\n\n"

            bot.reply_to(message, schedule_text)


@bot.message_handler(func=lambda message: message.text == 'Оценки')
def get_grades(message):
    if message.chat.id not in user_ids:
        bot.reply_to(message, "Пожалуйста, введите свой студенческий билет:")
        bot.register_next_step_handler(message, process_user_id)
    else:
        user_id = user_ids[message.chat.id]
        student_data = students_collection.find_one({'user_id': int(user_id)})
        if student_data is None:
            bot.reply_to(message, "You don't have any grades yet.")
        else:
            grades_text = f"Ваши текущие оценки:\n\n" \
                          f"Алгоритмы и структуры данных: {student_data['grades']['Алгоритмы и структуры данных']} баллов\n" \
                          f"Разработка мобильных приложений: {student_data['grades']['Разработка мобильных приложений']} баллов\n" \
                          f"Математика III: {student_data['grades']['Математика III']} баллов\n" \
                          f"Объектно-ориентированное программирование: {student_data['grades']['Объектно-ориентированное программирование']} баллов\n" \
                          f"Разработка игр: {student_data['grades']['Разработка игр']} баллов\n\n"
            bot.reply_to(message, grades_text)


@bot.message_handler(func=lambda message: message.text == 'Экзамены')
def send_exams(message):
    exams_text = "Exams:\n\n" \
                 "Алгоритмы и структура данных - Май 1, 8:00\n" \
                 "Математика III - Май 5, 12:00\n" \
                 "Разработка мобильных приложений - Май 10, 14:00\n" \
                 "Объектно-ориентированное программирование - Май 15, 10:00\n" \
                 "Разработка игр - Май 20, 13:00\n\n"
    bot.reply_to(message, exams_text)


FAQS = {
    "Кто такой эдвайзер?": "Эдвайзер это преподователь, выполняющий функции консультанта по академическим вопросам во время учебы. Эдвайзер оказывает содействия студенту в выборе дисциплин при составлении ИУПа, разъясняет правила кредитной технологии обучения и т.д. Эдвайзера назначет дирекция Университета",
    "Как авторизоваться в учебном портале?": "Войти в образовательный портал https://sso.satbayev.university и активировать своюучетную запись используя в качестве логина Ваш ИИН и тот же пароль, что и при подачедокументов в приёмную комиссию https://kb.satbayev.university. При входе в Учебныйпортал, система попросит вас сменить пароль на более сложный, и отобразит требованияк паролю. Введите новый пароль, запомните его и нажмите «Сохранить»!ближайшее время после успешного входа в Учебный портал, Вам станет доступнойсистема дистанционного образования Polytechonline и функционал облачных сервисовMicrosoft 365. Обязательно загрузите своё документальное фото и скачайте приложениеMicrosoft Teams на свой мобильный телефон.",
    "Как студент может получить справку с места учебы?": "Университет выдает справки с места учебы, которые подтверждают их академическую занятость в ВУЗе. Справки с места учебы выдаются только после издания Приказа о зачислении:  справка по воинскому учету (для отсрочки от армии) – 341 кабинет ГУК. справка для получения пособия (по инвалидности, многодетные семьи ит.д.) – 407А кабинет НК. справка в общежитие или в банк (для банковской карты), в школу, дляпрактики и т.д. – окно №1 Офиса регистратора. Справки «По месту требования» не выдаются.",
    "Как открыть банковскую карту для стипендии? Когда я буду получать стипендию?": "Для получения стипендии обладателям государственного гранта необходимо обратиться Халык Банк и открыть банковскую карту для начисления стипендии. Если Вам нет 18 лет, то сопровождение родителя обязательно. 20-значный номер счета, привязанного к карте, необходимо сообщить своему эдвайзеру до 15 сентября. Стипендия за сентябрь поступит на карту студента в октябре, последующие – в конце каждого месяца. Первый (осенний) семестр стипендия начисляется всем обладателям государственного гранта, во втором (весеннем) семестре – по результатам зимней сессии. Помните! Вы теряете стипендию, если у Вас будет хоть одна итоговая оценка «С» и ниже (70 и менее баллов). Стипендия может быть восстановлена в следующем учебном семестре при условии успешной сдачи сессии.",
    "Как родителям узнать об успеваемости и посещаемости занятий студента?": "Родители студента могут узнать об успеваемости и посещаемости своего ребёнка в образовательном портале (со страницы студента, через его логин и пароль). В обязанности эдвайзера не входит уведомление родителей об успеваемости студента, но эдвайзер может ответить на вопросы родителей по запросу.",
    "Есть ли какие-то пособия для студентов-сирот, инвалидов, из многодетных или малоимущихсемей?": "Да, такая помощь предусматривается при предоставлении соответствующих документов. Более подробно по таким вопросам вы можете обращаться в Департамент по студенческим вопросам (Социальный сектор, 407А кабинет НК).",
    "Что делать, если пропустил занятия?": "По правилам КТО допускается всего 20% пропусков по одной дисциплине за семестр, если дисциплина пятикредитная – 9 пропусков, если трехкредитная – 6 (не считая самостоятельной работы). Журнал в портале заполняется преподавателем по факту. Пропуски из журнала не удаляются. Если вы заболели, то справки не принимаются, так как пропуски по болезни входят в допустимые 20%. Заявление с просьбой убрать пропуски не принимаются. Пропуски свыше 20% не дают допуска к экзамену.",
    # Add more questions and answers here
}


@bot.message_handler(func=lambda message: message.text == 'FAQs')
def faq_command(message):
    questions = list(FAQS.keys())
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for question in questions:
        keyboard.add(types.KeyboardButton(question))
    keyboard.add(types.KeyboardButton('Вернуться в главное меню'))
    bot.reply_to(message, "Пожалуйста выберите вопрос:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in FAQS)
def faq_message(message):
    answer = FAQS[message.text]
    bot.reply_to(message, answer, reply_markup=get_faq_keyboard())


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


@bot.message_handler(func=lambda message: message.text == 'Подготовка к экзамену')
def exams_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    subjects = get_exam_subjects()
    for subject in subjects:
        markup.add(types.KeyboardButton(subject))
    markup.add(types.KeyboardButton('Вернуться в главное меню'))
    bot.send_message(message.chat.id, 'Выберите предмет:', reply_markup=markup)
    @bot.message_handler(func=lambda message: message.text in get_exam_subjects())
    def send_exam_materials(message):
        exam_materials_str = get_exam_materials(message.text)
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


EVENTS = {
    "Турнир по футболу": "Привет, друзья!\n\nМы рады пригласить вас на наш любимый спортивный праздник - турнир по футболу среди студентов Satbayev University! 🏆\n\n14 мая мы собираемся на поле внутри кампуса, чтобы продемонстрировать свои спортивные навыки и бороться за заслуженное признание от своих однокурсников. Команды будут состоять из 11 игроков, а матчи - в формате командных сражений. ⚽️\n\nКонечно же, на турнире мы не забываем и о развлечениях! Различные конкурсы, розыгрыши призов и другие интересные активности помогут вам провести время с пользой для здоровья и души, а также укрепить дружеские связи с другими студентами. 🎉\n\nНе упустите свой шанс стать настоящим чемпионом, показать свои спортивные способности и встретиться с новыми людьми! Регистрируйте свою команду на официальном сайте Satbayev University и ждем вас на поле 14 мая! ⚽️👊\n\nДо встречи на турнире! 😉",
    "Satbayev Fest": "🎉 Друзья, мы рады пригласить вас на наш главный праздник университета - Satbayev Fest! Это событие, которое объединит всех студентов, преподавателей и сотрудников вокруг общей цели - провести время с пользой и насладиться яркими впечатлениями. \n\nВ этом году Satbayev Fest будет еще более разнообразным и интересным! Вас ждут:\n\n🎤 Концерты известных артистов, которые порадуют вас своим творчеством и позволят насладиться музыкой в отличной компании;\n🎨 Выставки работ студентов, которые демонстрируют высокий уровень нашего образования и множество интересных проектов;\n🛍️ Ярмарка ремесел, на которой можно приобрести уникальные изделия ручной работы, а также попробовать национальные блюда;\n🎉 Различные конкурсы и активности, которые помогут вам познакомиться с новыми людьми, найти новых друзей и провести время с пользой для здоровья и души.\n\nSatbayev Fest - это отличная возможность не только получить новые знания и впечатления, но и почувствовать себя частью большой и дружной команды. Мы ждем вас на кампусе университета и обещаем, что вы не пожалеете о своем решении посетить Satbayev Fest!\n\nНе пропустите самое яркое событие университета, дата проведения - 5 июня. Следите за новостями на официальном сайте Satbayev University! 🎉🎨🎤🛍️",
    "День победы!": "🌺 Дорогие друзья!\n\n9 мая - это день, который важен для каждого из нас. Это день, когда мы отмечаем победу над нацизмом во Второй Мировой войне и почтили память тех, кто жертвовал своей жизнью за нашу свободу.\n\n❤️ В этот день мы хотим показать нашу благодарность и уважение к героям и ветеранам, которые отстояли мир и свободу нашей страны.\n\n🎉 Поэтому, в честь этого знаменательного события, в университете пройдет праздничное мероприятие, которое объединит студентов, преподавателей и сотрудников вокруг общей цели - чтоб вместе отметить этот день и почтить память героев.\n\n👀 Вас ждут:\n\nСочувственные выступления и поздравления от ветеранов;\nИнтересные конкурсы и игры;\nФотозона для селфи;\nВозможность поучаствовать в благотворительной акции и проявить свою заботу о ветеранах;\n❤️ Приходите в этот день к нам в университет, чтобы вместе отметить важное событие, показать свою благодарность к героям, и провести время с пользой для души и сердца.\n\nС праздником Победы! 🎉🌺💪",
}


@bot.message_handler(func=lambda message: message.text == 'Предстоящие события')
def events_command(message):
    events = list(EVENTS.keys())
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for event in events:
        keyboard.add(types.KeyboardButton(event))
    keyboard.add(types.KeyboardButton('Вернуться в главное меню'))
    bot.reply_to(message, "Выберите предстоящие события:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in EVENTS)
def events_message(message):
    answer = EVENTS[message.text]
    bot.reply_to(message, answer, reply_markup=get_events_keyboard())


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


def get_events_keyboard():
    questions = list(EVENTS.keys())
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for question in questions:
        keyboard.add(types.KeyboardButton(question))
    keyboard.add(types.KeyboardButton('Вернуться в главное меню'))
    return keyboard


def get_faq_keyboard():
    questions = list(FAQS.keys())
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for question in questions:
        keyboard.add(types.KeyboardButton(question))
    keyboard.add(types.KeyboardButton('Вернуться в главное меню'))
    return keyboard


bot.polling(non_stop=True)
