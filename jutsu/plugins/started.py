
import logging
from jutsu import Config, sedex

_LOG = logging.getLogger(__name__)

async def _init() -> None:
    try:
        await sedex.send_message(Config.LOG_CHANNEL_ID, "### **Sedex has started** ###")
    except Exception as e:
        print(e)
        _LOG.debug("ERROR in _init: %s", str(e))