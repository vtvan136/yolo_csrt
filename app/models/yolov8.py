import os
from ultralytics import YOLO


def load_model(model_path):
    # Kiểm tra sự tồn tại của file mô hình
    if os.path.exists(model_path):
        return YOLO(model_path)
    else:
        raise FileNotFoundError(f"Mô hình không tồn tại: {model_path}")



# Đường dẫn mô hình và ảnh
model_path = "app/models/yolov8n.pt"

try:
    # Tải mô hình YOLO
    model = load_model(model_path)

except (FileNotFoundError, ValueError) as e:
    print(f"Lỗi: {e}")
except Exception as e:
    print(f"Có lỗi xảy ra: {e}")
