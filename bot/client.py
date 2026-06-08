import hmac
import hashlib
import time
import requests
from urllib.parse import urlencode
from .logging_config import setup_logger

logger = setup_logger()

class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://testnet.binancefuture.com"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key
        })

    def _sign(self, params: dict) -> str:
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def request(self, method: str, endpoint: str, params: dict = None) -> dict:
        if params is None:
            params = {}
            
        # Add timestamp for all signed endpoints
        params['timestamp'] = int(time.time() * 1000)
        params['signature'] = self._sign(params)
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            logger.debug(f"Sending {method} request to {url} with params: {params}")
            response = self.session.request(method, url, params=params)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Response: {data}")
            return data
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
            raise
        except requests.exceptions.RequestException as err:
            logger.error(f"Network error occurred: {err}")
            raise
