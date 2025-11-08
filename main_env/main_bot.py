from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_path = "main_env/images/girl-03.jpeg"
    user_name = update.effective_user.first_name or update.effective_user.username or "there"


    caption = (
        f"🤝𝐖𝐄𝐋𝐂𝐎𝐌𝐄 {user_name}, \n\n"
        "Before We Start, If You're Not A Robot, \n" 
        "Kindly Tap「I'M NOT A ROBOT」 \n" 
        "To Get Unlimited Bonus Rewards 🎁 \n\n"
        "Earn Affiliate Commission Cash \n"
        "Share More & Earn More 💰 \n\n"
        "Win More With This Sexy Vibes, \n"
        "Try Tap「CHAT WITH HER」▶︎ •၊၊||၊|။|| 0:10"
    )

    keyboard = [
        [InlineKeyboardButton("I'M NOT A ROBOT 🟢", url="https://t.me/addlist/vU9C9Dvo_TJkZThl")],
        [InlineKeyboardButton("I'M NOT A ROBOT 🟢", url="https://heylink.me/tpaaustralia/")],
        [InlineKeyboardButton("CHAT WITH HER ﾒ૦ﾒ૦💋", url="https://t.me/hottxvideos18plus")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open(photo_path, "rb") as photo:
        await update.message.reply_photo(photo=photo, caption=caption, reply_markup=reply_markup)

if __name__ == "__main__":
    app = ApplicationBuilder().token("7996734575:AAFM3Me9g2dRf_kmTavIXap8TA1ZxfwVMi8").build()
    app.add_handler(CommandHandler("start", start))
    print("✅ Main Bot is running...")
    app.run_polling()
