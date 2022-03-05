import json
import time
import pypd
import pytz
import requests
from datetime import datetime

from constant import *
from redis_config import Redis
from crypto_alert import trigger_alert_script


class Binance:
    def __init__(self):
        self.url = "https://api.binance.com/api/v3/ticker/price"

    def get_data(self):
        response = requests.get(self.url)
        coin_info_list = json.loads(response.text)

        payload = {}
        for coin_info in coin_info_list:
            symbol = coin_info.get("symbol")
            price = coin_info.get("price")

            if symbol and symbol.endswith("USDT"):
                payload[symbol] = float(price)
        return payload


class DataWarehouse:
    def __init__(self):
        self.last_notification = 0
        self.redis_client = Redis().connection()
        self.time_zone = pytz.timezone('Asia/Kolkata')
        self.url = "https://min-api.cryptocompare.com/data/top/totalvolfull?limit=100&tsym=USD"
        self.current_datetime_ist = datetime.now(self.time_zone)

    def is_valid_notification(self):
       return (int(time.time()) - self.last_notification) > 60 # 10 Mins

    def mobile_notification(self, message):
        print (message)
        self.last_notification = int(time.time())
        pypd.EventV2.create(data={
            'routing_key': integration_key,
            'event_action': 'trigger',
            'payload': {
                'summary': message,
                'severity': 'error',
                'source': 'pypd bot',
            }
        })

    def data_collection(self):

        index = self.redis_client.get("last_index") or 0
        index = int(index) + 1

        while True:
            try:
                payload = Binance().get_data()
                payload["datetime"] = str(datetime.now(self.time_zone).strftime('%Y-%m-%d %H:%M:%S'))

                self.redis_client.set("last_index", str(index))
                self.redis_client.setex(index, 12*3600, str(payload))

                print (payload["datetime"], " => Index: ", index)
                index += 1
                # trigger_alert_script()
                time.sleep(60)
            except Exception as err:
                print(err)
                if self.is_valid_notification():
                    self.mobile_notification("Data Warehouse Service Down! Error: " + str(err))
                time.sleep(60)
try:
    crypto_compare = DataWarehouse()
    crypto_compare.data_collection()
except Exception as err:
    crypto_compare.mobile_notification("Data Warehouse Service Stopped: " + str(err))

