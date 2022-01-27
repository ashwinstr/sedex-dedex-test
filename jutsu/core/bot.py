

import logging

from pyrogram import Client

from pyrogram.errors import MessageNotModified

from jutsu import Config

# logging.basicConfig(level=logging.INFO)


class Sedex(Client):
    def __init__(self):
        kwargs = {
            'api_id': Config.API_ID,
            'api_hash': Config.API_HASH,
            'session_name': ':memory:',
            'bot_token': Config.BOT_TOKEN,
            'plugins': dict(root='jutsu/plugins')
        }
        super().__init__(**kwargs)

    async def start(self):
        await super().start()

    async def stop(self):
        await super().stop()

    async def sleep(self, msg):
        await msg.reply("`Sleeping for (10) Seconds.`")
        Config.HU_APP.restart()