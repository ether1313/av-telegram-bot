import os
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

# === 載入環境變數 ===
load_dotenv()

BOT_TOKEN = os.getenv("FORWARD_BOT_TOKEN", "7640340584:AAFRegFmJmrx-44r93wnQJFNPmtVQ_M0pKc")
SOURCE_GROUP_ID = int(os.getenv("FORWARD_GROUP_ID", "-4760638966"))
TARGET_CHANNEL = os.getenv("FORWARD_TARGET_CHANNEL", "@hottxvideos18plus")
INTERVAL_HOURS = int(os.getenv("INTERVAL_HOURS", 4))

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_recent_messages(chat_id, limit=50):
    """使用 getUpdates 代替抓取群組訊息"""
    try:
        url = f"{API_URL}/getUpdates"
        response = requests.get(url)
        data = response.json()

        messages = []
        for result in data.get("result", []):
            msg = result.get("message") or result.get("channel_post")
            if msg and msg.get("chat", {}).get("id") == chat_id:
                messages.append(msg)

        print(f"📦 抓取到 {len(messages)} 則符合群組的訊息")
        return messages[-limit:]  # 取最近幾則

    except Exception as e:
        print(f"⚠️ 無法抓取訊息: {e}")
        return []


def forward_message(msg):
    """把訊息轉發到頻道"""
    try:
        message_id = msg["message_id"]
        from_chat_id = msg["chat"]["id"]

        url = f"{API_URL}/forwardMessage"
        payload = {
            "chat_id": TARGET_CHANNEL,
            "from_chat_id": from_chat_id,
            "message_id": message_id
        }

        res = requests.post(url, data=payload)
        if res.status_code == 200:
            print(f"✅ 已轉發訊息 ID: {message_id}")
        else:
            print(f"⚠️ 轉發失敗 ({message_id}): {res.text}")

    except Exception as e:
        print(f"❌ 轉發錯誤: {e}")


def run_forward_cycle():
    print(f"\n🚀 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 開始執行轉發週期...")
    messages = get_recent_messages(SOURCE_GROUP_ID)
    if not messages:
        print("⚠️ 沒有可轉發的訊息。")
        return

    for msg in messages:
        forward_message(msg)
        time.sleep(2)

    print(f"✅ 本輪轉發完成，共 {len(messages)} 則。")


if __name__ == "__main__":
    print(f"🤖 Forward Bot 已啟動（每 {INTERVAL_HOURS} 小時轉發群組訊息）")
    while True:
        run_forward_cycle()
        print(f"🕒 等待 {INTERVAL_HOURS} 小時後再次執行...\n")
        time.sleep(INTERVAL_HOURS * 3600)
