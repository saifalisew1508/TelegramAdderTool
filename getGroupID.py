# getGroupID.py

from pyrogram import Client
import json

CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def get_group_info():
    config = load_config()

    api_id = config["api_id"]
    api_hash = config["api_hash"]
    session_name = config.get("session_name", "my_session")

    group_username = input("📥 Enter the group username (with @): ").strip()
    if not group_username.startswith("@"):
        print("❌ Please enter a valid username starting with @")
        return

    with Client(session_name, api_id=api_id, api_hash=api_hash) as app:
        try:
            chat = app.get_chat(group_username)
            print("\n✅ Group Info:")
            print(f"📛 Title: {chat.title}")
            print(f"🆔 ID: {chat.id}")
            print(f"📂 Type: {chat.type}")
            if chat.members_count:
                print(f"👥 Members: {chat.members_count}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    get_group_info()
