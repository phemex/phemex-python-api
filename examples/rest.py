import os 
import sys
import time

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "/../")

from phemex.client import Client
from phemex.exceptions import PhemexAPIException

# Create a testnet client
client = Client("api_key", "api_secret", True)

# Get account and positions
r = client.query_account_n_positions(Client.CURRENCY_BTC)
print(r)
r = client.query_account_n_positions(Client.CURRENCY_USD)
print(r)
try:
    r = client.query_account_n_positions("BTC1")
    print(r)
except PhemexAPIException as e:
    print(e)

# Place a new order, priceEp is scaled price, check our API doc for more info about scaling
# https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#scalingfactors
try:
    r = client.place_order({
        "symbol":Client.SYMBOL_BTCUSD, 
        "clOrdID":"JackTest1" + str(time.time()), 
        "side":Client.SIDE_BUY, 
        "orderQty":10, 
        "priceEp": 95000000,
        "ordType":Client.ORDER_TYPE_LIMIT,
        "timeInForce" : Client.TIF_GOOD_TILL_CANCEL})
    print("response:" + str(r))
    ordid = r["data"]["orderID"]
    print(ordid)
except PhemexAPIException as e:
    print(e)

# Send replace if this order not filled yet
try:
    r = client.amend_order(
        Client.SYMBOL_BTCUSD,
        ordid,
        {"priceEp": 95500000})
    print("response:" + str(r))
except PhemexAPIException as e:
    print(e)

# Cancel one order
try:
    r = client.cancel_order(
        Client.SYMBOL_BTCUSD,
        ordid)
    print("response:" + str(r))
except PhemexAPIException as e:
    print(e)

# Cancel all active orders
try:
    client.cancel_all_normal_orders(Client.SYMBOL_BTCUSD)
except PhemexAPIException as e:
    print(e)

# Cancel all conditional orders
try:
    client.cancel_all_untriggered_conditional_orders(Client.SYMBOL_BTCUSD)
except PhemexAPIException as e:
    print(e)

# Cancel all orders
try:
    client.cancel_all(Client.SYMBOL_BTCUSD)
except PhemexAPIException as e:
    print(e)

# Set leverage
try:
    # Set 0 to change back to cross margin
    # Set to 10x 
    r = client.change_leverage(Client.SYMBOL_BTCUSD, 10)
    print("response:" + str(r))
except PhemexAPIException as e:
    print(e)

# Set risklimit for 150 BTC
try:
    r = client.change_risklimit(Client.SYMBOL_BTCUSD, 150)
    print("response:" + str(r))
except PhemexAPIException as e:
    print(e)

# Get all active orders
try:
    r = client.query_open_orders(Client.SYMBOL_BTCUSD)
    print("response:" + str(r))
except PhemexAPIException as e:
    print(e)

try:
    print(client.query_24h_ticker("BTCUSD"))
except PhemexAPIException as e:
    print(e)