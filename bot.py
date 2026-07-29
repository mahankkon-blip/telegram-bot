import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# دریافت توکن و آدرس از متغیرهای محیطی یا مقداردهی مستقیم
TOKEN = os.environ.get("TOKEN", "8805155186:AAFzhMYy7FY6srGBRAYRV6s-EKb5TpXSnxw")
CHANNEL = "@K_mahan_O"

GAMES = [
    (
        "🎮 نوستالژی",
        "https://play.google.com/store/apps/details?id=fi.twomenandadog.zombiecatchers",
    ),
    (
        "🎮 شبیه ساز زندگی",
        "https://play.google.com/store/apps/details?id=adventure.party.real.life",
    ),
    ("🎮 قایم موشک", "https://share.google/OQ7FHGUGtYxx1xGQ3"),
    (
        "🎮 مهماندار هواپیما",
        "https://store.steampowered.com/app/4534960/Dear_Passengers/",
    ),
    ("🎮 چنل یوتیوب", "https://www.youtube.com/@mahanko44"),
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  keyboard = [
      [InlineKeyboardButton("📢 عضویت در کانال", url="https://t.me/K_mahan_O")],
      [InlineKeyboardButton("✅ عضو شدم", callback_data="check")],
  ]

  await update.message.reply_text(
      "👋 سلام\n\n"
      "برای دریافت لینک بازی ابتدا عضو کانال شوید و سپس روی «عضو شدم» بزنید.",
      reply_markup=InlineKeyboardMarkup(keyboard),
  )


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  user_id = query.from_user.id

  try:
    member = await context.bot.get_chat_member(CHANNEL, user_id)

    if member.status in ["member", "administrator", "creator"]:
      keyboard = []
      for name, link in GAMES:
        keyboard.append([InlineKeyboardButton(name, url=link)])

      await query.message.reply_text(
          "✅ عضویت شما تایید شد.\n\n🎮 یکی از بازی‌های زیر را انتخاب کنید:",
          reply_markup=InlineKeyboardMarkup(keyboard),
      )
    else:
      await query.message.reply_text("❌ هنوز عضو کانال نیستید.")

  except Exception as e:
    await query.message.reply_text(
        "❌ خطا در بررسی عضویت. مطمئن شوید ربات ادمین کانال است."
    )


def main():
  app = Application.builder().token(TOKEN).build()

  app.add_handler(CommandHandler("start", start))
  app.add_handler(CallbackQueryHandler(check, pattern="check"))

  # تنظیمات پورت و آدرس Render
  PORT = int(os.environ.get("PORT", 10000))
  RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")

  if RENDER_EXTERNAL_URL:
    # اجرای وب‌هوک روی سرور Render
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{RENDER_EXTERNAL_URL}/{TOKEN}",
    )
  else:
    # اجرا به صورت Polling (برای تست روی سیستم خودتان)
    app.run_polling()


if __name__ == "__main__":
  main()
