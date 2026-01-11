import time

from prettytable import PrettyTable

from database import dates_period_pivot, db_add_data
from utils.constants import Ai, Errors, Logs, Success, Support
from utils.exceptions import (AiError, AiVoiceError, DictDatesFormatError,
                              DictFormatError, PrettyPivotError,
                              PrettySavedDataError)
from utils.logger_config import logger
from utils.openai_config import deepseek, get_dates_from_ai, yandex_speech_kit


def process_step(message, start_time, bot, Session, dates_json=None):
    """Обрабатывает входящее сообщение пользователя, распознает данные.

    Сохраняет данные в БД.
    """
    try:
        logger.info(Logs.START_LOG.format(message.chat.username))

        user_name = message.chat.username or str(message.from_user.id)
        logger.debug(Logs.USER.format(message.chat.username))

        # 1.Если прошло 5 минут с момента прожатия /go - прерываем сессию.
        if time.time() - start_time > Support.SESSION_TIME:
            bot.send_message(
                message.chat.id,
                Support.OVERTIME.format(message.chat.username,)
            )
            logger.info(Logs.END_TIME_LOG.format(message.chat.username))
            return

        if dates_json is not None:
            logger.info(Logs.USER_CREATER_PIVOT.format(message.chat.username))
            # 1. Из БД выгружаем данные для отчета.
            result_pivot = dates_period_pivot(dates_json, Session, user_name)

            # 2. Полученные данные кладем в таблицу.
            table_string = pretty_pivot(result_pivot)
            header = Support.PIVOT_PERIOD.format(
                start=dates_json['start_date'],
                end=dates_json['end_date']
            )
            # 3. Отправляем сообщением отчет пользователю.
            bot.send_message(
                message.chat.id,
                Support.FULL_MESSAGE.format(
                    header=header, table_string=table_string),
                parse_mode=Support.PARSE_MODE
            )
            # 4. Перенаправляем пользователя на ввод затрат.
            bot.register_next_step_handler(
                message, process_step, start_time, bot, Session)
            logger.info(Logs.USER_REPEAT_INPUT.format(message.chat.username))
            return

        if message.content_type == 'text':
            logger.info(Logs.USER_INPUT_TEXT.format(message.chat.username))

            # 1. Ловим слово стоп, для выхода из сессии.
            if (
                'stop' in message.text.lower() or
                    'стоп' in message.text.lower()):
                bot.send_message(message.chat.id, Support.STOP)
                logger.info(Logs.USER_STOP_TEXT.format(message.chat.username))
                return

            # 2. Ловим слово отчет, для запуска функции формирующей отчет.
            if 'отчет' in message.text.lower():
                logger.info(Logs.USER_WANA_TEXT.format(message.chat.username))
                bot.send_message(
                    message.chat.id,
                    Support.PIVOT_HANDLERS_MESSAGE
                )
                bot.register_next_step_handler(
                    message, data_create, start_time, bot, Session)
                return

            # 3. ИИ проверил текст и функция is_dict_format_correct првоерила формат.
            result = deepseek(message.text)
            result = is_dict_format_correct(result)
            logger.success(
                Success.USER_DATA_CORRECT.format(message.chat.username))

            # 4. Сохраняем в БД и формируем красивую таблицу с данными.
            db_add_data(result, Session, user_name)
            table = pretty_output_saved_data(result)

            # 5. Выводим в ТГ в html формате таблицу с данными для сохранения.
            bot.send_message(
                message.chat.id,
                Success.SUCCESS_DB_SAVE.format(f'<pre>{table}</pre>'),
                parse_mode=Support.PARSE_MODE
            )

            # 6. Отправляем пользователя вновь вносить затраты.
            bot.register_next_step_handler(
                message, process_step, start_time, bot, Session)
        elif message.content_type == 'voice':
            logger.info(Logs.USER_VOICE_START.format(message.chat.username))

            # 1. Получаем ссылку на  звук для скачивания.
            file_info = bot.get_file(message.voice.file_id)

            # 2. Сохраняем содержимое звука в бинарном коде.
            downloaded_file = bot.download_file(file_info.file_path)

            # 3. Переводим звук в текст.
            # recognized_text = transcribe_voice(downloaded_file)
            recognized_text = yandex_speech_kit(downloaded_file)
            recognized_text = is_yandex_text_correct(recognized_text)
            logger.info(Logs.VOICE_TRANSLATE.format(recognized_text))

            # 4. ИИ проверил текст и функция is_dict_format_correct проверила формат.
            new_text = deepseek(recognized_text)
            new_text = is_dict_format_correct(new_text)
            logger.success(
                Success.USER_DATA_VOICE_OK.format(message.chat.username))

            # 5. Сохраняем в БД и формируем красивую таблицу с данными.
            db_add_data(new_text, Session, user_name)
            table = pretty_output_saved_data(new_text)

            # 6. Выводим в ТГ в html формате таблицу с данными для сохранения.
            bot.send_message(
                message.chat.id,
                Success.SUCCESS_DB_SAVE.format(f'<pre>{table}</pre>'),
                parse_mode=Support.PARSE_MODE
            )
            bot.register_next_step_handler(
                message, process_step, start_time, bot, Session)

    except AiVoiceError as error:
        bot.send_message(message.chat.id, Errors.LONG_VOICE_USER)
        logger.error(Errors.LONG_VOICE.format(error))
    except AiError as error:
        bot.send_message(message.chat.id, Errors.DEPPSEEK_FOR_USER_MES)
        logger.error(Errors.DEPPSEEK_ERROR.format(error))
    except Exception as error:
        logger.error(Errors.FULY_ERROR.format(error))
        bot.send_message(message.chat.id, Errors.ERROR_TEXT_UPS)

        #  1.Если у пользователя ошибка с формированием отчетности то:
        #  - отправляем его повторно вводить даты для отчета
        #  - в противном случае запускаем его повторно вносить затраты.
        if dates_json is not None:
            bot.register_next_step_handler(
                message, data_create, start_time, bot, Session)
        else:
            bot.register_next_step_handler(
                message, process_step, start_time, bot, Session)


