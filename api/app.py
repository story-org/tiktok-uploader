from asyncio import to_thread
from typing import Annotated

from aiohttp import ClientSession
from fastapi import Body, FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from api.database import Cookies, Database
from api.schemas.video import VideoClass
from api.services.google_genai import generate_video_description
from api.services.tiktok_upload import upload_to_tiktok

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/upload")
async def upload_file(
    name: Annotated[str, Body(embed=True)],
    url: Annotated[str | None, Body(embed=True)] = None,
    file: UploadFile | None = None,
):
    if file:
        file_bytes = await file.read()
    else:
        async with ClientSession() as session:
            async with session.get(url) as response:
                file_bytes = await response.read()
    video = VideoClass(
        buffer=file_bytes,
        name=name,
        mime_type="video/mp4",
    )
    desc = await to_thread(generate_video_description, video)
    await to_thread(upload_to_tiktok, video, desc)
    return {"status": "success", "response": desc}


@app.post("/cookies/{id}")
async def update_cookies(id: str, file: UploadFile):
    db = Database()
    value = await file.read()
    cookies = Cookies(id=id, value=value.decode("utf-8"))
    await to_thread(db.update_cookies, cookies)
    return {"status": "success"}
