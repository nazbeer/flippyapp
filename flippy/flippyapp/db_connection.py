from pymongo import MongoClient

def connect_to_mongo():
    try:
        client = MongoClient("mongodb://127.0.0.1:27017")
        db = client.flippydb
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
        return None