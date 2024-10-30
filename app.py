from flask import Flask, redirect, url_for
from flask_login import LoginManager
from routes import routes  # Import routes
from firebase_config import db  # Import db from firebase_config
import firebase_admin

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'routes.login'

@login_manager.user_loader
def load_user(user_id):
    from models import get_user  # Import here to avoid circular import
    return get_user(user_id)  # Call get_user from models.py

@app.route('/')
def index():
    return redirect(url_for('routes.login'))

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
