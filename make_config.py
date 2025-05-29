# make_config.py

import json
import os

CONFIG_FILE = "config.json"

def prompt_int(prompt_text):
    while True:
        try:
            return int(input(prompt_text))
        except ValueError:
            print("❌ Please enter a valid number.")

def create_config():
    print("🛠️ Let's set up your config file for TelegramAdderTool!\n")

    api_id = prompt_int("🔢 Enter your API ID: ")
    api_hash = input("🔐 Enter your API Hash: ").strip()
    session_name = input("💼 Enter a name for your session (default: my_session): ").strip()
    if not session_name:
        session_name = "my_session"

    group_id = input("👥 Enter the target group ID or username (with @): ").strip()
    if not group_id:
        print("❌ Group ID or username is required.")
        return

    config = {
        "api_id": api_id,
        "api_hash": api_hash,
        "session_name": session_name,
        "target_group": group_id
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

    print(f"\n✅ Config saved successfully to '{CONFIG_FILE}'.")

if __name__ == "__main__":
    create_config()
