import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)


# ۱. ساخت وب‌سرور برای پاس کردن Health Check رندر
class HealthCheckHandler(BaseHTTPRequestHandler):

  def do_GET(self):
    self.send_response(200)
    self.end_headers()
    self.wfile.write(b"Bot is active!")

  # خاموش کردن لاگ‌های اضافی سرور در ترمینال
  def log_message(self, format, *args):
    return


def run_health_check_server():
  port = int(os.environ.get("PORT", 10000))
  server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
  server.serve_forever()


# اجرای سرور در یک ترد (Thread) جداگانه
threading.Thread(target=run_health_check_server, daemon=True).start()

# --------------------------------------------------
# ۲. تنظیمات و کدهای اصلی ربات تلگرام
# --------------------------------------------------

TOKEN = os.environ.get("TOKEN", "8805155186:AAFtskJRMtTSD1MA67jSvGtm3RSUrotIsBE")  # توکن اصلی
TOKEN = os.environ.get("TOKEN")
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


# اجرای برنامه اصلی
if __name__ == "__main__":
  app = Application.builder().token(TOKEN).build()

  app.add_handler(CommandHandler("start", start))
  app.add_handler(CallbackQueryHandler(check, pattern="check"))

  print("🤖 Bot is running...")

  # drop_pending_updates=True باعث می‌شود آپدیت‌ها و درخواست‌های معلق قبلی پاک شوند و خطای Conflict ندهد
  app.run_polling(drop_pending_updates=True)
