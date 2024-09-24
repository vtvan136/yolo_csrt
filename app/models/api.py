import requests


def api_call_event_handing(data_ai):
    access_token = api_login_ai_account()
    api_call_send_data_event(access_token, data_ai)


def api_login_ai_account():
    _url = 'http://40.83.120.165:8024/api/auth/login/'
    _data = {
        "email": "vtvan136@gmail.com",
        "password": "12345678"
    }
    _response = requests.post(_url, data=_data)

    access_token = _response.json()['access']
    return access_token


def api_call_send_data_event(image_path, video_path, list_steps):
    access_token = api_login_ai_account()
    url = 'http://40.83.120.165:8024/api/event/handing/'
    headers = {
        'Content-Type': 'multipart/form-data'
    }

    # Mở các file video và hình ảnh
    with open(video_path, 'rb') as video_file, open(image_path, 'rb') as image_file:
        # Chuẩn bị payload để gửi
        files = {
            'video': ('video.mp4', video_file, 'video/mp4'),  # File video
            'image': ('image.jpg', image_file, 'image/jpeg')  # File ảnh
        }

        # Chuẩn bị mảng dữ liệu dưới dạng JSON
        data = {
            'array': list_steps  # Mảng dữ liệu
        }
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + access_token
        }
        # Gửi yêu cầu POST tới API
        response = requests.post(url, files=files, data=data, headers=headers)

    # Xử lý phản hồi từ API
    if response.status_code == 200:
        print('Data sent successfully!')
        print('Response:', response.json())  # In kết quả trả về từ API nếu có
    else:
        print('Failed to send data.')
        print('Status Code:', response.status_code)
        print('Response:', response.text)
    '''data = {
        "data_ai": data_ai,
        "camera": "089a5f8f-45bd-4e88-a582-46aa3de00dc0",
        "actor": "b4484a6f-2d9c-4721-8f79-964e1368a7a3"
    }


    _response = requests.post(url, headers=headers, json=data)
    print(_response.text)'''
