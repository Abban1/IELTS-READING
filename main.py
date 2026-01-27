from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from datetime import datetime

from utils import (
    generate_section_1,
    generate_section_2,
    generate_section_3
)
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = "ielts_db"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
ielts_reading_tests = db["ielts_reading_tests"]


app = FastAPI(title="IELTS Reading Test Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "IELTS Reading Test Generator API"}


@app.get("/section-1", response_class=PlainTextResponse)
def section_1(level: str = Query("Academic"), difficulty: str = Query("Medium")):
    return generate_section_1(level, difficulty)

@app.get("/section-2", response_class=PlainTextResponse)
def section_2(level: str = Query("Academic"), difficulty: str = Query("Hard")):
    return generate_section_2(level, difficulty)

@app.get("/section-3", response_class=PlainTextResponse)
def section_3(level: str = Query("Academic"), difficulty: str = Query("Hard")):
    return generate_section_3(level, difficulty)


@app.get("/full-test", response_class=PlainTextResponse)
def full_test(level: str = Query("Academic"), difficulty: str = Query("Hard")):
    section1 = generate_section_1(level, difficulty)
    section2 = generate_section_2(level, difficulty)
    section3 = generate_section_3(level, difficulty)

    full_test_text = (
        "IELTS READING TEST\n"
        "Time allowed: 60 minutes\n\n"
        f"{section1}\n\n"
        + "=" * 60 + "\n\n"
        f"{section2}\n\n"
        + "=" * 60 + "\n\n"
        f"{section3}"
    )

    try:
        ielts_reading_tests.insert_one({
            "level": level,
            "difficulty": difficulty,
            "full_test_text": full_test_text,
            "section_1": section1,
            "section_2": section2,
            "section_3": section3,
            "created_at": datetime.utcnow()
        })
    except Exception as e:
        return f"Error storing test in MongoDB: {str(e)}"

    return full_test_text
