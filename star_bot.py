import os
from telegram import LabeledPrice, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("TOKEN")  # token z Render Environment Variables

# Cesty k obrázkům
BLURRED_IMAGE = "blurred.jpg"
ORIGINAL_IMAGE = "original.jpg"

# Cena v hvězdičkách
PRICE = 200

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open(BLURRED_IMAGE, "rb"),
        caption="Obrázek je zamčený 🔒\nChceš vidět originál? Napiš /unlock"
    )

async def unlock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prices = [LabeledPrice("Odemknutí obrázku", PRICE)]
    await update.message.reply_invoice(
        title="Odemknutí",
        description="Plať ⭐ a uvidíš ostrý obrázek",
        payload="paywall-image",
        provider_token="",  # prázdné = Telegram Stars
        currency="XTR",
        prices=prices,
        start_parameter="unlock"
    )

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Platba proběhla ✅")
    await update.message.reply_photo(photo=open(ORIGINAL_IMAGE, "rb"), caption="Tady je originál 🎉")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("unlock", unlock))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    app.run_polling()

if __name__ == "__main__":
    main()
