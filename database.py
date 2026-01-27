import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = "ielts_db"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

ielts_reading_tests = db["ielts_reading_tests"]
