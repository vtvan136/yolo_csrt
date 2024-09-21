import cv2

print(cv2.__version__)

# Kiểm tra sự tồn tại của TrackerCSRT
try:
    tracker = cv2.TrackerCSRTx`()
    print("TrackerCSRT có sẵn.")
except AttributeError:
    print("TrackerCSRT không có sẵn.")
