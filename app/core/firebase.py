

import firebase_admin
from firebase_admin import credentials, firestore_async, messaging
from firebase_admin.exceptions import FirebaseError

_app = None

def init_firebase(credentials_path: str):
    global _app
    if not firebase_admin._apps:
        cred = credentials.Certificate(credentials_path)
        _app = firebase_admin.initialize_app(cred)

def get_firestore_client():
    return firestore_async.client()


def check_fcm_token(token):
    message = messaging.Message(token=token)
    
    try:
        # dry_run=True validates the token without sending an actual push
        messaging.send(message, dry_run=True)
        print("Token is valid.")
        return True
        
    except messaging.UnregisteredError:
        # Token is invalid / app was uninstalled. Safe to delete from database.
        print("Token is expired or unregistered.")
        return False
        
    except messaging.SenderIdMismatchError:
        # Token belongs to a different Firebase project console
        print("Token does not match this project's Sender ID.")
        return False
        
    except FirebaseError as e:
        # Catch-all for other Firebase issues (e.g., QUOTA_EXCEEDED, INTERNAL)
        print(f"Firebase error occurred: {e.code} - {e}")
        return False
        
    except Exception as e:
        print(f"Generic error occurred: {e}")
        return False


