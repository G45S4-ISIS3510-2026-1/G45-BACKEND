

import firebase_admin
from firebase_admin import credentials, firestore_async

_app = None

def init_firebase(credentials_path: str):
    global _app
    if not firebase_admin._apps:
        cred = credentials.Certificate(credentials_path)
        _app = firebase_admin.initialize_app(cred)

def get_firestore_client():
    return firestore_async.client()
