import requests
import json
from config import values


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException("Нельзя сконвертировать одинаковую валюту")

        try:
            quote_link = values[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать "{quote}"')

        try:
            base_link = values[base]
        except KeyError:
            raise APIException(f'Не удалось обработать "{base}"')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException('Количество валюты должно быть указано цифрой!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_link}&tsyms={base_link}')
        text = json.loads(r.content)[values[base]]
        final_value = float(round(text * int(amount), 3))
        return final_value

