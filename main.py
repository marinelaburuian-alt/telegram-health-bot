import os
import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Token del bot Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Connessione a Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
creds = ServiceAccountCredentials.from_json_keyfile_dict(eval(creds_json), scope)
client = gspread.authorize(creds)

# Apri il foglio di Google Sheets
sheet = client.open("Telo-Zdorovie").sheet1


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Ciao Marina! 🌿\nIl bot è attivo. Inviami un messaggio tipo:\n\n✔️ ho preso vitamine\n✔️ ho preso magnesio")


@bot.message_handler(func=lambda message: True)
def log_message(message):
    text = message.text.lower()

    if "vitamine" in text:
        sheet.append_row(["Vitamine", message.date])
        bot.reply_to(message, "✔️ Registrato: Vitamine prese")

    elif "magnesio" in text:
        sheet.append_row(["Magnesio", message.date])
        bot.reply_to(message, "✔️ Registrato: Magnesio preso")

    else:
        bot.reply_to(message, "Non ho capito, ma sono qui! 😊")


bot.polling()
