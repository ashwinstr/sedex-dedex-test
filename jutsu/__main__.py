
import os
import pyrogram
from decouple import config



APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)


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
