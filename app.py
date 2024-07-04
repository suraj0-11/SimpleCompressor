import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
)
from config import Config
from tools.compress import compress_file, ensure_folder_exists

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hi! Send me a file and I will compress it for you.')

async def compress(update: Update, context: CallbackContext) -> None:
    file = update.message.document
    file_id = file.file_id
    new_file = await context.bot.get_file(file_id)

    ensure_folder_exists(Config.INPUT_FOLDER)
    ensure_folder_exists(Config.OUTPUT_FOLDER)

    input_file_path = os.path.join(Config.INPUT_FOLDER, file.file_name)
    output_file_path = os.path.join(Config.OUTPUT_FOLDER, f"compressed_{file.file_name}")

    await new_file.download_to_drive(custom_path=input_file_path)

    compress_file(input_file_path, output_file_path)

    await update.message.reply_text('File compressed successfully. Sending back the compressed file...')
    await update.message.reply_document(document=open(output_file_path, 'rb'))

def main() -> None:
    application = ApplicationBuilder().token(Config.BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, compress))

    application.run_polling()

if __name__ == '__main__':
    main()
