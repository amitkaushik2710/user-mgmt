import firebase_admin
from firebase_admin import credentials, firestore
from core.config import settings

class Database:
    client: firestore.client = None
    collection = None

database = Database()

async def connect_to_firestore():
    cred = credentials.Certificate(settings.FIRESTORE_JSON_PATH)
    firebase_admin.initialize_app(cred)
    database.client = firestore.client()
    database.collection = database.client.collection(settings.FIRESTORE_COLLECTION_NAME)  

def get_database():
    return database
