import json

from playwright.sync_api import sync_playwright
from sqlmodel import select

from api.config import BL_TOKEN, log
from api.database import Cookies, Database
from api.schemas.video import VideoClass


class Browserless:
    def __init__(self, url):
        self.url = url
        self.browser = self.get_browser()
        self.db = Database()

    def get_browser(self):
        p = sync_playwright().start()
        return p.chromium.connect_over_cdp(
            endpoint_url=f"wss://production-sfo.browserless.io/chromium/playwright?token={BL_TOKEN}&proxy=residential"
        )

    def get_cookies(self):
        session = self.db.get_session()
        cookies = session.exec(select(Cookies).where(Cookies.key == "tiktok")).first()
        cookies_dict = json.loads(cookies.value)  # type: ignore
        for cookie in cookies_dict:
            if "sameSite" in cookie:
                if cookie["sameSite"] not in ["Strict", "Lax", "None"]:
                    cookie["sameSite"] = "Lax"
        return cookies_dict

    def upload_to_tiktok(self, video: VideoClass, description: str):
        context = self.browser.new_context()
        context.add_cookies(self.get_cookies())

        page = context.new_page()
        page.goto("https://www.tiktok.com/tiktokstudio/upload?from=creator_center")
        log.info(page.title())

        page.locator("input[type='file']").set_input_files(
            files=[
                {
                    "name": video.name,
                    "mimeType": video.mime_type,
                    "buffer": video.buffer,
                }
            ]
        )
        log.info("Putting file")

        page.locator("div.jsx-1979214919.info-status.success").wait_for()
        log.info("Put file successfully")

        page.locator(
            'div[contenteditable="true"].public-DraftEditor-content[aria-autocomplete="list"][aria-expanded="false"][role="combobox"][spellcheck="false"]'
        ).fill(description)
        log.info("Filling description")

        page.locator("button[data-e2e='post_video_button']").click()
        log.info("Clicking post button")
        page.wait_for_load_state("networkidle")

        page.close()
        context.close()

    def close(self):
        self.browser.close()
