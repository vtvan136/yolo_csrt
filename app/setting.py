


mirror_region = (0, 0, 200, 300)
colors = [
    (0, 255, 0),  # Xanh lá
    (0, 0, 255),  # Đỏ
    (255, 0, 0),  # Xanh dương
    (0, 255, 255), # Vàng
    (255, 0, 255), # Tím
    (255, 255, 0)  # Xanh lơ
]

detect_interval = 10  # Mỗi 5 frame thì detect lại
conf_threshold = 0.7
reset_time_threshold = 4
 # Lưu các bước đã thực hiện
required_counts = {
            1: 4,  # Step 1 cần 4 lần
            2: 2,  # Step 2 cần 3 lần (trong 2,5 giây)
            3: 2,  # Step 3 cần 2 lần (trong 3,5 giây)
            4: 2,  # Step 4 cần 2 lần (trong 4,5 giây)
            5: 2,  # Step 5 cần 2 lần (trong 4,5 giây)
            6: 4   # Step 6 cần 1 lần (trong 5 giây)
        }





