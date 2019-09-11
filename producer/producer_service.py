from crypto_repository import CryptoAPI, KinesisUtils
import time
import json
import boto3

COIN_PAGE = "https://api.coinranking.com/v1/public/coins"


def produce_crypto_data_into_kinesis(kinesis_client, stream_name):
    cryptoRepository = CryptoAPI()
    all_coins, status = cryptoRepository.get_json_api(COIN_PAGE)
    all_coins_with_model = cryptoRepository.get_all_coins_with_model(
                all_coins)
    for coin_with_model in all_coins_with_model:
        kinesis_client.put_record(
            StreamName=stream_name,
            Data=json.dumps(coin_with_model),
            PartitionKey="c-main")


if __name__ == "__main__":
    kinesis_utils = KinesisUtils()
    boto_session = boto3.Session(region_name="eu-east-1")
    kinesis_client = kinesis_utils.get_kinesis_client(boto_session)
    kinesis_utils.create_stream_if_not_exists(kinesis_client, "crypto", 1)
    while True:
        produce_crypto_data_into_kinesis(kinesis_client, "crypto")
        time.sleep(5)
