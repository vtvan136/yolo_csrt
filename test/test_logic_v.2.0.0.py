import math

import cv2
from ultralytics import YOLO
import time
# Khởi tạo YOLOv8 model và video
model = YOLO("/models/yolov8n.pt")
video_path = 'E:/HW/data/test_video_TOD.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Cannot open video.")
    exit(0)

frame_count = 0
detect_interval = 25
tracker = None
steps_detected = []  # Stores detected steps with timestamps
steps_executed = []  # Steps that have been executed
last_step = None
confidence_threshold = 0.7
step_frequency = {}
tracking_start_time = None
execution_threshold = 10
output_path = 'E:/HW/data/ouput_video_av1.mkv'
fourcc = cv2.VideoWriter_fourcc(*'AV01')  # Codec mp4
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))


def get_color_for_step(step):
    # Define colors for different steps; add more as needed
    colors = [
        (0, 255, 0),   # Green
        (0, 0, 255),   # Red
        (255, 0, 0),   # Blue
        (255, 255, 0), # Cyan
        (0, 255, 255), # Yellow
        (255, 0, 255), # Magenta
    ]
    return colors[step % len(colors)]
def detect_and_track(frame, frame_time):
    global tracker, last_step, steps_detected, tracking_start_time

    results = model(frame)
    detections = results[0].boxes.data.cpu().numpy()

    if len(detections) > 0:
        for det in detections:
            if len(det) >= 6:
                x1, y1, x2, y2, conf, cls = det[:6]
            elif len(det) >= 4:
                x1, y1, x2, y2 = det[:4]
                conf = 1.0
                cls = 0
            else:
                continue

            if conf > confidence_threshold:
                current_step = int(cls)

                if tracking_start_time is None:
                    tracking_start_time = frame_time

                if current_step != last_step and current_step not in [s[0] for s in steps_detected]:
                    tracker = cv2.TrackerCSRT_create()
                    # Ensure the bounding box is within frame boundaries
                    height, width, _ = frame.shape
                    x1 = max(0, min(int(x1), width - 1))
                    y1 = max(0, min(int(y1), height - 1))
                    x2 = max(0, min(int(x2), width - 1))
                    y2 = max(0, min(int(y2), height - 1))

                    bbox = (x1, y1, x2 - x1, y2 - y1)
                    tracker.init(frame, bbox)
                    last_step = current_step
                    steps_detected.append((current_step, frame_time))
                    break

def update_tracker(frame):
    global tracker, last_step, step_frequency, steps_executed

    if tracker is not None:
        success, bbox = tracker.update(frame)
        if success:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            step_color = get_color_for_step(last_step)
            cv2.rectangle(frame, p1, p2, step_color, 2, 1)

            # Draw the step number on the box
            step_text = f'Step: {last_step + 1 }'  # Text to display
            cv2.putText(frame, step_text, (p1[0] + 10, p1[1] - 10 if p1[1] - 10 > 10 else p1[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, step_color, 2)

            if last_step not in step_frequency:
                step_frequency[last_step] = 0
            step_frequency[last_step] += 1

            if step_frequency[last_step] >= execution_threshold and last_step not in steps_executed:
                steps_executed.append(last_step)
                step_frequency[last_step] = 0

def middle_frame_video(video_path,output_image_path):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    middle_frame = total_frames // 2
    for frame in range(middle_frame-5,middle_frame+5):
        cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)
        ret, frame = cap.read()
        cap.release()
        if ret:
            cv2.imwrite(output_image_path, frame)

def frame_to_image(frame):
    # Mã hóa frame thành định dạng JPEG
    success, encoded_image = cv2.imencode('.jpg', frame)
    if success:
        # Chuyển đổi ảnh đã mã hóa thành bytes
        return encoded_image.tobytes()
    else:
        print("Error: Cannot encode frame.")
        return None

def convert_to_seconds(steps_detected):
    steps_in_seconds = [(step, time / 1000) for step, time in steps_detected]
    return steps_in_seconds
def format_time(seconds):
    total_seconds = math.floor(seconds)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:02d}"

def generate_frames():
    global frame_count
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        frame_time = cap.get(cv2.CAP_PROP_POS_MSEC)

        if (frame_count % detect_interval == 0 or tracker is None) and (
                tracking_start_time is None or frame_time >= tracking_start_time):
            detect_and_track(frame, frame_time)
        else:
            update_tracker(frame)

        cv2.imshow('Hand Washing Detection', frame)
        out.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Output the detected and executed steps
generate_frames()
# Kết quả quy đổi
steps_in_seconds = convert_to_seconds(steps_detected)

middle_frame_video('E:/HW/data/test_video_TOD.mp4','E:/HW/data/test_video_TOD.jpg')
# In kết quả
print("Step Times in Seconds:")
for step, time in steps_in_seconds:
    time = format_time(time)
    print(f"Step: {step}, Time: {time}")
