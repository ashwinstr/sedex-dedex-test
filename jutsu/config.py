
import os
from heroku3 import from_key


class Config:
    API_ID = int(os.environ.get("APP_ID", 0))
    API_KEY = os.environ.get("HEROKU_API_KEY", None)
    API_HASH = os.environ.get("API_HASH", None)
    APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    DB_URI = os.environ.get("DB_URL", None)
    HU_APP = from_key(API_KEY).apps()[APP_NAME]
    LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID", 0))
    OWNER_ID = int(os.environ.get("OWNER_ID", 0))
    