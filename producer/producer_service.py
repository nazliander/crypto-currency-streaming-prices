
import os
import time
from pathlib import Path
from json import dumps

from confluent_kafka import Producer

from utils import (
    set_logger, config_reader, acked)
from crypto_repository import CryptoAPI


COIN_PAGE = "https://api.coinranking.com/v1/public/coins"
LOGGER = set_logger("producer_logger")
PARENT_PATH = os.fspath(Path(__file__).parents[1])
CONFIG_PATH = os.path.join(
    PARENT_PATH,
    "configurations",
    "settings.ini")
KAFKA_CONFIG_DICT = config_reader(
    CONFIG_PATH, "kafka")
CRYPTO_TOPIC = config_reader(
    CONFIG_PATH, "app.settings")["topic_raw"]


def produce_list_of_coin_dict_into_kafka(list_of_dict):
    producer = Producer(KAFKA_CONFIG_DICT)
    for coin_with_model in list_of_dict:
        coin_name = coin_with_model["nameCoin"]
        try:
            producer.produce(
                topic=CRYPTO_TOPIC,
                value=dumps(coin_with_model).encode("utf-8"),
                callback=acked)
            producer.poll(1)
        except Exception as e:
            LOGGER.info(
                f"There is a problem with the {coin_name}\n"
                f"The problem is: {e}!")


if __name__ == "__main__":
    crypto_api = CryptoAPI()
    while True:
        all_coins, status = crypto_api.get_json_api(COIN_PAGE)
        coins_with_model = crypto_api.get_all_coins_with_model(all_coins)
        produce_list_of_coin_dict_into_kafka(coins_with_model)
        LOGGER.info(f"Produced into Kafka topic: {CRYPTO_TOPIC}.")
        LOGGER.info(f"Waiting for the next round...")
        time.sleep(10)
