from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot GGMAX está online!'

def run():
    app.run(host='0.0.0.0', port=8080)

def start_web():
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
