from bot.client import BinanceFuturesClient


class OrderManager:
    def __init__(self):
        self.client = BinanceFuturesClient()

    def place_order(self, symbol, side, order_type, quantity, price=None):
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity
        }

        if order_type.upper() == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        return self.client.post("/fapi/v1/order", params)