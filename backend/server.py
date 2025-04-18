from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from datetime import datetime, timedelta
from flask_cors import CORS
import hashlib
import random
import threading
import time

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

blockchain = []
current_color = "#FFFFFF"
base_color = "#FFFFFF"
start_time = datetime.utcnow()

CYCLE_DURATION = 4 * 60 * 60  # 4 hours
INTERVAL_DURATION = 3 * 60    # 3 minutes


def generate_random_color():
    return "#" + ''.join(random.choices('0123456789ABCDEF', k=6))


def encrypt_color(color):
    return hashlib.sha256(color.encode()).hexdigest()


def generate_new_color(prev_color):
    encrypted = encrypt_color(prev_color)
    return "#" + encrypted[:6].upper()


def get_elapsed_time():
    return (datetime.utcnow() - start_time).total_seconds()


def get_time_left():
    time_left = CYCLE_DURATION - get_elapsed_time()
    return max(0, int(time_left))


def get_blocks():
    return blockchain[-10:]


@app.route("/add_block", methods=["POST"])
def add_block():
    global current_color
    data = request.json
    encrypted_guess = data.get("guess")
    encrypted_actual = encrypt_color(current_color)

    if encrypted_guess == encrypted_actual:
        new_block = {
            "index": len(blockchain) + 1,
            "timestamp": datetime.utcnow().isoformat(),
            "color": current_color,
            "encrypted_color": encrypted_actual
        }
        blockchain.append(new_block)
        current_color = generate_new_color(current_color)

        socketio.emit('new_block', new_block)

        return jsonify({"message": "Correct! Block added.", "block": new_block}), 200

    return jsonify({"message": "Incorrect guess."}), 400


@app.route("/current_color", methods=["GET"])
def get_current_color():
    return jsonify({"color": current_color})


@app.route("/timer", methods=["GET"])
def timer():
    return jsonify({"time_left": get_time_left()})


@app.route("/last_n_encrypted", methods=["GET"])
def get_last_n_encrypted():
    n = int(request.args.get("n", 10))
    last_n = blockchain[-n:]
    return jsonify(last_n[::-1])


@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit("init", {"color": current_color, "time_left": get_time_left(), "blockchain": get_blocks()})


def cycle_controller():
    global base_color, current_color, start_time
    while True:
        elapsed = get_elapsed_time()
        if elapsed >= CYCLE_DURATION:
            base_color = generate_random_color()
            current_color = base_color
            start_time = datetime.utcnow()
            print("New cycle started with base color:", base_color)
            socketio.emit('new_cycle', {"base_color": base_color})
        time.sleep(10)  # check every 10 seconds


if __name__ == '__main__':
    base_color = generate_random_color()
    current_color = base_color
    start_time = datetime.utcnow()
    threading.Thread(target=cycle_controller, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)