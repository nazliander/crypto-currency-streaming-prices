import requests
from utils import set_logger, current_milli_time, config_reader


LOGGER = set_logger("repository_logger")


class CryptoAPI:
    def get_json_api(self, page):
        get_request = requests.get(page)
        assert get_request.status_code == 200, "Request not successful"
        return get_request.json(), get_request.status_code

    def get_coin_model(self, coin):
        try:
            return {"nameCoin": coin["name"],
                    "symbolCoin": coin["symbol"],
                    "numberOfMarkets": coin["numberOfMarkets"],
                    "volume": coin["volume"],
                    "marketCap": coin["marketCap"],
                    "totalSupply": coin["totalSupply"],
                    "price": coin["price"],
                    "timestamp_logger": current_milli_time()}
            # In the API milli seconds are used.
        except Exception as e:
            LOGGER.info(
                f"The current coin with name has "
                "defected dict keys. Exception says: {exception}")
            return {}

    def get_all_coins_with_model(self, all_coins):
        coins_with_model = []
        for coin in all_coins["data"]["coins"]:
            coin_with_model_temp = self.get_coin_model(coin)
            coins_with_model.append(coin_with_model_temp)
        return coins_with_model
