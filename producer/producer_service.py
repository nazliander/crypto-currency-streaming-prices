
import os
import time
from pathlib import Path
from json import dumps

from confluent_kafka import Producer

from utils import (
    set_logger, config_reader, acked)
from nft_repository import NFTPortAPI


NFT_PAGE = "https://api.nftport.xyz/v0/nfts"
NFT_PORT_API_KEY = "b4b89ab2-20e7-435a-8d3b-808c5d419703"
LOGGER = set_logger("producer_logger")
PARENT_PATH = os.fspath(Path(__file__).parents[1])
CONFIG_PATH = os.path.join(
    PARENT_PATH,
    "configurations",
    "settings.ini")
KAFKA_CONFIG_DICT = config_reader(
    CONFIG_PATH, "kafka")
NFT_TOPIC = config_reader(
    CONFIG_PATH, "app.settings")["topic_raw"]


def produce_list_of_nft_dict_into_kafka(list_of_dict):
    producer = Producer(KAFKA_CONFIG_DICT)
    for nft_with_model in list_of_dict:
        nft_name = nft_with_model["nameNft"]
        try:
            producer.produce(
                topic=NFT_TOPIC,
                value=dumps(nft_with_model).encode("utf-8"),
                callback=acked)
            producer.poll(1)
        except Exception as e:
            LOGGER.info(
                f"There is a problem with the {nft_name}\n"
                f"The problem is: {e}!")


if __name__ == "__main__":
    nft_api = NFTPortAPI()
    while True:
        all_nfts, status = nft_api.get_json_api(NFT_PAGE,NFT_PORT_API_KEY)
        nfts_with_model = nft_api.get_all_nfts_with_model(all_nfts)
        produce_list_of_nft_dict_into_kafka(nfts_with_model)
        LOGGER.info(f"Produced into Kafka topic: {NFT_TOPIC}.")
        LOGGER.info(f"Waiting for the next round...")
        time.sleep(10)
