from api.services.google_genai import generate_video_description
from api.services.tiktok_upload import upload_to_tiktok
from api.schemas.video import VideoClass

video = VideoClass(
    name="100001.mp4",
    mime_type="video/mp4",
    buffer=open("100001.mp4", "rb").read(),
)

description = generate_video_description(video)

print(description)

upload_to_tiktok(video, description)
