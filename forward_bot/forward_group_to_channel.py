import os
import asyncio
from datetime import datetime, timedelta
from telegram import Bot
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

BOT_TOKEN = os.getenv("FORWARD_BOT_TOKEN", "7640340584:AAFRegFmJmrx-44r93wnQJFNPmtVQ_M0pKc")
SOURCE_GROUP_ID = int(os.getenv("FORWARD_GROUP_ID", "-1003199070793"))
TARGET_CHANNEL = os.getenv("FORWARD_TARGET_CHANNEL", "@hottxvideos18plus")

# === Define message groups ===
MESSAGE_GROUPS = [
    [47, 48, 49, 50, 51],
    [52, 53, 54, 55, 56],
    [57, 58, 59, 60, 61],
]

bot = Bot(token=BOT_TOKEN)


async def forward_messages(message_ids, round_label):
    print("=" * 70)
    print(f"🕓 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🚀 Sending batch ({round_label}): {message_ids}")
    print("-" * 70)

    for msg_id in message_ids:
        try:
            await bot.copy_message(
                chat_id=TARGET_CHANNEL,
                from_chat_id=SOURCE_GROUP_ID,
                message_id=msg_id
            )
            print(f"✅ Forwarded message ID: {msg_id}")
            await asyncio.sleep(3)  # small delay between messages
        except Exception as e:
            print(f"⚠️ Failed to forward {msg_id}: {e}")

    print(f"✅ Batch {round_label} complete.")
    print("=" * 70)


async def schedule_loop():
    print("🤖 Bot started (auto 6-hour cycle mode).")

    # Load the last round index from file (if exists)
    state_file = "forward_state.txt"
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            round_index = int(f.read().strip())
    else:
        round_index = 0

    while True:
        current_group = MESSAGE_GROUPS[round_index]
        label = f"Round {round_index + 1}"

        await forward_messages(current_group, label)

        # Save next round index for persistence
        next_index = (round_index + 1) % len(MESSAGE_GROUPS)
        with open(state_file, "w") as f:
            f.write(str(next_index))

        print(f"🕒 Next batch in 6 hours (will send group {next_index + 1}).")
        await asyncio.sleep(6 * 60 * 60)  # 6 hours delay

        round_index = next_index


if __name__ == "__main__":
    asyncio.run(schedule_loop())
