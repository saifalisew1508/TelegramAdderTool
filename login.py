import asyncio
import json

from helper.login import login, create
from helper.logs import log
from init import clr, banner, w, r, rs

clr()
banner()
print(f"  {r}Version: {w}3.1 {r}| Author: {w}SAIF ALI{rs}\n")
print(f"  {r}Telegram {w}@PrinceXofficial {r}| Instagram: {w}@saifalisew1508{rs}\n")


# load config for accounts
config = json.load(open("config.json", "r"))
group_source_id = str(config["group_source_username"])
group_target_id = str(config["group_target_username"])
auto_join = bool(config["auto_join"])
option = input("Login or Signup type one : ")


async def createall():
    PYRO = log("PYRO-START_LOGIN")
    PYRO.propagate = False
    for account in config["accounts"]:
        phone = account["phone"]
        api_id = int(account["api_id"])
        api_hash = account["api_hash"]
        PYRO.info(phone)
        await create(phone, api_id, api_hash)


async def loginall():
    PYRO = log("PYRO-START_LOGIN")
    PYRO.propagate = False
    for account in config["accounts"]:
        phone = account["phone"]
        api_id = int(account["api_id"])
        api_hash = account["api_hash"]
        PYRO.info(phone)
        await login(
            phone, api_id, api_hash, auto_join, group_source_id, group_target_id
        )


if option.lower()[0] == "l":
    asyncio.run(loginall())
elif option.lower()[0] == "s":
    asyncio.run(createall())
