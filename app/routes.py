import os

from flask import request

from app.models.generate_frames import generate_frames
from app.models.middle_frame_video import *

from app.models.api import api_call_event_handing


def init_routes(app, socketio):
    @app.route('/detect', methods=['POST'])
    def detect():
        data = request.json
        video_url = data.get('url')
        event_id = data.get('event_id')
        if not video_url:
            return {'error': 'URL không hợp lệ'}, 400
        cap = cv2.VideoCapture(video_url)
        if not cap.isOpened():
            print("Error: Cannot open video.")
            exit(0)
        # Ouput Video & List Time Steps
        steps_in_seconds, output_path = generate_frames(cap, socketio, event_id)
        print(steps_in_seconds, output_path)
        # Middle Frame In Video
        output_image_path = f'data/{event_id}.jpg'
        if os.path.exists(output_path):
            print(output_path)
        if os.path.exists(output_image_path):
            print(output_image_path)
        middle_frame_video(video_url, output_image_path)
        # Call API
        api_call_event_handing(
            event_id=event_id,
            list_steps=steps_in_seconds,
            image_path=output_image_path,
            video_path=output_path
        )
        return {'status': 'Started processing video '}, 200

    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')
