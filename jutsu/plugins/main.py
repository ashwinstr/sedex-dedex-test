import re
from sre_constants import error as sre_err

from unidecode import unidecode
from pyrogram import Client, filters
from pyrogram.errors import MessageDeleteForbidden

DELIMITERS = ("/", ":", "|", "_")


async def separate_sed(sed_string):
    """Separate sed arguments."""
    
    if str(sed_string).endswith(" -n"):
        sed_string = sed_string.replace(" -n", "")
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
    filters.regex(pattern=r"^[a]/*/*"), group=-1
)
async def sed(bot, message):
    """For sed command, use sed on Telegram."""
    og_text = message.text
    if not str(og_text).endswith(" -n"):
            try:
                await bot.delete_messages(message.chat.id, [message.message_id])
            except MessageDeleteForbidden:
                pass 
    reply_ = message.reply_to_message
    is_reply = True
    if not reply_:
        is_reply = False
    else:
        if not reply_.text and not reply_.caption:
            await bot.send_message(message.chat.id, "Reply to message with text plox...", reply_to_message_id=reply_.message_id)
            return
    sed_result = await separate_sed(og_text)
    if sed_result:
        repl, repl_with, flags = sed_result
    else:
        return
    if not repl:
            return await bot.send_message(
                "`Master, I don't have brains. Well you neither I guess.`"
            ) 
    if is_reply:
        textx = await bot.get_messages(message.chat.id, message.reply_to_message.message_id)
        reply_to = message.reply_to_message.message_id
    else:
        found = False
        last = False
        for one in range(15):
            msg_id = (message.message_id - one) - 1
            try:
                textx = await bot.get_messages(message.chat.id, msg_id)
                if not last:
                    last_msg = textx
                    last = True
            except:
                continue
            if textx.text:
                msg_text = textx.text
                if repl in msg_text:
                    reply_to = textx.message_id
                    found = True
                    break
#        async for textx in bot.search_messages(message.chat.id, query=str(repl), limit=1):
#            reply_to = textx.message_id
#            found = True
        if not found:
            textx = last_msg
            reply_to = textx.message_id
    if sed_result:
        if textx:
            to_fix = textx.text
        else:
            return await bot.send_message(
                "`Master, I don't have brains. Well you neither I guess.`"
            )
        try:
            repl_with = unicode(repl_with)
        except:
            pass
        try:
            check = re.match(repl, to_fix, flags=re.IGNORECASE)
            if check and check.group(0).lower() == to_fix.lower():
                 pass
            if "i" in flags and "g" in flags:
                text = re.sub(fr"{repl}", repl_with, to_fix, flags=re.I).strip()
            elif "i" in flags:
                text = re.sub(fr"{repl}", repl_with, to_fix, count=1, flags=re.I).strip()
            elif "g" in flags:
                text = re.sub(fr"{repl}", repl_with, to_fix).strip()
            else:
                text = re.sub(fr"{repl}", repl_with, to_fix, count=1).strip()
        except sre_err as e:
#            return await bot.send_message(message.chat.id, f"ERROR: {e}")
            return await bot.send_message(message.chat.id, "[**Learn Regex**](https://regexone.com)")
        if text:
            await bot.send_message(message.chat.id, text, reply_to_message_id=reply_to)
           
