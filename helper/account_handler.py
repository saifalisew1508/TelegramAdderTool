import asyncio
import json
import os
import ast
import signal
import sys
import readchar
import platform
from datetime import datetime, timedelta
from pathlib import Path
import logging

from pyrogram import Client, enums
from pyrogram.errors import (
    YouBlockedUser,
    RPCError,
    FloodWait,
    ChatAdminRequired,
    PeerFlood,
    PeerIdInvalid,
    UserIdInvalid,
    UserPrivacyRestricted,
    UserRestricted,
    ChannelPrivate,
    UserNotMutualContact,
    PhoneNumberBanned,
    UserChannelsTooMuch,
    UserKicked,
    UserDeactivated,  # updated: was UserDeactivatedBan
    UsernameNotOccupied,
)
from helper.applist import addlogin
from helper.logs import log

# update the py for info
def updatecount(count):
    with open("current_count.py", "w") as g:
        g.write(str(count))


async def add_member(user_id, config, active, method):
    # Stop gracefully when a signal is received.
    def handler(signum, frame):
        msg = " Ctrl-c OR Ctrl-z was pressed. Do you really want to exit? y/n "
        print(msg)
        res = readchar.readchar()
        if res.lower() == "y":
            updatecount(counterall)
            PYRO.info("Bye!")
            sys.exit()
        else:
            PYRO.info("Okay then, I will continue.")

    # Create logger
    PYRO = log("PYRO-Adder")
    PYRO.propagate = False

    # Check if need to continue (read the current counter)
    try:
        with open("current_count.py") as f:
            data = f.read()
            counterall = ast.literal_eval(data)
            counter = counterall["counter"]
            added2 = counterall["added"]
            skipped2 = counterall["skipped"]
            privacy2 = counterall["privacy"]
            uc2 = counterall["already in too many channel/group"]
    except Exception:
        counter = added2 = skipped2 = privacy2 = uc2 = 0
        counterall = {}

    chat_idt = int(str(-100) + str(config["group_target"]))
    g_s_id = int(str(-100) + str(config["group_source"]))

    # Initialize counters
    added = skipped = privacy = uc = um = bot = noname = osr = 0
    waittime = config.get("wait_time", 10)

    async def prints():
        updatecount(counterall)
        wait_time = waittime / len(applist)
        PYRO.info(f"Sleeping: {wait_time} seconds")
        await asyncio.sleep(wait_time)

    def printfinal():
        print(
            f"{added} : members were added\n"
            f"{skipped} : members were skipped\n"
            f"{privacy} : members had privacy enabled or not in mutual contact\n"
            f"{uc} : user banned in chat\n"
            f"{um} : members not in mutual contact\n"
            f"{bot}: bot account skipped"
        )
        if method == "username":
            PYRO.info(f"{noname} : account has no username")
        updatecount(counterall)
        print(datetime.now().strftime("%H:%M:%S"))

    total_account = len(config["accounts"])
    PYRO.info(f"Total accounts trying to login: {total_account}")
    await asyncio.sleep(0.2)
    applist = await addlogin(config["accounts"], g_s_id)
    logined_account = len(applist)
    PYRO.info(f"Total logged-in accounts: {logined_account}")
    await asyncio.sleep(1)

    usermethod = "username" if method[0] == "u" else "userid"
    print(len(user_id), counter)

    if platform.system() == "Windows":
        signal.signal(signal.SIGTERM, handler)
        signal.signal(signal.SIGINT, handler)
    else:
        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGTSTP, handler)

    while len(user_id) - counter > 1:
        leftmem = len(user_id) - counter
        counterall = {
            "counter": int(counter),
            "left_to_add": int(leftmem),
            "added": int(added2) + int(added),
            "skipped": int(skipped2) + int(skipped),
            "privacy": int(privacy2) + int(privacy),
            "already in too many channel/group": int(uc2) + int(uc),
        }
        for account in applist:
            try:
                if not applist:
                    printfinal()
                    exit()
                elif added == (30 * len(applist)):
                    printfinal()
                    PYRO.info("Sleeping for two hours")
                    now = datetime.now()
                    end = now + timedelta(hours=2)
                    print("Sleep started at: ", now.strftime("%H:%M:%S"))
                    print("Sleep ends at: ", end.strftime("%H:%M:%S"))
                    added = 0
                    await asyncio.sleep(3500)
                    PYRO.info("1 hour left to continue")
                    await asyncio.sleep(3500)
            except Exception as e:
                PYRO.info(str(e))
            phone = account["phone"]
            app = account["app"]
            try:
                while (
                    user_id[counter]["bot"] == True
                    or user_id[counter][usermethod] == "None"
                    or user_id[counter]["status"] not in active
                ):
                    try:
                        if user_id[counter]["status"] not in active:
                            counter += 1
                            skipped += 1
                            updatecount(counterall)
                            PYRO.info("Inactive user skipped")
                        if user_id[counter]["bot"] == True:
                            counter += 1
                            bot += 1
                            updatecount(counterall)
                            PYRO.info("Bot skipped")
                        if user_id[counter][usermethod] == "None":
                            counter += 1
                            noname += 1
                            updatecount(counterall)
                            PYRO.info("No USERNAME found for this user; skipped")
                    except Exception:
                        printfinal()
                        PYRO.info("Finished")
                        return
            except Exception:
                printfinal()
                PYRO.info("Finished")
                return
            try:
                postiton = applist.index(account)
                current_user = user_id[counter]["userid"]
                postion2 = len(applist)
                PYRO.info(
                    f"Trying to add {current_user} using account {phone} (position: {postiton + 1} / {postion2})"
                )
                await app.add_chat_members(
                    chat_id=chat_idt, user_ids=user_id[counter][usermethod]
                )
                PYRO.info(f"{current_user} added successfully")
                counter += 1
                added += 1
                await prints()
            except UserBannedInChannel:
                await app.stop()
                applist.remove(account)
                PYRO.info("Phone number limited")
                await prints()
            except UsernameNotOccupied:
                PYRO.info("User not using username anymore")
                counter += 1
                await prints()
            except UserDeactivated:
                PYRO.info("User removed from Telegram")
                counter += 1
                await prints()
            except UserKicked:
                PYRO.info("This user is banned")
                counter += 1
                await prints()
            except PhoneNumberBanned:
                await app.stop()
                applist.remove(account)
                PYRO.info(f"Phone number banned: {phone}")
                await prints()
            except PeerFlood:
                applist.remove(account)
                await app.stop()
                counter += 1
                PYRO.info(f"{phone} removed for this run")
                try:
                    await prints()
                except Exception:
                    printfinal()
            except UserChannelsTooMuch:
                counter += 1
                uc += 1
                PYRO.info("User already in too many channels")
                await prints()
            except FloodWait as e:
                applist.remove(account)
                await app.stop()
                PYRO.info(f"{e.value} seconds sleep required for account {phone}")
            except (ChatAdminRequired, ChannelPrivate):
                PYRO.info("Chat admin permission required or Channel is private")
                applist.remove(account)
                await app.stop()
                await prints()
            except UserRestricted:
                PYRO.info("Removing this restricted account")
                applist.remove(account)
                await app.stop()
            except UserIdInvalid:
                PYRO.info(f"User invalid or never met user {phone}")
                counter += 1
                await prints()
            except UserNotMutualContact:
                PYRO.info("User is not a mutual contact")
                counter += 1
                um += 1
                await prints()
            except PeerIdInvalid:
                PYRO.info("If you see this line many times, rerun the get_data.py script")
                counter += 1
                await prints()
            except UserPrivacyRestricted:
                PYRO.info("User has privacy enabled")
                counter += 1
                privacy += 1
                await prints()
            except TimeoutError:
                PYRO.info("Network problem encountered")
            except RPCError as e:
                PYRO.info(f"{phone} encountered an RPC error")
                PYRO.info(f"{e}")
                m = user_id[counter][usermethod]
                PYRO.info(f"{m}")
                counter += 1
                await prints()
            except OSError:
                osr += 1
            except BaseException as e:
                PYRO.info(phone, "error info below")
                PYRO.info(f"{e}")
                m = user_id[counter][usermethod]
                PYRO.info(f"{m}")
                counter += 1
                await prints()
            if osr == 30:
                PYRO.info("OSError count reached 30")
                PYRO.info("This might be due to internet problems; try again later")
                await prints()
                exit()