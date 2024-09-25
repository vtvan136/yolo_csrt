import cv2
from ultralytics import YOLO

# Tải mô hình YOLOv8
model = YOLO('E:\HW/app\models\yolov8n.pt')  # Bạn có thể thay đổi thành yolov8s.pt, yolov8m.pt, ...

# Khởi tạo video
video_source = 'E:\HW\data/test_video_TOD.mp4'  # Thay thế bằng đường dẫn video của bạn
cap = cv2.VideoCapture(video_source)

# Khởi tạo CSRT tracker
tracker = cv2.TrackerCSRT_create()
tracking = False
bbox = None
last_object_id = None  # ID của đối tượng trước đó

# Biến đếm frame
frame_count = 0
no_detection_count = 0  # Biến đếm số frame không phát hiện

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1  # Tăng biến đếm frame

    # Nếu chưa theo dõi đối tượng hoặc đến thời điểm phát hiện lại
    if not tracking or frame_count % 25 == 0:
        # Phát hiện đối tượng
        results = model(frame)

        # Kiểm tra xem có phát hiện đối tượng không
        if results.xyxy[0].size(0) > 0:
            # Lọc các bbox có confidence > 0.7
            high_conf_boxes = results.xyxy[0][results.xyxy[0][:, 4] > 0.7]  # Lọc theo confidence

            if high_conf_boxes.size(0) > 0:
                # Reset biến đếm không phát hiện
                no_detection_count = 0

                # Lấy bbox đầu tiên có confidence cao
                current_bbox = high_conf_boxes[0][:4].cpu().numpy()  # bbox: [x1, y1, x2, y2]
                current_bbox = (int(current_bbox[0]), int(current_bbox[1]), int(current_bbox[2] - current_bbox[0]), int(current_bbox[3] - current_bbox[1]))

                # Kiểm tra xem đối tượng có khác với đối tượng trước đó không
                current_object_id = int(high_conf_boxes[0][5])  # ID của đối tượng (có thể là lớp hoặc ID cụ thể)

                if not tracking or current_object_id != last_object_id:
                    # Khởi tạo tracker với bbox
                    tracker.init(frame, current_bbox)
                    tracking = True
                    last_object_id = current_object_id  # Cập nhật ID đối tượng trước đó
                else:
                    # Cập nhật tracker nếu vẫn theo dõi cùng một đối tượng
                    success, bbox = tracker.update(frame)
                    if success:
                        (x, y, w, h) = [int(v) for v in bbox]
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            else:
                # Tăng biến đếm không phát hiện
                no_detection_count += 1

                # Nếu không có phát hiện trong 50 frame, dừng theo dõi
                if no_detection_count >= 50:
                    tracking = False
                    last_object_id = None  # Reset ID đối tượng trước đó
        else:
            # Tăng biến đếm không phát hiện
            no_detection_count += 1

            # Nếu không có phát hiện trong 50 frame, dừng theo dõi
            if no_detection_count >= 50:
                tracking = False
                last_object_id = None  # Reset ID đối tượng trước đó
    else:
        # Theo dõi đối tượng
        success, bbox = tracker.update(frame)
        if success:
            # Vẽ bbox lên frame
            (x, y, w, h) = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow('Object Tracking', frame)

    # Thoát bằng phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
