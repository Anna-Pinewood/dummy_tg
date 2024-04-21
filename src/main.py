from pathlib import Path
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, filters, CallbackQueryHandler, Application
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import time

import yaml

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


QA_DICT = {
    "Как дела?": "Хорошо, спасибо!",
    "Какой сегодня день?": "Сегодня вторник.",
    "Что делаешь?": "Отвечаю на твои сообщения!",
    "Привет": "Привет! Чем могу помочь?"
}


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я бот с кнопками реакции.')


async def echo(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    logger.info("Got message: %s", user_input)

    keyboard = [[InlineKeyboardButton("👍", callback_data='like'),
                 InlineKeyboardButton("👎", callback_data='dislike')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if user_input in QA_DICT:
        # await update.message.reply_text("Подождите немного...")
        time.sleep(N_SECONDS_SLEEP)
        await update.message.reply_text(QA_DICT[user_input], reply_markup=reply_markup)
    else:
        await update.message.reply_text("Извините, я не знаю ответ на этот вопрос.")


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Вы выбрали {query.data}")


def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()


if __name__ == '__main__':
    path_to_config = Path(__file__).parent.parent / 'config.yaml'
    with open(path_to_config, 'r') as file:
        config = yaml.safe_load(file)

    TELEGRAM_TOKEN = config['telegram_token']
    N_SECONDS_SLEEP = int(config['n_seconds_sleep'])
    QA_DF_PATH = config['qa_df_path']
    main()
