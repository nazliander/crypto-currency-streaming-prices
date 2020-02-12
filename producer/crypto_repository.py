import requests
from utils import set_logger, current_milli_time


LOGGER = set_logger("repository_logger")


class CryptoAPI:
    def get_json_api(self, page):
        get_request = requests.get(page)
        assert get_request.status_code == 200, "Request not successful"
        return get_request.json(), get_request.status_code

    def get_coin_model(self, coin):
        try:
            return {"nameCoin": coin.get("name"),
                    "symbolCoin": coin.get("symbol"),
                    "numberOfMarkets": coin.get("numberOfMarkets"),
                    "volume": coin.get("volume"),
                    "marketCap": coin.get("marketCap"),
                    "totalSupply": coin.get("totalSupply"),
                    "price": coin.get("price"),
                    "timestamp_logger": current_milli_time()}
            # In the API milliseconds are used.
        except Exception as e:
            LOGGER.info(
                f"Exception: {e}")
            return {}

    def get_all_coins_with_model(self, all_coins):
        coins_with_model = []
        for coin in all_coins["data"]["coins"]:
            coin_with_model_temp = self.get_coin_model(coin)
            coins_with_model.append(coin_with_model_temp)
        return coins_with_model
