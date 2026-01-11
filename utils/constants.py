
import os

from dotenv import load_dotenv

load_dotenv()


class Ai:
    STATUS_CODE = 200
    TOKEN = os.getenv('TOKEN_TELEGRAMM')
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
    DEPPSEEK_API_URL = 'https://api.deepseek.com'
    PROMPT_1 = """
    You are a highly specialized financial transaction parser.
        Your sole task is to extract expense data from user text
        and convert it into a strict JSON format.

    [RESPONSE RULES]
    - Use Russian language for BOTH "product" and "category" values.
    - Return ONLY pure JSON.
    - DO NOT provide any explanations, introductions, or additional text.
    - DO NOT use Markdown formatting (no ```json code blocks).
    - If the input text does NOT contain a clear price or product,
        return an empty list: [].

    [OUTPUT FORMAT]
    - Always return a list of objects, even for a single item
    - Single expense: [{"category": "str", "product": "str", "price": int}]
    - Multiple expenses:
        [{"category": "str", "product": "str", "price": int}, {...}]

    [DATA PROCESSING]
    - product: Correct typos, convert to lowercase, and
        keep only the core noun (e.g., "fresh chicken breast" -> "chicken").
    - price: Strictly an integer.
    - category: Determine a suitable category based on the item in RUSSIAN
        (e.g., еда, машина, одежда, питомцы, развлечения, гигиена и т.д.).

    [EXAMPLES]
    Input: "dog food 1234"
    Output: {"category": "pets", "product": "food", "price": 1234}

    Input: "hand cream for 100 and pickled cucumbers for 500"
    Output: [{"category": "cosmetics", "product": "cream", "price": 100},
        {"category": "food", "product": "cucumbers", "price": 500}]

    Input: "just bought some stuff"
    Output: []
    """
    DEEPSEEK_MODEL = 'deepseek-chat'
    YA_SPEECH_KIT_URL = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    YA_URL = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'
    YA_SPEECH_KIT_JSON = {'yandexPassportOauthToken': os.getenv('AUTH')}
    YANDEX_FOLDER_ID = os.getenv('FOLDER_ID')
    YA_SPEECH_KIT_HEADERS = {'Content-Type': 'application/json'}
    YA_LANG = 'ru-RU'
    YA_FORMAT = 'oggopus'
    TEMPERATURE = 0.1
    MAX_TOKENS = 200
    MAX_TOKENS_DATE = 50
    PROMT_DATA = """
    You are a highly specialized time interval parser.
        Your task is to extract the start date and end date of
        a period from the user's text, based on the provided current date.

    [CONTEXT]
    Today's date (today): {today}

    [RESPONSE RULES]
    - Return ONLY pure JSON or an empty list [].
    - DO NOT write any explanations or additional text.
    - DO NOT use Markdown formatting (no ```json).
    - Date format: YYYY-MM-DD.

    [OUTPUT FORMAT]
    {{"start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD"}}
    Or [] if no dates are found.

    [LOGIC]
    - Missing Year: If the user did not specify a year
        (e.g., "from January 1 to 5"), use the year from {today}.
    - Relative Dates: Use {today} as the reference point
        ("yesterday", "last week").
    - Single Date: If only one day is mentioned,
        use it for both start_date and end_date.
    - Unknown: If no dates are found or cannot be determined,
        return strictly [].

    [EXAMPLES]
    Input: "for yesterday" (Today: 2026-01-07)
    Output: {{"start_date": "2026-01-06", "end_date": "2026-01-06"}}

    Input: "from January 1 to 3" (Today: 2026-01-07)
    Output: {{"start_date": "2026-01-01", "end_date": "2026-01-03"}}

    Input: "hello, how are you"
    Output: []
    """


class Logs:
    ROTATION = '10 MB'
    RETENTION = 5
    LEVEL = 'INFO'
    CONSOLE_FORMAT = (
        '{time:HH:mm:ss} | {level} | {module} | {function}| {message}')
    FAIL_FORMAT = (
        '{time:YYYY-MM-DD HH:mm:ss} | {level} | '
        '{module} | {function}| {message}'
    )
    DIR_NAME = 'logs'
    LOG_NAME = 'log.log'
    ENCODING = 'utf-8'
    END_TIME_LOG = '[Session] Время сессии пользователя {} истекло'
    START_LOG = '[DB] {} начал ввод данных.'
    USER = 'Пользователь: {}'
    USER_CREATER_PIVOT = 'Пользователь {} формирует отчет по затратам'
    USER_REPEAT_INPUT = '[DB] {} вводит данные повторно.'
    USER_INPUT_TEXT = '[In] {} пишет текст'
    USER_STOP_TEXT = ('[Session] {} прервал сессию (stop).')
    USER_WANA_TEXT = '[Report] {} запросил текстовый отчет.'
    USER_VOICE_START = '[In] {} пишет голос.'
    VOICE_TRANSLATE = '[STT] Голос распознан: "{}"'


class Support:
    OVERTIME = '{}, время сессии истекло ⌛ Нажми /go, чтобы продолжить.'
    STOP = 'Запись остановлена ⛔ Сессия завершена.'
    SESSION_TIME = 300
    MAX_WIDTH_CAT = 20
    MAX_WIDTH_PRICE = 15
    ALIGN_CAT = 'l'
    ALIGN_PRICE = 'c'
    PIVOT_HANDLERS_MESSAGE = (
        'Напиши период для отчета 🧾 '
        '(например: "вчера" или "с 1 по 10 января")'
    )
    DATA_CREATE_STOP = (
        'Действие отменено ⛔ Я снова в режиме записи расходов'
    )
    USER_WANA_STOP = (
        'Пользователь {} ввел "stop/стоп" и'
        'прервал формирование отчетов.'
    )
    PIVOT_PERIOD = '📊 Отчет за период: {start} — {end}'
    FULL_MESSAGE = (
        '{header}\n\n<pre>{table_string}</pre>\n\n'
        'Я снова в режиме записи — присылай новые расходы!\n'
        'Для формирования отчета снова введи слово отчет...'
    )
    USER_DATA_START = 'Пользователь приступил к вводу даты для отчета'
    PARSE_MODE = 'HTML'
    PARSE_MODE_MARK = 'MarkdownV2'


