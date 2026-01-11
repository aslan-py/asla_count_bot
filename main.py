import sys
import time

from sqlalchemy.orm import sessionmaker
from telebot import TeleBot

from handlers import process_step
from utils.constants import Ai, Errors, MainSettings, Success, Support
from utils.logger_config import logger, setup_logging
from utils.models import database_setup


def main():
    """Инициализирует базу данных и запускает основной цикл Telegram-бота."""
    setup_logging()
    try:
        engine = database_setup()
        Session = sessionmaker(bind=engine)
        logger.success(Success.DB_SUCCESS)
    except Exception as error:
        logger.error(Errors.DB_ERROR.format(error))
        sys.exit(1)

    bot = TeleBot(Ai.TOKEN)
    bot.delete_my_commands()

    @bot.message_handler(commands=['about', 'go'])
    def commands(message):
        """Регистрирует команды /go и /about."""
        try:
            if message.text == '/go':
                start = time.time()
                bot.send_message(message.chat.id, MainSettings.START_MESSAGE)
                logger.info(MainSettings.USER_START)
                bot.register_next_step_handler(
                    message, process_step, start, bot, Session)

            elif message.text == '/about':
                logger.info(MainSettings.USER_ABOUT)
                bot.send_message(
                    message.chat.id,
                    MainSettings.ABOUT_MESSAGE,
                    parse_mode=Support.PARSE_MODE
                )
        except Exception as error:
            logger.error(Errors.GO_ERROR.format(error))
            bot.send_message(message.chat.id, Errors.FUNC_COMMANDS_ERROR)

    @bot.message_handler(
        content_types=[
            'text', 'audio', 'voice', 'video', 'photo', 'document', 'sticker'
        ]
    )
    def is_correct_start_message(message):
        """Проверяет, является ли сообщение допустимым началом работы."""
        bot.reply_to(
            message,
            Errors.INCORRECT_MESSAGE.format(
                name=message.from_user.first_name,),
            parse_mode=Support.PARSE_MODE
        )

    logger.success(Success.BOT_SUCCESS)
    bot.infinity_polling()


if __name__ == "__main__":
    main()
