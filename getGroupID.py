import json
from pathlib import Path

from pyrogram import Client

root = Path.cwd()
config = json.load(open(root / "config.json"))
phone_data = config["accounts"][0]
phone = phone_data["phone"]

groupName = input("Group ID: ").lower()

with Client(phone, workdir="session") as app:
    chat = app.get_chat(groupName)
    # print(chat)
    print(str(chat.id))
