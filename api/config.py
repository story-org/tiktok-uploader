import logging
import os

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_LEVEL = logging.INFO


logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

BL_TOKEN = os.environ["BL_TOKEN"]
GENAI_TOKEN = os.environ["GENAI_TOKEN"]
DATABASE_URL = os.environ["DATABASE_URL"]
