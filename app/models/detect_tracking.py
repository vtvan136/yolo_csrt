# app/models/detect_tracking.py

import cv2

confidence_threshold = 0.7
execution_threshold = 10

# Hàm lấy màu cho step
def get_color_for_step(step):
    colors = [
        (0, 255, 0),   # Green
        (0, 0, 255),   # Red
        (255, 0, 0),   # Blue
        (255, 255, 0), # Cyan
        (0, 255, 255), # Yellow
        (255, 0, 255), # Magenta
    ]
    return colors[step % len(colors)]

# Hàm detect và track
def detect_and_track(frame, frame_time, model, tracker, last_step, steps_detected, tracking_start_time):
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

    return tracker, last_step, steps_detected, tracking_start_time

# Hàm update tracker
def update_tracker(frame, tracker, last_step, step_frequency, steps_executed):
    if tracker is not None:
        success, bbox = tracker.update(frame)
        if success:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            step_color = get_color_for_step(last_step)
            cv2.rectangle(frame, p1, p2, step_color, 2, 1)

            step_text = f'Step: {last_step + 1}'  
            cv2.putText(frame, step_text, (p1[0] + 10, p1[1] - 10 if p1[1] - 10 > 10 else p1[1] + 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, step_color, 2)

            if last_step not in step_frequency:
                step_frequency[last_step] = 0
            step_frequency[last_step] += 1

            if step_frequency[last_step] >= execution_threshold and last_step not in steps_executed:
                steps_executed.append(last_step)
                step_frequency[last_step] = 0

    return tracker, step_frequency, steps_executed
