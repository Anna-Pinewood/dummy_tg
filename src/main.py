from pathlib import Path
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, filters, CallbackQueryHandler, Application
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import time
import pandas as pd
import yaml

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я бот с кнопками реакции.')


async def echo(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    logger.info("Got message: %s", user_input)

    keyboard = [[InlineKeyboardButton("👍", callback_data='like'),
                 InlineKeyboardButton("👎", callback_data='dislike')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    df = pd.read_excel(QA_DF_PATH)
    qa_dict_live = dict(zip(df['question'].str.strip().to_list(),
                            df[ANSWER_COLUMN].to_list()))

    # print(qa_dict_live)
    if user_input in qa_dict_live:
        # await update.message.reply_text("Подождите немного...")
        time.sleep(N_SECONDS_SLEEP)

        answer = str(qa_dict_live[user_input])
        answer += "\n\n\nОцените, пожалуйста, ответ:"
        await update.message.reply_text(answer, reply_markup=reply_markup)
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
    df = pd.read_excel(QA_DF_PATH)
    ANSWER_COLUMN = 'model_answer'
    main()
