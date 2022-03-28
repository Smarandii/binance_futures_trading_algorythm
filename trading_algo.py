from time import sleep
from binance.futures import Futures
from binance.enums import *
from secrets import _API, _SECRET_KEY

client = Futures(_API, _SECRET_KEY)


def get_10_prices_for_last_70_secs(trading_symbol):
    prices = []
    for price in client.mark_price_klines(trading_symbol, interval="1m")[-10:]:
        prices.append(price)
    return prices


def define_market_trend(trading_symbol):
    prices = get_10_prices_for_last_70_secs(trading_symbol)
    rise_counter = 0
    fall_counter = 0
    base_price = prices[0]
    for price in prices:
        if price > base_price:
            rise_counter += 1
        if price < base_price:
            fall_counter += 1
        base_price = price

    if rise_counter > fall_counter:
        return "bull"
    else:
        return "bear"


def open_position_based_on_trend(trend, price, trading_symbol, quantity):
    if trend == 'bull':
        order = client.new_order(
            symbol=trading_symbol,
            side=SIDE_BUY,
            type=FUTURE_ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity,
            price=str(price),
            isIsolated=True)
    if trend == "bear":
        order = client.new_order(
            symbol=trading_symbol,
            side=SIDE_SELL,
            type=FUTURE_ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity,
            price=str(price),
            isIsolated=True)


def calculate_price_for_take_profit_order(trend, current_coin_price):
    if trend == "bull":
        return current_coin_price + current_coin_price * 0.005
    if trend == "bear":
        return current_coin_price - current_coin_price * 0.005


def get_current_futures_balance():
    for coin in client.balance():
        if coin['asset'] == "USDT":
            return coin["balance"]


def get_current_coin_price(trading_symbol):
    return float(client.mark_price(symbol=trading_symbol)["markPrice"])


def calculate_price_for_stop_loss_order(trend, current_coin_price):
    if trend == "bull":
        return current_coin_price - current_coin_price * 0.05
    if trend == "bear":
        return current_coin_price + current_coin_price * 0.05


def create_take_profit_order(trend, take_profit_price, quantity):
    if trend == "bull":
        order_take_profit = client.new_order(symbol=trading_symbol,
                                             side=SIDE_SELL,
                                             type=FUTURE_ORDER_TYPE_TAKE_PROFIT,
                                             timeInForce=TIME_IN_FORCE_GTC,
                                             quantity=quantity,
                                             price=str(take_profit_price),
                                             stopPrice=str(take_profit_price),
                                             isIsolated=True)
    if trend == "bear":
        order_take_profit = client.new_order(symbol=trading_symbol,
                                             side=SIDE_BUY,
                                             type=FUTURE_ORDER_TYPE_TAKE_PROFIT,
                                             timeInForce=TIME_IN_FORCE_GTC,
                                             quantity=quantity,
                                             price=str(take_profit_price),
                                             stopPrice=str(take_profit_price),
                                             isIsolated=True)


def create_stop_loss_order(trend, stop_loss_price, quantity):
    if trend == "bull":
        order_stop_loss = client.new_order(symbol=trading_symbol,
                                           side=SIDE_SELL,
                                           type=FUTURE_ORDER_TYPE_STOP,
                                           timeInForce=TIME_IN_FORCE_GTC,
                                           quantity=quantity,
                                           price=str(stop_loss_price),
                                           stopPrice=str(stop_loss_price),
                                           isIsolated=True)
    if trend == "bear":
        order_stop_loss = client.new_order(symbol=trading_symbol,
                                           side=SIDE_BUY,
                                           type=FUTURE_ORDER_TYPE_STOP,
                                           timeInForce=TIME_IN_FORCE_GTC,
                                           quantity=quantity,
                                           price=str(stop_loss_price),
                                           stopPrice=str(stop_loss_price),
                                           isIsolated=True)


def get_open_position():
    return client.get_open_orders()


trading_symbol = "RUNEUSDT" # Выбор случайный
while True:
    opened_position = get_open_position()
    if opened_position is None:
        trend = define_market_trend(trading_symbol)
        current_balance = get_current_futures_balance()
        current_coin_price = get_current_coin_price(trading_symbol)
        quantity = current_balance // current_coin_price
        take_profit_price = calculate_price_for_take_profit_order(trend, current_coin_price)
        stop_loss_price = calculate_price_for_stop_loss_order(trend, current_coin_price)
        open_position_based_on_trend(trend, current_coin_price, trading_symbol, quantity)
        create_take_profit_order(trend, take_profit_price, trading_symbol)
        create_stop_loss_order(trend, stop_loss_price, trading_symbol)
    else:
        sleep(7)
