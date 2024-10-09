import cv2
import numpy as np
import onnxruntime

def preprocess_image(image):
    input_size = (640, 640)
    image_resized = cv2.resize(image, input_size)
    image_normalized = image_resized / 255.0
    image_transposed = np.transpose(image_normalized, (2, 0, 1))
    image_transposed = np.expand_dims(image_transposed, axis=0)
    return image_transposed.astype(np.float32)

def detect_objects(image, session):
    input_tensor = preprocess_image(image)
    outputs = session.run(None, {session.get_inputs()[0].name: input_tensor})

    boxes = outputs[:, :4]
    scores = outputs[:, :4]
    class_ids = outputs[:, 4:]
    print(boxes, scores, class_ids)
    return boxes, scores, class_ids

def main():
    model_path = r'E:\HW\models\yolov8_v2.1.onnx'
    session = onnxruntime.InferenceSession(model_path)

    image = cv2.imread(r"D:\dataset_v2.1\images\3_frame_122.jpg")
    boxes, scores, class_ids = detect_objects(image, session)

    # Chuyển đổi scores thành numpy array
    scores_np = np.array(scores)

    # Lọc các chỉ số có score lớn hơn 0.7
    high_scores_indices = np.where(scores_np > 0.7)[0]

    if high_scores_indices.size > 0:
        # Lấy các bounding boxes và class_ids tương ứng
        high_score_boxes = boxes[high_scores_indices]
        high_score_scores = scores_np[high_scores_indices]
        high_score_class_ids = class_ids[high_scores_indices]

        # Tìm score lớn nhất
        max_index = np.argmax(high_score_scores)
        best_box = high_score_boxes[max_index]
        best_score = high_score_scores[max_index]
        best_class_id = high_score_class_ids[max_index]

        x1, y1, x2, y2 = best_box

        # Vẽ bounding box và hiển thị thông tin
        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(image, f'ID: {int(best_class_id)}, Score: {best_score:.2f}',
                    (int(x1), int(y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    cv2.imshow('Detected Objects', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
