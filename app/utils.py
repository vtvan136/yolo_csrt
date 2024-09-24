import math
from app.setting  import required_counts


'''def check_and_update_steps(current_time, detected_step,completed_steps,step_timestamps, list_steps,socketio):
    if detected_step not in completed_steps:
        # Cập nhật timestamp cho bước được phát hiện
        step_timestamps[detected_step].append(current_time)

        # Kiểm tra thời gian và số lần xuất hiện
        timestamps = [ts for ts in step_timestamps[detected_step] if current_time - ts <= 5]
        step_timestamps[detected_step] = timestamps

        if len(timestamps)  >= required_counts.get(detected_step, 0) :
            count_non_zero = sum(1 for x in list_steps if x != 0)
            list_steps[detected_step] = count_non_zero +1
            completed_steps.add(detected_step )
            socketio.emit('update_list_steps', {'list_steps': list_steps})
            print(f'Updated list_steps: {list_steps}')
            # Thêm vào danh sách bước đã thực hiện

# Hàm tính IoU (Intersection over Union) để so sánh hai bounding boxes
def calculate_iou(box1, box2):
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2

    inter_x_min = max(x1_min, x2_min)
    inter_y_min = max(y1_min, y2_min)
    inter_x_max = min(x1_max, x2_max)
    inter_y_max = min(y1_max, y2_max)

    inter_area = max(0, inter_x_max - inter_x_min) * max(0, inter_y_max - inter_y_min)
    area_box1 = (x1_max - x1_min) * (y1_max - y1_min)
    area_box2 = (x2_max - x2_min) * (y2_max - y2_min)
    union_area = area_box1 + area_box2 - inter_area

    return inter_area / union_area

def adjust_bbox_to_frame(x, y, w, h, frame_width, frame_height):
    return max(0, x), max(0, y), min(w, frame_width - x), min(h, frame_height - y)
'''
############## VERSION 2.0 ###########################################################
def get_color_for_step(step):
    # Define colors for different steps; add more as needed
    colors = [
        (0, 255, 0),  # Green
        (0, 0, 255),  # Red
        (255, 0, 0),  # Blue
        (255, 255, 0),  # Cyan
        (0, 255, 255),  # Yellow
        (255, 0, 255),  # Magenta
    ]
    return colors[step % len(colors)]

def convert_to_seconds(steps_detected):
    steps_in_seconds = [(step, format_time(time / 1000)) for step, time in steps_detected]
    return steps_in_seconds
def format_time(seconds):
    total_seconds = math.floor(seconds)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:02d}"
