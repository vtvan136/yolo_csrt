import cv2

def check_video_open(video_path):
    # Mở video
    cap = cv2.VideoCapture(video_path)

    # Kiểm tra nếu không mở được video
    if not cap.isOpened():
        print("Error: Cannot open video.")
        return False
    else:
        print("Video opened successfully.")
        # Có thể thực hiện thêm các thao tác khác ở đây, ví dụ kiểm tra frame
        cap.release()  # Đóng video sau khi kiểm tra
        return True

# Đường dẫn đến video
video_path = 'E:\HW\data\ouput_video.mp4'

# Kiểm tra video
is_video_opened = check_video_open(video_path)
