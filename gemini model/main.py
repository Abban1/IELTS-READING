from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from datetime import datetime
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from fastapi import HTTPException

from utils import (
    generate_section_1,
    generate_section_2,
    generate_section_3
)
section_map = {
    "section1": generate_section_1,
    "section2": generate_section_2,
    "section3": generate_section_3,
}
load_dotenv()

client = MongoClient(
    os.getenv("MONGODB_URI")
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



@app.get("/full-test", response_class=PlainTextResponse)
def full_test(
    level: str = "General Training",
    difficulty: str = "Hard",
    section: str | None = None
):
    try:
        
        if section:
            func = section_map[section.lower()]  
            return func(level, difficulty)

       
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

    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid section")

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Test generation failed: {str(e)}"
        )
