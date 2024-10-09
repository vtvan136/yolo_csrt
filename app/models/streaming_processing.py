import cv2
from app.yolov8 import YOLOv8
import os
os.getcwd()

# Initialize the webcam
cap = cv2.VideoCapture(r"C:/Users/vtvan/OneDrive/Máy tính/video-rua-tay-1-10-20241002T075259Z-001/video-rua-tay-1-10/2.mp4")
if not cap.isOpened():
    print("Error: Cannot open video.")

# Initialize YOLOv8 object detector
model_path = r"E:\HW\models\yolov8_v2.1.onnx"
yolov8_detector = YOLOv8(model_path, conf_thres=0.7, iou_thres=0.8)
#Variable
frame_count = 0
while True:
    # Read frame from the video
    ret, frame = cap.read()

    if not ret:
        print("Error: Cannot read frame.")
        break

    if frame_count % 25 == 0:
        # Update object localizer
        boxes, scores, class_ids = yolov8_detector(frame)

    # Draw detections on the current frame
    combined_img = yolov8_detector.draw_detections(frame)
    cv2.imshow("Detected Objects", combined_img)

    # Press key q to stop
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

    # Increment frame counter
    frame_count += 1

# Release resources and close windows
cap.release()
cv2.destroyAllWindows()
