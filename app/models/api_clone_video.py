import cloudinary
import cloudinary.uploader


class UpLoadFileToClone:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(UpLoadFileToClone, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        cloudinary.config(
            cloud_name="df8w3e7si",
            api_key="942237674279446",
            api_secret="H-hCbLs6QmDpIsgQZatjZ0T0RZg",
            secure=True
        )
        self.clone = cloudinary

    def upload_video_to_clone(self, path):
        video_result = self.clone.uploader.upload_large(
            path,
            resource_type="video",
            chunk_size=6000000
        )
        return video_result["secure_url"]

    def upload_image_to_clone(self, path):
        image_result = self.clone.uploader.upload(
            path
        )
        return image_result["secure_url"]


if __name__ == "__main__":
    clone_video = UpLoadFileToClone()
    print(clone_video.upload_image_to_clone("/home/thanhvy/PycharmProjects/yolo_csrt/data/21ebc565-a2db-4a12-bdf4-037e17a043e4.jpg"))
