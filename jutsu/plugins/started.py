
from jutsu import Config, sedex

async def _init() -> None:
    await sedex.send_message(Config.LOG_CHANNEL_ID, "### **Sedex has started** ###)
