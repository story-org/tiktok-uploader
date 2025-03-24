from api.services.tiktok_upload import Browserless

browserless = Browserless("https://www.tiktok.com/foryou")
browserless.upload_to_tiktok("https://www.tiktok.com/foryou")
browserless.close()