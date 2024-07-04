import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from config import Config
from tools.compress import compress_file, ensure_folder_exists

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Send me a file and I will compress it for you.')

def compress(update: Update, context: CallbackContext) -> None:
    file = update.message.document
    file_id = file.file_id
    new_file = context.bot.get_file(file_id)

    ensure_folder_exists(Config.INPUT_FOLDER)
    ensure_folder_exists(Config.OUTPUT_FOLDER)

    input_file_path = os.path.join(Config.INPUT_FOLDER, file.file_name)
    output_file_path = os.path.join(Config.OUTPUT_FOLDER, f"compressed_{file.file_name}")

    new_file.download(custom_path=input_file_path)

    compress_file(input_file_path, output_file_path)

    update.message.reply_text('File compressed successfully. Sending back the compressed file...')
    update.message.reply_document(document=open(output_file_path, 'rb'))

def main() -> None:
    updater = Updater(Config.BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document, compress))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
