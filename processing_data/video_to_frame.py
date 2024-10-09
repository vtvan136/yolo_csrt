import cv2
import os


def extract_frames(video_path, _frames_per_second, output_folder):
    # Kiểm tra và tạo thư mục đầu ra nếu chưa tồn tại
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Mở video
    cap = cv2.VideoCapture(video_path)

    # Lấy FPS của video
    video_fps = cap.get(cv2.CAP_PROP_FPS)

    # Tính số frame cần bỏ qua để lấy đúng số hình cắt trên 1 giây
    frame_skip = int(video_fps / _frames_per_second)

    # Biến để đếm frame
    frame_count = 0
    saved_image_count = 0

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Nếu đây là frame cần lưu lại (dựa trên frame_skip)
        if frame_count % frame_skip == 0:
            # Tạo tên file ảnh
            image_path = os.path.join(output_folder, f'frame_{saved_image_count}.jpg')
            # Lưu frame thành ảnh
            cv2.imwrite(image_path, frame)
            saved_image_count += 1

        frame_count += 1

    # Đóng video
    cap.release()
    print(f'Đã lưu {saved_image_count} hình ảnh vào {output_folder}')


def extract_frames_from_videos(video_folder, _frames_per_second, output_parent_folder):
    # Kiểm tra nếu thư mục chứa video không tồn tại
    if not os.path.exists(video_folder):
        print(f'Thư mục {video_folder} không tồn tại.')
        return

    # Duyệt qua các file trong thư mục video
    for video_file in os.listdir(video_folder):
        # Chỉ xử lý file có định dạng .mp4 (hoặc các định dạng video khác nếu cần)
        if video_file.endswith('.mp4'):
            # Đường dẫn đầy đủ đến video
            video_path = os.path.join(video_folder, video_file)

            # Tên file không có phần mở rộng
            video_name = os.path.splitext(video_file)[0]

            # Tạo thư mục con để lưu hình ảnh có cùng tên với video
            output_folder = os.path.join(output_parent_folder, video_name)

            # Cắt và lưu hình ảnh từ video
            extract_frames(video_path, _frames_per_second, output_folder)


# Ví dụ sử dụng:
if __name__ == '__main__':
    path_video = "C:/Users/vtvan/OneDrive/Máy tính/video-rua-tay-1-10-20241002T075259Z-001/video-rua-tay-1-10"
    frames_per_second = 10
    path_image = "E:/HW/data/frame_data/"
    extract_frames_from_videos(path_video, frames_per_second, path_image)
