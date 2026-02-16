import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN")

try:
    with open("homework.json", "r") as f:
        homework = json.load(f)
except:
    homework = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if ":" in text:
        subject, task = text.split(":", 1)
        homework[subject.strip()] = task.strip()

        with open("homework.json", "w") as f:
            json.dump(homework, f)

        await update.message.reply_text("Homework saved ✅")

    elif text == "homework":
        if homework:
            result = ""
            for subject, task in homework.items():
                result += f"{subject.title()} - {task}\n"
            await update.message.reply_text(result)
        else:
            await update.message.reply_text("No homework yet.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.run_polling()
