import os

from google import genai
from google.genai.types import Content, GenerateContentConfig, Part

from api.schemas.video import VideoClass
from api.services.tiktok_upload import Browserless

google_api = os.environ["GENAI_TOKEN"]
model_name = "gemini-2.0-flash"


def generate_video_description(video: VideoClass):
    client = genai.Client(api_key=google_api)

    def upload_to_tiktok(description: str):
        browserless = Browserless(video)
        browserless.upload_to_tiktok(video, description)
        browserless.close()

    config = GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
        tools=[upload_to_tiktok],
    )
    contents = [
        Content(
            role="user",
            parts=[
                Part.from_bytes(
                    data=video.buffer,
                    mime_type=video.mime_type,
                ),
            ],
        ),
        Content(
            role="user",
            parts=[
                Part.from_text(
                    text="Hãy upload video lên tiktok bằng upload_to_tiktok và với mô tả bằng tiếng Anh. Nội dung mô tả lôi cuốn, phản ánh chính xác nội dung video và kèm theo các hashtag liên quan bằng tiếng Việt và có thể bổ sung thêm tiếng Anh, các hashtag phải được viết liền nhau và bạn không cần tôi trả lời sau khi đưa ra tiêu đề. luôn chứa 2 hashtag là #fyp và #xuhuong"
                ),
            ],
        ),
    ]
    response = client.models.generate_content(
        model=model_name,
        contents=contents,
        config=config,
    )

    return response.text
