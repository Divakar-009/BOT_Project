from binance import Client
from binance.exceptions import BinanceAPIException
from config import API_KEY, API_SECRET, BASE_URL
from logger import logger

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)

        if testnet:
            self.client.FUTURES_URL = BASE_URL

        logger.info("Trading Bot Initialized")

    def place_market_order(self, symbol, side, quantity):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity
            )
            logger.info(f"Market Order Response: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Market Order Error: {e}")
            return None

    def place_limit_order(self, symbol, side, quantity, price):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                timeInForce="GTC",
                quantity=quantity,
                price=price
            )
            logger.info(f"Limit Order Response: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Limit Order Error: {e}")
            return None

    def place_stop_limit_order(self, symbol, side, quantity, stop_price, price):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="STOP",
                quantity=quantity,
                stopPrice=stop_price,
                price=price,
                timeInForce="GTC"
            )
            logger.info(f"Stop-Limit Order Response: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Stop-Limit Order Error: {e}")
            return None


def validate_side(side):
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")


def main():
    bot = BasicBot(API_KEY, API_SECRET)

    print("\n--- Binance Futures Testnet Trading Bot ---")
    symbol = input("Enter symbol (e.g. BTCUSDT): ").upper()
    side = input("Order side (BUY/SELL): ").upper()
    validate_side(side)

    order_type = input("Order type (MARKET / LIMIT / STOP_LIMIT): ").upper()
    quantity = float(input("Quantity: "))

    if order_type == "MARKET":
        result = bot.place_market_order(symbol, side, quantity)

    elif order_type == "LIMIT":
        price = float(input("Limit price: "))
        result = bot.place_limit_order(symbol, side, quantity, price)

    elif order_type == "STOP_LIMIT":
        stop_price = float(input("Stop price: "))
        price = float(input("Limit price: "))
        result = bot.place_stop_limit_order(symbol, side, quantity, stop_price, price)

    else:
        print("Invalid order type")
        return

    if result:
        print("\nOrder Placed Successfully!")
        print("Order ID:", result["orderId"])
        print("Status:", result["status"])
        print("Executed Qty:", result["executedQty"])
    else:
        print("Order Failed. Check logs for details.")


if __name__ == "__main__":
    main()
