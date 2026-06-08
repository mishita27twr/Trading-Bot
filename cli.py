import argparse

from bot.orders import OrderManager
from bot.validators import validate_order
from bot.logging_config import logger


def main():
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot"
    )

    parser.add_argument("--symbol", required=True, help="Example: BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", required=True, help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, type=float)
    parser.add_argument("--price", type=float, help="Required for LIMIT order")

    args = parser.parse_args()

    try:
        validate_order(
            args.symbol,
            args.side,
            args.type,
            args.quantity,
            args.price
        )

        print("\nOrder Request Summary")
        print("---------------------")
        print(f"Symbol: {args.symbol.upper()}")
        print(f"Side: {args.side.upper()}")
        print(f"Order Type: {args.type.upper()}")
        print(f"Quantity: {args.quantity}")

        if args.type.upper() == "LIMIT":
            print(f"Price: {args.price}")

        order_manager = OrderManager()

        response = order_manager.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )

        print("\nOrder Response Details")
        print("----------------------")
        print(f"Order ID: {response.get('orderId')}")
        print(f"Status: {response.get('status')}")
        print(f"Executed Quantity: {response.get('executedQty')}")
        print(f"Average Price: {response.get('avgPrice', 'N/A')}")

        print("\nSuccess: Order placed successfully.")

    except Exception as error:
        logger.error(f"Order failed: {error}")
        print(f"\nFailure: {error}")


if __name__ == "__main__":
    main()