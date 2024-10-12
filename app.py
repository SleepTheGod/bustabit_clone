from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Bet
from config import Config
import random

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_user', methods=['POST'])
def create_user():
    user_address = request.json.get('address')
    if user_address:
        new_user = User(address=user_address)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created"}), 201
    return jsonify({"message": "Invalid data"}), 400

@app.route('/place_bet', methods=['POST'])
def place_bet():
    user_id = request.json.get('user_id')
    amount = request.json.get('amount')
    multiplier = random.uniform(2.0, 10.0)  # Random multiplier for the example
    new_bet = Bet(user_id=user_id, amount=amount, multiplier=multiplier)
    db.session.add(new_bet)
    db.session.commit()
    return jsonify({"message": "Bet placed", "multiplier": multiplier}), 201

@socketio.on('bet_event')
def handle_bet_event(data):
    socketio.emit('update_bets', data, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)
