import os
import asyncio
from datetime import datetime
from telegram import Bot
from dotenv import load_dotenv

# === 載入環境變數 ===
load_dotenv()

BOT_TOKEN = os.getenv("FORWARD_BOT_TOKEN", "7640340584:AAFRegFmJmrx-44r93wnQJFNPmtVQ_M0pKc")
SOURCE_GROUP_ID = int(os.getenv("FORWARD_GROUP_ID", "-1003199070793"))  # 群組 ID
TARGET_CHANNEL = os.getenv("FORWARD_TARGET_CHANNEL", "@hottxvideos18plus")  # 頻道 ID
INTERVAL_HOURS = int(os.getenv("INTERVAL_HOURS", 4))  # 每幾小時轉發一次

# ✅ 固定要轉發的訊息 ID
MESSAGE_IDS = [41, 42, 43, 44, 46]

bot = Bot(token=BOT_TOKEN)

async def forward_fixed_messages():
    while True:
        try:
            print(f"\n🕓 檢查時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            for msg_id in MESSAGE_IDS:
                try:
                    await bot.copy_message(
                        chat_id=TARGET_CHANNEL,
                        from_chat_id=SOURCE_GROUP_ID,
                        message_id=msg_id
                    )
                    print(f"✅ 成功重新轉發訊息 ID: {msg_id}")
                except Exception as e:
                    print(f"⚠️ 無法轉發訊息 ID {msg_id}: {e}")

            print(f"⏳ 等待下一輪（{INTERVAL_HOURS} 小時後）...\n")
            await asyncio.sleep(INTERVAL_HOURS * 3600)

        except Exception as e:
            print(f"💥 錯誤：{e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    print(f"🤖 Scheduled Forward Bot 啟動中，每 {INTERVAL_HOURS} 小時自動轉發一次固定訊息...")
    asyncio.run(forward_fixed_messages())
