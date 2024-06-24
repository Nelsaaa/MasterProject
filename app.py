from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os
import jwt
import datetime

app = Flask(__name__)
CORS(app)

# Retrieve the secret key from the environment variable
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))

# Configure SQLAlchemy with a SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/nelsayago/MasterProject2/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

# Define the Photo model
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    photo_url = db.Column(db.String(200), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not (username and email and password):
        return jsonify({'msg': 'All fields are required'}), 400

    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({'msg': 'User already exists'}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'msg': 'Registration successful'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.secret_key)

        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }

        return jsonify({'user': user_data, 'token': token, 'msg': 'Login successful'})
    else:
        return jsonify({'msg': 'Invalid username or password'}), 401

@app.route('/logout')
def logout():
    session.clear()
    return jsonify({'msg': 'Logout successful'})

@app.route('/photos', methods=['POST'])
def upload_photo():
    data = request.get_json()
    token = request.headers.get('Authorization').split(" ")[1]
    try:
        decoded_token = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        user_id = decoded_token['user_id']
    except Exception as e:
        return jsonify({'msg': 'Invalid token'}), 401

    photo_url = data.get('photo_url')
    if not photo_url:
        return jsonify({'msg': 'Photo URL is required'}), 400

    new_photo = Photo(user_id=user_id, photo_url=photo_url)
    db.session.add(new_photo)
    db.session.commit()

    return jsonify({'msg': 'Photo uploaded successfully'})

@app.route('/photos', methods=['GET'])
def get_photos():
    token = request.headers.get('Authorization').split(" ")[1]
    try:
        decoded_token = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        user_id = decoded_token['user_id']
    except Exception as e:
        return jsonify({'msg': 'Invalid token'}), 401

    photos = Photo.query.filter_by(user_id=user_id).all()
    photo_urls = [photo.photo_url for photo in photos]

    return jsonify({'photos': photo_urls})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
