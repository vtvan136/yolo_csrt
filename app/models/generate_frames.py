import time

import cv2

from app.models.yolov8 import  model
from app.utils import *
import numpy as np
from collections import defaultdict
from app.setting import detect_interval,mirror_region,conf_threshold,reset_time_threshold,colors

list_steps = [0, 0, 0, 0, 0, 0]
step_timestamps = defaultdict(list)
def generate_frames(cap, fps, width, height,socketio):
    global list_steps

    tracker = cv2.TrackerCSRT_create()
    tracking = False
    # Ngưỡng confidence
    no_detected_time = 0  # Biến theo dõi thời gian không phát hiện
    last_detection_time = time.time()
      # Lưu thời gian phát hiện của từng bước
    completed_steps = set()

    frame_count = 0
    prev_bbox, prev_label = None, None
    while cap.isOpened():
        ret, frame = cap.read()
        print('aaaaaaaaa')
        if not ret:
            break

        frame_count += 1
        current_time = time.time()

        # Chỉ detect mỗi 5 frame
        if frame_count % detect_interval == 0 or not tracking:

            mask = np.zeros(frame.shape, dtype=np.uint8)
            x1, y1, x2, y2 = mirror_region
            mask[y1:y2, x1:x2] = frame[y1:y2, x1:x2]
            blurred_mask = cv2.GaussianBlur(mask, (15, 15), 0)
            frame_with_blur = cv2.addWeighted(frame, 1, blurred_mask, -1, 0)

            # Detect object trên frame hiện tại
            results = model(frame_with_blur)[0]

            # Lọc ra đối tượng có confidence cao nhất
            best_box = max(results.boxes, key=lambda box: box.conf.item(), default=None)

            if best_box is not None:
                no_detected_time += (current_time - last_detection_time)
                last_detection_time = current_time
                conf = best_box.conf.item()  # Lấy ra giá trị conf
                if conf > conf_threshold:  # Nếu conf > 0.7 thì vẽ box
                    # Lấy tọa độ của bounding box
                    x1, y1, x2, y2 = map(int, best_box.xyxy[0].tolist())
                    new_bbox = (x1, y1, x2 - x1, y2 - y1)  # Tọa độ (x, y, width, height)
                    label = int(best_box.cls.item())  # Nhãn của đối tượng được detect
                    detected_step = label
                    # Cập nhật thời điểm phát hiện và số lần xuất hiện
                    check_and_update_steps(current_time, detected_step,completed_steps,step_timestamps,list_steps,socketio)
                    # Nếu chưa có bounding box trước đó thì init tracker
                    if prev_bbox is None:
                        tracker.init(frame, new_bbox)
                        tracking = True
                        prev_label = label
                    else:
                        prev_box_coords = (
                        prev_bbox[0], prev_bbox[1], prev_bbox[0] + prev_bbox[2], prev_bbox[1] + prev_bbox[3])
                        new_box_coords = (x1, y1, x2, y2)
                        iou = calculate_iou(prev_box_coords, new_box_coords)

                        # Nếu IoU nhỏ (bounding box đã thay đổi), khởi tạo lại tracker
                        if iou < 0.8:
                            tracker = cv2.TrackerCSRT_create()  # Reset tracker
                            tracker.init(frame, new_bbox)  # Khởi tạo lại tracker với box mới

                    prev_bbox = new_bbox  # Cập nhật bounding box trước
                    prev_label = label  # Cập nhật nhãn mới

            else:
                no_detected_time += (current_time - last_detection_time)
                last_detection_time = current_time
                if no_detected_time >= reset_time_threshold:
                    # Reset dữ liệu
                    # Xóa tất cả đối tượng đang theo dõi
                    list_steps = [0] * len(required_counts)  # Reset danh sách bước
                    completed_steps.clear()  # Xóa các bước đã thực hiện
                # Ngắt tracking nếu không có bước nào được phát hiện
                tracking = False
                prev_bbox = None
                prev_label = None

        # Nếu đang tracking, cập nhật vị trí đối tượng
        if tracking:
            success, bbox = tracker.update(frame)

            if success:
                # Vẽ bounding box từ kết quả tracking
                x, y, w, h = [int(v) for v in bbox]
                x, y, w, h = adjust_bbox_to_frame(x, y, w, h, width, height)
                color = colors[prev_label % len(colors)]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, f"Step: {prev_label + 1}", (x + 10, y - 10 if y - 10 > 10 else y + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            else:
                tracking = False

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Gửi frame đến client qua WebSocket
        socketio.emit('video_frame', frame_bytes)
        socketio.sleep(1 / fps)

