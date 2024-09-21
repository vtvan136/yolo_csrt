from flask_socketio import SocketIO
from flask import Flask
from app.routes import init_routes

def create_app():
    app = Flask(__name__)
    socketio = SocketIO(app,cors_allowed_origins="*")
    init_routes(app,socketio)  # Khởi tạo các routes từ routes.py
    return app,socketio
