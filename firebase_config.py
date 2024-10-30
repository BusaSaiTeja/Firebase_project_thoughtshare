import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('firebase.json')  # Update this path
firebase_admin.initialize_app(cred)

# Create Firestore client
db = firestore.client()
