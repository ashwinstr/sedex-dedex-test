import heroku3
import os
from os import system
import asyncio
import time

from pyrogram import Client, filters
from git import Repo
from git.exc import GitCommandError


HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
HEROKU_ENV = True
HEROKU_APP = (
        heroku3.from_key(HEROKU_API_KEY).apps()[HEROKU_APP_NAME]
        if HEROKU_ENV and HEROKU_API_KEY and HEROKU_APP_NAME
        else None
    )


@Client.on_message(
    filters.command(["test"], prefixes=";")
    & filters.user([1013414037]),
    group=4
)
async def tester_(bot, message):
    input_ = message.text
    up_repo = "http://github.com/ashwinstr/sedex"
    branch = "main"
    repo = Repo()
    await bot.send_message(message.chat.id, "testing") 
    try:
        out = _get_updates(repo, branch)
    except GitCommandError as g_e:
        if "128" in str(g_e):
            system(
                f"git fetch {up_repo} {branch} && git checkout -f {branch}"
            )
            out = _get_updates(repo, branch)
        else:
            await bot.send_message(message.chat.id, g_e)
            return
    if input_.endswith("-pull"):
        if out:
            send = await bot.send_message(message.chat.id, f"`New update found for [{branch}], Now pulling...`")
            await _pull_from_repo(repo, branch)
            await send.edit(
                "**SedexBot Successfully Updated!**\n"
                "`Now restarting... Wait for a while!`",
            )
            asyncio.get_event_loop().create_task(bot.restart(True))
        else:
            await bot.send_message(message.chat.id, "**SedexBot is up-to-date.**")
    else:
        if out:
            change_log = (
                f"**New UPDATE available for [{branch}]:\n\n📄 CHANGELOG 📄**\n\n"
            )
            await bot.send_message(
                message.chat.id,
                change_log + out, disable_web_page_preview=True
            )
        else:
            uptodate = await bot.send_message(message.chat.id, f"**SedexBot is up-to-date with [{branch}]**")
        return 

def _get_updates(repo: Repo, branch: str) -> str:
    up_repo = "http://github.com/ashwinstr/sedex"
    repo.remote(up_repo).fetch(branch)
    upst = up_repo.rstrip("/")
    out = ""
    for i in repo.iter_commits(f"HEAD..{up_repo}/{branch}"):
        out += f"🔨 **#{i.count()}** : [{i.summary}]({upst}/commit/{i}) 👷 __{i.author}__\n\n"
    return out


async def _pull_from_repo(repo: Repo, branch: str) -> None:
    up_repo = "http://github.com/ashwinstr/sedex"
    repo.git.checkout(branch, force=True)
    repo.git.reset("--hard", branch)
    repo.remote(up_repo).pull(branch, force=True)
    await asyncio.sleep(1) 


@Client.on_message(
    filters.command(["update"], prefixes=";")
    & filters.user([1013414037]),
    group=0
)
async def updater_(bot, message):
    if HEROKU_APP:
        await bot.send_message(
            message.chat.id,
            "`Heroku app found, trying to restart dyno...\nthis will take upto 30 sec`",
        )
        Config.HEROKU_APP.restart()
        time.sleep(20)
    else:
        await bot.send_message(message.chat.id, "`Restarting [HARD] ...`")
        asyncio.get_event_loop().create_task(bot.restart(hard=True))
