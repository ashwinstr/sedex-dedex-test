import os

from pyrogram import Client, filters
from .updater import HEROKU_APP


@Client.on_message(
    filters.command(["logs"], prefixes=";")
    & filters.user([1013414037]),
    group=3
)
async def logging_(bot, message):
    msg_ = await bot.send_message(message.chat.id, "`Checking logs...`")
    try:
        limit = int((message.text).split()[1])
    except:
        limit = 100
    if HEROKU_APP:
        logs = (HEROKU_APP.get_log)(lines=limit)
        if not os.path.isdir("logs"):
            os.mkdir("logs")
        file_name = "logs/sedex-heroku.log"
        with open(file_name, "w+") as file:
            file.write(logs)
            file.close()
        await msg_.delete()
        await bot.send_document(
            chat_id=message.chat.id,
            document=file_name,
            caption=f"**Sedex-heroku.log** [ {limit} lines ]",
        )
        os.remove(file_name)