class MainSettings:
    ABOUT_MESSAGE = """
    <b>🤖 Я — asla_count_bot</b>

    <b>Веду учет финансов.</b>
    Пиши текст или отправляй голос.

    <b>Как вводить данные:</b>
    • <i>«Кофе 250»</i>
    • <i>«Бензин на 2000»</i>
    • <i>«Продукты 500, такси 300»</i>

    <b>Команды:</b>
    🚀 /go — начать работу.
    📊 <b>отчет</b> — показать статистику
    ⛔ <b>stop</b> — завершить сессию
    """
    START_MESSAGE = 'Готов к приёму данных...'
    USER_START = 'Пользователь начал работу с ботом прожав кнопку /go'
    USER_ABOUT = 'Пользователь запросил справку'


class Errors:
    DB_ERROR = '[Fatal] Ошибка инициализации БД: {} ❌'
    GO_ERROR = '[DB] Ошибка записи в БД: {} ⚠️'
    FUNC_COMMANDS_ERROR = (
        'Упс, у меня что то сломалось 🦥\n'
        'Попробуй еще раз'
    )
    INCORRECT_MESSAGE = """
        Привет, <b>{name}</b>! 🌚

        Чтобы начать работу, введи команду: /go
        Узнать о моих возможностях: /about
        """
    FULY_ERROR = 'Ошибка : {}'
    ERROR_TEXT_UPS = (
        '⚠️ Не удалось распознать данные. Убедись, что указал и товар, и цену.'
    )
    IS_DICT_EMPTY = 'Данные пришли пустыми: {}'
    IS_DICT_NO_DICT = 'Данные не в формате словаря: {}'
    NO_DICT_IN_LIST = 'Внутри списка не словарь: {}'
    WRONG_KEYS = 'В словаре нет необходимых ключей category, product или price'
    PRETTY_TABLE_ERROR = (
        'Ошибка при формировании красивой таблички вывода данных: {}')
    IS_DATA_CREATE_CORRECT_EMPTY = 'Формат даты не распознан'
    IS_DATA_CREATE_CORRECT_DICT = 'Дата пришла не в формате словаря'
    IS_DATA_CREATE_CORRECT_KEYS = (
        'Нет нужных ключей словаря дат для формирования периодна отчета')
    DATA_FOR_PIVOT = (
        'Для {user} ошибка формирования даты для отчета: '
        '{error}, перенаправляю повторно ввести дату!'
    )
    FAIL_DATA = 'Не смог распознать дату, ошибка:  {}'
    DB_DATA_NOT_OK = 'Данные пользователя не сохранились в БД {}'
    NO_DB_DATA = 'За этот период записей не найдено. Попробуй другие даты 📂'
    DB_ERROR_FULY = 'Выгрузка за указанные даты с ошибкой {}'
    SYS_ERROR_DB = '[System] Критическая ошибка формирования отчета: {} ❌'
    DEPPSEEK_ERROR = ('[AI] Ошибка DeepSeek: {} 🤖')
    DEPPSEEK_FOR_USER_MES = (
        'Что -то сломалось с распознованием текста в работе ИИ\n'
        'Попробуй через пару минут, либо сообщи Аслану о проблеме'
    )
    IAM_TOKEN_ERROR = '[Auth] Ошибка IAM-токена: {} 🔑'
    IAM_EMPTY = 'IAM токен пустой: {}'
    VOICE_ERROR = '[STT] Ошибка распознавания: {} 🎤'
    NO_RESULT = (
        'Финальный словарь распознавания голоса не корректен, '
        'нет ключа result: {}'
    )
    LONG_VOICE = 'Ошибка с работой функции распознавания голоса speechkit: {}'
    LONG_VOICE_USER = ('🎤 Слишком длинная запись. Максимум — 30 секунд.')


class Success:
    DB_SUCCESS = '[DB] База данных успешно запущена ✅'
    BOT_SUCCESS = 'Бот запущен'
    USER_DATA_CORRECT = ('[AI] Данные пользователя {} успешно обработаны.')
    USER_DATA_VOICE_OK = (
        'У пользователя {} голосовая заметка  успешно обработана ИИ'
        'и проверена на валидность формата'
    )
    SUCCESS_DB_SAVE = (
        '✅ Данные сохранены\n'
        '{}\n\n'
        'Можешь вносить ещё!'
    )
    PRETY_USER_DATA = 'Красивая выгрузка данных для пользователя готова'
    PRETY_PIVOT_READY = 'Красивая выгрузка отчета готова'
    DICT_SUCCESS = (
        'Словарь для пользователя для сохранения в БД получени и проверен '
        'на корректность\n {} перенаправлен в process_step'
    )
    DB_DATA_OK = '[DB] Транзакция успешно сохранена ✅'
    DB_UPLOAD_OK = '[DB] Выгрузка данных для отчета завершена.'


class Models_SQL:
    STR_LEN = 50
    STR_PROd_LEN = 100
    DB_STAFF = 'sqlite:///db.sqlite'
