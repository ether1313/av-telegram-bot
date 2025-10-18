import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# === 載入環境變數 ===
load_dotenv()

# === Telegram 基本設定 ===
BOT_TOKEN = os.getenv("FORWARD_BOT_TOKEN", "7640340584:AAFRegFmJmrx-44r93wnQJFNPmtVQ_M0pKc")

# ⚠️ 使用正確的群組 ID（來自 GetIDsBot）
SOURCE_GROUP_ID = int(os.getenv("FORWARD_GROUP_ID", "-1003199070793"))

# ✅ 目標頻道（公開頻道可以直接用 @名稱）
TARGET_CHANNEL = os.getenv("FORWARD_TARGET_CHANNEL", "@hottxvideos18plus")


# === 主轉發邏輯 ===
async def forward_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    # 僅轉發來自指定群組的訊息
    if msg and msg.chat.id == SOURCE_GROUP_ID:
        try:
            # 使用 Telegram 內建的 forward（能保持原作者 & 原格式）
            await msg.forward(chat_id=TARGET_CHANNEL)
            print(f"✅ 成功轉發訊息 ID: {msg.message_id}")

        except Exception as e:
            print(f"⚠️ 轉發失敗: {e}")


# === 啟動 Bot ===
if __name__ == "__main__":
    print("🤖 Forward Bot 已啟動，正在監聽群組訊息...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, forward_all))
    app.run_polling()
