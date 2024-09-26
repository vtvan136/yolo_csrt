import requests
from app.models.api_clone_video import UpLoadFileToClone


def api_call_event_handing(event_id, list_steps, image_path, video_path):
    access_token = api_login_ai_account()
    api_call_send_data_event(
        access_token=access_token,
        event_id=event_id,
        list_steps=list_steps,
        image_path=image_path,
        video_path=video_path
    )


def api_login_ai_account():
    _url = 'http://0.0.0.0:8000/api/auth/login/'
    _data = {
        "email": "hungpm372@gmail.com",
        "password": "12345678"
    }
    _response = requests.post(_url, data=_data)

    access_token = _response.json()['access']
    return access_token


def api_call_send_data_event(access_token, event_id, image_path, video_path, list_steps):
    url = f'http://0.0.0.0:8000/api/event/{event_id}'

    clone_video = UpLoadFileToClone()
    url_image = clone_video.upload_image_to_clone(image_path)
    url_video = clone_video.upload_video_to_clone(video_path)

    data = {
        'data_ai': list_steps,
        'image_url': url_image,
        'video_result': url_video
    }
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.put(url, json=data, headers=headers)

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
