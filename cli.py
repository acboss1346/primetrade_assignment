import argparse
import os
import sys
from dotenv import load_dotenv

from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_price_for_limit
from bot.logging_config import setup_logger

logger = setup_logger()

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol", type=str, required=True, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, required=True, choices=["BUY", "SELL", "buy", "sell"], help="Order side: BUY or SELL")
    parser.add_argument("--type", type=str, required=True, choices=["MARKET", "LIMIT", "market", "limit", "STOP_MARKET", "stop_market"], help="Order type: MARKET, LIMIT, STOP_MARKET")
    parser.add_argument("--quantity", type=float, required=True, help="Order quantity")
    parser.add_argument("--price", type=float, help="Order price (required for LIMIT)")
    parser.add_argument("--stop-price", type=float, help="Stop price (required for STOP_MARKET)")

    args = parser.parse_args()

    # Load environment variables
    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print("Error: API credentials not found. Please set BINANCE_API_KEY and BINANCE_API_SECRET in .env file.")
        sys.exit(1)

    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.type)
        validate_price_for_limit(order_type, args.price)

        client = BinanceFuturesClient(api_key, api_secret)
        manager = OrderManager(client)

        print("\n--- Order Request Summary ---")
        print(f"Symbol:   {symbol}")
        print(f"Side:     {side}")
        print(f"Type:     {order_type}")
        print(f"Quantity: {args.quantity}")
        if args.price:
            print(f"Price:    {args.price}")
        if args.stop_price:
            print(f"Stop Px:  {args.stop_price}")
        print("-----------------------------\n")

        print("Sending request to Binance Futures Testnet...")
        response = manager.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price
        )

        print("\n--- Order Response Details ---")
        print(f"Order ID:     {response.get('orderId')}")
        print(f"Status:       {response.get('status')}")
        print(f"Executed Qty: {response.get('executedQty')}")
        if 'avgPrice' in response and float(response.get('avgPrice', 0)) > 0:
            print(f"Avg Price:    {response.get('avgPrice')}")
        print("------------------------------\n")
        print("SUCCESS: Order placed successfully.")

    except ValueError as ve:
        print(f"Validation Error: {ve}")
        sys.exit(1)
    except Exception as e:
        print(f"\nFAILURE: An error occurred while placing the order.\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
