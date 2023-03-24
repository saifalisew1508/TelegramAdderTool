import json
import csv
from csv import reader
from pathlib import Path
import re
import time
from colorama import init, Fore
import pyfiglet
import os, random

lg = Fore.LIGHTGREEN_EX
rs = Fore.RESET
r = Fore.RED
w = Fore.WHITE
cy = Fore.CYAN


info = lg + '(' + w + 'i' + lg + ')' + rs
error = lg + '(' + r + '!' + lg + ')' + rs
success = w + '(' + lg + '+' + w + ')' + rs
INPUT = lg + '(' + cy + '~' + lg + ')' + rs
colors = [lg, w, r, cy]


def banner():
    f = pyfiglet.Figlet(font='slant')
    logo = f.renderText('Tele Adder')
    print(random.choice(colors) + logo + rs)
    
def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

clr()
banner()
print(f'  {r}Version: {w}3.1 {r}| Author: {w}SAIF ALI{rs}\n')
print(f'  {r}Telegram {w}@PrinceXofficial {r}| Instagram: {w}@saifalisew1508{rs}\n')
print(f'  {r}For Get Your Group ID Add {w}@MissCutieRobot {r}To Your Group And Send /id In Your Group After Get Your Group ID Remove -100 From Your Group ID Before Enter In Script\n')


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
delay = int(input("Enter Delay Timing For Per Member Adding : "))
group_source = input("Enter The Group ID Of The Group From Which The Members Have To Be Scraped : ")
group_target = input("Enter The Group ID Of The Group In Which The Member Is To Be Added : ")
group_source_username = input("Enter The Username Of The Group From Which The Members Have To Be Scraped : ")
if '+' in group_source_username:
    pass
else:
    group_source_username = re.sub(
    "(@)|(https://t.me/)|(http://t.me/)",
    "",
     group_source_username)
group_target_username = input("Enter The Username Of The Group In Which The Member Is To Be Added : ")
if '+' in group_target_username:
    pass
else:
    group_target_username = re.sub(
    "(@)|(https://t.me/)|(http://t.me/)",
    "",
     group_target_username)

choice = input(f"\n\nType YES To Add API And HASH Manually\nType NO To Use Default One From Telegram :> ").lower()


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
                                "wait_time": delay,
                                "accounts": []
                            }
                for pphone in str_list:
                    phone = check_num(pphone)
                    po += 1
                    print(f"{phone} Added To Config Run python login.py To Login Your Accounts")
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
                                    "wait_time": delay, 
                                    "accounts": []
                                }
                count = int(input("How Many Numbers You Want To Add : "))
                while count > 0:
                    phon = input("Enter Your Number With Country Code : ")
                    phone = check_num(phon)
                    print(f"{phone} Added To Config Path Now Run python login.py To Login Your Accounts")
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
         count = int(input("How Many Numbers You Want To Add : "))
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
                                        "wait_time": delay, 
                                        "accounts": []
                                    }
             count = int(input("How Many Numbers You Want To Add : "))
         while count > 0:
              phon = input("Enter Your Number With Country Code : ")
              phone = check_num(phon)
              apiid = int(input("Enter Your API_ID : "))
              hashid=input("Enter Your API_HASH : ")
              print(f"{phone} Added To Config Path Run python login.py To Login Your Accounts")
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
