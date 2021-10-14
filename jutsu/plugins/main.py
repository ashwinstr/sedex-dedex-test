import re
from sre_constants import error as sre_err

from pyrogram import Client, filters

DELIMITERS = ("/", ":", "|", "_")


async def separate_sed(sed_string):
    """Separate sed arguments."""
    
    if len(sed_string) < 1:
        return

    if sed_string[1] in DELIMITERS and sed_string.count(sed_string[1]) >= 1:
        delim = sed_string[1]
        start = counter = 2
        while counter < len(sed_string):
            if sed_string[counter] == "\\":
                counter += 1

            elif sed_string[counter] == delim:
                replace = sed_string[start:counter]
                counter += 1
                start = counter
                break

            counter += 1

        else:
            return None

        while counter < len(sed_string):
            if (
                sed_string[counter] == "\\"
                and counter + 1 < len(sed_string)
                and sed_string[counter + 1] == delim
            ):
                sed_string = sed_string[:counter] + sed_string[counter + 1 :]

            elif sed_string[counter] == delim:
                replace_with = sed_string[start:counter]
                counter += 1
                break

            counter += 1
        else:
            return replace, sed_string[start:], ""

        flags = ""
        if counter < len(sed_string):
            flags = sed_string[counter:]
        return replace, replace_with, flags.lower()
    return None


@Client.on_message(
    filters.regex(pattern="s/*/*")
)
async def sed(bot, message):
    """For sed command, use sed on Telegram."""
    text = message.text
    reply_ = message.reply_to_message
    if not reply_:
        return
    sed_result = await separate_sed(text)
    textx = await bot.get_messages(message.chat.id, message.reply_to_message.message_id)
    if sed_result:
        if textx:
            to_fix = textx.text
        else:
            return await bot.send_message(
                "`Master, I don't have brains. Well you neither I guess.`"
            )

        repl, repl_with, flags = sed_result

        if not repl:
            return await bot.send_message(
                "`Master, I don't have brains. Well you neither I guess.`"
            )

        try:
            check = re.match(repl, to_fix, flags=re.IGNORECASE)
            if check and check.group(0).lower() == to_fix.lower():
                return await bot.send_message(message.chat.it, "`Boi!, that's a reply. Don't use sed`")

            if "i" in flags and "g" in flags:
                text = re.sub(repl, repl_with, to_fix, flags=re.I).strip()
            elif "i" in flags:
                text = re.sub(repl, repl_with, to_fix, count=1, flags=re.I).strip()
            elif "g" in flags:
                text = re.sub(repl, repl_with, to_fix).strip()
            else:
                text = re.sub(repl, repl_with, to_fix, count=1).strip()
        except sre_err:
            return await bot.send_message("[**Learn Regex**](https://regexone.com)")
        if text:
            await bot.send_message(message.chat.id, f"`{text}`", reply_to_message_id=reply_.message_id)
            
        if text.endswith("-d"):
            try:
                await bot.delete_messages(message.chat.id, message.message_id)
            except:
                pass
