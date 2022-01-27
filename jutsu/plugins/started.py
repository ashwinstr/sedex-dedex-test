
import logging
from jutsu import Config, sedex

async def _init() -> None:
    try:
        await sedex.send_message(Config.LOG_CHANNEL_ID, "### **Sedex has started** ###")
    except Exception as e:
        print(e)