def is_dict_format_correct(data):
    """Проверяеn формат словаря с данными по затратам после генерации AI."""
    if not data:
        raise DictFormatError(Errors.IS_DICT_EMPTY.format(data))

    if isinstance(data, dict):
        data = [data]

    if not isinstance(data, list):
        raise DictFormatError(Errors.IS_DICT_NO_DICT.format(data))

    for item in data:
        if not isinstance(item, dict):
            raise DictFormatError(Errors.NO_DICT_IN_LIST.format(item))
        if (
            not item.get('category') or
            not item.get('product') or
            not item.get('price')
        ):
            raise DictFormatError(Errors.WRONG_KEYS)
    return data


#  [{'category': 'еда', 'product': 'хлеб', 'price': 700}]
def pretty_output_saved_data(clean_data):
    """Форматирует список сохраненных транзакций в читаемый текстовый вид.
    """
    try:
        mytable = PrettyTable()
        mytable.field_names = ['Категория', 'Объект', 'Цена']
        mytable.add_rows(
            [
                [item['category'],
                 item['product'],
                 item['price']] for item in clean_data
            ]
        )

        mytable.align["Категория"] = 'c'
        mytable.align["Объект"] = 'c'
        mytable.align["Цена"] = 'r'

        mytable.max_width["Категория"] = Support.MAX_WIDTH_CAT
        mytable.max_width["Объект"] = Support.MAX_WIDTH_CAT
        mytable.max_width["Цена"] = Support.MAX_WIDTH_PRICE
        logger.success(Success.PRETY_USER_DATA)
        return mytable

    except Exception as error:
        logger.error(Errors.PRETTY_TABLE_ERROR.format(error))
        raise PrettySavedDataError(Errors.PRETTY_TABLE_ERROR.format(error))


def pretty_pivot(pivot):
    """Красивое формирование отчета за указанный период."""
    try:
        table = PrettyTable()
        table.field_names = ['Категория', 'Затраты']
        total_sum = 0
        for item in pivot:
            category = item[0]
            # 1. Между числами деляю пробелы для простоты чтения.
            price = f'{item[1]:,}'.replace(',', ' ')
            table.add_row([category, price])
            if item[1]:
                total_sum += item[1]

        #  2. Между числами деляю пробелы для простоты чтения в Total.
        formatted_total = f'{total_sum:,}'.replace(',', ' ')
        table.add_row(['------', '------'])
        table.add_row(['Итого : ', formatted_total])

        #  3. Настройка отступов и длинны полей таблицы.
        table.align["Категория"] = Support.ALIGN_CAT
        table.align["Затраты"] = Support.ALIGN_PRICE
        table.max_width["Категория"] = Support.MAX_WIDTH_CAT
        table.max_width["Затраты"] = Support.MAX_WIDTH_CAT
        logger.success(Success.PRETY_PIVOT_READY)
        return table
    except Exception as error:
        logger.error(Errors.PRETTY_TABLE_ERROR.format(error))
        raise PrettyPivotError(Errors.PRETTY_TABLE_ERROR.format(error))


def is_dates_correct(dates_json):
    """Проверяем корректность словаря с датами сформирьванного ИИ."""
    if not dates_json:
        raise DictDatesFormatError(Errors.IS_DATA_CREATE_CORRECT_EMPTY)
    if not isinstance(dates_json, dict):
        raise DictDatesFormatError(Errors.IS_DATA_CREATE_CORRECT_DICT)
    if not dates_json.get('start_date') or not dates_json.get('end_date'):
        raise DictDatesFormatError(Errors.IS_DATA_CREATE_CORRECT_KEYS)


def data_create(message, start_time, bot, Session):
    """
    Управляет процессом формирования отчета.

    Запрашивает период,обрабатывает даты через ИИ и выгружает данные из базы.
    """
    try:
        logger.info(Support.USER_DATA_START)

        # 1. Если в сообщении присутсвует слово стоп.
        # Выходим из функции и вновь и работаем с вводом данных с затратами.
        if 'stop' in message.text.lower() or 'стоп' in message.text.lower():
            bot.send_message(message.chat.id, Support.DATA_CREATE_STOP)
            bot.register_next_step_handler(
                message, process_step, start_time, bot, Session)
            logger.info(Support.USER_WANA_STOP.format(message.chat.username))
            return

        # 2. Текст уходит в ИИ для формирования словаря нужного формата.
        #  Проверяем формат словаря
        result = get_dates_from_ai(message.text)
        is_dates_correct(result)
        logger.success(Success.DICT_SUCCESS.format(message.chat.username))

        #  3.Повторно запускаем функцию , но уже с переданным словарем.
        process_step(message, start_time, bot, Session, dates_json=result)

    except Exception as error:
        logger.error(
            Errors.DATA_FOR_PIVOT.format(
                user=message.chat.username,
                error=error
            )
        )
        bot.send_message(message.chat.id, Errors.FAIL_DATA.format(error))
        bot.register_next_step_handler(
            message, data_create, start_time, bot, Session)


def is_yandex_text_correct(response):
    """Проверям формат  перевода яндексом голоса в текст."""
    if response.status_code != Ai.STATUS_CODE:
        raise AiVoiceError(Errors.VOICE_ERROR.format(response.status_code))
    result = response.json().get('result')
    if not result:
        raise AiVoiceError(Errors.NO_RESULT.format(response.text))
    return result
