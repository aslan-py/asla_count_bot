import json
from datetime import datetime as dt

import requests
from openai import OpenAI

from utils.constants import Ai, Errors
from utils.exceptions import AiError

client = OpenAI(api_key=Ai.DEEPSEEK_API_KEY, base_url=Ai.DEPPSEEK_API_URL)


def deepseek(user_text):
    """Отправляет текст в DeepSeek API.

    Получаем словарь: {'category': 'str', 'product': 'str', 'price': int}.
    """
    try:
        messages = [
            {"role": "system", "content": Ai.PROMPT_1},
            {"role": "user", "content": user_text}
        ]
        response = client.chat.completions.create(
            model=Ai.DEEPSEEK_MODEL,
            messages=messages,
            stream=False,
            temperature=Ai.TEMPERATURE,
            max_tokens=Ai.MAX_TOKENS
        )
        return json.loads(response.choices[0].message.content)
    except Exception as error:
        raise AiError(error)


def get_dates_from_ai(user_text):
    """
    Распознает временные интервалы в тексте пользователя.

    Возвращает даты начала и конца периода.
    """
    try:
        messages = [
            {"role": "system", "content": Ai.PROMT_DATA.format(
                today=dt.today().date())},
            {"role": "user", "content": user_text}
        ]

        response = client.chat.completions.create(
            model=Ai.DEEPSEEK_MODEL,
            messages=messages,
            temperature=Ai.TEMPERATURE,
            max_tokens=Ai.MAX_TOKENS_DATE
        )

        return json.loads(response.choices[0].message.content)
    except Exception as error:
        raise AiError(error)


def get_iam_token():
    """Получаем  iam токен."""
    response = requests.post(
        Ai.YA_SPEECH_KIT_URL,
        json=Ai.YA_SPEECH_KIT_JSON,
        headers=Ai.YA_SPEECH_KIT_HEADERS
    )

    if response.status_code != Ai.STATUS_CODE:
        raise Exception(Errors.IAM_TOKEN_ERROR.format(response.status_code))
    iam = response.json().get('iamToken')
    if not iam:
        raise Exception(Errors.IAM_EMPTY.format(response.text))
    return iam


def yandex_speech_kit(binary_code):
    """Переводим голос из ТГ в текст."""
    iam_token = get_iam_token()
    response = requests.post(
        Ai.YA_URL,
        headers={
            "Authorization": f'Bearer {iam_token}',
            "Content-Type": 'application/octet-stream'
        },
        params={
            "folderId": Ai.YANDEX_FOLDER_ID,
            "lang": Ai.YA_LANG,
            "format": Ai.YA_FORMAT
        },
        data=binary_code,
        verify=False
    )
    return response
