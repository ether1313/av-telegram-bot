import os
import asyncio
from datetime import datetime
from telegram import Bot
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

BOT_TOKEN = os.getenv("FORWARD_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
SOURCE_GROUP_ID = int(os.getenv("FORWARD_GROUP_ID", "-1003199070793"))
TARGET_CHANNEL = os.getenv("FORWARD_TARGET_CHANNEL", "@yourtargetchannel")

bot = Bot(token=BOT_TOKEN)

# === Message ID groups (5 messages per batch) ===
MESSAGE_GROUPS = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15]
]

STATE_FILE = "forward_round.txt"

async def forward_messages():
    """Forward one batch of messages based on saved state."""
    # Read last round index
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            round_index = int(f.read().strip())
    else:
        round_index = 0

    current_group = MESSAGE_GROUPS[round_index]
    next_index = (round_index + 1) % len(MESSAGE_GROUPS)

    print("=" * 70)
    print(f"🕓 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🚀 Forwarding group {round_index + 1}: {current_group}")
    print("-" * 70)

    for msg_id in current_group:
        try:
            await bot.copy_message(
                chat_id=TARGET_CHANNEL,
                from_chat_id=SOURCE_GROUP_ID,
                message_id=msg_id
            )
            print(f"✅ Forwarded message ID: {msg_id}")
            await asyncio.sleep(3)
        except Exception as e:
            print(f"⚠️ Failed to forward message {msg_id}: {e}")

    print(f"✅ Group {round_index + 1} done. Next group will be {next_index + 1}.")
    print("=" * 70)

    # Save the next index
    with open(STATE_FILE, "w") as f:
        f.write(str(next_index))

async def schedule_loop():
    """Run the forward task every 6 hours."""
    print("🤖 Forward bot started — will forward messages every 6 hours.")
    while True:
        await forward_messages()
        print("⏳ Waiting 6 hours for the next round...")
        await asyncio.sleep(6 * 60 * 60)  # 6 hours = 21600 seconds

if __name__ == "__main__":
    asyncio.run(schedule_loop())
