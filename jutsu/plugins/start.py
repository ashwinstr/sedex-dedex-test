from pyrogram import Client, filters


@Client.on_message(
    filters.command(["start"])
)
async def start_(bot, message):
    await bot.send_message(
        message.chat.id,
        f"Hello {message.from_user.first_name}, thank you for using this bot...",
    )
