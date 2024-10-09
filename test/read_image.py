import cv2
image_path = 'E:\HW\data/frame_data/1/frame_100.jpg'  # Thay đổi thành đường dẫn đến hình ảnh của bạn
output_file = 'E:\HW\data/frame_data/1/frame_100.txt'  # Tên file xuất kết quả

image = cv2.imread(image_path)

# Đọc file annotation
with open(output_file, 'r') as f:
    lines = f.readlines()

# Duyệt qua từng dòng trong file annotation
for line in lines:
    parts = line.strip().split()

    if len(parts) != 5:
        continue  # Bỏ qua các dòng không hợp lệ

    id_class = int(parts[0])
    xc = float(parts[1])
    yc = float(parts[2])
    w = float(parts[3])
    h = float(parts[4])

    # Tính toán tọa độ góc hộp giới hạn
    x1 = int((xc - w / 2) * image.shape[1])
    y1 = int((yc - h / 2) * image.shape[0])
    x2 = int((xc + w / 2) * image.shape[1])
    y2 = int((yc + h / 2) * image.shape[0])

    # Vẽ hộp giới hạn lên hình ảnh
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(image, f'Class: {id_class}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Hiển thị hình ảnh
cv2.imshow('Annotated Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()