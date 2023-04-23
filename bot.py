import json

from re import escape

from aiocron import crontab
from decouple import config
from aiogram import Bot, Dispatcher, executor, types

import globals as g
import dock

TOKEN = config("TOKEN")
ADMIN = int(config("ADMIN"))

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    pass


@dp.message_handler(commands=["status"])
async def status(message: types.Message):
    containers = dock.containters()
    text = f"*Number of working containers:* `{len(containers)}`\n"
    for container in containers:
        text += escape(f"`{container['name']}`\n")
    await bot.send_message(message.from_user.id, text, parse_mode="MarkdownV2")


@crontab("* * * * *")
async def check_status():
    running_containers = dock.containters()
    if len(running_containers) == g.CONTAINERS_COUNT:
        with open(g.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(running_containers, f, indent=4, ensure_ascii=False)
    else:
        with open(g.DATA_FILE, "r", encoding="utf-8") as f:
            containers = json.load(f)

        stopped_containers = [
            container for container in containers if container not in running_containers
        ]

        text = "*Following containers have been stopped and restarted:*\n"

        for container in stopped_containers:
            text += escape(f"`{container['name']}`\n")
            dock.start_container(container)

        await bot.send_message(ADMIN, text, parse_mode="MarkdownV2")


if __name__ == "__main__":
    executor.start_polling(dp)
