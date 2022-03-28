
# В примере использовался данный скрипт
from binance.futures import Futures
from binance.enums import *
from secrets import _SECRET_KEY, _API


def get_usdt_balance(client):
    for coin in client.balance():
        if coin['asset'] == "USDT":
            return coin["balance"]


def define_side(client):
    return

client = Futures(_API, _SECRET_KEY)
budget = 1
leverage = 10
trading_symbol = "OGNUSDT"
entry_price = mark_price = float(client.mark_price(symbol=trading_symbol)["markPrice"])
mark_price = float("{:.4f}".format(mark_price))
quantity = budget * 10 // mark_price
print(get_usdt_balance(client))

print("Buying OGN/USDT price:", mark_price, "quantity: ", quantity)
order = client.new_order(
    symbol=trading_symbol,
    side=SIDE_BUY,
    type=FUTURE_ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=quantity,
    price=str(mark_price),
    isIsolated=True)
print(get_usdt_balance(client))


mark_price_out = mark_price * 1.001
mark_price_out = float("{:.4f}".format(mark_price_out))
print("Selling OGN/USDT price:", mark_price_out, "quantity: ", quantity)
order_take_profit = client.new_order(symbol=trading_symbol,
                             side=SIDE_SELL,
                             type=FUTURE_ORDER_TYPE_TAKE_PROFIT,
                             timeInForce=TIME_IN_FORCE_GTC,
                             quantity=quantity,
                             price=str(mark_price_out),
                             stopPrice=str(mark_price_out),
                             isIsolated=True)

mark_price_stop = float("{:.4f}".format(mark_price * 0.995))
order_stop_loss = client.new_order(symbol=trading_symbol,
                             side=SIDE_SELL,
                             type=FUTURE_ORDER_TYPE_STOP,
                             timeInForce=TIME_IN_FORCE_GTC,
                             quantity=quantity,
                             price=str(mark_price_stop),
                             stopPrice=str(mark_price_stop),
                             isIsolated=True)
print(get_usdt_balance(client))
