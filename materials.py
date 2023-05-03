import pymongo

client = pymongo.MongoClient('mongodb+srv://madiayzhalby:kanada19@cluster0.zodb7u9.mongodb.net/test')

db = client['students_db']
student_collections = db['students']

materials = [
    {
        "subject": "Алгоритмы и структуры данных",
        "lecture": [
            {
                "title": "Введение в алгоритмы и структуры данных",
                "url": "https://example.com/lecture1.pdf"
            },
            {
                "title": "Сложность алгоритмов",
                "url": "https://example.com/lecture2.pdf"
            }
        ],
        "textbook": [
            {
                "title": "Алгоритмы: построение и анализ",
                "url": "https://example.com/textbook1.pdf"
            },
            {
                "title": "Структуры данных и алгоритмы",
                "url": "https://example.com/textbook2.pdf"
            }
        ],
        "problem": [
            {
                "title": "Сортировка пузырьком",
                "url": "https://example.com/problem1.pdf"
            },
            {
                "title": "Поиск подстроки в строке",
                "url": "https://example.com/problem2.pdf"
            }
        ]
    },
    {
        "subject": "Математика III",
        "lecture": [
            {
                "title": "Линейная алгебра",
                "url": "https://example.com/lecture3.pdf"
            },
            {
                "title": "Дифференциальные уравнения",
                "url": "https://example.com/lecture4.pdf"
            }
        ],
        "textbook": [
            {
                "title": "Высшая математика",
                "url": "https://example.com/textbook3.pdf"
            },
            {
                "title": "Дифференциальные уравнения",
                "url": "https://example.com/textbook4.pdf"
            }
        ],
        "problem": [
            {
                "title": "Определители",
                "url": "https://example.com/problem3.pdf"
            },
            {
                "title": "Матрицы",
                "url": "https://example.com/problem4.pdf"
            }
        ]
    },
    {
        "subject": "Разработка мобильных приложений",
        "lecture": [
            {
                "title": "Основы разработки мобильных приложений",
                "url": "https://example.com/lecture5.pdf"
            },
            {
                "title": "UI/UX дизайн для мобильных приложений",
                "url": "https://example.com/lecture6.pdf"
            }
        ],
        "textbook": [
            {
                "title": "Android Programming: The Big Nerd Ranch Guide",
                "url": "https://example.com/textbook5.pdf"
            },
            {
                "title": "iOS Programming: The Big Nerd Ranch Guide",
                "url": "https://example.com/textbook6.pdf"
            }
        ],
        "problem": [
            {
                "title": "Разработка приложения для Android",
                "url": "https://example.com/problem5.pdf"
            },
            {
                "title": "Разработка приложения для iOS",
                "url": "https://example.com/problem6.pdf"
            }
        ]
    },
    {
        "subject": "Объектно-ориентированное программирование",
        "lectures": [
            {
                "title": "Введение в ООП",
                "url": "https://www.youtube.com/watch?v=9BPR-YNvKfE"
            },
            {
                "title": "Наследование и полиморфизм",
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            }
        ],
        "textbooks": [
            {
                "title": "Объектно-ориентированное программирование",
                "author": "Бобренко И.В.",
                "year": 2015,
                "publisher": "Питер"
            },
            {
                "title": "Паттерны проектирования",
                "author": "Gamma E., Helm R., Johnson R., Vlissides J.",
                "year": 1995,
                "publisher": "Addison-Wesley"
            }
        ],
        "problems": [
            {
                "problem": "Реализовать иерархию классов для геометрических фигур",
                "solution": "https://github.com/example/oop-geometry"
            },
            {
                "problem": "Написать программу для банковской системы",
                "solution": "https://github.com/example/oop-banking"
            }
        ]
    }
]


filter = {"user_id": 15}
update = {
    "$set": {
        "materials.Алгоритмы и структуры данных": {
            "lectures": ["Основные алгоритмы и структуры данных", "Алгоритмы сортировки"],
            "textbooks": ["Алгоритмы и структуры данных в Python", "Основы алгоритмизации"],
            "problems": ["Работа с массивами и списками", "Поиск и сортировка"]
        },
        "materials.Математика III": {
            "lectures": ["Дифференциальные уравнения", "Теория вероятностей"],
            "textbooks": ["Математический анализ", "Теория вероятностей и статистика"],
            "problems": ["Решение дифференциальных уравнений", "Расчет вероятностей"]
        },
        "materials.Разработка мобильных приложений": {
            "lectures": ["Android разработка", "iOS разработка"],
            "textbooks": ["Разработка мобильных приложений на Android", "iOS приложения для начинающих"],
            "problems": ["Разработка приложения для Android", "Разработка приложения для iOS"]
        },
        "materials.Объектно-ориентированное программирование": {
            "lectures": ["ООП в Python", "Классы и объекты", "Наследование и полиморфизм"],
            "textbooks": ["Python для начинающих", "Изучение ООП на примерах"],
            "problems": ["Наследование в Python", "Полиморфизм в ООП"]
        },
        "materials.Разработка игр": {
            "lectures": ["Геймдизайн", "Разработка игр на Unity"],
            "textbooks": ["Игровая индустрия", "Разработка игр на Unity для начинающих"],
            "problems": ["Создание игрового уровня", "Реализация геймплея"]
        }
    }
}
result = student_collections.update_one(filter, update)
