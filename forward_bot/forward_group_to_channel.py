import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# === 載入環境變數 ===
load_dotenv()

BOT_TOKEN = os.getenv("FORWARD_BOT_TOKEN", "7640340584:AAFRegFmJmrx-44r93wnQJFNPmtVQ_M0pKc")
SOURCE_GROUP_ID = int(os.getenv("FORWARD_GROUP_ID", "-4760638966"))  # 群組 ID
TARGET_CHANNEL = os.getenv("FORWARD_TARGET_CHANNEL", "@hottxvideos18plus")  # 目標頻道

async def forward_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg and msg.chat.id == SOURCE_GROUP_ID:
        try:
            # 轉發文字
            if msg.text:
                await context.bot.send_message(chat_id=TARGET_CHANNEL, text=msg.text)

            # 轉發圖片
            elif msg.photo:
                await context.bot.send_photo(chat_id=TARGET_CHANNEL, photo=msg.photo[-1].file_id, caption=msg.caption or "")

            # 轉發影片
            elif msg.video:
                await context.bot.send_video(chat_id=TARGET_CHANNEL, video=msg.video.file_id, caption=msg.caption or "")

            # 轉發文件
            elif msg.document:
                await context.bot.send_document(chat_id=TARGET_CHANNEL, document=msg.document.file_id, caption=msg.caption or "")

            print(f"✅ 成功轉發訊息 ID: {msg.message_id}")
        except Exception as e:
            print(f"⚠️ 轉發失敗: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, forward_all))
    print("🤖 Forward Bot 已啟動，正在監聽群組訊息...")
    app.run_polling()
