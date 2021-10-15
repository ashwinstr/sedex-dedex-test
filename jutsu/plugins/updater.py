
from os import system
import asyncio

from pyrogram import Client, filters
from git import Repo
from git.exc import GitCommandError

@userge.on_message(
    filters.command([update], prefixes=";"),
    filters.user([1013414037])
)
async def updater_(bot, message):
    input_ = message.text
    up_repo = "http://github.com/ashwinstr/regex"
    branch = "main"
    repo = Repo()
    try:
        out = _get_updates(repo, branch)
    except GitCommandError as g_e:
        if "128" in str(g_e):
            system(
                f"git fetch {up_repo} {branch} && git checkout -f {branch}"
            )
            out = _get_updates(repo, branch)
        else:
            await message.err(g_e, del_in=5)
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
            await bot.send_message(message.chat.id, "**SedexBot is already up-to-date.**")
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
    up_repo = "http://github.com/ashwinstr/regex"
    repo.remote(up_repo).fetch(branch)
    upst = up_repo.rstrip("/")
    out = ""
    for i in repo.iter_commits(f"HEAD..{up_repo}/{branch}"):
        out += f"🔨 **#{i.count()}** : [{i.summary}]({upst}/commit/{i}) 👷 __{i.author}__\n\n"
    return out


async def _pull_from_repo(repo: Repo, branch: str) -> None:
    up_repo = "http://github.com/ashwinstr/regex"
    repo.git.checkout(branch, force=True)
    repo.git.reset("--hard", branch)
    repo.remote(up_repo).pull(branch, force=True)
    await asyncio.sleep(1) 
