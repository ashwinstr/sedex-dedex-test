import os
import pyrogram
from decouple import config



APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)
HEROKU_API_KEY = config("HEROKU_API_KEY", default=None)
HEROKU_APP_NAME = config("HEROKU_APP_NAME", default=None)
HEROKU_ENV = config(bool(int("HEROKU_ENV")), default=False)
HEROKU_APP = (
        heroku3.from_key(HEROKU_API_KEY).apps()[HEROKU_APP_NAME]
        if HEROKU_ENV and HEROKU_API_KEY and HEROKU_APP_NAME
        else None
    )


if __name__ == "__main__" :
    print("### Starting Bot... ###")
    plugins = dict(root="jutsu/plugins")
    app = pyrogram.Client(
        "sharingan",
        bot_token=BOT_TOKEN,
        api_id=APP_ID,
        api_hash=API_HASH,
        
        plugins=plugins
    )
    app.run()
