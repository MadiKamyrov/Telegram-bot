from db import *

new_student = {
    "user_id": 15,
    "name": "Елтай Камыров",
    "gpa": 3.28,
    "schedule": {
        "Понедельник": [
            {
                "предмет": "Компьютерные сети",
                "время": "10:00-12:00"
            },
            {
                "предмет": "Дискретная математика",
                "время": "14:00-16:00"
            }
        ],
        "Вторник": [
            {
                "предмет": "Теория информации",
                "время": "12:00-14:00"
            },
            {
                "предмет": "Функциональное программирование",
                "время": "16:00-18:00"
            }
        ],
        "Среда": [
            {
                "предмет": "Компьютерные сети",
                "время": "10:00-12:00"
            },
            {
                "предмет": "Дискретная математика",
                "время": "14:00-16:00"
            }
        ],
        "Четверг": [
            {
                "предмет": "",
                "время": ""
            },
            {
                "предмет": "",
                "время": ""
            }
        ],
        "Пятница": [
            {
                "предмет": "Сетевые технологии программирования",
                "время": "10:00-12:00"
            },
            {
                "предмет": "Теория информации",
                "время": "14:00-16:00"
            }
        ]
    },
    "grades": {
        "Сетевые технологии программирования": 81,
        "Компьютерные сети": 80,
        "Дискретная математика": 92,
        "Функциональное программирование": 90,
        "Теория информации": 85
    }
}

# добавляем объект в базу данных
result = students_collection.insert_one(new_student)