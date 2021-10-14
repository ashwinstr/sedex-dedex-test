from pyrogram import filters, Client


@Client.on_message(
    filters.command(["help"], prefixes=";")
)
async def helper(bot, message):
    reply_to = message.message_id
    help = f"""
Hello there **{message.from_user.first_name}**, this is the Sedex bot.

**USAGE:**
Replace any part of the target message to have fun with friends...

**HOW:**
To use this bot, you need to send command with reply to the targeted message with the command.
`a/text that will be replaced/text that will replace`

**EXAMPLE:**
Reply to a message with text as "Hi, nice to meet you." with
`a/Hi/Bye`

For more help or to learn regex, go [here](www.regexone.com).

Good luck.
"""
    await bot.send_message(
        message.chat.id,
        help,
        reply_to_message_id=reply_to,
        disable_web_page_preview=True
    )
