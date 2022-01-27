

import asyncio
import importlib
import logging

from typing import List
from types import ModuleType

from pyrogram import Client

from pyrogram.errors import MessageNotModified

from jutsu import Config, logbot
from jutsu.plugins import get_all_plugins

# logging.basicConfig(level=logging.INFO)

_LOG = logging.getLogger(__name__)
_LOG_STR = "<<<!  #####  %s  #####  !>>>"


_IMPORTED: List[ModuleType] = []
_INIT_TASKS: List[asyncio.Task] = []


async def _complete_init_tasks() -> None:
    if not _INIT_TASKS:
        return
    await asyncio.gather(*_INIT_TASKS)
    _INIT_TASKS.clear()


class _AbstractUserge(Client):
    async def finalize_load(self) -> None:
        """ finalize the plugins load """
        await asyncio.gather(_complete_init_tasks(), self.manager.init())

    async def load_plugin(self, name: str, reload_plugin: bool = False) -> None:
        """ Load plugin to Userge """
        _IMPORTED.append(
            importlib.import_module(f"userge.plugins.{name}"))
        if reload_plugin:
            _IMPORTED[-1] = importlib.reload(_IMPORTED[-1])
        plg = _IMPORTED[-1]
        self.manager.update_plugin(plg.__name__, plg.__doc__)
        if hasattr(plg, '_init'):
            # pylint: disable=protected-access
            if asyncio.iscoroutinefunction(plg._init):
                _INIT_TASKS.append(self.loop.create_task(plg._init()))

    async def _load_plugins(self) -> None:
        _IMPORTED.clear()
        _INIT_TASKS.clear()
        logbot.edit_last_msg("Importing All Plugins", _LOG.info, _LOG_STR)
        for name in get_all_plugins():
            try:
                await self.load_plugin(name)
            except ImportError as i_e:
                _LOG.error(_LOG_STR, f"[{name}] - {i_e}")
        await self.finalize_load()
        _LOG.info(_LOG_STR, f"Imported ({len(_IMPORTED)}) Plugins => "
                  + str([i.__name__ for i in _IMPORTED]))



class Sedex(_AbstractUserge):
    def __init__(self):
        kwargs = {
            'api_id': Config.API_ID,
            'api_hash': Config.API_HASH,
            'session_name': ':memory:',
            'bot_token': Config.BOT_TOKEN,
            'plugins': dict(root='jutsu/plugins')
        }
        super().__init__(**kwargs)

    async def start(self):
        await super().start()

    async def stop(self):
        await super().stop()

    async def sleep(self, msg):
        await msg.reply("`Sleeping for (10) Seconds.`")
        Config.HU_APP.restart()