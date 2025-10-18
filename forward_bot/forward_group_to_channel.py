import os
import asyncio
from datetime import datetime, timedelta
from telegram import Bot
from dotenv import load_dotenv

# === 載入環境變數 ===
load_dotenv()

BOT_TOKEN = os.getenv("FORWARD_BOT_TOKEN", "7640340584:AAFRegFmJmrx-44r93wnQJFNPmtVQ_M0pKc")
SOURCE_GROUP_ID = int(os.getenv("FORWARD_GROUP_ID", "-1003199070793"))
TARGET_CHANNEL = os.getenv("FORWARD_TARGET_CHANNEL", "@hottxvideos18plus")

bot = Bot(token=BOT_TOKEN)


async def forward_recent_messages():
    """轉發群組內過去 4 小時的新訊息"""
    print(f"\n🕓 檢查時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        # 計算過去 4 小時的時間範圍
        four_hours_ago = datetime.now() - timedelta(hours=4)

        # 取得最近 100 條訊息（Telegram 限制）
        updates = await bot.get_chat_history(chat_id=SOURCE_GROUP_ID, limit=100)

        count = 0
        for msg in reversed(updates):
            if msg.date.replace(tzinfo=None) > four_hours_ago:
                try:
                    await msg.forward(chat_id=TARGET_CHANNEL)
                    count += 1
                except Exception as e:
                    print(f"⚠️ 無法轉發訊息: {e}")

        print(f"✅ 本輪共轉發 {count} 則訊息")

    except Exception as e:
        print(f"⚠️ 任務錯誤: {e}")


async def scheduler():
    """每 4 小時自動執行"""
    while True:
        await forward_recent_messages()
        print("⏳ 等待下一輪（4 小時後）...")
        await asyncio.sleep(4 * 60 * 60)  # 4 小時


if __name__ == "__main__":
    print("🤖 Scheduled Forward Bot 啟動中，每 4 小時自動轉發一次...")
    asyncio.run(scheduler())
