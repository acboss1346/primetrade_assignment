def validate_symbol(symbol: str) -> str:
    symbol = symbol.upper()
    if not symbol.endswith("USDT"):
        raise ValueError("Symbol must be a USDT-M pair (e.g., BTCUSDT).")
    return symbol

def validate_side(side: str) -> str:
    side = side.upper()
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL.")
    return side

def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper()
    valid_types = ["MARKET", "LIMIT", "STOP_MARKET", "STOP", "TAKE_PROFIT_MARKET", "TAKE_PROFIT"]
    if order_type not in valid_types:
        raise ValueError(f"Order type must be one of {valid_types}.")
    return order_type

def validate_price_for_limit(order_type: str, price: float):
    if order_type == "LIMIT" and (price is None or price <= 0):
        raise ValueError("Price is required and must be > 0 for LIMIT orders.")
