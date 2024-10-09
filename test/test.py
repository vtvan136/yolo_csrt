'''import cv2
import time
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO('E:/HW/app/models/yolov8_v2.pt')

# Initialize CSRT tracker
tracker = cv2.TrackerCSRT_create()

# Variables for tracking state
tracking_active = False
current_step = None
frame_count = 0  # Counter for the number of frames processed
conf_threshold = 0.45

# Open video stream
cap = cv2.VideoCapture("C:/Users/vtvan/OneDrive/Máy tính/video-rua-tay-1-10-20241002T075259Z-001/video-rua-tay-1-10/1.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Increment frame count
    frame_count += 1

    # Perform detection every 10 frames
    if not tracking_active or (frame_count % 20 == 0):  # Detect every 10 frames
        # Detect step using YOLOv8
        results = model(frame)
        detections = results[0].boxes
        detect_flag = False

        for box in detections:
            conf = box.conf[0]
            step_label = int(box.cls[0])  # assuming steps are labeled as classes

            # Check if the confidence is above threshold
            if conf > conf_threshold:
                detect_flag = True
                if current_step is None or step_label != current_step:
                    # Update current step and start tracking new step
                    current_step = step_label
                    bbox_xyxy = box.xyxy[0].cpu().numpy()  # Assuming box is a tensor and convert to numpy array

                    # Convert bbox to (x, y, width, height)
                    x_min, y_min, x_max, y_max = bbox_xyxy
                    x = int(x_min)  # Convert to int
                    y = int(y_min)  # Convert to int
                    width = int(x_max - x_min)  # Calculate width
                    height = int(y_max - y_min)  # Calculate height
                    bbox = (x, y, width, height)  # Ensure bbox is a tuple of ints

                    # Initialize tracker with converted bbox
                    tracker = cv2.TrackerCSRT_create()
                    tracker.init(frame, bbox)

                    tracking_active = True
                break

        # If no step detected above threshold, stop tracking
        if not detect_flag and tracking_active:
            tracking_active = False
            current_step = None

    # Tracking active, update tracker
    if tracking_active:
        success, bbox = tracker.update(frame)
        if success:
            # Draw the tracking bounding box
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)

            # Draw step label on the bounding box
            step_text = f"Step: {current_step}"  # Adjust as needed for step labeling
            cv2.putText(frame, step_text, (p1[0], p1[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        else:
            # Stop tracking if tracker fails
            tracking_active = False
            current_step = None

    # Display the frame with detections and tracking
    cv2.imshow('Hand Washing Steps Detection', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

'''
import os
import matplotlib.pyplot as plt

def plot_label_distribution(label_folder, image_width, image_height):
    x_coords = []
    y_coords = []

    # Duyệt qua tất cả các tệp nhãn trong thư mục
    for filename in os.listdir(label_folder):
        if filename.endswith('.txt'):
            # Đọc tệp nhãn
            with open(os.path.join(label_folder, filename), 'r') as file:
                lines = file.readlines()
                for line in lines:
                    data = list(map(float, line.split()))
                    # Lấy tọa độ của bounding box
                    class_id, x_center, y_center, width, height = data

                    # Chuyển đổi tọa độ từ tỷ lệ sang pixel
                    x = x_center * image_width
                    y = y_center * image_height

                    # Thêm tọa độ vào danh sách
                    x_coords.append(x)
                    y_coords.append(y)

    # Vẽ biểu đồ phân bố
    plt.figure(figsize=(10, 6))
    plt.scatter(x_coords, y_coords, alpha=0.5, color='blue', s=10)  # Bạn có thể điều chỉnh kích thước điểm (s)
    plt.title('Distribution of Label Positions')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.xlim(0, image_width)  # Giới hạn trục x
    plt.ylim(0, image_height)  # Giới hạn trục y
    plt.grid()
    plt.show()

# Đường dẫn tới thư mục chứa các tệp nhãn
label_folder_path = 'D:/new_dataset/labels'
# Kích thước hình ảnh (bạn có thể điều chỉnh theo kích thước thực tế của hình ảnh)
image_width = 512  # Thay đổi theo kích thước của hình ảnh
image_height = 512  # Thay đổi theo kích thước của hình ảnh

plot_label_distribution(label_folder_path, image_width, image_height)
