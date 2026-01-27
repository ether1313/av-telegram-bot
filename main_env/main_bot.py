import os
import sqlite3
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ========== Database (fly.io persistent volume) ==========
DB_PATH = "/data/users.db"

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    first_seen TEXT,
    last_seen TEXT
)
""")
conn.commit()


def save_user(user):
    now = datetime.utcnow().isoformat()

    cur.execute("SELECT user_id FROM users WHERE user_id = ?", (user.id,))
    exists = cur.fetchone()

    if exists:
        cur.execute("UPDATE users SET last_seen = ? WHERE user_id = ?", (now, user.id))
    else:
        cur.execute(
            "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",
            (
                user.id,
                user.username,
                user.first_name,
                user.last_name,
                now,
                now
            )
        )
    conn.commit()


# ========== Handlers ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_path = "main_env/images/sexygirl.gif"
    user = update.effective_user
    save_user(user)

    user_name = user.first_name or user.username or "there"

    caption = (
        f"<b>✨ Welcome ✨ {user_name}!</b>\n\n"
        "<b>⚡️ Quick Verification</b>\n"
        "Tap I'M NOT A ROBOT 🟢 to unlock rewards\n\n"
        "<b>💰 Earn Extra Money Now</b>\n"
        "Share & earn affiliate commissions\n\n"
        "<b>💋 Ready To Chat With Her?</b>\n"
        "Find your perfect match in our chat room"
    )

    keyboard = [
        [
            InlineKeyboardButton("I'M NOT A ROBOT 🟢", url="https://t.me/addlist/vU9C9Dvo_TJkZThl"),
            InlineKeyboardButton("I'M NOT A ROBOT 🟢", url="https://heylink.me/tpaaustralia/")
        ],
        [InlineKeyboardButton("CHAT WITH HER ﾒ૦ﾒ૦💋", url="https://t.me/hottxvideos18plus")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        with open(photo_path, "rb") as gif:
            await update.message.reply_animation(animation=gif, caption=caption, reply_markup=reply_markup, parse_mode="HTML")
    else:
        await update.callback_query.message.reply_text("Please use /start in private chat.")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cur.execute("SELECT COUNT(*) FROM users")
    total = cur.fetchone()[0]
    await update.message.reply_text(f"👥 Total Users: {total}")


# ========== Main ==========
def main():
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise RuntimeError("❌ BOT_TOKEN is missing!")

    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))

    print("✅ Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
