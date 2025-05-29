import json
import os
from pyrogram import Client
from pyrogram.errors import FloodWait
from time import sleep

CONFIG_FILE = "config.json"
OUTPUT_FILE = "data/users.json"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(users, f, indent=4)
    print(f"\n✅ Saved {len(users)} users to {OUTPUT_FILE}")

def get_group_members():
    config = load_config()
    api_id = config["api_id"]
    api_hash = config["api_hash"]
    session_name = config.get("session_name", "my_session")

    group_username = input("📥 Enter the group username (with @): ").strip()
    if not group_username.startswith("@"):
        print("❌ Please enter a valid group username (starting with @)")
        return

    app = Client(session_name, api_id=api_id, api_hash=api_hash)

    with app:
        users = []
        print("🔍 Collecting members from group...")

        try:
            for member in app.get_chat_members(group_username):
                user_id = member.user.id
                users.append({"user_id": user_id})
                print(f"➕ Found user ID: {user_id}")
                sleep(1)  # Slow scraping to avoid flood
        except FloodWait as e:
            print(f"⏳ Flood wait! Sleeping for {e.value} seconds.")
            sleep(e.value)
        except Exception as e:
            print(f"❌ Error occurred: {e}")
            return

    save_users(users)

if __name__ == "__main__":
    get_group_members()
