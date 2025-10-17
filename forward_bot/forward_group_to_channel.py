import os
import asyncio
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv

# === 載入環境變數 ===
load_dotenv()

BOT_TOKEN = os.getenv("FORWARD_BOT_TOKEN", "7640340584:AAFRegFmJmrx-44r93wnQJFNPmtVQ_M0pKc")
SOURCE_GROUP_ID = int(os.getenv("FORWARD_GROUP_ID", "-4760638966"))  # 群組 ID
TARGET_CHANNEL = os.getenv("FORWARD_TARGET_CHANNEL", "@hottxvideos18plus")  # 目標頻道
INTERVAL_HOURS = 4  # 每 4 小時執行一次

bot = Bot(token=BOT_TOKEN)


async def forward_group_messages():
    print(f"🚀 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 開始執行轉發週期...")
    messages_forwarded = 0

    try:
        # 使用迴圈抓取最近 100 條訊息
        async for msg in bot.get_chat_history(chat_id=SOURCE_GROUP_ID, limit=100):
            try:
                if msg.text:
                    await bot.send_message(chat_id=TARGET_CHANNEL, text=msg.text)
                elif msg.caption and msg.photo:
                    await bot.send_photo(chat_id=TARGET_CHANNEL, photo=msg.photo[-1].file_id, caption=msg.caption)
                elif msg.caption and msg.video:
                    await bot.send_video(chat_id=TARGET_CHANNEL, video=msg.video.file_id, caption=msg.caption)
                elif msg.document:
                    await bot.send_document(chat_id=TARGET_CHANNEL, document=msg.document.file_id, caption=msg.caption or "")
                else:
                    continue

                messages_forwarded += 1
                await asyncio.sleep(1)

            except TelegramError as e:
                print(f"⚠️ 無法發送訊息: {e}")

        print(f"✅ 本輪轉發完成，共 {messages_forwarded} 則。")

    except Exception as e:
        print(f"❌ 抓取或轉發出錯: {e}")

    print(f"🕒 等待 {INTERVAL_HOURS} 小時後再次執行...\n")


async def main():
    print(f"🤖 Forward Bot 已啟動（每 {INTERVAL_HOURS} 小時轉發群組訊息）")

    while True:
        await forward_group_messages()
        await asyncio.sleep(INTERVAL_HOURS * 3600)


if __name__ == "__main__":
    asyncio.run(main())
