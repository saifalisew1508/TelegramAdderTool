import json
import csv
from csv import reader
from pathlib import Path
import re
import time


def check_num(phone):
    """Parses the given phone, or returns None if it's invalid."""
    if isinstance(phone, int):
        return str(phone)
    else:
        phone = re.sub(r'[+()\s-]', '', str(phone))
        if phone.isdigit():
            return phone

DEFAULT_API_ID = 25194789
DEFAULT_API_HASH = "e59afe25c17585635ec031c889eb5b34"
DEFAULT = "UserStatus.RECENTLY"

OPTIONS = "UserStatus.LAST_MONTH", "UserStatus.LAST_WEEK", "UserStatus.OFFLINE", "UserStatus.RECENTLY", "UserStatus.ONLINE"
config_path = Path("config.json")
WAIMT_TYM = input("Enter delay time per request 0 for None, i suggest enter 5 to add members properly : ")
group_source = input("Enter the user ID of the group from which the members have to be scraped : ")
group_target = input("Enter the user ID of the group in which the member is to be added : ")
group_source_username = input("Enter the username of the group from which the members have to be scraped : ")
if '+' in group_source_username:
    pass
else:
    group_source_username = re.sub(
    "(@)|(https://t.me/)|(http://t.me/)",
    "",
     group_source_username)
group_target_username = input("Enter the username of the group in which the member is to be added : ")
if '+' in group_target_username:
    pass
else:
    group_target_username = re.sub(
    "(@)|(https://t.me/)|(http://t.me/)",
    "",
     group_target_username)

choice = input(f"\n\nType YES to add api and hash manually \nType NO to use default one from telegram :> ").lower()


def main():
    # for _ in range(n):
    if choice[0] == "n":
        with open('phone.csv', 'r') as f:
            str_list = [row[0] for row in csv.reader(f)]
            po = 0
            if str_list:
                config = {
                                "group_source": group_source,
                                "group_target": group_target,
                                "group_source_username": group_source_username,
                                "group_target_username": group_target_username,
                                "from_date_active": DEFAULT,
                                "auto_join": True, 
                                "spam_check": True,
                                "wait_time": WAIMT_TYM,
                                "accounts": []
                            }
                for pphone in str_list:
                    phone = check_num(pphone)
                    po += 1
                    print(f"{phone} added to config run python login.py to login")
                    new_account = {
                        "phone": phone,
                        "api_id": DEFAULT_API_ID,
                        "api_hash": DEFAULT_API_HASH
                    }
                    config["accounts"].append(new_account)
            else:
                if config_path.exists():
                    with open(config_path, 'r', encoding='utf-8') as file:
                        config = json.load(file)
                else:
                    config = {
                                    "group_source": group_source,
                                    "group_target": group_target,
                                    "group_source_username": group_source_username,
                                    "group_target_username": group_target_username,
                                    "from_date_active": DEFAULT,
                                    "auto_join": True,  
                                    "spam_check": True,  
                                    "wait_time": WAIMT_TYM, 
                                    "accounts": []
                                }
                count = int(input("how many numbers you want to add: "))
                while count > 0:
                    phon = input("enter ur number with country code: ")
                    phone = check_num(phon)
                    print(f"{phone} added to config run python login.py to login")
                    new_account = {
                        "phone": phone,
                        "api_id": DEFAULT_API_ID,
                        "api_hash": DEFAULT_API_HASH
                    }
                    config["accounts"].append(new_account)
                    count -= 1
        with open(config_path, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4)
    elif  choice[0] == "y":
         count = int(input("how many numbers you want to add: "))
         if config_path.exists():
             with open(config_path, 'r', encoding='utf-8') as file:
                 config = json.load(file)
         else:
             config = {
                                        "group_source": group_source,
                                        "group_target": group_target,
                                        "group_source_username": group_source_username,
                                        "group_target_username": group_target_username,
                                        "from_date_active": DEFAULT,
                                        "auto_join": True, 
                                        "spam_check": True,  
                                        "wait_time": WAIMT_TYM, 
                                        "accounts": []
                                    }
             count = int(input("how many numbers you want to add: "))
         while count > 0:
              phon = input("enter ur number with country code: ")
              phone = check_num(phon)
              apiid = int(input("enter api id: "))
              hashid=input("enter hash id: ")
              print(f"{phone} added to config run python login.py to login")
              new_account={
                            "phone": phone,
                            "api_id": apiid,
                            "api_hash": hashid
                        }
              config["accounts"].append(new_account)
              count -= 1
         with open(config_path, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4)
    else:
        print("wrong option use YES / NO")

main()
