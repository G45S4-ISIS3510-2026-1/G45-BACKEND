

import firebase_admin
from firebase_admin import credentials, firestore_async, messaging

_app = None

def init_firebase(credentials_path: str):
    global _app
    if not firebase_admin._apps:
        cred = credentials.Certificate(credentials_path)
        _app = firebase_admin.initialize_app(cred)

def get_firestore_client():
    return firestore_async.client()

def check_fcm_token(token):
    # 2. Create a message with the dry_run flag
    message = messaging.Message(
        token=token,
    )
    
    try:
        # 3. Attempt to send (dry_run=True ensures no notification is actually sent)
        messaging.send(message, dry_run=True)
        print("Token is valid.")
        return True
    except messaging.ApiCallError as e:
        # 4. Handle specific error codes
        # UNREGISTERED (404) or INVALID_ARGUMENT (400) usually mean the token is bad
        print(f"Token validation failed: {e.code}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
