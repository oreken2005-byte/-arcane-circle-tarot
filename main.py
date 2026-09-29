import os
import random
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import time
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.environ.get("BOT_TOKEN")

CARDS = [
    ("Шут", "Новый этап, свобода и смелый первый шаг. Не бойся начать."),
    ("Маг", "У тебя есть ресурсы, чтобы повлиять на ситуацию. Действуй осознанно."),
    ("Верховная Жрица", "Прислушайся к интуиции и не спеши раскрывать все карты."),
    ("Императрица", "Рост, творчество и забота о себе. Дай идеям пространство."),
    ("Император", "Структура и ответственность помогут навести порядок."),
    ("Влюблённые", "Важен честный выбор и соответствие решения твоим ценностям."),
    ("Колесница", "Движение вперёд. Определи цель и держи направление."),
    ("Сила", "Мягкость и внутреннее спокойствие сейчас сильнее давления."),
    ("Отшельник", "Пауза и самоанализ помогут увидеть главное."),
    ("Колесо Фортуны", "Обстоятельства меняются. Используй открывшуюся возможность."),
    ("Справедливость", "Смотри на факты и последствия. Баланс возвращается."),
    ("Звезда", "Надежда, восстановление и вдохновение. Не отказывайся от цели."),
    ("Луна", "Не всё сейчас очевидно. Проверяй предположения и не спеши."),
    ("Солнце", "Ясность, энергия и хорошие перспективы для открытого действия."),
    ("Мир", "Завершение цикла и переход на новый уровень."),
]

def draw_card():
    return random.choice(CARDS)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🔮 <b>Arcane Circle Tarot</b>\n\n"
        "Твой цифровой проводник в мир Таро.\n\n"
        "🃏 /today — карта дня\n"
        "🎴 /card — вытянуть карту\n"
        "❤️ /love — карта на отношения\n"
        "💰 /money — карта на деньги\n"
        "📖 /advice — совет карты\n"
        "❓ /help — помощь\n\n"
        "Таро — инструмент для саморефлексии, а не гарантия будущих событий."
    )
    await update.message.reply_text(text, parse_mode="HTML")

async def card_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name, meaning = draw_card()
    await update.message.reply_text(
        f"🃏 <b>Твоя карта: {name}</b>\n\n{meaning}",
        parse_mode="HTML",
    )

async def today_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name, meaning = draw_card()
    await update.message.reply_text(
        f"☀️ <b>Карта дня — {name}</b>\n\n{meaning}\n\n"
        "✨ Вопрос дня: что ты можешь сделать сегодня, чтобы поддержать эту энергию?",
        parse_mode="HTML",
    )

async def love_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name, meaning = draw_card()
    await update.message.reply_text(
        f"❤️ <b>Карта на отношения — {name}</b>\n\n{meaning}",
        parse_mode="HTML",
    )

async def money_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name, meaning = draw_card()
    await update.message.reply_text(
        f"💰 <b>Карта на деньги — {name}</b>\n\n{meaning}",
        parse_mode="HTML",
    )

async def advice_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name, meaning = draw_card()
    await update.message.reply_text(
        f"📖 <b>Совет карты — {name}</b>\n\n{meaning}",
        parse_mode="HTML",
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def daily_job(context: ContextTypes.DEFAULT_TYPE):
    chat_id = os.environ.get("DAILY_CHAT_ID")
    if not chat_id:
        return
    name, meaning = draw_card()
    await context.bot.send_message(
        chat_id=int(chat_id),
        text=f"🌙 <b>Arcane Circle — карта дня</b>\n\n🃏 <b>{name}</b>\n\n{meaning}",
        parse_mode="HTML",
    )
    
 class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Arcane Circle Tarot is alive!")

        def log_message(self, format, *args):
            pass


def run_health_server():
        port = int(os.environ.get("PORT", 10000))
        server = HTTPServer(("0.0.0.0", port), HealthHandler)
        print(f"Health server listening on 0.0.0.0:{port}", flush=True)
        server.serve_forever()
    
 def main():
        threading.Thread(target=run_health_server, daemon=True).start()
        
        if not TOKEN:
            raise RuntimeError("BOT_TOKEN is not set")
            
        app = Application.builder().token(TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("today", today_command))
        app.add_handler(CommandHandler("card", card_command))
        app.add_handler(CommandHandler("love", love_command))
        app.add_handler(CommandHandler("money", money_command))
        app.add_handler(CommandHandler("advice", advice_command))
        app.add_handler(CommandHandler("help", help_command))

        # Optional automatic daily post. Set DAILY_CHAT_ID and DAILY_HOUR (0–23).
        daily_hour = int(os.environ.get("DAILY_HOUR", "9"))
        app.job_queue.run_daily(daily_job, time(hour=daily_hour, minute=0))

        app.run_polling()

if __name__ == "__main__":
    main()
