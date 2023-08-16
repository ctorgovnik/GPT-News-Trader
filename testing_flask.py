from flask import Flask, request, jsonify
import time
import multiprocessing
from flask_cors import CORS
from multiprocessing import Array, Process, Value, Lock
from multiprocessing import Manager


app = Flask(__name__)
CORS(app)


@app.route('/set-trading-mode', methods=['POST'])
def set_trading_mode():
    mode = request.json.get('mode')
    if mode in ["paper", "live"]:
        with lock:
            trading_mode.value = mode
        return jsonify({"status": "success", "message": f"Mode set to {mode}"}), 200
    return jsonify({"status": "error", "message": "Invalid mode"}), 400


def print_trading_mode(trading_mode, lock):
    while True:
        with lock:
            print(trading_mode.value)  # Access the value directly
        time.sleep(5)



if __name__ == '__main__':
    # Use a shared string and a lock
    manager = Manager()
    trading_mode = manager.Value('c', 'paper')  # Create a managed Value
    # trading_mode = Array('c', 'paper')  # Array of characters
    lock = Lock()

     # Start the loop in a separate process
    print_process = multiprocessing.Process(target=print_trading_mode, args=(trading_mode, lock))
    print_process.start()
    
    # Run Flask app in the main process
    app.run(port=5000, threaded=False)
