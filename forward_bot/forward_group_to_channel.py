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
INTERVAL_HOURS = int(os.getenv("INTERVAL_HOURS", 4))  # Interval in hours between each round

# ✅ Fixed message IDs to forward
MESSAGE_IDS = [41, 42, 43, 44, 46]

bot = Bot(token=BOT_TOKEN)

async def forward_fixed_messages():
    while True:
        try:
            print(f"\n🕓 Checking time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            for msg_id in MESSAGE_IDS:
                try:
                    await bot.copy_message(
                        chat_id=TARGET_CHANNEL,
                        from_chat_id=SOURCE_GROUP_ID,
                        message_id=msg_id
                    )
                    print(f"✅ Successfully forwarded message ID: {msg_id}")
                except Exception as e:
                    print(f"⚠️ Failed to forward message ID {msg_id}: {e}")

            print(f"⏳ Waiting for the next round ({INTERVAL_HOURS} hours later)...\n")
            await asyncio.sleep(INTERVAL_HOURS * 3600)

        except Exception as e:
            print(f"💥 Error occurred: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    print(f"🤖 Scheduled Forward Bot started — automatically forwarding fixed messages every {INTERVAL_HOURS} hours...")
    asyncio.run(forward_fixed_messages())
