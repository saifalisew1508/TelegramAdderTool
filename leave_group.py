from pyrogram import Client
import json

CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def leave_group():
    config = load_config()

    api_id = config["api_id"]
    api_hash = config["api_hash"]
    session_name = config.get("session_name", "my_session")

    group_input = input("👋 Enter the group username (with @) or group ID: ").strip()
    if not group_input:
        print("❌ Group username or ID is required.")
        return

    with Client(session_name, api_id=api_id, api_hash=api_hash) as app:
        try:
            app.leave_chat(group_input)
            print(f"✅ Successfully left the group: {group_input}")
        except Exception as e:
            print(f"❌ Error leaving group: {e}")

if __name__ == "__main__":
    leave_group()
