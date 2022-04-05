from logging import Logger
import requests
from utils import set_logger, current_milli_time


LOGGER = set_logger("repository_logger")


class NFTPortAPI:
    def get_json_api(self, page, apiKey):
        get_request = requests.get(page, headers={"Authorization" : apiKey})
        LOGGER.info(get_request)
        assert get_request.status_code == 200, "Request not successful"
        return get_request.json(), get_request.status_code

    def get_nft_model(self, nft):
        try:
            return {"nameNft": nft.get("name"),
                    "symbolNft": nft.get("symbol"),
                    "numberOfMarkets": nft.get("numberOfMarkets"),
                    "volume": nft.get("volume"),
                    "marketCap": nft.get("marketCap"),
                    "totalSupply": nft.get("totalSupply"),
                    "price": nft.get("price"),
                    "timestamp_logger": current_milli_time()}
            # In the API milliseconds are used.
        except Exception as e:
            LOGGER.info(
                f"Exception: {e}")
            return {}

    def get_all_nft_with_model(self, all_nfts):
        nfts_with_model = []
        for nft in all_nfts["data"]["nfts"]:
            nft_with_model_temp = self.get_nft_model(nft)
            nfts_with_model.append(nft_with_model_temp)
        return nfts_with_model
