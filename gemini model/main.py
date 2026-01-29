from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from datetime import datetime
import os
from dotenv import load_dotenv
from pymongo import MongoClient

from utils import (
    generate_section_1,
    generate_section_2,
    generate_section_3
)

load_dotenv()

client = MongoClient(
    os.getenv("MONGODB_URI"),
    tls=True,
    tlsAllowInvalidCertificates=True
)

db = client["ielts_db"]
ielts_tests = db["ielts_tests"]

app = FastAPI(title="IELTS Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "IELTS Generator API is running"}


# ---------- READING ----------
@app.get("/section-1", response_class=PlainTextResponse)
def section_1(level: str = "General Training", difficulty: str = "Easy"):
    return generate_section_1(level, difficulty)


@app.get("/section-2", response_class=PlainTextResponse)
def section_2(level: str = "General Training", difficulty: str = "Medium"):
    return generate_section_2(level, difficulty)


@app.get("/section-3", response_class=PlainTextResponse)
def section_3(level: str = "General Training", difficulty: str = "Hard"):
    return generate_section_3(level, difficulty)


@app.get("/full-test", response_class=PlainTextResponse)
def full_test(level: str = "General Training", difficulty: str = "Hard"):
    s1 = generate_section_1(level, difficulty)
    s2 = generate_section_2(level, difficulty)
    s3 = generate_section_3(level, difficulty)

    full_text = (
        "IELTS GENERAL TRAINING READING TEST\n"
        "Time allowed: 60 minutes\n\n"
        f"{s1}\n\n{'='*60}\n\n{s2}\n\n{'='*60}\n\n{s3}"
    )

    ielts_tests.insert_one({
        "type": "reading",
        "level": level,
        "difficulty": difficulty,
        "content": full_text,
        "created_at": datetime.utcnow()
    })

    return full_text
