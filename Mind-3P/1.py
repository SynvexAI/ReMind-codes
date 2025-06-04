# Напиши на python конвертер валют с актуальным курсом (через AP)
import requests

def get_exchange_rate(from_currency, to_currency):

"""

Получает актуальный курс валют с API.

Args:

from_currency (str): Исходная валюта (например, USD).

to_currency (str): Целевая валюта (например, RUB).

Returns:

float: Курс валют, или None в случае ошибки.

"""