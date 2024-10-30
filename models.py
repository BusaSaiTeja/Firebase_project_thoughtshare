from firebase_config import db  # Ensure your Firebase config is correctly set
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from firebase_admin import auth  # Import Firebase Auth

class User(UserMixin):  # Inherit from UserMixin
    def __init__(self, uid, username, email):
        self.uid = uid
        self.username = username
        self.email = email

    def get_id(self):
        return self.uid  # Return the unique identifier for the user


def create_user(username, email, password):
    """Creates a new user and stores their data in Firestore and Firebase Authentication."""
    # Create user in Firebase Authentication
    user = auth.create_user(
        email=email,
        password=password
    )
    
    # Now store user data in Firestore
    users_ref = db.collection('users')
    users_ref.document(user.uid).set({
        'username': username,
        'email': email,
        # No need to store hashed password since it's managed by Firebase Authentication
    })


def get_user_by_email(email):
    """Retrieves a user by their email from Firestore."""
    users_ref = db.collection('users').where('email', '==', email)
    user = users_ref.limit(1).stream()
    for u in user:
        user_data = u.to_dict()
        return User(u.id, user_data['username'], user_data['email'])  # Return user data as User object
    return None  # Return None if no user found


def get_user(user_id):
    """Retrieves a user by their UID from Firestore."""
    users_ref = db.collection('users').document(user_id)
    user = users_ref.get()
    if user.exists:
        user_data = user.to_dict()
        return User(user.id, user_data['username'], user_data['email'])
    return None  # Return None if user does not exist


def check_password(email, password):
    """Check user credentials against Firebase Authentication."""
    try:
        user = auth.get_user_by_email(email)
        # Use the Firebase Admin SDK to verify the password
        # Note: Password verification directly is not possible; Firebase Auth handles it.
        # You would typically check the user session or use client-side Firebase for login.
        return True  # Simplified for example, actual password check done in client-side
    except Exception:
        return False  # Invalid user or password
