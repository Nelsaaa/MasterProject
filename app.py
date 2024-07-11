import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import torch
from PIL import Image
from pathlib import Path
import numpy as np

# Add the directory containing `first_nb_project_garbage_class.py` to the sys.path
model_dir = '/Users/nelsayago/MasterProject2/Innov project'
sys.path.append(model_dir)

# Print the sys.path to ensure the path is added correctly
print("sys.path:", sys.path)

try:
    # Now you can import the module
    from first_nb_project_garbage_class import (
        test_transformations, predict_image, calculate_recycling_score, load_model
    )
    loaded_model = load_model('model.pth')
except ImportError as e:
    print(f"Error importing module: {e}")
    sys.exit(1)

app = Flask(__name__)
CORS(app)

app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'mysecretkey')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/nelsayago/MasterProject2/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

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
        }, app.secret_key, algorithm="HS256")

        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }

        return jsonify({'user': user_data, 'token': token, 'msg': 'Login successful'})
    else:
        return jsonify({'msg': 'Invalid username or password'}), 401

@app.route('/analyze-photo', methods=['POST'])
def analyze_photo():
    try:
        if 'photo' not in request.files:
            app.logger.error('No photo part in the request')
            return jsonify({'msg': 'No photo part in the request'}), 400

        file = request.files['photo']
        img = Image.open(file.stream).convert('RGB')

        # Debugging: Save and compare images
        img.save('debug_flask_image.jpg')
        app.logger.info('Image saved for debugging: debug_flask_image.jpg')

        example_image = test_transformations(img)
        app.logger.info(f"Transformed image tensor: {example_image}")

        loaded_model.eval()  # Ensure the model is in evaluation mode
        predicted_labels = predict_image(example_image, loaded_model)
        recycling_score = calculate_recycling_score(predicted_labels)

        # Debugging prints
        app.logger.info(f"Predicted Labels: {predicted_labels}")
        app.logger.info(f"Recycling Score: {recycling_score}")

        return jsonify({
            'predicted_labels': {k: float(v) for k, v in predicted_labels.items()},
            'recycling_score': float(recycling_score)
        })
    except Exception as e:
        app.logger.error(f"Error processing the image: {e}")
        return jsonify({'msg': 'Error processing the image'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
