import pymongo
from fastapi import FastAPI

client = pymongo.MongoClient('mongodb+srv://madiayzhalby:kanada19@cluster0.zodb7u9.mongodb.net/test')

db = client['students_db']
students_collection = db['students']
feedback_collection = db['feedback']
faqs_collection = db['FAQs']
events_collection = db['events']

app = FastAPI()

@app.get("/")
async def main():
    return {"message": "Привет"}

@app.get("/student/{user_id}")
async def get_student_by_user_id(user_id: int):
    student = students_collection.find_one({"user_id": user_id})
    if student:
        student["_id"] = str(student["_id"])
        return {"user": student}
    else:
        return {"error": "User not found"}

@app.get("/faqs")
async def get_all_faqs():
    faqs = faqs_collection.find()
    result = []
    for faq in faqs:
        faq["_id"] = str(faq["_id"])
        result.append(faq)
    return {"faqs": result}

@app.get("/events")
async def get_all_faqs():
    events = events_collection.find()
    result = []
    for event in events:
        event["_id"] = str(event["_id"])
        result.append(event)
    return {"events": result}
