import os
import cv2
from ultralytics import YOLO

# Khởi tạo mô hình YOLOv8
model = YOLO('E:/HW/app/models/yolov8n.pt')  # Thay 'yolov8n.pt' bằng mô hình bạn muốn sử dụng

input_directory = r'E:/HW/data/frame_data'  # Thay đổi đường dẫn này
output_directory = r'E:/HW/data/frame_data'  # Đường dẫn để lưu file TXT đầu ra



# Duyệt qua từng thư mục và file trong thư mục đầu vào
for root, dirs, files in os.walk(input_directory):
    for file in files:
        if file.endswith(('.jpg', '.png', '.jpeg')):  # Bạn có thể thêm định dạng khác nếu cần
            image_path = os.path.join(root, file)
            output_file = os.path.join(root, f"{os.path.splitext(file)[0]}.txt")
            # Đọc hình ảnh
            image = cv2.imread(image_path)
            if image is None:
                print(f"Không thể đọc hình ảnh: {image_path}")
                continue

            # Phát hiện đối tượng trong hình ảnh
            results = model(image)
            height, width, _ = image.shape

            # Ghi kết quả vào file
            with open(output_file, 'w') as f:
                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        # Lấy tọa độ hộp giới hạn
                        x1, y1, x2, y2 = box.xyxy[0].int().tolist()
                        id_class = int(box.cls[0].item())

                        # Tính toán tọa độ trung tâm, chiều rộng và chiều cao
                        xc = (x1 + x2) / 2
                        yc = (y1 + y2) / 2
                        w = x2 - x1
                        h = y2 - y1

                        # Ghi kết quả vào file
                        f.write(f"{id_class} {xc / width} {yc / height} {w / width} {h / height}\n")

print("Hoàn thành! Kết quả đã được lưu vào thư mục:", output_directory)
