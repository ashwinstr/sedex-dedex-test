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
        await msg_.send_as_file(
            text=logs,
            filename="sedex-heroku.log",
            caption=f"sedex-heroku.log [ {limit} lines ]",
        )
