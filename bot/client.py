import os
import time
import hmac
import hashlib
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

from bot.logging_config import logger

load_dotenv()


class BinanceFuturesClient:
    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")
        self.base_url = os.getenv(
            "BINANCE_BASE_URL",
            "https://testnet.binancefuture.com"
        )

        if not self.api_key or not self.api_secret:
            raise ValueError("API key and secret are missing in .env file")

    def _sign(self, params):
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        params["signature"] = signature
        return params

    def post(self, endpoint, params):
        url = self.base_url + endpoint

        params["timestamp"] = int(time.time() * 1000)
        signed_params = self._sign(params)

        headers = {
            "X-MBX-APIKEY": self.api_key
        }

        logger.info(f"POST Request URL: {url}")
        logger.info(f"Request Params: {params}")

        try:
            response = requests.post(
                url,
                headers=headers,
                params=signed_params,
                timeout=10
            )

            logger.info(f"Response Status Code: {response.status_code}")
            logger.info(f"Response Body: {response.text}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError:
            logger.error(f"API Error: {response.text}")
            raise Exception(f"API Error: {response.text}")

        except requests.exceptions.RequestException as error:
            logger.error(f"Network Error: {error}")
            raise Exception(f"Network Error: {error}")