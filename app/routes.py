import cv2
from flask import  request
from app.models.generate_frames import generate_frames
def init_routes(app,socketio):
    @app.route('/detect', methods=['POST'])
    def detect():
        data = request.json
        video_url = data.get('url')

        if not video_url:
            return {'error': 'URL không hợp lệ'}, 400

        cap = cv2.VideoCapture(video_url)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        socketio.start_background_task(
            target=generate_frames(cap, fps, width, height,socketio))

        return {'status': 'Started processing video stream'}, 200

    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')