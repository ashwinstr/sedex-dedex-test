from pyrogram import Client, filters


@Client.on_message(
    filters.command(["start"], prefixes=";"), group=2
)
async def start_(bot, message):
    reply_to = message.message_id
    await bot.send_message(
        message.chat.id,
        f"Hello **{message.from_user.first_name}**, thank you for using this bot...",
        reply_to_message_id=reply_to
    )
