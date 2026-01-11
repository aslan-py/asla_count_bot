class DictFormatError(Exception):
    """Ошибка формата словаря после генерации ИИ."""
    pass


class PrettySavedDataError(Exception):
    """Ошибка создания красивой таблицы с сохраненными данными."""
    pass


class PrettyPivotError(Exception):
    """Ошибка формирования красивого отчета по затратам за период."""
    pass


class DictDatesFormatError(Exception):
    """Ошибка формата словаря с датами."""
    pass


class AiError(Exception):
    """Ошибка получения IAM токена."""
    pass


class AiVoiceError(Exception):
    """Ошибки с распознованием голоса."""
    pass
