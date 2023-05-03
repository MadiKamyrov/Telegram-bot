import pymongo

client = pymongo.MongoClient('mongodb+srv://madiayzhalby:kanada19@cluster0.zodb7u9.mongodb.net/test')
db = client["students_db"]
students_collection = db["students"]


def get_exam_materials(subject):
    student = students_collection.find_one({"user_id": 10})
    materials = student['materials'].get(subject)
    if materials is None:
        return 'Извините, материалы для этого предмета еще не добавлены в базу данных'

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


def get_exam_subjects():
    student = students_collection.find_one({"user_id": 10})
    subjects = list(student['materials'].keys())
    return subjects


EXAM_SUBJECTS = {
    'Алгоритмы и структуры данных': 'algorithms',
    'Математика III': 'math',
    'Разработка мобильных приложений': 'mobile',
    'Объектно-ориентированное программирование': 'oop',
    'Разработка игр': 'games',
}