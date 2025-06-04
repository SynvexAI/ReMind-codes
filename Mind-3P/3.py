# Напиши на python конвертер валют с актуальным курсом (через AP)
# БОЖЕ ОНО ЖРЕТ МОЙ ПРОЦ И ВИДЮХУ НА 100%!!!
# 9 МИНУТ НА 4060 КАРЛ

import requests

def get_exchange_rate(from_currency, to_currency):
    """
    Получает актуальный курс обмена валют с использованием API exchangerate-api.com.

    Args:
        from_currency (str): Код валюты, из которой нужно конвертировать (например, USD).
        to_currency (str): Код валюты, в которую нужно конвертировать (например, EUR).

    Returns:
        float: Курс обмена, или None, если произошла ошибка.
    """
    try:
        url = f"https://v6.exchangerate-api.com/v6/YOUR_API_KEY/pair/{from_currency}/{to_currency}"  # Замените YOUR_API_KEY на свой ключ API
        response = requests.get(url)
        response.raise_for_status()  # Вызывает исключение для плохих ответов (4xx или 5xx)
        data = response.json()
        return data['conversion_rates'][to_currency]
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None
    except KeyError:
        print("Неверный код валюты или ошибка в ответе API.")
        return None

def convert_currency(amount, from_currency, to_currency):
    """
    Конвертирует валюту.

    Args:
        amount (float): Сумма для конвертации.
        from_currency (str): Код валюты, из которой нужно конвертировать.
        to_currency (str): Код валюты, в которую нужно конвертировать.

    Returns:
        float: Конвертированная сумма, или None, если произошла ошибка.
    """
    exchange_rate = get_exchange_rate(from_currency, to_currency)
    if exchange_rate is not None:
        return amount * exchange_rate
    else:
        return None

def main():
    """
    Основная функция для взаимодействия с пользователем.
    """
    while True:
        try:
            amount = float(input("Введите сумму для конвертации: "))
            from_currency = input("Введите код валюты, из которой конвертировать (например, USD): ").upper()
            to_currency = input("Введите код валюты, в которую конвертировать (например, EUR): ").upper()

            converted_amount = convert_currency(amount, from_currency, to_currency)

            if converted_amount is not None:
                print(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
            else:
                print("Не удалось конвертировать валюту. Проверьте коды валют и подключение к интернету.")

            another_conversion = input("Хотите выполнить еще одну конвертацию? (да/нет): ").lower()
            if another_conversion != "да":
                break

        except ValueError:
            print("Неверный ввод. Пожалуйста, введите число для суммы.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
