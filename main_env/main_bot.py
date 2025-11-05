from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_path = "main_env/images/girl-03.jpeg"
    user_name = update.effective_user.first_name or update.effective_user.username or "there"


    caption = (
        f"Welcome {user_name}, hey there! 👋\n\n"
        "Before we start, if you're not a robot \n" 
        "Pls tap the both buttons [I'M NOT A ROBOT] \n" 
        "to get the bonus rewards 🎁 \n\n"
        "Earn Affiliate Commission Cash \n"
        "Share More, Earn More 💰 \n\n"
        "Earn Cash Win More With This Sexy Vibes 💦 \n"
        "Click [CHAT WITH HER]"
    )

    keyboard = [
        [InlineKeyboardButton("I'M NOT A ROBOT 🟢", url="https://t.me/addlist/vU9C9Dvo_TJkZThl")],
        [InlineKeyboardButton("I'M NOT A ROBOT 🟢", url="https://www.13auteam.com/")],
        [InlineKeyboardButton("CHAT WITH HER 💗⃝🌕", url="https://t.me/hottxvideos18plus")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open(photo_path, "rb") as photo:
        await update.message.reply_photo(photo=photo, caption=caption, reply_markup=reply_markup)

if __name__ == "__main__":
    app = ApplicationBuilder().token("7996734575:AAFM3Me9g2dRf_kmTavIXap8TA1ZxfwVMi8").build()
    app.add_handler(CommandHandler("start", start))
    print("✅ Main Bot is running...")
    app.run_polling()
