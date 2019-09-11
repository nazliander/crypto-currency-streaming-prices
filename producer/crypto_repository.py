import requests
import os
from pathlib import Path
from utils import set_logger, current_milli_time, config_reader


LOGGER = set_logger("general_log")
PARENT_PATH = os.fspath(Path(__file__).parents[1])
CONFIG_PATH = os.path.join(
    PARENT_PATH,
    "configurations",
    "settings.ini")
KINESIS_CONFIG = config_reader(CONFIG_PATH, "kinesis")


class KinesisUtils:
    def __init__(self):
        self.host_url = KINESIS_CONFIG["host_url"]
        self.aws_access_key_id = KINESIS_CONFIG["aws_access_key_id"]
        self.aws_secret_access_key = KINESIS_CONFIG["aws_secret_access_key"]

    def get_kinesis_client(self, boto_session):
        return boto_session.client(
            'kinesis',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            endpoint_url=self.host_url)

    def create_stream_if_not_exists(
            self, kinesis_client, stream_name, shard_count):
        stream_names_list = kinesis_client.list_streams()["StreamNames"]
        if stream_name not in stream_names_list:
            kinesis_client.create_stream(
                StreamName=stream_name, ShardCount=shard_count)
            LOGGER.info(
                "Kinesis client with name {kinesis_stream_name}"
                "is created.".format(kinesis_stream_name=stream_name))


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
            LOGGER.error(
                "The current coin with name has "
                "defected dict keys. Exception says: {exception}".format(
                    exception=e))
            return {}

    def get_all_coins_with_model(self, all_coins):
        coins_with_model = []
        for coin in all_coins["data"]["coins"]:
            coin_with_model_temp = self.get_coin_model(coin)
            coins_with_model.append(coin_with_model_temp)
        return coins_with_model
