
from pymongo import MongoClient

# Replace <your_password> with your actual MongoDB Atlas password before using
MONGO_URI = "mongodb+srv://gyanvi19:Gyanvi%402025@coldchainai.50wng0j.mongodb.net/?retryWrites=true&w=majority&appName=ColdchainAI"

client = MongoClient(MONGO_URI)
db = client["ColdchainAI"]
collection = db["FreshScoreLogs"]

def log_freshscore(data):
    result = collection.insert_one(data)
    print(f"✅ Logged to MongoDB with ID: {result.inserted_id}")
