# login.py

from pyrogram import Client
import os
import json

CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print("❌ Config file not found. Please run make_config.py first.")
        exit()
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def create_session():
    config = load_config()

    api_id = config.get("api_id")
    api_hash = config.get("api_hash")
    session_name = config.get("session_name", "my_session")

    print("📲 Starting login process...")

    app = Client(session_name, api_id=api_id, api_hash=api_hash)

    try:
        app.start()
        me = app.get_me()
        print(f"✅ Successfully logged in as: {me.first_name} (@{me.username})")
        app.stop()
    except Exception as e:
        print("⚠️ Login failed:", str(e))

if __name__ == "__main__":
    create_session()
