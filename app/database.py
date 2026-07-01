from pymongo import MongoClient
from app.config import MONGODB_URI, DATABASE_NAME

client = MongoClient(MONGODB_URI)

db = client[DATABASE_NAME]

documents_collection = db["documents"]

history_collection = db["history"]