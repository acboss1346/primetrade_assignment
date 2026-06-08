from typing import Optional
from .client import BinanceFuturesClient
from .logging_config import setup_logger

logger = setup_logger()

class OrderManager:
    def __init__(self, client: BinanceFuturesClient):
        self.client = client

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None, stop_price: Optional[float] = None) -> dict:
        endpoint = "/fapi/v1/order"
        
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity
        }

        if order_type == "LIMIT":
            params["timeInForce"] = "GTC"
            params["price"] = price
        elif order_type in ["STOP_MARKET", "TAKE_PROFIT_MARKET"]:
            params["stopPrice"] = stop_price
        elif order_type in ["STOP", "TAKE_PROFIT"]:
            params["price"] = price
            params["stopPrice"] = stop_price

        logger.info(f"Placing {order_type} order for {symbol}: Side={side}, Qty={quantity}, Price={price}, StopPrice={stop_price}")
        
        try:
            response = self.client.request("POST", endpoint, params)
            logger.info("Order request summary:")
            logger.info(f"Symbol: {symbol}, Side: {side}, Type: {order_type}, Quantity: {quantity}")
            logger.info("Order response details:")
            logger.info(f"Order ID: {response.get('orderId')}")
            logger.info(f"Status: {response.get('status')}")
            logger.info(f"Executed Qty: {response.get('executedQty')}")
            if 'avgPrice' in response and float(response.get('avgPrice', 0)) > 0:
                logger.info(f"Avg Price: {response.get('avgPrice')}")
            
            logger.info("SUCCESS: Order placed successfully.")
            return response
        except Exception as e:
            logger.error(f"FAILURE: Failed to place order: {e}")
            raise
