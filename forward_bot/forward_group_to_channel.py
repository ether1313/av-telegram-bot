import os
import asyncio
from datetime import datetime
from telegram import Bot
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

BOT_TOKEN = os.getenv("FORWARD_BOT_TOKEN", "7640340584:AAFRegFmJmrx-44r93wnQJFNPmtVQ_M0pKc")
SOURCE_GROUP_ID = int(os.getenv("FORWARD_GROUP_ID", "-1003199070793"))  # Source group ID
TARGET_CHANNEL = os.getenv("FORWARD_TARGET_CHANNEL", "@hottxvideos18plus")  # Target channel ID
INTERVAL_HOURS = int(os.getenv("INTERVAL_HOURS", 6))  # Interval in hours between each round

# ✅ All message IDs
MESSAGE_IDS = [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61]

# === Group into cycles ===
GROUPS = [
    MESSAGE_IDS[0:6],    # Round 1: first 6
    MESSAGE_IDS[6:12],   # Round 2: next 6
    MESSAGE_IDS[12:15] + MESSAGE_IDS[0:3]  # Round 3: last 3 + first 3
]

bot = Bot(token=BOT_TOKEN)

async def forward_fixed_messages():
    round_index = 0  # which group to send this round

    while True:
        try:
            current_group = GROUPS[round_index]
            next_group = GROUPS[(round_index + 1) % len(GROUPS)]

            print("=" * 70)
            print(f"🕓 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"🚀 Round {round_index + 1} started — sending these message IDs:")
            print(f"👉 {current_group}")
            print("-" * 70)

            # === Forward each message ===
            for msg_id in current_group:
                try:
                    await bot.copy_message(
                        chat_id=TARGET_CHANNEL,
                        from_chat_id=SOURCE_GROUP_ID,
                        message_id=msg_id
                    )
                    print(f"✅ Forwarded message ID: {msg_id}")
                except Exception as e:
                    print(f"⚠️ Failed to forward message ID {msg_id}: {e}")

            print("-" * 70)
            print(f"✅ This round ({round_index + 1}) finished successfully.")
            print(f"🔁 Next round will send these message IDs: {next_group}")
            print(f"⏳ Waiting {INTERVAL_HOURS} hours before next round...\n")
            print("=" * 70 + "\n")

            # Move to next group
            round_index = (round_index + 1) % len(GROUPS)

            await asyncio.sleep(INTERVAL_HOURS * 3600)

        except Exception as e:
            print(f"Error occurred: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    print(f"🤖 Bot started — forwarding grouped messages every {INTERVAL_HOURS} hours.\n")
    asyncio.run(forward_fixed_messages())
