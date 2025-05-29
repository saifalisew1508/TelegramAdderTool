import json
import time
import random
from pyrogram import Client, errors
from pyrogram.types import ChatMember

CONFIG_FILE = "config.json"
USERS_FILE = "data/users.json"

# Load config data
def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

# Load users to add
def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

# Add a single user to the group
def add_user_to_group(app, group_id, user_id):
    try:
        app.add_chat_members(group_id, user_id)
        print(f"✅ Added user {user_id}")
        return True
    except errors.UserAlreadyParticipant:
        print(f"⚠️ User {user_id} is already in the group.")
    except errors.PeerFlood:
        print("❌ PeerFloodError! Too many requests. Stop and try again later.")
        exit()
    except errors.UserPrivacyRestricted:
        print(f"🚫 User {user_id} has privacy settings that block invites.")
    except Exception as e:
        print(f"❌ Failed to add {user_id}: {str(e)}")
    return False

# Main function
def main():
    config = load_config()
    users = load_users()

    api_id = config["api_id"]
    api_hash = config["api_hash"]
    session_name = config.get("session_name", "my_session")
    group_id = config.get("target_group")

    if not group_id:
        print("❌ Group ID not specified in config.json")
        return

    app = Client(session_name, api_id=api_id, api_hash=api_hash)

    with app:
        print(f"🚀 Starting to add members to {group_id}...")

        for user in users:
            user_id = user.get("user_id")
            if not user_id:
                print("⚠️ Skipping invalid user entry.")
                continue

            added = add_user_to_group(app, group_id, user_id)

            # Delay to avoid flooding
            time.sleep(random.randint(10, 20))

        print("🎉 Finished adding users.")

if __name__ == "__main__":
    main()
